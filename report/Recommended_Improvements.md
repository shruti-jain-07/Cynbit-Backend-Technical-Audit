# Recommended Backend Improvements

These are defensive design suggestions based on limited public observations, not claims about Cynbit's current backend.

## 1. Contact API contract

A clear contact endpoint could use:

```http
POST /api/contact
Content-Type: application/json
Accept: application/json
```

Example request:

```json
{
  "fullName": "Alex Rivera",
  "email": "alex@example.com",
  "company": "Example Ltd",
  "industry": "Fintech",
  "message": "We would like to discuss a software project."
}
```

Example successful response:

```http
HTTP/1.1 202 Accepted
Content-Type: application/json
```

```json
{
  "success": true,
  "message": "Your inquiry has been received.",
  "requestId": "server-generated-reference"
}
```

Use `202 Accepted` if processing is queued/asynchronous. If fully processed synchronously, `200 OK` or `201 Created` may be more appropriate depending on the resource model.

## 2. Server-side validation

Suggested starting rules (confirm product requirements before adoption):
- `fullName`: required, trimmed, 2–100 characters.
- `email`: required, maximum 254 characters, validated with a suitable email parser.
- `company`: optional, maximum 120 characters.
- `industry`: optional, maximum 80 characters.
- `message`: required, trimmed, 10–5,000 characters.
- Reject unexpected fields if the API contract is intended to be strict.
- Apply request-body size limits before parsing.
- Treat all values as untrusted, even if the browser has `required`, `type=email`, or `maxlength` attributes.

These limits are examples, not known Cynbit requirements.

## 3. Error handling

Use consistent machine-readable errors. Example:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Please check the highlighted fields.",
    "fields": {
      "email": "Enter a valid email address."
    },
    "requestId": "server-generated-reference"
  }
}
```

Avoid returning stack traces, database errors, internal paths, provider credentials, or raw exception messages to the browser. Log detailed diagnostics server-side with a correlation/request ID.

## 4. Abuse prevention and operational safeguards
- Apply conservative per-IP and per-identity rate limits to public submission endpoints.
- Consider a honeypot field or risk-based bot protection.
- Add idempotency protection if retries could create duplicate inquiries.
- Set request-body and processing-time limits.
- Validate and normalize before persistence or forwarding.
- Avoid logging full message bodies or unnecessary personal information.
- Define retention and deletion policies for contact submissions.
- Alert on abnormal error rates and provider delivery failures.

Tune anti-spam controls to avoid blocking legitimate users behind shared networks.

## 5. CORS and security headers
- Review CORS policy on API routes, not only the homepage HTML.
- Use explicit trusted origins where cross-origin browser access is required.
- Do not allow credentialed requests from arbitrary origins.
- Consider CSP in report-only mode before enforcing it.
- Add `X-Content-Type-Options: nosniff`.
- Set framing controls through CSP `frame-ancestors`.
- Configure `Referrer-Policy` and `Permissions-Policy`.
- Retain HTTPS and HSTS; consider `includeSubDomains` or preload only after confirming every affected subdomain supports HTTPS.

## 6. Caching and performance
- Cache public, non-personalized content where appropriate.
- Do not shared-cache user-specific or sensitive API responses.
- Confirm cache keys vary correctly when content depends on locale, authentication, or request headers.
- Use immutable caching for versioned static assets.
- Monitor cache hit ratio and stale-content behaviour.
- Measure Core Web Vitals and real-user performance rather than relying only on one DevTools snapshot.
- Review third-party analytics impact and load non-essential scripts in a privacy-conscious manner.

## 7. Suggested authorized staging test plan
1. Verify required-field and format validation in browser and API independently.
2. Test boundary lengths at the documented maximum and one character above.
3. Verify unexpected fields are handled according to the API contract.
4. Confirm safe errors for malformed JSON and unsupported content types.
5. Confirm retries do not create unintended duplicate records.
6. Verify rate limiting with an approved, low-volume test plan.
7. Verify CORS behaviour for allowed and disallowed origins.
8. Confirm sensitive values are not exposed in logs, errors, or responses.
9. Verify cache headers for public versus personalized content.
10. Confirm monitoring and alerting for failed notification delivery.

Do not run these tests against production without explicit written authorization and agreed limits.
