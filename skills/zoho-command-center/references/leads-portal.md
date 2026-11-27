# The leads portal

Read by Command Center when a task builds a site, adds or changes a lead form, or goes live (steps 2 and 5), when the
settings name a "Leads portal". No such setting, or "none": skip this file; leads then go by email and the form's
own store, with no portal step anywhere.

**What it is** (the lead's rule, 20 Nov 2026: hosting mail sometimes fails, so the company keeps every lead in its own
portal): a leads portal at the URL in the settings. A website sends each lead to it server to server: a JSON POST to
the project's endpoint with `Authorization: Bearer <write key>`. So a lead is kept even when the site's email fails.
Each project page in the portal admin shows ready examples for WordPress, PHP, Next.js and a curl test. A GET to the
endpoint with the same header checks the endpoint and key and stores nothing. There is no test key: a test POST stores
a real lead.

## When it is required (only when the settings name a portal)
- Every live website with a lead form: every new build and every go-live. An existing live site only as its own task.
- The lead can exclude a project (quoted and dated in its handoff.md rules, e.g. a site with no forms).

## Which way, by stack (Command Center decides and puts it in the brief)
- WordPress built with convert-to-wordpress or figma-to-wordpress: the kit's leads sender (convert-to-wordpress,
  `forms-email.md` > The leads portal) and that skill's live checklist.
- Another WordPress site: the same sender, as a small must-use plugin made from the kit's file.
- Plain PHP: the portal's PHP example; the key in a config file outside the web root.
- Next.js: the portal's Next.js example (a server action); the endpoint and key as environment variables on the host.
- A platform with no server code of ours (Shopify, Wix, hosted forms): a finding for the lead, not a blocker.

## Rules for the code
- The lead is sent whether the email worked or not: never only after a successful send.
- One send per submission, with a unique idempotency key (the portal ignores duplicates); 200 and 202 both mean
  delivered.
- The code goes in during the build. The portal project (its name, the live domain, the client login, whose password
  the lead or developer types) and the endpoint and write key come only at go-live, pasted on live by the developer.
  The key never goes in git, notes, handoff files, reports or chat. Local, development and staging stay off.

## Proof at go-live
- The GET check passes with the live endpoint and key (convert-to-wordpress has a script for it, `leads-check.py`;
  it never prints the key).
- Then one TEST lead per form, sent from the live site, shows in the portal's form counts.
- Command Center's review at done (step 5) checks both before the close-out comment.
