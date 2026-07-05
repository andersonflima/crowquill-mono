#!/usr/bin/env bash
# Instala as 4 faces da fonte Crowquill Mono em ~/Library/Fonts.
# O tema (editor + terminal) vive em repo proprio: andersonflima/crowquill-theme.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Fontes -> ~/Library/Fonts"
mkdir -p "$HOME/Library/Fonts"
cp "$ROOT/dist/CrowquillMono-Regular.ttf" \
   "$ROOT/dist/CrowquillMono-Bold.ttf" \
   "$ROOT/dist/CrowquillMono-Italic.ttf" \
   "$ROOT/dist/CrowquillMono-BoldItalic.ttf" \
   "$HOME/Library/Fonts/"
echo "    ok: 4 faces instaladas (Regular/Bold/Italic/BoldItalic)"

echo
echo "Pronto. Configure a familia 'Crowquill Mono' no editor/terminal, com ligaduras."
echo "Tema Crowquill Ink: https://github.com/andersonflima/crowquill-theme"
