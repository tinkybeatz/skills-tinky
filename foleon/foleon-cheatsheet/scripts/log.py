#!/usr/bin/env python3
"""Dedupe-before-append enforcement for the PCS-6 discoveries log.

The cheat sheet gets its non-redundancy from a byte-stable Dedupe key (row.py).
The log had only an instruction telling the model to "search first", which is
weaker on the side that matters most for Claude. This closes that gap.

  check    find existing entries whose symptom overlaps a candidate.
           Exit 1 when one looks like a duplicate — extend that entry instead.
  append   validate the schema, run `check`, and append only if clean.
  lint     verify every entry in the log conforms to the PCS-6 schema.

Similarity is token-set overlap (Jaccard) on the symptom, restricted to the same
area. Deliberately crude and deterministic: it is a tripwire for the model, not a
semantic search — a near-miss it fails to flag is caught by the human review gate,
whereas a silently duplicated log entry is not caught by anything.
"""

import argparse
import os
import re
import sys

AREAS = [
    'Editor', 'Viewer', 'Core / rendering',
    'Build & tooling', 'Tests & Playwright', 'Conventions',
]

LOG_RELPATH = os.path.join(
    'foleon', 'foleon-ripley', 'references', 'knowledge.md')

ENTRY_RE = re.compile(
    r'^- (?P<date>\d{4}-\d{2}-\d{2}) · (?P<area>[^·]+?) · (?P<symptom>.+?) — ',
    re.S)

# Words too common in this domain to signal a duplicate on their own. Quantifiers
# are included because "every"/"all"/"some" distinguish nothing and, left in,
# inflate the union enough to hide a real duplicate.
STOPWORDS = {
    'the', 'a', 'an', 'in', 'on', 'of', 'to', 'and', 'or', 'is', 'are', 'not',
    'with', 'for', 'from', 'it', 'its', 'no', 'only', 'but', 'that', 'this',
    'be', 'has', 'have', 'when', 'after', 'before', 'wont', 'cant',
    'all', 'every', 'some', 'any', 'one', 'two', 'still', 'always', 'never',
    'does', 'did', 'get', 'gets', 'was', 'were', 'you', 'your',
}

DUPLICATE_AT = 0.60   # exit 1 — almost certainly the same finding
REPORT_AT = 0.30      # worth showing the model
MIN_SHARED = 2        # one shared word is coincidence, not a duplicate


def repo_root(start):
    d = os.path.dirname(os.path.realpath(start))
    while d != '/':
        if os.path.isfile(os.path.join(d, 'CATEGORIES.md')):
            return d
        d = os.path.dirname(d)
    raise SystemExit('log.py: could not locate the skills-tinky root')


def log_path():
    return os.path.join(repo_root(__file__), LOG_RELPATH)


def read_entries(path):
    """Return [(line_no, area, symptom, first_line)] for every entry."""
    entries = []
    with open(path, encoding='utf-8') as fh:
        lines = fh.readlines()
    for i, line in enumerate(lines, start=1):
        if not line.startswith('- 20'):
            continue
        # An entry's header may wrap; the em-dash can end the first line.
        joined = line.rstrip('\n')
        if ' — ' not in joined and not joined.endswith('—'):
            joined = joined + ' ' + (lines[i].strip() if i < len(lines) else '')
        m = ENTRY_RE.match(joined if ' — ' in joined else joined + ' — x')
        if m:
            entries.append((i, m.group('area').strip(),
                            m.group('symptom').strip(), line.rstrip('\n')))
    return entries


def stem(word):
    """Crudest possible stemmer: kill a trailing plural 's'.

    Enough to stop "snapshot" and "snapshots" reading as different findings,
    which is the failure mode that actually shows up in symptom phrasing.
    """
    if len(word) > 3 and word.endswith('s') and not word.endswith('ss'):
        return word[:-1]
    return word


def tokens(text):
    text = re.sub(r'`[^`]*`', ' ', text.lower())
    words = re.findall(r'[a-z0-9]+', text)
    return {stem(w) for w in words if w not in STOPWORDS and len(w) > 2}


