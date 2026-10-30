# Cynbit Website – Backend Technical Audit

**Assessment date:** 31 October 2026  
**Target:** https://www.cynbit.in/  
**Approach:** Passive inspection of publicly accessible pages and browser developer tools.

## Purpose
This repository documents observable HTTP response metadata, framework/hosting indicators, Contact form markup, browser event-listener observations, and defensive recommendations.

## Scope limitations
- No Contact form was submitted and no test inquiry was created.
- No authenticated/private resources were accessed.
- No active scanning, fuzzing, brute force, exploit attempts, or load testing was performed.
- The actual form submission endpoint, backend framework, database, server-side validation, persistence, and authentication design were not confirmed.
- Recommendations are proposals, not claims about Cynbit's deployed implementation.

## Repository structure
```text
Cynbit-Backend-Technical-Audit/
├── README.md
├── report/
│   ├── Backend_Technical_Audit.md
│   ├── Security_Performance_Findings.md
│   └── Recommended_Improvements.md
├── evidence/
│   ├── observations.md
│   └── screenshots/README.md
├── architecture/proposed_architecture.md
└── code-examples/
    ├── input-validation.py
    └── api-error-handling.py
```

## Key observations
1. Inspected homepage and Contact responses were served over HTTPS and included `Server: Vercel`.
2. Contact navigation used a Next.js-style RSC route and returned `Content-Type: text/x-component`.
3. Inspected responses included `X-Nextjs-Prerender: 1` and `X-Vercel-Cache: HIT`.
4. Brotli compression and HSTS were present on inspected responses.
5. The homepage HTML response included `Access-Control-Allow-Origin: *`; API CORS behaviour remains unknown.
6. The Contact form contains `fullName`, `email`, `company`, `industry`, and `message`.
7. The form has no visible `action` or `method`; JavaScript may handle submission.
8. Document-level click and submit listeners were visible; the actual submission handler/API was not identified.

## Suggested GitHub description
Passive backend-focused technical audit of Cynbit's public website, including observable HTTP behaviour, contact-form markup, security/performance considerations, and proposed improvements.

## Suggested GitHub topics
`backend-audit` `web-security` `performance-review` `nextjs` `technical-assessment`
