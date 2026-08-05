#!/usr/bin/env python3
"""Mechanical enforcement of the cheat-sheet standard (docs/stds/CHEAT_SHEET.md v2.1.0).

There is no database and no per-item fields — a proposed addition is one entry
(a bullet, optionally with an explanatory clause and/or a fenced code block).
CHS-6 (v2.1.0) deliberately has no length cap: an entry is as short as the fact
allows and may extend to include a "how to use it" clause or a command
snippet. This script does NOT check length. It checks the things that are
still genuinely mechanical: banned openers (CHS-4) and hedge/narrative voice
(CHS-7). It does not, and cannot, check CHS-2 gate 5 ("not already said") —
that requires reading the live page — or whether the entry is "as short as
the fact allows," which is judgement, not a regex.

Exit 0 = pass, 1 = fail. Prints one line per violation. A pass here is
necessary, never sufficient — gate 5 and the maintainer's yes still apply.
"""

import argparse
import re
import sys

# CHS-4: openers that carry no information.
BANNED_OPENERS = [
    'issue with', 'issues with', 'problem with', 'problems with',
    'how to', 'note about', 'note on', 'fix for', 'when you',
    'something about', 'a', 'an', 'the',
]

# CHS-7: uncertainty belongs nowhere on this surface. An uncertain fact fails
# admission gate 4 instead of getting hedged onto the page.
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

# Not a rule, not a fail — past this, ask yourself whether it's still one
# fact (CHS-3) or should split. Purely a nudge for the writer.
LONG_ENTRY_NUDGE_WORDS = 120


def strip_formatting(text):
    """Strip inline code, bold and fenced code blocks so voice checks read
    what a reader actually parses, not markup or literal command text."""
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    text = re.sub(r'`[^`]*`', ' ', text)
    text = text.replace('**', '')
    return text


def count_words(text):
    return len([w for w in strip_formatting(text).split() if w.strip()])


def find_phrases(text, phrases):
    low = ' ' + re.sub(r'[^a-z0-9\s]+', ' ', strip_formatting(text).lower()) + ' '
    low = re.sub(r'\s+', ' ', low)
    return [p for p in phrases if f' {p} ' in low]


def check(entry):
    problems = []
    notes = []

    if not entry.strip():
        return ['entry is empty'], []

    # Banned opener check: strip a leading bold marker, then check the first words.
    lead = re.sub(r'^\*\*', '', entry.strip())
    normalised = re.sub(r'[^a-z0-9\s]+', ' ', lead.lower()).strip()
    for opener in sorted(BANNED_OPENERS, key=len, reverse=True):
        if normalised == opener or normalised.startswith(opener + ' '):
            problems.append(
                f'opens with banned non-informative "{opener}" — '
                f'front-load the informative words instead (CHS-4)')
            break

    for hedge in find_phrases(entry, HEDGE_WORDS):
        problems.append(
            f'hedge "{hedge}" — an uncertain fact fails admission gate 4, '
            f'it does not get hedged onto the page (CHS-7)')
    for phrase in find_phrases(entry, NARRATIVE_PHRASES):
        problems.append(f'discovery narrative "{phrase}" (CHS-7)')

    words = count_words(entry)
    if words > LONG_ENTRY_NUDGE_WORDS:
        notes.append(
            f'{words} words (excluding code) — not a violation, but check CHS-3: '
            f'is this still one fact, or has it drifted into two that should split?')

    return problems, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cmd', choices=['check'])
    parser.add_argument('--bullet', required=True,
                         help='the full entry as it would be written to the page — '
                              'the bullet, plus any explanatory clause and fenced code block')
    args = parser.parse_args()

    problems, notes = check(args.bullet)
    if problems:
        print('FAIL — rewrite before proposing it:')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('PASS (still needs CHS-2 gate 5 — read the live page — and the maintainer\'s yes)')
    for n in notes:
        print(f'  note: {n}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
