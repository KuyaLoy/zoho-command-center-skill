#!/bin/sh
# Release guard (run by .github/workflows/check.yml on every pull request; also works locally).
#   sh .github/scripts/release-guard.sh <base commit>      e.g. origin/main
# A change to the skill or its manifests (skills/, .claude-plugin/) is a release: main is always a released version.
# So such a change must raise "version" in .claude-plugin/plugin.json and add its "## [x.y.z]" section to CHANGELOG.md.
# Docs-only changes (README, AGENTS.md, .github/) need no version change.
set -eu
base="$1"
ver() { node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).version))'; }
changed=$(git diff --name-only "$base"...HEAD -- skills .claude-plugin)
if [ -z "$changed" ]; then
  echo "OK: no change under skills/ or .claude-plugin/, so no new version is needed."
  exit 0
fi
new=$(ver < .claude-plugin/plugin.json)
old=$(git show "$base:.claude-plugin/plugin.json" | ver)
top=$(printf '%s\n%s\n' "$old" "$new" | sort -V | tail -n 1)
if [ "$new" = "$old" ] || [ "$top" != "$new" ]; then
  echo "::error::The skill changed, so raise \"version\" in .claude-plugin/plugin.json (it is $new; main has $old)."
  echo "Changed: $changed"
  exit 1
fi
if ! grep -q "^## \[$new\]" CHANGELOG.md; then
  echo "::error::CHANGELOG.md needs a \"## [$new] - YYYY-MM-DD\" section for this release."
  exit 1
fi
echo "OK: version $old -> $new, with its CHANGELOG section."
