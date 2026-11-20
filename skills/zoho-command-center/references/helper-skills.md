# Helper skills

Moved from SKILL.md in 2.5.3 (unchanged). Added 19 Nov 2026: used by task, QA and build chats when installed;
otherwise the current checks. They serve the task: no extra scope, steps or approval flow of their own; findings
outside the task go to "Findings (not touched)".

| Helper | When |
|---|---|
| web-quality-audit | the QA chat's pass on the staging or live pages the task touched, for M and L tasks and every go-live (Lighthouse: performance, accessibility, SEO, best practices); not for S text edits |
| performance, core-web-vitals | tasks about speed, a PageSpeed score, LCP, CLS or INP |
| accessibility | tasks that add or change forms, menus, new pages or interactive parts |
| seo | tasks on titles, meta, schema, sitemaps or redirects, and every go-live |
| best-practices | security headers, mixed content and console errors, in QA on every go-live |
| wp-plugin-development | any custom PHP (plugin or theme functions): its nonce, capability, sanitising and escaping rules |
| wp-wpcli-and-ops | every WP-CLI job: search-replace, database export or import, local copies, migrations, cache flush |
| wp-performance | backend slowness: slow admin, slow queries, autoloaded options, cron |
| wp-phpstan | L tasks with new custom PHP, when PHPStan is available |
| Chrome DevTools MCP | performance traces, LCP or layout-shift debugging, computed CSS; Playwright stays for clicks, forms and screenshots |
