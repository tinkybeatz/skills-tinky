# Mode 🔧 Diagnose — official 5-step procedure

When the user says: "Claude isn't applying X", "Claude ignores my instruction", "I wrote Y in CLAUDE.md but Claude does Z".

Source: [Anthropic — memory.md, Troubleshoot memory issues section](https://code.claude.com/docs/en/memory.md).

---

## Step 1 — Is the file actually loaded?

**Action**: ask the user to run `/memory` in Claude Code.

**What we check**:
- Does the target CLAUDE.md appear in the list?
- At which cascade level is it?
- Are there other, unexpected CLAUDE.md files loaded in parallel?

**If the file doesn't appear**:
- Check the location (see Step 2)
- Check that Claude Code was started from the correct CWD
- Check there's no typo in the name (`CLAUDE.md`, not `claude.md`, not `CLAUDE.MD`)

---

## Step 2 — Is the location correct?

**Action**: compare the file's location against the expected cascade.

| If the rule should apply... | Then the file should be... |
|---|---|
| To all of the user's projects | `~/.claude/CLAUDE.md` |
| To this project, for the whole team | `<project>/CLAUDE.md` or `<project>/.claude/CLAUDE.md` |
| To this project, just for me | `<project>/CLAUDE.local.md` |
| To a single technical sub-domain only | `<project>/<subdir>/CLAUDE.md` |

**Common pitfalls**:
- File placed in a subdirectory when the rule should be global → walk-up stops too low
- `.claude/CLAUDE.md` AND `CLAUDE.md` at the root at the same time → Claude loads both, may have conflicts
- `CLAUDE.local.md` accidentally committed → not gitignored → other devs receive your preferences

---

## Step 3 — Is the instruction verifiable?

**Test**: can you write a grep, a linter rule, or a test that proves the rule is being followed?

| Instruction | Verifiable? |
|---|---|
| "Use 2-space indentation" | ✅ (linter) |
| "React imports must be `import * as React`" | ✅ (grep) |
| "Responses in French" | ✅ (language of the output) |
| "Be careful with the database" | ❌ vague |
| "Write good code" | ❌ vague |
| "Always test before commit" | ⚠️ verifiable only if "test" is defined precisely |

**If not verifiable**: rewrite the rule in concrete terms.

**Before**: `Be thoughtful about performance.`
**After**: `Any loop over > 100 items must use a streaming approach, not in-memory accumulation.`

---

## Step 4 — Is there a contradiction?

**Action**:
1. List every loaded CLAUDE.md (from Step 1).
2. Grep the rule AND its opposites/variants in each of them.
3. Check the `.claude/rules/*.md` files too.
4. Check `MEMORY.md` (may contain a contradictory learned preference).

**Example contradiction**:
- `~/.claude/CLAUDE.md`: "Always use TypeScript"
- `<project>/CLAUDE.md`: "This project is plain JavaScript (legacy)"
- → Claude may arbitrate arbitrarily.

**Resolution**:
- Pick a **single source of truth** per rule
- Put the rule at the most specific relevant level
- Remove it from the other levels

---

## Step 5 — Do you need a hook?

**The decisive question**: "Must this rule be followed 100% of the time, no exceptions?"

**If YES → CLAUDE.md isn't enough. Migrate to a hook.**

CLAUDE.md = probabilistic guidance. For strict enforcement, use:
- **PreToolUse hook** — block an action before execution (e.g. refuse edits to `.env`)
- **PostToolUse hook** — check afterward (e.g. reject a commit with no tests)
- **Stop hook** — check before the session ends

**Migration example**:

**Before** in CLAUDE.md
```markdown
- NEVER commit into `.env`
- ALWAYS run the tests before a commit
```

**After**:
- PreToolUse hook that blocks `git commit` if `.env` is staged
- PreToolUse hook that blocks `git commit` if `npm test` hasn't been run recently

**Anthropic docs**: [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md).

---

## Full workflow (mental script)

```
1. /memory → file loaded?
   ├── NO → fix location, retest
   └── YES → continue

2. Location = expected scope?
   ├── NO → move it within the cascade, retest
   └── YES → continue

3. Instruction verifiable?
   ├── NO → rewrite concretely, retest
   └── YES → continue

4. Cross-level contradiction?
   ├── YES → unify, retest
   └── NO → continue

5. Critical, zero-tolerance rule?
   ├── YES → migrate to a hook, that's the fix
   └── NO → CLAUDE.md did its job, the session context is probably saturated
              → test with /context: if > 80% used, /clear
```

---

## Special cases

### "Claude kept forgetting after /compact"

- Check the rule is in the **project root** or `~/.claude/CLAUDE.md` (both survive compaction)
- NOT in a subdirectory (lazy-load only)
- NOT in the conversation alone (lost on compaction)

### "Claude applies the rule sometimes but not always"

- Either the rule is at the bottom of a long CLAUDE.md → reposition it at the top
- Or the CLAUDE.md is too long overall → refactor (Mode ✂️)
- Or the instruction is ambiguous depending on context → specify the conditions under which it applies

### "A new session doesn't see my recent edit"

- Check the session was restarted after the edit
- Check there's no cache (rare, but possible in some environments)
- `/memory` to confirm the loaded version is the latest
