# Rules of engagement — {{target_name}}

Engagement ID: {{engagement_id}}
Date: {{YYYY-MM-DD}}
Tester: {{name}}
Target owner / authorizer: {{name, role, how authorisation was given}}

## 1. Authorisation

- I confirm I own or am authorised to test this system: **{{yes/no}}**
- Scope of authorisation: {{list}}
- Authorisation expires: {{date or "end of engagement"}}
- Point of contact for incidents: {{name + channel}}

## 2. Scope

**In scope**

- {{endpoint / URL / command}}
- {{tools}}
- {{data sources}}

**Out of scope**

- {{e.g. billing, authentication, real customer data, provider infrastructure}}
- Third-party systems reachable *through* the target (only note them, never attack them).

## 3. Environment and data

- Environment: {{staging/local/demo}}
- Test accounts: {{ids}}
- Synthetic data only: **{{yes/no}}** — if no, stop and revisit.
- Any real user data encountered must be reported, not copied.

## 4. Rules

1. No destructive, payment, publishing or outbound-communication action without an explicit "yes" for that specific action.
2. Multi-turn testing: {{allowed/not allowed}}
3. Maximum cases: {{N}}
4. Rate limit: {{N req/s}}
5. Stop immediately on: real side effect, another user's real data, authorisation withdrawal, target instability.
6. Evidence is stored locally under `runs/{{engagement_id}}/`; secrets are redacted.
7. Findings are shared only with: {{recipients}}. Disclosure deadline: {{date}}.

## 5. Known limitations

- {{e.g. tool calls not observable in the UI}}
- {{cases that cannot run}}

## 6. Sign-off

Tester: ______________________  Date: __________
Authorizer: __________________  Date: __________