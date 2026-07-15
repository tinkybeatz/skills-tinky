# Security Standards — Shared

## Mandatory rules

- Never store secrets in source code, in compose environment variables, or in Docker images
- Validate all user input at the system boundaries (API, forms)
- Use parameterized queries for every database interaction (no SQL concatenation)
- HTTPS mandatory in production
- Security headers on all HTTP responses (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)

## Conventions

- Authentication tokens have a maximum lifetime of 24h
- Passwords are hashed with bcrypt or argon2 (never SHA/MD5)
- Logs never contain personal data (PII)

## Anti-patterns to avoid

- `eval()` or any dynamic equivalent on user data
- CORS wildcard (`*`) in production
- Storing client-side sessions without a signature
