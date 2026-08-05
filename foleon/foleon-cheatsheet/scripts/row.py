#!/usr/bin/env python3
"""Mechanical enforcement of the cheat-sheet standard (docs/stds/CHEAT_SHEET.md v2.0.0).

There is no database and no per-item fields anymore — a proposed addition is one
markdown bullet line, full stop. This script checks that ONE line against the
caps, banned openers and hedge/narrative words in CHS-4/6/7. It does not, and
cannot, check CHS-2 gate 5 ("not already said") — that requires reading the
live page, which is judgement, not a regex.

Exit 0 = pass, 1 = fail. Prints one line per violation.
"""

import argparse
import re
import sys

MAX_WORDS = 35  # CHS-6 — whole bullet, not split across fields

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


def strip_formatting(text):
    """Strip inline code, bold and markdown link syntax so counts reflect the
    words a reader actually parses, not the markup around them."""
    text = re.sub(r'`[^`]*`', ' ', text)
    text = text.replace('**', '')
    return text


def count_words(text):
    return len([w for w in strip_formatting(text).split() if w.strip()])


def count_lines(text):
    return len([ln for ln in text.splitlines() if ln.strip()])


def find_phrases(text, phrases):
    low = ' ' + re.sub(r'[^a-z0-9\s]+', ' ', strip_formatting(text).lower()) + ' '
    low = re.sub(r'\s+', ' ', low)
    return [p for p in phrases if f' {p} ' in low]


def check(bullet):
    problems = []

    if not bullet.strip():
        return ['bullet is empty']

    if count_lines(bullet) > 1:
        problems.append('bullet spans more than one line — CHS-5 wants one bullet, '
                         'one fact (a fenced code block for a command sequence is fine, '
                         'that goes under the bullet, not counted here)')

    words = count_words(bullet)
    if words > MAX_WORDS:
        problems.append(f'{words} words, max {MAX_WORDS} (CHS-6)')

    # Banned opener check: strip a leading bold marker, then check the first words.
    lead = re.sub(r'^\*\*', '', bullet.strip())
    normalised = re.sub(r'[^a-z0-9\s]+', ' ', lead.lower()).strip()
    for opener in sorted(BANNED_OPENERS, key=len, reverse=True):
        if normalised == opener or normalised.startswith(opener + ' '):
            problems.append(
                f'opens with banned non-informative "{opener}" — '
                f'front-load the informative words instead (CHS-4)')
            break

    for hedge in find_phrases(bullet, HEDGE_WORDS):
        problems.append(
            f'hedge "{hedge}" — an uncertain fact fails admission gate 4, '
            f'it does not get hedged onto the page (CHS-7)')
    for phrase in find_phrases(bullet, NARRATIVE_PHRASES):
        problems.append(f'discovery narrative "{phrase}" (CHS-7)')

    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cmd', choices=['check'])
    parser.add_argument('--bullet', required=True,
                         help='the exact markdown bullet line, as it would be written to the page')
    args = parser.parse_args()

    problems = check(args.bullet)
    if problems:
        print('FAIL — rewrite before proposing it:')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('PASS (still needs CHS-2 gate 5 — read the live page — and the maintainer\'s yes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
