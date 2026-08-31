# Close — ending a cycle

Governed by CYC-13. The close routine has one job beyond bookkeeping: turn what went wrong into
something the next intake can use.

## Sequence

**1. Record `Shipped:` and `Cut:` on every topic.** `cycle.py close` refuses without them.

- `Shipped:` — what actually landed, in the outcome's terms.
- `Cut:` — everything dropped: the surviving `~` tasks, any hammered scope, anything rolled to next
  cycle. This list is the cycle's most useful artifact; it is the record of trade-offs that would
  otherwise be invisible by the next planning meeting.

Ask; don't derive it. Task checkboxes tell you what got done, not what was consciously abandoned
versus quietly forgotten.

Ask for the divergences too, or rather read them: `cycle.py close` lists every `As built` entry
recorded during the cycle (CYC-19). They are shaping feedback of the same kind as a scope that never
reached downhill, arriving from the other end — that one says the work was under-shaped, this one says
it was **mis**-shaped, confidently and in writing.

**2. Run the close.**
```bash
python3 scripts/cycle.py close
```
It validates the whole doc, requires the two fields per topic, flips `Status: closed`, and prints the
shaping signal.

**3. Read the shaping signal out loud.** Every scope that never reached `downhill` gets listed. Shape
Up's stopping test is that remaining work be *"all downhill. No unsolved problems; no open questions.
Any uphill work at the end of the cycle points to an oversight in the shaping or a hole in the
concept."*

Frame it as exactly that — a shaping oversight, not a performance problem. The useful question is
*which question, asked at intake, would have surfaced this?* That answer belongs in the next cycle's
interview.

**4. Answer or drop every open question.** An open question carried silently into an archive is a
question that will be rediscovered the hard way. If it's still open and still matters, it becomes a
topic or a rabbit hole in the next cycle.

**5. Mirror once more** (see `mirror.md`) so the Notion page shows the final state, then stop
mirroring that cycle.

**6. Hand the retro to `sprint-review`.** That skill reads commits, PRs and code to produce the
progress report, efficiency and architecture review. This skill does not do retrospection and should
not try — pass it the closed doc as input.

**7. Route any durable facts out.** A gotcha or convention the cycle surfaced belongs in
`foleon-ripley` / `foleon-fio`'s `knowledge.md` (CYC-12), from where `foleon-cheatsheet` can mirror it
if it clears the gates. Do this *before* the doc is archived — after close, nothing reads it again.

## After close

The doc is read-only: `cycle.py log` refuses, and no hill value may change. Follow-on work belongs to
the next cycle's doc, which starts with `cycle.py new` — refused while any cycle is still active, so
closing properly is what unblocks the next cycle.
