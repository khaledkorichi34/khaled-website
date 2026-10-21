#!/usr/bin/env bash
# Put files on the `etsy-media` branch of khaledkorichi34/khaled-website so Make can download them.
# The branch is replaced each time (only the latest batch lives there). Prints one URL per file.
#   publish_media.sh /path/to/folder_with_files
set -euo pipefail
SRC="${1:?usage: publish_media.sh FOLDER}"
REPO="${REPO:-/home/claude/khaled-website}"
ORIGIN="$(git -C "$REPO" remote get-url origin)"
REPO_PATH="$(echo "$ORIGIN" | sed -E 's#^https://github.com/##; s#\.git$##')"
TMP="$(mktemp -d)"
cp -r "$SRC"/. "$TMP/"
cd "$TMP"
git init -q -b etsy-media
git add -A
git -c user.name="Etsy media bot" -c user.email="noreply@anthropic.com" commit -q -m "Etsy media $(date -u +%F)"
git remote add origin "$ORIGIN"
git push -q -f origin etsy-media
SHA="$(git rev-parse HEAD)"
find . -type f -not -path './.git/*' | sed 's#^\./##' | sort | while read -r f; do
  enc="$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$f")"
  echo "https://raw.githubusercontent.com/$REPO_PATH/$SHA/$enc"
done
rm -rf "$TMP"
