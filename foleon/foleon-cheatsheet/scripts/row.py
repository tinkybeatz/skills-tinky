#!/usr/bin/env python3
"""Mechanical enforcement of the cheat-sheet standard (docs/stds/CHEAT_SHEET.md).

Two jobs, both deterministic so the model never has to eyeball them:

  key    derive the canonical Dedupe key (CHS-11). Must be byte-stable — if the
         derivation drifts, dedupe silently stops working and duplicates appear.
  check  enforce the caps, banned openers and hedge words (CHS-4/6/7).

Exit 0 = pass, 1 = fail. `check` prints one line per violation.
"""

import argparse
import re
import sys

# CHS-8: the closed enumeration. A seventh value is a standard amendment.
AREAS = [
    'Editor',
    'Viewer',
    'Core / rendering',
    'Build & tooling',
    'Tests & Playwright',
    'Conventions',
]

MAX_SYMPTOM_WORDS = 10
MAX_FIX_WORDS = 40
MAX_FIX_LINES = 3
MAX_SLUG_LEN = 60

# CHS-4: openers that carry no information. Matched on the normalised prefix.
BANNED_OPENERS = [
    'issue with', 'issues with', 'problem with', 'problems with',
    'how to', 'note about', 'note on', 'fix for', 'when you',
    'something about', 'a', 'an', 'the',
]

# CHS-7: uncertainty belongs nowhere on this surface. An uncertain fact fails
# admission gate 4 instead.
HEDGE_WORDS = [
    'probably', 'possibly', 'apparently', 'presumably', 'maybe',
    'might be', 'may be', 'seems', 'seem to', 'i think', 'i believe',
    'sort of', 'kind of', 'unclear', 'not sure', 'perhaps',
]

# CHS-7: how it was discovered is never part of the answer.
NARRATIVE_PHRASES = [
    'we found', 'we discovered', 'we noticed', 'i found', 'i noticed',
    'it turned out', 'turns out', 'after investigating', 'after digging',
    'during debugging', 'it appears that',
]


def strip_code(text):
    """Remove inline code spans so backticked content can't skew counts."""
    return re.sub(r'`[^`]*`', ' ', text)


def slugify(text, keep_len=MAX_SLUG_LEN):
    text = text.lower()
    text = text.replace("'", '').replace('’', '')  # won't -> wont
    text = text.replace('&', ' ')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    if len(text) > keep_len:
        text = text[:keep_len].rsplit('-', 1)[0]
    return text


def dedupe_key(area, symptom):
    if area not in AREAS:
        raise SystemExit(f'unknown Area {area!r} — must be one of: {", ".join(AREAS)}')
    return f'{slugify(area, 40)}:{slugify(symptom)}'


def count_words(text):
    return len([w for w in strip_code(text).split() if w.strip()])


def count_sentences(text):
    text = strip_code(text)
    for abbrev in ('e.g.', 'i.e.', 'etc.', 'vs.'):
        text = text.replace(abbrev, '')
    return len(re.findall(r'[.!?]+(?=\s|$)', text.strip()))


def find_phrases(text, phrases):
    low = ' ' + re.sub(r'[^a-z0-9\s]+', ' ', strip_code(text).lower()) + ' '
    low = re.sub(r'\s+', ' ', low)
    return [p for p in phrases if f' {p} ' in low]


def check(symptom, fix, why, area):
    problems = []

    if area is not None and area not in AREAS:
        problems.append(f'Area: {area!r} is not one of the six permitted values (CHS-8)')

    # --- Symptom (CHS-4, CHS-6) ---
    words = count_words(symptom)
    if not symptom.strip():
        problems.append('Symptom: empty')
    if words > MAX_SYMPTOM_WORDS:
        problems.append(f'Symptom: {words} words, max {MAX_SYMPTOM_WORDS} (CHS-6)')
    normalised = re.sub(r'[^a-z0-9\s]+', ' ', symptom.lower()).strip()
    for opener in sorted(BANNED_OPENERS, key=len, reverse=True):
        if normalised == opener or normalised.startswith(opener + ' '):
            problems.append(
                f'Symptom: opens with banned non-informative "{opener}" — '
                f'front-load the informative words (CHS-4)')
            break

    # --- Fix (CHS-6, CHS-7) ---
    if not fix.strip():
        problems.append('Fix: empty')
    fix_words = count_words(fix)
    if fix_words > MAX_FIX_WORDS:
        problems.append(f'Fix: {fix_words} words, max {MAX_FIX_WORDS} (CHS-6)')
    fix_lines = len([ln for ln in fix.splitlines() if ln.strip()])
    if fix_lines > MAX_FIX_LINES:
        problems.append(f'Fix: {fix_lines} lines, max {MAX_FIX_LINES} (CHS-6)')

    # --- Why (CHS-5, CHS-6) — empty is valid and preferred over speculation ---
    if why and why.strip():
        sentences = count_sentences(why)
        if sentences > 1:
            problems.append(f'Why: {sentences} sentences, max 1 — link instead (CHS-6)')

    # --- Voice, across all authored fields (CHS-7) ---
    for field, text in (('Symptom', symptom), ('Fix', fix), ('Why', why or '')):
        for hedge in find_phrases(text, HEDGE_WORDS):
            problems.append(
                f'{field}: hedge "{hedge}" — an uncertain fact fails admission '
                f'gate 4, it does not get hedged onto the sheet (CHS-7)')
        for phrase in find_phrases(text, NARRATIVE_PHRASES):
            problems.append(f'{field}: discovery narrative "{phrase}" (CHS-7)')

    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_key = sub.add_parser('key', help='derive the canonical Dedupe key')
    p_key.add_argument('--area', required=True)
    p_key.add_argument('--symptom', required=True)

    p_check = sub.add_parser('check', help='enforce caps, openers and voice')
    p_check.add_argument('--symptom', required=True)
    p_check.add_argument('--fix', required=True)
    p_check.add_argument('--why', default='')
    p_check.add_argument('--area', default=None)

    args = parser.parse_args()

    if args.cmd == 'key':
        print(dedupe_key(args.area, args.symptom))
        return 0

    problems = check(args.symptom, args.fix, args.why, args.area)
    if problems:
        print('FAIL — rewrite before writing to Notion:')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('PASS')
    if args.area:
        print(f'  Dedupe key: {dedupe_key(args.area, args.symptom)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
