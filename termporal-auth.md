## Core Security / Auth Docs

**1. Self-hosted Security Overview** — start here
`https://docs.temporal.io/self-hosted-guide/security`

Covers mTLS configuration (both internode and frontend sections), the ClaimMapper plugin for JWT-based auth, and the Authorizer plugin for API call access control. Also covers SSO via OAuth/OIDC for the Web UI.

---

**2. mTLS Configuration Reference**
`https://docs.temporal.io/temporal-service/configuration`

Self-hosted mTLS is configured in the `tls` section of the static YAML config. Includes `internode` (traffic between Temporal nodes) and `frontend` (traffic from your clients/workers) as two separate sections. You can also set `serverName` in the client section to prevent MITM/spoofing.

---

**3. ClaimMapper & Authorizer Plugins**
`https://docs.temporal.io/self-hosted-guide/security` (Authorization section)

The ClaimMapper extracts claims from JWTs — translating `AuthInfo` structs into Temporal role claims (Reader, Writer, etc.). The Authorizer then uses those claims to gate API calls. Both are pluggable via `temporal.WithClaimMapper` and custom Authorizer server options. A default JWT ClaimMapper is provided out of the box.

This is the path if you want to integrate with your existing IdP (Okta, Azure AD, etc.) and have the Nudge Consumer pass a JWT.

---

**4. Server Options Reference** (for wiring auth into your Go server)
`https://docs.temporal.io/references/server-options`

Shows how to wire in `WithClaimMapper` when bootstrapping the Temporal server, using `authorization.NewDefaultJWTClaimMapper` with a `TokenKeyProvider` that fetches public keys from your issuer URI.

---

**5. Self-hosted Guide — Security Section**
`https://docs.temporal.io/self-hosted-guide`

The self-hosted guide index — covers TLS/mTLS, authentication, authorization, and hardening controls end to end. Good as a checklist.

---

## Supplementary

**6. Role-based auth implementation walkthrough (community blog)**
`https://www.bitovi.com/blog/implementing-role-based-authentication-for-self-hosted-temporal`

Walks through building a custom Authorizer and ClaimMapper, integrating them into the Temporal server, and deploying with Docker and Helm. Practical code-level walkthrough — useful if you're going the JWT/OIDC route.

---

## TL;DR for Your Setup

For the **Nudge Consumer → GDC Temporal** call (no user IAM session):

| Option | What it involves |
|---|---|
| **mTLS** | Client cert on Nudge Consumer, CA cert registered on Temporal server. No secrets at runtime. |
| **JWT via ClaimMapper** | Nudge Consumer gets a service token from your IdP (e.g. Azure AD client credentials), passes it as bearer token, Temporal validates via ClaimMapper. Closer to the B2B pattern you're already familiar with from the CALS work. |

The JWT/ClaimMapper path would align well with your existing IAM infrastructure at Extreme — worth checking if your GDC Temporal instance already has `requireClientAuth` or any ClaimMapper configured.