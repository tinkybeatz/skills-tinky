# MSW Patterns — Mock Service Worker

## Why MSW

MSW intercepts at the network level. Your `fetch`/`axios`/`api.get` code runs exactly as it does in production. No fragile `vi.mock('./api')`.

## Basic setup

```typescript
// src/test/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/bff/api/v1/backend/admin/sites', () => {
    return HttpResponse.json([
      { id: '1', name: 'Central Station', address: '12 Paris Street' },
      { id: '2', name: 'North Station', address: '45 North Avenue' },
    ])
  }),

  http.post('/bff/api/v1/backend/admin/catalog', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({ id: 'new-1', ...body }, { status: 201 })
  }),
]
```

```typescript
// src/test/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

## Per-test override

```typescript
import { server } from '@/test/server'
import { http, HttpResponse } from 'msw'

it('shows an error message when the API fails', async () => {
  // Override the default handler for this test only
  server.use(
    http.get('/bff/api/v1/backend/admin/sites', () => {
      return HttpResponse.json(
        { error: 'internal_error', message: 'Database down' },
        { status: 500 }
      )
    })
  )

  render(<SiteList />)
  expect(await screen.findByText(/error/i)).toBeInTheDocument()
})
```

## Testing the requests that are sent

```typescript
it('sends the right data to the server', async () => {
  let capturedBody: unknown

  server.use(
    http.post('/bff/api/v1/backend/admin/catalog', async ({ request }) => {
      capturedBody = await request.json()
      return HttpResponse.json({ id: '1' }, { status: 201 })
    })
  )

  const user = userEvent.setup()
  render(<CreateProgramForm />)

  await user.type(screen.getByLabelText(/name/i), 'Premium Wash')
  await user.click(screen.getByRole('button', { name: /create/i }))

  await waitFor(() => {
    expect(capturedBody).toEqual(
      expect.objectContaining({ name: 'Premium Wash' })
    )
  })
})
```

## Simulating network latency

```typescript
server.use(
  http.get('/bff/api/v1/backend/admin/sites', async () => {
    await delay(2000) // simulates 2s of latency
    return HttpResponse.json([])
  })
)
```

## Simulating a network error

```typescript
server.use(
  http.get('/bff/api/v1/backend/admin/sites', () => {
    return HttpResponse.error() // simulates a network failure (not an HTTP status)
  })
)
```

## With React Query

React Query retries by default — disable it in tests:

```typescript
// src/test/utils.tsx
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
}
```

## Pattern for query keys

```typescript
// Invalidate the cache in tests to force a re-fetch
const queryClient = createTestQueryClient()

afterEach(() => {
  queryClient.clear()
})
```
