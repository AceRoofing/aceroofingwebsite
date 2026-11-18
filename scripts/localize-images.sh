#!/usr/bin/env bash
# Downloads every image the site loads from the old website host
# (irp.cdn-website.com) into assets/images/ and rewrites the pages to use
# the local copies. Run from the repository root:  bash scripts/localize-images.sh
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p assets/images

urls=$(grep -rhoE 'https://l?irp\.cdn-website\.com/[^"'"'"' )]+' --include='*.html' . | sort -u)

for url in $urls; do
  name=$(basename "$url" | sed 's/+/-/g')
  if [ ! -f "assets/images/$name" ]; then
    echo "Downloading $name"
    curl -fsSL "$url" -o "assets/images/$name"
  fi
done

# Rewrite URLs in every page to a path relative to that page.
find . -name '*.html' -not -path './.git/*' | while read -r file; do
  depth=$(echo "${file#./}" | tr -cd '/' | wc -c)
  prefix=""
  for ((i = 0; i < depth; i++)); do prefix="../$prefix"; done
  [ "$file" = "./404.html" ] && prefix="/"
  for url in $urls; do
    name=$(basename "$url" | sed 's/+/-/g')
    # escape characters that are special to sed
    esc=$(printf '%s' "$url" | sed 's/[.[\*^$]/\\&/g')
    sed -i.bak "s|$esc|${prefix}assets/images/$name|g" "$file"
  done
  rm -f "$file.bak"
done

echo "Done. Images are in assets/images/."
