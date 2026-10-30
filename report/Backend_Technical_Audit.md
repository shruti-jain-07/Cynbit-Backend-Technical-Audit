# Backend Technical Audit Report – Cynbit Website

**Target:** https://www.cynbit.in/  
**Assessment date:** 31 October 2026  
**Perspective:** Backend Developer Intern Technical Assessment  
**Approach:** Passive inspection using browser developer tools

## 1. Executive Summary
This review examined publicly observable behaviour of the Cynbit website, focusing on HTTP response metadata, frontend-to-server interaction clues, caching/compression indicators, security-related response headers, and the Contact form structure.

The inspected responses show a website using Next.js-style rendering/navigation and Vercel delivery infrastructure. The homepage and Contact navigation response included prerendering and cache-hit indicators. Both inspected response types were delivered over HTTPS, used Brotli compression, and included HSTS.

The Contact form exposes five named fields. Three are required (`fullName`, `email`, and `message`), while `company` and `industry` are optional. The form HTML does not expose an explicit `action` or `method`, and document-level click and submit listeners were visible. These observations are compatible with JavaScript-managed form handling, but the actual submission endpoint and server-side processing were not established.

No confirmed exploitable vulnerability was identified from the evidence collected. A deeper authorized review should inspect the form submission flow in a controlled environment, verify server-side validation and persistence, and review API-specific CORS and security headers.

## 2. Scope and Methodology

### In scope
- Public homepage response metadata.
- Public Contact page navigation response metadata.
- Visible Contact form DOM structure and input attributes.
- Browser developer tools' event-listener observations.
- Passive interpretation of caching, compression, transport-security, and framework indicators.

### Out of scope
- Submitting the Contact form or creating a real inquiry.
- Authenticated areas, private APIs, or non-public data.
- Active scanning, fuzzing, brute force, exploit attempts, or load testing.
- Source-code access, server configuration access, database inspection, or infrastructure enumeration beyond visible response metadata.

### Evidence standard
- **Observed:** directly visible in supplied browser inspection evidence.
- **Inferred:** a likely interpretation supported by observable indicators, but not directly proven.
- **Unknown:** not established within this passive assessment.
- **Recommended:** a proposed improvement, not a statement that the current system lacks it.

## 3. Observable Architecture and Technology Indicators

### 3.1 Frontend framework indicators
The Network panel showed navigation requests with names such as `contact?_rsc=...`, `careers?_rsc=...`, `story?_rsc=...`, `services?_rsc=...`, and `products?_rsc=...`.

The inspected Contact navigation response had:
- Request method: `GET`
- Status: `200`
- Content type: `text/x-component`
- Matched path: `/contact.rsc`
- `Vary: rsc, next-router-state-tree, next-router-prefetch, next-router-segment-prefetch`
- `X-Nextjs-Prerender: 1`

The response body contained serialized React Server Component / Flight-style payload fragments.

**Assessment:** These are strong indicators of Next.js App Router and React Server Components navigation. They do not identify the business backend or prove that all application data is delivered through conventional REST APIs.

### 3.2 Hosting and delivery indicators
The inspected homepage and Contact responses included `Server: Vercel`, `X-Vercel-Cache: HIT`, `X-Matched-Path`, and `X-Vercel-Id`.

**Assessment:** The inspected requests were served through Vercel infrastructure and the responses were cache hits. This is evidence about the delivery path for those responses, not proof that every backend service or database is hosted on Vercel.

### 3.3 Request snapshot
The initial Network panel showed 74 requests in the captured page session, with 25 visible under the selected Fetch/XHR filter. Visible requests included Next.js-style route navigation and analytics collection calls. The panel showed approximately 262 KB transferred and approximately 3,401 KB of resources at the time of capture.

These values are a single browser-session snapshot, not a repeatable benchmark or complete page-weight measurement.

## 4. HTTP Response and Header Review

### 4.1 Homepage document
The supplied homepage response metadata included:

```http
HTTP status: 200
Content-Type: text/html; charset=utf-8
Content-Encoding: br
Server: Vercel
Cache-Control: public, max-age=0, must-revalidate
Strict-Transport-Security: max-age=63072000
Access-Control-Allow-Origin: *
ETag: W/"babdce9795e4ef3d84461090987852d3"
X-Nextjs-Prerender: 1
X-Nextjs-Stale-Time: 300
X-Vercel-Cache: HIT
X-Matched-Path: /
```

Additional observed metadata included `Age: 106663` and a `Vary` header containing Next.js router/RSC-related values.

