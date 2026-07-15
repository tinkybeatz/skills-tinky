# Guidance by feature type

Load this file when the feature under analysis matches one of the archetypes below. The listed checks are meant to be applied **in addition to** the 9 dimensions of the main framework — not instead of them.

---

## Destructive action

**Examples**: deleting a user, deleting a document, deleting a project, permanent cancellation, unsubscribing, data purge, revoking access.

**Check in this order**:

1. **Real reversibility.** Is the action truly irreversible, or could it be made undoable? A "soft" deletion (soft delete with 30-day retention) protects better than hard deletion in 90% of cases.
2. **Business alternatives before deletion.** Deactivation, archiving, soft delete, restore, prior export, role-based restriction. Often one of these options meets the need without the risk.
3. **Strong confirmation only if the risk warrants it.** If the user can undo in 1 click within 5 minutes, a blocking modal is a cost for nothing. If the loss is real and permanent: a stronger confirmation (typing the name, a two-step flow, a delay).
4. **Explicit consequences.** List what will be lost: data, revoked access, impacted dependencies, linked invoices, affected users. The user should not discover a consequence after the fact.
5. **Restore strategy** if realistic: who can restore, within what window, until when. Failing that, explain why not.

**Common traps**:
- An "Are you sure?" modal with no content = friction that protects no one.
- Hard deletion when the real business need is "stop showing me this item".
- No log/audit of who deleted what and when.

---

## Data creation or editing

**Examples**: creation form, profile editing, business resource creation, multi-field configuration.

**Check**:

1. **Validation**: when (live, blur, submit)? Helpful messages (what to do to fix it, not just "invalid")? Are the rules consistent between front and back?
2. **Errors**: positioned in the right place (the field concerned), not in an anonymous banner at the top of the page. Server errors translated into user language.
3. **Saving / loss prevention**: auto-save or a warning if the user leaves with unsaved changes? For long forms, intermediate saving.
4. **Fields**: are they all necessary? Logical order (following the user's mental model, not the DB schema)? Are optional fields marked as such?
5. **Smart defaults**: can anything be pre-filled from context? A field that 95% of users fill in the same way = a candidate for a default.
6. **Consistency between creation and editing**: same rules, same validation, same UI? If not, why?

**Common traps**:
- A "required" field with no asterisk or indication.
- Validation only at submit → the user discovers 3 errors after clicking.
- The form resets on a server error.

---

## List, table, or dashboard

**Examples**: user list, invoice table, analytics dashboard, ticket view, task queue.

**Check**:

1. **Search**: available if > 20 items? On the right fields (what the user knows, not an internal ID)?
2. **Sorting**: on the relevant columns? Default sort aligned with the need (most recent first, highest priority first)?
3. **Filters**: do they cover the real decision axes (status, date, owner, type)? Combinable? Persisted in the URL for sharing?
4. **Pagination**: reasonable page size, total count visible, position preserved after an action?
5. **Empty states**: distinguish "empty for the first time" (onboarding) vs "filter with no results" (action: reset filters) vs "loading error" (action: retry).
6. **Bulk actions**: if an action is useful on 1 item, it's often useful on N items. Multi-select + bulk action?
7. **Missing information to decide**: does the user have enough signal *in the list* to decide whether to act, or do they have to open each item?
8. **Visual noise**: too many columns, too many colors, too many badges = lower readability. Establish hierarchy.

**Common traps**:
- Pagination that resets the sort/filter.
- A generic empty state "No data" with no CTA.
- Bulk action with no progress feedback.

---

## Multi-step workflow

**Examples**: onboarding, checkout, multi-screen configuration, wizard.

**Check**:

1. **Visible progress**: where the user is, how many steps remain, what is mandatory vs optional.
2. **Intermediate saving**: if the user leaves at step 3 of 5, do they get their state back? If not → massive friction.
3. **Non-destructive back navigation**: going back to the previous step must not wipe what was entered.
4. **Recovery after error**: if step 4 fails (network, server validation), the user must not redo 1, 2, 3.
5. **Are the steps necessary?** Each added step has an abandonment cost. Justify each one. Merge trivial steps.
6. **Mandatory vs optional vs irreversible**: clear at each step. An irreversible step (e.g., payment) must be announced as such.
7. **Exit allowed at any time**: the user must be able to abandon without feeling trapped.

**Common traps**:
- No breadcrumb / progress indicator.
- Validation at step N that requires data entered at step 1, without recalling it.
- A "Next" button that becomes "Submit" without announcing the final nature of the action.
