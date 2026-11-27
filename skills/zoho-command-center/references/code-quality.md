# Code quality, bulk jobs and the site folder

Read by task, QA and build chats before they write code, a bulk script or put a site in the project folder, and by
the review (moved unchanged from SKILL.md in 2.10.0 to make room for the hard rules there).

- **Lean code** (learned 19 Nov 2026): before writing code, use what already exists (the site's theme, plugin or
  helper, then WordPress or the platform, then an installed library); add no option, wrapper or abstraction nobody
  asked for; never cut validation, error handling, security or accessibility; new logic with a branch or loop gets
  one small check.
- **Clean code** (the lead's rule, 19 Nov 2026: reusable, simple, best practice, no spaghetti; task, QA and build
  chats, senior WordPress level): enqueue CSS and JS, never echo `<style>` or `<script>` from shortcodes or templates;
  use the theme's or builder's globals for colours, fonts and spacing (CSS variables, kit globals, theme.json, ACF
  options), never hex values or font copies; prefix functions, hooks, meta keys, options, shortcode tags, script and
  style handles, CSS classes and post types with the project's prefix (plan.md names it); a value with no global yet
  gets one added in the theme (a decision in the report); one shared helper per piece of logic, no near-copies; lists
  and names that belong in data go in data (ACF, options, a taxonomy), not in code; custom PHP lives in a versioned
  file (the child theme or an mu-plugin) when the site has one, and a site that only uses a snippets plugin also gets
  the exact code in `tasks/<TASK-ID>/build/`; generated SEO titles and descriptions use the SEO plugin's variables,
  not fixed text per page; scripts and builders find elements by selector or ID, never by position ("the third
  widget"). Before DONE, one checks.md line for a search of `<style`, `<script`, hex values and unprefixed names;
  fixes that bring code up to these rules are always inside the plan and its go.
- **Bulk scripts are safe to re-run** (learned 19 Nov 2026, a 209-page task): items a script creates carry a source key
  (a meta field) and it checks that key, slug or ID before each create; a script never trashes or deletes. Duplicates:
  keep the one that menus or links use, else the lowest ID; check what links to the others, then trash them by explicit
  ID under the rule above (trash only; emptying the trash needs the lead's OK).
- **The project folder is the site** (learned 18 Nov 2026: a copy in a sibling folder split the project). A local
  copy, clone or Duplicator install goes in the project folder itself, so the local URL is `<folder>.test`, matching
  the live name (folder "example" -> example.test for example.com). Backups go in `tasks/<TASK-ID>/backup/` (kept off
  the web, out of git and deploys), never in sibling folders; prove a 403 for `tasks/` before a database dump goes
  there, else keep the dump outside the web root. Only for a redesign: the old site is the sibling
  `<folder>-old` (`<folder>-old.test`), removed after go-live on the lead's OK. Putting the site in the folder is a
  plan step of the task chat, in this order: add the handoff skill's file block to the root `.htaccess` and
  `Require all denied` in `tasks/` and `eod/`; then remove Command Center's whole-folder deny (merge into the site's
  `.htaccess`, never replace it); check 403 for the handoff files, `tasks/` and `eod/` and 200 for the home page,
  again after the install and after a permalink save. Site packages and deploys exclude `tasks/`, `eod/` and the
  handoff files (the plan names the filter; check the package).
