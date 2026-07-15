# Test anti-patterns — What NOT to do

## 1. Testing the implementation

```typescript
// ❌ BAD — tests internal state
it('sets loading to true', () => {
  const { result } = renderHook(() => useUsers())
  expect(result.current.isLoading).toBe(true)
  // What happens if you rename isLoading to pending?
  // The test breaks, but the behavior hasn't changed
})

// ✅ GOOD — tests the visible behavior
it('shows a spinner while loading', () => {
  render(<UserList />)
  expect(screen.getByRole('progressbar')).toBeInTheDocument()
})
```

## 2. Queries by DOM structure

```typescript
// ❌ BAD — coupled to the HTML structure and the CSS classes
const button = container.querySelector('.btn-primary')
const input = container.querySelector('#email-field')
const card = wrapper.find('div.card > span.title')

// ✅ GOOD — semantic queries
const button = screen.getByRole('button', { name: /save/i })
const input = screen.getByLabelText(/email/i)
const card = screen.getByText('My title')
```

## 3. Over-mocking

```typescript
// ❌ BAD — everything is mocked, you're no longer testing anything real
vi.mock('./useAuth')
vi.mock('./useTheme')
vi.mock('./Button')
vi.mock('./Layout')
vi.mock('@/shared/lib/cn')
vi.mock('react-router-dom')

it('renders the component', () => {
  render(<Dashboard />)
  // Fine, but what have we proven? That the mocks work.
})

// ✅ GOOD — mock only at the boundaries (network, navigation)
it('shows the dashboard with its data', async () => {
  server.use(
    http.get('/bff/api/dashboard', () =>
      HttpResponse.json({ stats: { users: 42 } })
    )
  )
  render(<Dashboard />)
  expect(await screen.findByText('42')).toBeInTheDocument()
})
```

## 4. Giant snapshots

```typescript
// ❌ BAD — a 500-line snapshot that nobody reads
it('matches the snapshot', () => {
  const { container } = render(<ComplexPage />)
  expect(container).toMatchSnapshot()
  // Result: a 500-line .snap file updated blindly
})

// ✅ GOOD — targeted assertions or small inline snapshots
it('shows the right title and stats', () => {
  render(<DashboardHeader name="Ada" stats={3} />)
  expect(screen.getByRole('heading')).toHaveTextContent('Ada')
  expect(screen.getByText('3')).toBeInTheDocument()
})

// ✅ OK — inline snapshot for a short value
it('formats the date correctly', () => {
  expect(formatDate(new Date('2025-01-15'))).toMatchInlineSnapshot('"Jan 15, 2025"')
})
```

## 5. Tests with no assertion

```typescript
// ❌ BAD — the test always passes, it verifies nothing
it('renders without error', () => {
  render(<MyComponent />)
  // no expect → false sense of security
})

// ✅ GOOD
it('shows the form title', () => {
  render(<MyComponent />)
  expect(screen.getByRole('heading', { name: /sign up/i })).toBeInTheDocument()
})
```

## 6. Async without await

```typescript
// ❌ BAD — the test finishes before the assertion runs
it('loads the data', () => {
  render(<UserList />)
  waitFor(() => { // ← missing the await!
    expect(screen.getByText('Alice')).toBeInTheDocument()
  })
  // The test ALWAYS passes because the assertion is never evaluated
})

// ✅ GOOD
it('loads the data', async () => {
  render(<UserList />)
  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument()
  })
})
```

## 7. Copy-pasting setup

```typescript
// ❌ BAD — 15 lines of setup duplicated in every test
it('test 1', () => {
  const queryClient = new QueryClient(...)
  const user = { id: '1', email: 'test@test.com', role: 'admin' }
  render(
    <QueryClientProvider client={queryClient}>
      <AuthProvider value={user}>
        <MyComponent />
      </AuthProvider>
    </QueryClientProvider>
  )
  // ...
})

// ✅ GOOD — centralized factory + wrapper
it('test 1', () => {
  renderWithProviders(<MyComponent />, { user: { role: 'admin' } })
  // ...
})
```

## 8. Testing third-party libraries

```typescript
// ❌ BAD — you're testing React Query, not your code
it('invalidates the cache after a mutation', async () => {
  const queryClient = new QueryClient()
  // ... check that invalidateQueries is called
  // Working correctly is React Query's job, not your tests' job
})

// ✅ GOOD — test the visible result
it('refreshes the list after a deletion', async () => {
  render(<UserManagement />)
  const user = userEvent.setup()

  await user.click(screen.getByRole('button', { name: /delete Alice/i }))
  await user.click(screen.getByRole('button', { name: /confirm/i }))

  await waitFor(() => {
    expect(screen.queryByText('Alice')).not.toBeInTheDocument()
  })
})
```

## 9. fireEvent instead of userEvent

```typescript
// ❌ Less realistic — no intermediate focus, blur, keydown
fireEvent.change(input, { target: { value: 'hello' } })
fireEvent.click(button)

// ✅ Simulates real user behavior
const user = userEvent.setup()
await user.type(input, 'hello')
await user.click(button)
```

## 10. Tests that are too big (God Test)

```typescript
// ❌ BAD — a single test that checks 10 things
it('works correctly', async () => {
  // renders the component
  // checks the title
  // fills in the form
  // submits
  // checks the loading state
  // checks the success
  // checks the navigation
  // checks the toast
  // checks the cache was invalidated
  // checks the analytics tracking
})

// ✅ GOOD — one test per behavior
it('shows the empty form on mount', () => { ... })
it('submits the entered data', async () => { ... })
it('shows an error when submission fails', async () => { ... })
it('redirects to the list after success', async () => { ... })
```
