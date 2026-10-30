# Security & Performance Findings

**Target:** https://www.cynbit.in/  
**Assessment date:** 31 October 2026  
**Evidence basis:** Passive browser inspection only

## Severity approach
- **Informational:** An observed configuration or architecture detail; no demonstrated negative impact.
- **Low:** A hardening opportunity or limited concern requiring confirmation.
- **Medium/High/Critical:** Reserved for demonstrated issues with meaningful impact. No such issue was confirmed.

## F-01 – Security response-header hardening should be verified
**Severity:** Informational / Low-priority hardening opportunity  
**Status:** Not a confirmed vulnerability

**Evidence:** The supplied complete homepage response-header list did not include CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, or Permissions-Policy.

**Impact:** Depending on application behaviour and other controls, these headers can reduce the impact of certain browser-side attacks, control framing, limit MIME sniffing, and constrain browser features.

**Limitations:** This applies only to the captured homepage response. Headers may differ by route or be enforced through other mechanisms. No exploit or clickjacking test was performed.

**Recommendation:** Evaluate CSP initially in report-only mode; consider `X-Content-Type-Options: nosniff`; configure framing controls using CSP `frame-ancestors`; and set deliberate Referrer-Policy and Permissions-Policy values.

## F-02 – Wildcard CORS header observed on homepage document
**Severity:** Informational  
**Status:** Scope requires verification; not a confirmed CORS vulnerability

**Evidence:** The homepage HTML response included `Access-Control-Allow-Origin: *`.

**Impact:** A wildcard CORS policy on a public static document is often harmless. Risk depends on whether the same policy is applied to sensitive API responses and whether credentials or sensitive data are involved.

**Limitations:** No API endpoint response was inspected. The homepage header alone cannot establish that private or sensitive API data is readable cross-origin.

**Recommendation:** Review CORS separately for each API route; use explicit trusted origins where needed; do not combine wildcard origins with credentialed access; and add tests for expected CORS behaviour.

## F-03 – Contact form has no visible client-side length constraints
**Severity:** Informational / Low-priority validation improvement  
**Status:** Server-side behaviour unknown

**Evidence:** The five inspected form controls did not expose `maxlength`, `minlength`, or `pattern`. `fullName`, `email`, and `message` were required; `company` and `industry` were optional.

**Impact:** Unbounded input can create poor user experience and avoidable processing/storage costs if it is not bounded server-side. Absence of browser attributes does not prove absence of backend validation.

**Recommendation:** Define field-specific limits in the API contract; enforce them on the server; align browser limits with server rules; and return field-specific errors without echoing unsafe raw input.

## F-04 – Contact submission endpoint and processing path not established
**Severity:** Informational  
**Status:** Evidence gap

**Evidence:** The form has no explicit `action` or `method` attribute. Document-level click and submit listeners were visible.

**Impact:** Passive evidence does not reveal submission destination, method, payload schema, authentication requirements, persistence, or notification workflow. This is an assessment limitation, not a defect.

**Recommendation:** In an owner-approved staging environment, document the submit request, response schema, validation behaviour, and failure states. Confirm server-side validation, spam controls, request limits, safe logging, and persistence/notification behaviour.

## F-05 – Performance evidence is a single-session snapshot
**Severity:** Informational  
**Status:** No performance defect confirmed

**Evidence:** One Network snapshot showed 74 total requests, 25 visible under the selected Fetch/XHR filter, approximately 262 KB transferred, and approximately 3,401 KB of resources. Some visible request timings were around 107–337 ms, with one around 1.43 seconds.

**Impact:** These figures do not isolate server processing time from network, browser, cache, or third-party latency.

**Recommendation:** Repeat measurements under consistent conditions; separate first-party and third-party requests; record Core Web Vitals and resource sizes; investigate slow requests only after reproducing and identifying the responsible component.

## Positive controls observed

| Control | Evidence | Assessment |
|---|---|---|
| HTTPS delivery | Inspected URLs use HTTPS | Positive |
| HSTS | `Strict-Transport-Security: max-age=63072000` | Positive |
| Brotli compression | `Content-Encoding: br` | Positive |
| Cache delivery | `X-Vercel-Cache: HIT` | Positive for inspected responses |
| ETag | Weak ETag on homepage | Supports cache validation |
| Prerendering | `X-Nextjs-Prerender: 1` | Positive delivery indicator |

## Not assessed / not confirmed
Do not report the following as findings because evidence was not collected:
- SQL injection, XSS, CSRF, SSRF, or authentication bypass.
- API authorization or IDOR behaviour.
- Database encryption, backup, or access controls.
- Server-side validation and persistence.
- API rate limiting or anti-automation controls.
- Backend error leakage or stack traces.
- Secrets exposure in frontend bundles.
- Cache poisoning or cross-user cache leakage.

A deeper review of these areas requires explicit authorization and a suitable test environment.
