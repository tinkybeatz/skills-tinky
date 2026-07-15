---
name: "test-writer"
description: "Writes production-quality unit and integration tests for TypeScript and React. Use this skill whenever the user asks to write tests, test a component, test a function, add tests, test a hook, verify a behavior, cover code, or mentions: test, spec, vitest, jest, testing-library, coverage, TDD, mock, assertion. Even if the user simply says 'test this' or 'add tests', this skill applies."
---

# Test Writer

You write unit and integration tests that verify **observable behavior**, not internal implementation. Every test you write must answer the question: "if this test breaks, has a real bug just been introduced?"

## Core principles

### The Testing Trophy (not the pyramid)

For React/TypeScript apps, invest your testing effort like this:

```
         E2E          ← A few (Playwright — critical journeys)
      Integration     ← THE MAJORITY of tests (component + children + hooks + context)
        Unit          ← Some (pure functions, utilities, isolated hooks)
   Static Analysis    ← TypeScript + ESLint (free, catches the most bugs)
```

Integration tests give the best return on investment: a single test that renders a form, fills it in and submits it covers more real bugs than 20 unit tests on individual components.

### Test behavior, not implementation

A good test survives a refactor. If you change the internal implementation without changing user-facing behavior, no test should break.

**Good**: "when the user clicks Save, the form submits the data"
**Bad**: "when the user clicks, setState is called with { loading: true }"

## Step 0 — Detect the test environment

Before writing a test, check the project's test stack:

1. Look for `vitest.config.ts`, `jest.config.ts`, or the `test` section in `vite.config.ts`
2. Check the dependencies in `package.json`: `vitest`, `jest`, `@testing-library/react`, `msw`, `@testing-library/user-event`
3. Look for a `setupTests.ts` or `test/setup.ts` file
4. Look at existing tests to understand the patterns in use

If no test infrastructure exists, propose the minimal setup needed before writing any tests. See `references/setup.md` for the installation guide.

## Step 1 — Analyze the code under test

Read the file under test in full. Identify:

| Type | What to test | Approach |
|------|---------------------|----------|
| **Pure function** | Inputs → outputs, edge cases, errors | Direct unit test |
| **Custom hook** | Returned values, state transitions, side effects | `renderHook` or via a consumer component |
| **Simple UI component** | Correct rendering, props, variants | `render` + assertions on the DOM |
| **Interactive component** | User actions → visible result | `render` + `userEvent` + assertions |
| **Component with API** | Loading, data, error | `render` + MSW handlers |
| **Component with routing** | Navigation, params, guards | `render` with a `MemoryRouter` wrapper |

## Step 2 — Write the tests

### Required structure: AAA (Arrange, Act, Assert)

```typescript
it('filters products by category', async () => {
  // Arrange — set up state, render, create the data
  const user = userEvent.setup()
  render(<ProductList products={mockProducts} />)

  // Act — perform the user action
  await user.selectOptions(screen.getByLabelText(/category/i), 'clothing')

  // Assert — check the result
  expect(screen.getByText('T-shirt')).toBeInTheDocument()
  expect(screen.queryByText('Laptop')).not.toBeInTheDocument()
})
```

### Test naming

```typescript
// describe: the unit under test
// it: the behavior, starting with a lowercase verb

describe('AuthGuard', () => {
  it('redirects unauthenticated users to the login page', () => { ... })
  it('renders the children when the user is authenticated', () => { ... })
  it('shows a spinner while the check is in progress', () => { ... })
})
```

- Start `it` with a verb: renders, redirects, returns, calls, sends, hides
- Describe the behavior, not the implementation
- At most 2 levels of nested `describe`

### RTL query priority

Use in this order (from most to least recommended):

1. **`getByRole`** — the best, reflects the accessibility tree
2. **`getByLabelText`** — for form fields
3. **`getByPlaceholderText`** — fallback for inputs without a label
4. **`getByText`** — for non-interactive content
5. **`getByDisplayValue`** — for pre-filled fields
6. **`getByTestId`** — last resort only

**Forbidden**: `container.querySelector()`, queries by CSS class, queries by DOM structure.

### userEvent, not fireEvent

```typescript
// GOOD — simulates real browser behavior
const user = userEvent.setup()
await user.click(screen.getByRole('button', { name: /save/i }))
await user.type(screen.getByLabelText(/email/i), 'test@example.com')

// BAD — low-level synthetic event
fireEvent.click(button)
fireEvent.change(input, { target: { value: 'test' } })
```

### Asynchronous tests

```typescript
// For elements that appear after loading
expect(await screen.findByText('Alice')).toBeInTheDocument()

// To wait for an element to disappear
await waitFor(() => {
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
})
```

- `findBy*` = `waitFor` + `getBy` combined — prefer it
- Never use `setTimeout` or `sleep` in tests

## What to mock, what not to mock

### Mock (at the boundaries)

| What | How |
|------|---------|
| Network requests | MSW (`http.get`, `http.post`) |
| Timers | `vi.useFakeTimers()` |
| Browser APIs missing in jsdom | `vi.stubGlobal('IntersectionObserver', ...)` |
| Non-deterministic values | `vi.spyOn(Date, 'now')`, `vi.spyOn(crypto, 'randomUUID')` |
| Navigation (react-router) | `vi.mock('react-router-dom', ...)` or `MemoryRouter` |

