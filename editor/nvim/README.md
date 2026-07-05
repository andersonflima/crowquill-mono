# Crowquill — Neovim colorscheme

A playful-but-professional dark theme tuned for the **Crowquill Mono** font.
Its signature: language **keywords render BOLD** in a coral-pink accent
(`#FF6B9D`), on a comfortable deep blue-gray base (`#1B1E2B`) for long coding
sessions. The palette is identical to the Crowquill Dark VS Code theme.

## Requirements

- Neovim `>= 0.9` (uses `vim.api.nvim_set_hl` and `@`-style Treesitter groups)
- A true-color terminal (`termguicolors`)

## Install

### Manual

Copy the `crowquill` directory onto your `runtimepath`. The colorscheme file
must live under `colors/crowquill.lua`:

```
~/.config/nvim/
└── colors/
    └── crowquill.lua        # copy of editor/nvim/crowquill/colors/crowquill.lua
```

Then enable it:

```lua
vim.opt.termguicolors = true
vim.cmd.colorscheme("crowquill")
```

### lazy.nvim

Point lazy.nvim at this repo's `editor/nvim/crowquill` subdirectory:

```lua
{
  "andersonflima/crowquill-mono",
  name = "crowquill",
  lazy = false,       -- load the colorscheme during startup
  priority = 1000,    -- load before other plugins
  config = function()
    vim.opt.termguicolors = true
    vim.cmd.colorscheme("crowquill")
  end,
}
```

> If your plugin manager does not support subdirectories, copy
> `editor/nvim/crowquill/colors/crowquill.lua` into your own config's
> `colors/` folder (see **Manual** above).

### packer.nvim

```lua
use({
  "andersonflima/crowquill-mono",
  config = function()
    vim.opt.termguicolors = true
    vim.cmd.colorscheme("crowquill")
  end,
})
```

## Enabling the Crowquill Mono font

The colorscheme sets `bold = true` on keyword/storage/control-flow groups, so
you need a font whose **bold** face carries the Crowquill signature.

### GUI clients (Neovide, VimR, etc.)

```lua
vim.opt.guifont = "Crowquill Mono:h14"
```

### Terminal Neovim

Neovim in a terminal uses the terminal emulator's font. Set **Crowquill Mono**
as the font in your terminal profile, and make sure **bold text is rendered
with the real bold glyphs** (not a synthetic/faux bold), so keywords show the
font's bold signature:

- **kitty** — `font_family Crowquill Mono` and `bold_font Crowquill Mono Bold`
- **Alacritty** — set `font.normal.family` and `font.bold.family` to
  `Crowquill Mono`
- **WezTerm** — `config.font = wezterm.font("Crowquill Mono")`
- **iTerm2 / Ghostty** — pick `Crowquill Mono` as the font and keep
  "use bold font" enabled

Make sure bold rendering is not disabled anywhere in your setup:

```lua
-- keep bold attributes (do NOT force nobold)
vim.opt.termguicolors = true
```

## Palette reference

| Role                         | Hex       |
| ---------------------------- | --------- |
| Background (base)            | `#1B1E2B` |
| Foreground                   | `#E4E6F1` |
| Keyword / storage (BOLD) ⭐   | `#FF6B9D` |
| String                       | `#A5E075` |
| Number / constant            | `#F5A25C` |
| Function / method            | `#6BC1FF` |
| Type / class / interface     | `#FFD166` |
| Language const / this / decorator | `#C792EA` |
| Operator / regex / builtin   | `#5FD7C4` |
| Comment (italic)             | `#6C7392` |
| Error / diagnostic           | `#FF5C7A` |
