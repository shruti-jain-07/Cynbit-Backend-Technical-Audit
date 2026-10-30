# Proposed Reference Architecture

This is a generic recommended architecture for a public contact form. It is **not** a diagram of Cynbit's confirmed internal systems.

```mermaid
flowchart TD
    A[Visitor browser] --> B[Next.js frontend]
    B -->|HTTPS POST /api/contact| C[API route / backend service]
    C --> D[Request size and schema validation]
    D --> E[Rate limit and anti-spam checks]
    E --> F[Contact service]
    F --> G[(Database or approved CRM)]
    F --> H[Notification queue/provider]
    H --> I[Email / CRM notification]
    C --> J[Structured response with request ID]
    J --> B
    C --> K[Redacted application logs and metrics]
    F --> K
```

## Design principles
1. Keep the browser-facing contract small and stable.
2. Validate all inputs on the server.
3. Apply abuse controls before expensive processing.
4. Store only necessary personal information.
5. Use asynchronous notification delivery where appropriate.
6. Return generic client errors and retain detailed diagnostics server-side.
7. Track requests with correlation IDs.
8. Keep private data and user-specific responses out of shared caches.
