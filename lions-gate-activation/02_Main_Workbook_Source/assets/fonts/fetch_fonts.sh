#!/bin/bash
# Fetch static TTFs from Google Fonts (all OFL-licensed, commercially safe)
set -e
get() { # family css-spec outprefix
  curl -s "https://fonts.googleapis.com/css2?family=$1" | grep -o 'https://[^)]*\.ttf' > /tmp/urls.txt
  i=0
  while read -r u; do
    curl -s -o "$2_$i.ttf" "$u"; i=$((i+1))
  done < /tmp/urls.txt
}
# Cormorant Garamond static weights
for w in 400 500 600 700; do
  curl -s "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@$w" | grep -o 'https://[^)]*\.ttf' | head -1 | xargs -I{} curl -s -o "CormorantGaramond-$w.ttf" {}
done
for w in 400 500 600; do
  curl -s "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,$w" | grep -o 'https://[^)]*\.ttf' | head -1 | xargs -I{} curl -s -o "CormorantGaramond-Italic-$w.ttf" {}
done
curl -s "https://fonts.googleapis.com/css2?family=Marcellus" | grep -o 'https://[^)]*\.ttf' | head -1 | xargs -I{} curl -s -o "Marcellus-400.ttf" {}
for w in 300 400 700; do
  curl -s "https://fonts.googleapis.com/css2?family=Lato:wght@$w" | grep -o 'https://[^)]*\.ttf' | head -1 | xargs -I{} curl -s -o "Lato-$w.ttf" {}
done
curl -s "https://fonts.googleapis.com/css2?family=Lato:ital,wght@1,400" | grep -o 'https://[^)]*\.ttf' | head -1 | xargs -I{} curl -s -o "Lato-Italic-400.ttf" {}
