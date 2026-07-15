# Test setup — Installation guide

## Vitest + React Testing Library + MSW

### 1. Install the dependencies

```bash
pnpm add -D vitest @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom msw jest-axe @types/jest-axe
```

### 2. Configure Vitest

Add to `vite.config.ts` (or create `vitest.config.ts`):

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from 'vite'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: false,
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'html'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.stories.tsx',
        'src/**/*.d.ts',
        'src/test/**',
        'src/main.tsx',
      ],
    },
  },
})
```

### 3. Create the setup file

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, afterAll, beforeAll } from 'vitest'
import { server } from './server'

// MSW
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => {
  server.resetHandlers()
  cleanup()
})
afterAll(() => server.close())
```

### 4. Configure MSW

```typescript
// src/test/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

```typescript
// src/test/handlers.ts
import { http, HttpResponse } from 'msw'

// Default handlers — override in each test as needed
export const handlers = [
  // Example: mock of the auth endpoint
  http.get('/bff/auth/me', () => {
    return HttpResponse.json({
      userId: 'dev-test',
      email: 'test@example.com',
      role: 'super_admin',
      accountType: 'admin',
    })
  }),
]
```

### 5. Add the package.json scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

### 6. TypeScript — add the types

In `tsconfig.json`, add to `compilerOptions.types`:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  }
}
```

### 7. Test utility files

```typescript
// src/test/factories.ts
import type { User } from '@/shared/types'

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: 'dev-test',
    email: 'test@example.com',
    ...overrides,
  }
}
```

```typescript
// src/test/utils.tsx
import { render, type RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import type { ReactElement } from 'react'

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  const queryClient = createTestQueryClient()
  return render(ui, {
    wrapper: ({ children }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    ),
    ...options,
  })
}

// Re-export everything from RTL for convenience
export * from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'
```