Interpretation:
- `200` indicates a successful HTTP response; it does not prove application-level correctness.
- `Content-Encoding: br` indicates Brotli compression.
- HSTS advertises a 63,072,000-second (two-year) HTTPS policy for the host that emitted the header.
- `ETag` provides a validator that can support conditional cache revalidation.
- `X-Vercel-Cache: HIT` indicates a cache hit for this response.
- `Access-Control-Allow-Origin: *` was observed on the homepage HTML response. Its presence on an HTML document does not establish that sensitive API endpoints allow cross-origin reads.
- `Age` reports the age of the cached response as represented by the intermediary. A large value alone does not prove stale or incorrect content.

### 4.2 Contact navigation response
The inspected Contact RSC response included status `200`, `Content-Type: text/x-component`, `Content-Encoding: br`, `Server: Vercel`, `X-Nextjs-Prerender: 1`, `X-Vercel-Cache: HIT`, `Age: 2348`, `Cache-Control: public, max-age=0, must-revalidate`, and HSTS.

**Assessment:** This is consistent with a prerendered/cached Next.js RSC navigation response delivered through Vercel. The observed cache metadata is not, by itself, a defect.

### 4.3 Security headers not observed in supplied homepage header list
The following headers were not present in the complete response-header list supplied for the homepage:
- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`
- `Permissions-Policy`

This is limited to the captured homepage response. It does not establish absence from every route, API response, or deployment configuration. Browser-displayed request `Referrer Policy` metadata is not equivalent to a `Referrer-Policy` response header.

## 5. Contact Form – DOM and Data Handling Review

### 5.1 Observed fields

| Field | Element/type | Required | Other observed attributes |
|---|---|---:|---|
| Full Name | `input type="text"` | Yes | `name="fullName"` |
| Email Address | `input type="email"` | Yes | `name="email"` |
| Company | `input type="text"` | No | `name="company"` |
| Industry | `input type="text"` | No | `name="industry"` |
| Your Message | `textarea` | Yes | `name="message"`, `rows="5"` |

No `maxlength`, `minlength`, or `pattern` attributes were visible on the inspected fields.

### 5.2 Validation implications
The `required` attribute enables browser-native required-field validation. `type="email"` enables basic browser email-format validation.

These controls improve user experience but are not a substitute for server-side validation. Browser-side attributes can be bypassed by clients and must not be the only validation layer.

No visible length constraints were present in the inspected markup. This is a potential validation/UX improvement, not proof that server-side validation is absent.

### 5.3 Form submission wiring
The inspected form opening tag was:

```html
<form class="space-y-6" style="opacity: 1;">
```

No explicit `action`, `method`, or `enctype` attribute was visible. The submit button used `type="submit"`.

Browser developer tools showed document-level `click` and `submit` event listeners associated with the main framework bundle and analytics scripts. Both capture- and bubble-phase submit listeners were reported.

**Assessment:** The evidence is consistent with framework-level event delegation and possibly JavaScript-managed form submission. It does not identify the exact handler, request destination, HTTP method, payload, API route, or backend processing. No form submission was performed.

## 6. Performance Observations

Positive indicators:
- Brotli compression was enabled on inspected homepage and RSC responses.
- Vercel cache-hit headers were present for both inspected responses.
- Prerender indicators were present for homepage and Contact navigation.
- ETag metadata was present on the homepage response.

Limitations:
- Network timing values represent one browser session.
- No controlled repeated runs, cold-cache comparison, mobile throttling, Core Web Vitals measurement, or backend load test was performed.
- A single slow request or large `Age` value is not proof of a performance defect.

Recommended follow-up:
1. Capture at least three normal page loads under consistent conditions.
2. Compare cold-cache and warm-cache behaviour.
3. Record document, script, image, and API transfer sizes separately.
4. Measure LCP, CLS, and INP using an approved browser workflow.
5. Review whether dynamic or user-specific responses are excluded from shared caching.

## 7. Overall Assessment
The inspected public pages show modern frontend delivery indicators: Next.js RSC navigation, Vercel response headers, prerendering/cache metadata, Brotli compression, and HSTS. The Contact form uses a five-field structure with native required/email validation.

The main unresolved backend question is the Contact form's server-side processing path. Without an authorized submission in a test environment or access to implementation/configuration, it is not possible to confirm API design, server-side validation, persistence, notification delivery, rate limiting, or error handling.

No confirmed exploitable vulnerability is reported based on the available evidence. Recommendations are defensive engineering improvements and validation steps for a deeper authorized review.

## 8. Conclusion
The passive inspection provides a baseline of the website's observable delivery architecture and contact-form frontend. Further assurance requires authorized access to a staging environment, API documentation, or backend implementation. Any further testing should be scoped and approved by the site owner.
