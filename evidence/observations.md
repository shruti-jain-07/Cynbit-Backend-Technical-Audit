# Evidence Register

**Target:** https://www.cynbit.in/  
**Date:** 31 October 2026  
**Source:** User-provided browser Developer Tools observations

| ID | Area | Direct observation | Interpretation / confidence |
|---|---|---|---|
| O-01 | Network | Requests included route names with `?_rsc=` such as Contact, Careers, Story, Services, Products | Strong indicator of Next.js RSC navigation |
| O-02 | Response | Contact request returned `text/x-component` and matched `/contact.rsc` | Supports RSC interpretation |
| O-03 | Response | Contact response included `X-Nextjs-Prerender: 1` | Prerender indicator |
| O-04 | Hosting | Inspected homepage and Contact response included `Server: Vercel` | Vercel served inspected responses |
| O-05 | Cache | Inspected responses included `X-Vercel-Cache: HIT` | Cache hit for those responses |
| O-06 | Transport | Inspected responses included HSTS `max-age=63072000` | Positive HTTPS hardening signal |
| O-07 | Compression | Inspected responses included `Content-Encoding: br` | Brotli compression enabled |
| O-08 | CORS | Homepage HTML response included `Access-Control-Allow-Origin: *` | API scope unknown; not a confirmed vulnerability |
| O-09 | Cache validator | Homepage response included a weak ETag | Can support conditional revalidation |
| O-10 | Headers | CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy not in supplied homepage response header list | Limited to captured response |
| O-11 | Form | Full Name is required `input type="text"` named `fullName` | Browser-side required constraint |
| O-12 | Form | Email is required `input type="email"` named `email` | Browser required + basic email-format constraint |
| O-13 | Form | Company is optional text input named `company` | Optional free-text field |
| O-14 | Form | Industry is optional text input named `industry` | Optional free-text field |
| O-15 | Form | Message is required textarea named `message`, `rows="5"` | Required free-text field |
| O-16 | Form | No visible `maxlength`, `minlength`, or `pattern` on inspected controls | Server-side validation unknown |
| O-17 | Form | `<form>` had no visible `action`, `method`, or `enctype` | Submission path not established |
| O-18 | Form | Submit button had `type="submit"` | Native submit trigger; JS may intercept |
| O-19 | Events | Document-level click and submit listeners visible; framework and analytics scripts associated | Consistent with event delegation; exact business handler unknown |
| O-20 | Performance | One Network snapshot: 74 requests total; 25 visible under Fetch/XHR; ~262 KB transferred; ~3,401 KB resources | Snapshot only, not benchmark |
| O-21 | Performance | Visible request timings ranged roughly 107–337 ms, with one around 1.43 s | Individual timings; root cause unknown |
| O-22 | Response | Contact response body contained a serialized React Server Component (RSC) stream | Consistent with Next.js RSC response; does not establish that a form submission or API call occurred |

## Evidence handling
- Save original screenshots in `evidence/screenshots/`.
- Screenshots included: Network-Snapshot.png, Contact-Header.png, Contact-HeaderGeneral.png, Contact-Response.png, Contact-ResponseHeader.png, Cynbit-ResponseHeader.png, EventListener.png.
- Do not alter screenshots in a way that changes evidence. Redact personal data if needed.
- Record date, browser, and capture conditions if known.
- Do not include credentials, tokens, cookies, or personal inquiry data.

## Evidence gaps
- No actual Contact form request was captured.
- No API response or API schema was confirmed.
- No server-side code or configuration was reviewed.
- No authenticated workflow was assessed.
- No controlled performance benchmark was run.
