#!/bin/bash
# 1st VRL auto-deploy: GitHub repo (site/) -> public_html/1stvrlpackersandmovers.com
# Runs from cPanel cron. Copies only files changed since the last deployed commit.
# Never touches shifting-price.html, zips, csv lead files, .well-known or cgi-bin.
set -u
H="$HOME"
REPO="$H/deploy/1stvrl-website"
TARGET="$H/public_html/1stvrlpackersandmovers.com"
STATE="$H/deploy/last_sha"
log(){ echo "$(date '+%F %T') $*"; }
GIT=$(command -v git 2>/dev/null || true)
[ -z "$GIT" ] && [ -x /usr/local/cpanel/3rdparty/bin/git ] && GIT=/usr/local/cpanel/3rdparty/bin/git
[ -z "$GIT" ] && { log "git not found"; exit 1; }
if command -v flock >/dev/null 2>&1; then exec 9>"$H/deploy/.lock"; flock -n 9 || { log "already running"; exit 0; }; fi
export GIT_SSH_COMMAND="ssh -i $H/.ssh/1stvrl_deploy -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=$H/.ssh/known_hosts_1stvrl"
URL="git@github.com:gatipackersandmoversshifting-pixel/1stvrl-website.git"
if [ ! -d "$REPO/.git" ]; then
  "$GIT" clone -q --depth 50 -b main "$URL" "$REPO" || { log "clone failed"; exit 1; }
fi
cd "$REPO" || exit 1
"$GIT" fetch -q --depth 50 origin main || { log "fetch failed"; exit 1; }
"$GIT" reset -q --hard origin/main
NEW=$("$GIT" rev-parse HEAD); OLD=$(cat "$STATE" 2>/dev/null || true)
[ "$NEW" = "$OLD" ] && exit 0
if [ -z "$OLD" ]; then echo "$NEW" > "$STATE"; log "bootstrap at $NEW (nothing copied)"; exit 0; fi
"$GIT" cat-file -e "$OLD^{commit}" 2>/dev/null || "$GIT" fetch -q --deepen 200 origin main
FILES=$("$GIT" diff --name-only --diff-filter=ACMRT "$OLD" "$NEW" -- site/) || { log "diff failed"; exit 1; }
n=0
while IFS= read -r f; do
  [ -z "$f" ] && continue
  rel="${f#site/}"
  case "$rel" in
    shifting-price.html|*.zip|*.csv|leads*|.well-known/*|cgi-bin/*) log "skip $rel"; continue;;
  esac
  mkdir -p "$TARGET/$(dirname "$rel")"
  cp -f "$REPO/$f" "$TARGET/$rel" && n=$((n+1)) && log "copied $rel"
done <<< "$FILES"
echo "$NEW" > "$STATE"
log "deployed $NEW ($n files)"
