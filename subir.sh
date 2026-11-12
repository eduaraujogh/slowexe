#!/bin/sh
# Puxa o que esta na main do GitHub pro servidor da Hostinger.
# Rodar DEPOIS do git push. Ver docs/DEPLOY.md.
set -e
echo "local:  $(git rev-parse --short HEAD) $(git log -1 --pretty=%s)"
ssh hostinger-slowexe 'cd ~/domains/slowexe.com/public_html && git pull --ff-only origin main 2>&1 | tail -3 && printf "servidor: %s %s\n" "$(git rev-parse --short HEAD)" "$(git log -1 --pretty=%s)"'
printf 'no ar:  %s\n' "$(curl -s -o /dev/null -w '%{http_code}' https://slowexe.com/)"
python3 tools/indexnow.py
