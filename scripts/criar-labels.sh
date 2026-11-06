#!/usr/bin/env bash
# Cria (ou atualiza) as labels do projeto nos dois repositorios.
# Mesmo catalogo do InsCompanion.
#
# Uso: GITHUB_TOKEN=<token com permissao Issues: write> scripts/criar-labels.sh
set -euo pipefail

: "${GITHUB_TOKEN:?defina GITHUB_TOKEN}"
DONO="InsCode-Solucoes-Tecnologicas"
REPOS=(api-gestprev ui-gestprev)

# nome|cor|descricao
LABELS=(
  "fase-0|1d76db|Fundacao da plataforma"
  "fase-1|1d76db|Motor da media"
  "fase-2|1d76db|Base mensal e dados"
  "fase-3|1d76db|Telas e fluxo de analise"
  "fase-4|1d76db|Homologacao e implantacao"
  "api|0e8a16|Repositorio api-gestprev"
  "ui|8250df|Repositorio ui-gestprev"
  "infra|d93f0b|Docker, CI, servidor"
  "docs|6e7781|Documentacao"
  "negocio|fbca04|Regra, caso ou decisao de negocio"
  "bloqueante|b60205|Impede outra tarefa de andar"
)

api() {
  curl -sS -o /dev/null -w '%{http_code}' -X "$1" "https://api.github.com/repos/$DONO/$2" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -d "$3"
}

for repo in "${REPOS[@]}"; do
  for item in "${LABELS[@]}"; do
    IFS='|' read -r nome cor desc <<<"$item"
    corpo=$(printf '{"name":"%s","color":"%s","description":"%s"}' "$nome" "$cor" "$desc")
    status=$(api POST "$repo/labels" "$corpo")
    if [ "$status" = "422" ]; then
      status=$(api PATCH "$repo/labels/$nome" "$corpo")
    fi
    echo "$repo $nome -> $status"
  done
done