def similarity(a, b):
    """Containment, not Jaccard.

    Jaccard punishes length differences, so "Snapshot fails in CI" scores badly
    against "Snapshot passes locally, fails in CI" — the exact near-duplicate
    this needs to catch. Containment over the shorter symptom handles it, and
    MIN_SHARED keeps a single coincidental word from tripping it.
    """
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    shared = ta & tb
    if len(shared) < MIN_SHARED:
        return 0.0
    return len(shared) / min(len(ta), len(tb))


def check(area, symptom, quiet=False):
    path = log_path()
    hits = []
    for line_no, e_area, e_symptom, raw in read_entries(path):
        if e_area != area:
            continue
        score = similarity(symptom, e_symptom)
        if score >= REPORT_AT:
            hits.append((score, line_no, e_symptom))
    hits.sort(reverse=True)

    if not quiet:
        if not hits:
            print(f'no similar entry in "{area}" — safe to append')
        else:
            print(f'{len(hits)} similar entr(ies) in "{area}":')
            for score, line_no, e_symptom in hits[:5]:
                flag = 'DUPLICATE' if score >= DUPLICATE_AT else 'similar  '
                print(f'  [{flag} {score:.2f}] line {line_no}: {e_symptom}')
    if hits and hits[0][0] >= DUPLICATE_AT:
        if not quiet:
            print('\nExtend the existing entry and refresh its date — '
                  'do not append a near-duplicate (PCS-6).')
        return 1
    return 0


def lint():
    path = log_path()
    with open(path, encoding='utf-8') as fh:
        content = fh.read()
    starts = [i for i, ln in enumerate(content.splitlines(), start=1)
              if ln.startswith('- 20')]
    entries = read_entries(path)
    problems = []
    found_lines = {e[0] for e in entries}
    for line_no in starts:
        if line_no not in found_lines:
            problems.append(f'line {line_no}: does not match the PCS-6 schema')
    for line_no, area, symptom, _ in entries:
        if area not in AREAS:
            problems.append(f'line {line_no}: area {area!r} is not one of the six')
    # every entry needs refs: and sheet:
    blocks = re.split(r'\n(?=- 20\d\d-)', content)
    for b in blocks:
        if not b.startswith('- 20'):
            continue
        head = b.splitlines()[0][:70]
        if 'sheet:' not in b:
            problems.append(f'missing "sheet:" — {head}')
        if 'refs:' not in b:
            problems.append(f'missing "refs:" — {head}')

    print(f'{len(entries)} entries parsed')
    if problems:
        print('FAIL:')
        for p in problems:
            print(f'  - {p}')
        return 1
    print('PASS — all entries conform to PCS-6')
    return 0


def append(args):
    if args.area not in AREAS:
        raise SystemExit(f'unknown area {args.area!r}')
    if check(args.area, args.symptom) != 0:
        print('\nrefusing to append (see above)')
        return 1
    sheet = args.sheet or 'none'
    refs = args.refs or '—'
    entry = (f'- {args.date} · {args.area} · {args.symptom} — {args.finding}'
             f' · refs: {refs} · sheet: {sheet}\n')
    with open(log_path(), 'a', encoding='utf-8') as fh:
        fh.write(entry)
    print(f'appended to {LOG_RELPATH}')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)

    c = sub.add_parser('check', help='look for an existing similar entry')
    c.add_argument('--area', required=True)
    c.add_argument('--symptom', required=True)

    a = sub.add_parser('append', help='dedupe-checked append')
    a.add_argument('--date', required=True)
    a.add_argument('--area', required=True)
    a.add_argument('--symptom', required=True)
    a.add_argument('--finding', required=True)
    a.add_argument('--refs', default='')
    a.add_argument('--sheet', default='none')

    sub.add_parser('lint', help='verify the whole log against the schema')

    args = p.parse_args()
    if args.cmd == 'check':
        return check(args.area, args.symptom)
    if args.cmd == 'append':
        return append(args)
    return lint()


if __name__ == '__main__':
    sys.exit(main())