### Do NOT mock (internal modules)

| What | Why |
|------|---------|
| Child components | That's the whole point of integration tests |
| Pure functions/utilities | They are fast and deterministic |
| Internal state management | Test through the UI, not by inspecting the store |
| The module under test | Obviously |

If a test needs more than 3 mocks, that's a sign the code needs refactoring, not more mocks.

## Patterns by test type

### Pure function

```typescript
describe('formatCurrency', () => {
  it('formats euros with two decimals', () => {
    expect(formatCurrency(24.5, 'EUR')).toBe('€24.50')
  })

  it('returns "—" for null values', () => {
    expect(formatCurrency(null, 'EUR')).toBe('—')
  })

  it('handles large numbers with separators', () => {
    expect(formatCurrency(1234567.89, 'EUR')).toBe('€1 234 567.89')
  })
})
```

### Component with a form

```typescript
describe('LoginForm', () => {
  it('submits the entered credentials', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<LoginForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'secret123')
    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'secret123',
    })
  })

  it('shows validation errors on empty submission', async () => {
    const user = userEvent.setup()
    render(<LoginForm onSubmit={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument()
  })
})
```

### Component with API data (MSW)

```typescript
describe('UserList', () => {
  it('shows the users after loading', async () => {
    server.use(
      http.get('/bff/api/users', () =>
        HttpResponse.json([
          { id: '1', name: 'Alice' },
          { id: '2', name: 'Bob' },
        ])
      )
    )

    render(<UserList />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()
    expect(await screen.findByText('Alice')).toBeInTheDocument()
    expect(screen.getByText('Bob')).toBeInTheDocument()
  })

  it('shows an error message when the API fails', async () => {
    server.use(
      http.get('/bff/api/users', () =>
        HttpResponse.json({ error: 'fail' }, { status: 500 })
      )
    )

    render(<UserList />)

    expect(await screen.findByText(/error/i)).toBeInTheDocument()
  })
})
```

### Custom hook

```typescript
describe('useDebounce', () => {
  it('returns the value after the delay', async () => {
    vi.useFakeTimers()
    const { result } = renderHook(() => useDebounce('hello', 300))

    expect(result.current).toBe('') // initial value

    act(() => { vi.advanceTimersByTime(300) })

    expect(result.current).toBe('hello')
    vi.useRealTimers()
  })
})
```

Prefer testing a hook **through a component** when the hook is tightly coupled to the UI. If `useCounter` is only used in `<Counter />`, test `<Counter />` directly.

## Factories and test utilities

Create typed factories instead of copy-pasted fixtures:

```typescript
// test/factories.ts
export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    role: 'admin',
    ...overrides,
  }
}
```

Create a reusable render wrapper if the project uses providers:

```typescript
// test/utils.tsx
export function renderWithProviders(
  ui: React.ReactElement,
  options: { user?: Partial<User> } = {}
) {
  const testUser = createUser(options.user)
  return render(ui, {
    wrapper: ({ children }) => (
      <QueryClientProvider client={new QueryClient()}>
        <AuthContext.Provider value={{ user: testUser }}>
          {children}
        </AuthContext.Provider>
      </QueryClientProvider>
    ),
  })
}
```

## Accessibility

Add an `axe` check to your integration tests — it costs a single line:

```typescript
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

it('has no accessibility violations', async () => {
  const { container } = render(<LoginForm />)
  expect(await axe(container)).toHaveNoViolations()
})
```

## File organization

```
src/
├── shared/
│   ├── ui/
│   │   ├── Badge.tsx
│   │   └── Badge.test.tsx          ← co-located with the component
│   └── lib/
│       ├── cn.ts
│       └── cn.test.ts
├── features/
│   └── auth/
│       ├── hooks/
│       │   ├── useSessionCheck.ts
│       │   └── useSessionCheck.test.ts
│       └── ui/
│           ├── AuthGuard.tsx
│           └── AuthGuard.test.tsx
└── test/
    ├── setup.ts                    ← global configuration (MSW, matchers)
    ├── handlers.ts                 ← default MSW handlers
    ├── factories.ts                ← factory functions
    └── utils.tsx                   ← renderWithProviders, helpers
```

Tests co-located with the source code (not in a separate `__tests__` folder).

## Failure modes

| Problem | Action |
|----------|--------|
| No test infrastructure in the project | Propose the setup first (see `references/setup.md`), don't write tests into a void |
| Component with no accessible semantics (no roles, no labels) | Flag the problem and propose adding the ARIA attributes before writing the test |
| Too many mocks needed | Sign the code is too coupled — flag it and propose a refactor |
| Test that breaks on a refactor without a behavior change | The test is too tied to the implementation — rewrite it with role/label queries |
| Snapshot of 500+ lines | Don't create it — use targeted assertions or inline snapshots |
| Async test that passes without waiting | Check that every async assertion uses `await` / `findBy` |
| High coverage but bugs in production | Review the quality of the assertions — an `expect(true).toBe(true)` still bumps coverage |

## Resources

| File | When to read it |
|---------|---------------|
| `references/setup.md` | When the project has no test infrastructure configured |
| `references/msw-patterns.md` | When the test involves API calls |
| `references/anti-patterns.md` | To check you aren't falling into the classic traps |
