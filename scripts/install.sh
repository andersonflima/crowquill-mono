#!/usr/bin/env bash
# Instala as fontes Crowquill Mono e a extensao de tema do VS Code.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Fontes -> ~/Library/Fonts"
mkdir -p "$HOME/Library/Fonts"
cp "$ROOT/dist/CrowquillMono-Regular.ttf" "$ROOT/dist/CrowquillMono-Bold.ttf" "$HOME/Library/Fonts/"
echo "    ok: CrowquillMono-Regular.ttf, CrowquillMono-Bold.ttf"

echo "==> Tema VS Code -> ~/.vscode/extensions/crowquill-theme"
EXT="$HOME/.vscode/extensions/crowquill-theme"
mkdir -p "$EXT/themes"
cp "$ROOT/editor/vscode/package.json" "$EXT/"
cp "$ROOT/editor/vscode/themes/crowquill-dark-color-theme.json" "$EXT/themes/"
echo "    ok: reinicie o VS Code e selecione o tema 'Crowquill Dark'"

echo "==> Neovim colorscheme -> ~/.config/nvim/colors/crowquill.lua"
mkdir -p "$HOME/.config/nvim/colors"
cp "$ROOT/editor/nvim/crowquill/colors/crowquill.lua" "$HOME/.config/nvim/colors/"
echo "    ok: use  :colorscheme crowquill"

echo
echo "Pronto. Configure a fonte no editor (veja editor/vscode/settings-snippet.jsonc)"
echo "e no terminal/Neovim GUI use a familia 'Crowquill Mono' com ligaduras ligadas."
