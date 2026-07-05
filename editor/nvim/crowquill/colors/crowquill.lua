-- =============================================================================
--  Crowquill  —  Neovim colorscheme
-- -----------------------------------------------------------------------------
--  A playful-but-professional dark theme, tuned for the Crowquill Mono font.
--  Signature: language keywords / storage / control-flow render BOLD in a
--  coral-pink accent, on a comfortable deep blue-gray base for long sessions.
--
--  Palette is kept identical to the VS Code "Crowquill Dark" theme.
--
--    bg        #1B1E2B   base editor background (deep blue-gray)
--    bg_alt    #171922   sidebars / floats / statusline
--    bg_dark   #15171F   deepest surfaces / ansi black
--    bg_hi     #232838   line highlight
--    sel       #39405C   selection / visual
--    fg        #E4E6F1   default foreground
--    fg_dim    #C4C8DC   secondary foreground
--    gutter    #4A5070   line numbers / muted UI
--    comment   #6C7392   comments (italic)
--    pink      #FF6B9D   SIGNATURE keyword accent (bold)
--    green     #A5E075   strings
--    orange    #F5A25C   numbers / constants
--    blue      #6BC1FF   functions / methods
--    blue_lt   #8FD1FF   properties
--    yellow    #FFD166   types / classes / interfaces
--    purple    #C792EA   language constants / this / decorators
--    cyan      #5FD7C4   operators / regex / escapes / builtins
--    red       #FF5C7A   errors / diagnostics / diff delete
--    param     #E8B98A   parameters (italic)
--
--  Usage:  vim.o.background = "dark"  →  vim.cmd.colorscheme("crowquill")
-- =============================================================================

local M = {}

-- Reset any previously loaded highlights.
vim.cmd("highlight clear")
if vim.fn.exists("syntax_on") == 1 then
  vim.cmd("syntax reset")
end

vim.o.background = "dark"
vim.g.colors_name = "crowquill"

-- ---------------------------------------------------------------------------
-- Palette
-- ---------------------------------------------------------------------------
local c = {
  bg      = "#1B1E2B",
  bg_alt  = "#171922",
  bg_dark = "#15171F",
  bg_hi   = "#232838",
  sel     = "#39405C",
  border  = "#2A3048",
  fg      = "#E4E6F1",
  fg_dim  = "#C4C8DC",
  gutter  = "#4A5070",
  comment = "#6C7392",
  pink    = "#FF6B9D",
  pink_lt = "#FF7EAA",
  green   = "#A5E075",
  orange  = "#F5A25C",
  blue    = "#6BC1FF",
  blue_lt = "#8FD1FF",
  yellow  = "#FFD166",
  purple  = "#C792EA",
  cyan    = "#5FD7C4",
  red     = "#FF5C7A",
  red_lt  = "#FF7B93",
  param   = "#E8B98A",
  none    = "NONE",
}

-- ---------------------------------------------------------------------------
-- Helper
-- ---------------------------------------------------------------------------
local set = vim.api.nvim_set_hl
local function hl(group, opts)
  set(0, group, opts)
end

-- ---------------------------------------------------------------------------
-- Editor UI
-- ---------------------------------------------------------------------------
hl("Normal",         { fg = c.fg, bg = c.bg })
hl("NormalNC",       { fg = c.fg, bg = c.bg })
hl("NormalFloat",    { fg = c.fg, bg = c.bg_alt })
hl("FloatBorder",    { fg = c.border, bg = c.bg_alt })
hl("FloatTitle",     { fg = c.pink, bg = c.bg_alt, bold = true })
hl("ColorColumn",    { bg = c.bg_hi })
hl("Cursor",         { fg = c.bg, bg = c.pink })
hl("CursorLine",     { bg = c.bg_hi })
hl("CursorColumn",   { bg = c.bg_hi })
hl("CursorLineNr",   { fg = c.pink, bold = true })
hl("LineNr",         { fg = c.gutter })
hl("SignColumn",     { fg = c.gutter, bg = c.bg })
hl("FoldColumn",     { fg = c.gutter, bg = c.bg })
hl("Folded",         { fg = c.comment, bg = c.bg_alt })
hl("VertSplit",      { fg = c.border })
hl("WinSeparator",   { fg = c.border })
hl("Visual",         { bg = c.sel })
hl("VisualNOS",      { bg = c.sel })
hl("Search",         { fg = c.bg_dark, bg = c.yellow })
hl("IncSearch",      { fg = c.bg_dark, bg = c.pink })
hl("CurSearch",      { fg = c.bg_dark, bg = c.pink })
hl("MatchParen",     { fg = c.pink, bold = true, underline = true })
hl("NonText",        { fg = "#333A52" })
hl("Whitespace",     { fg = "#333A52" })
hl("SpecialKey",     { fg = "#333A52" })
hl("EndOfBuffer",    { fg = c.bg })
hl("Conceal",        { fg = c.comment })
hl("Directory",      { fg = c.blue })
hl("Title",          { fg = c.pink, bold = true })
hl("ErrorMsg",       { fg = c.red })
hl("WarningMsg",     { fg = c.yellow })
hl("ModeMsg",        { fg = c.fg_dim, bold = true })
hl("MoreMsg",        { fg = c.cyan })
hl("Question",       { fg = c.cyan })
hl("WildMenu",       { fg = c.bg_dark, bg = c.pink })

-- Statusline / tabline
hl("StatusLine",     { fg = c.fg_dim, bg = c.bg_alt })
hl("StatusLineNC",   { fg = c.comment, bg = c.bg_alt })
hl("TabLine",        { fg = c.comment, bg = c.bg_dark })
hl("TabLineFill",    { fg = c.comment, bg = c.bg_dark })
hl("TabLineSel",     { fg = c.pink, bg = c.bg, bold = true })
hl("WinBar",         { fg = c.fg_dim, bg = c.none })
hl("WinBarNC",       { fg = c.comment, bg = c.none })

-- Popup menu
hl("Pmenu",          { fg = c.fg, bg = c.bg_dark })
hl("PmenuSel",       { fg = c.pink, bg = c.bg_hi, bold = true })
hl("PmenuSbar",      { bg = c.bg_alt })
hl("PmenuThumb",     { bg = c.gutter })
hl("PmenuKind",      { fg = c.blue, bg = c.bg_dark })
hl("PmenuExtra",     { fg = c.comment, bg = c.bg_dark })

-- ---------------------------------------------------------------------------
-- Syntax groups (legacy / vim regex)
-- ---------------------------------------------------------------------------
hl("Comment",        { fg = c.comment, italic = true })

hl("Constant",       { fg = c.orange })
hl("String",         { fg = c.green })
hl("Character",      { fg = c.green })
hl("Number",         { fg = c.orange })
hl("Float",          { fg = c.orange })
hl("Boolean",        { fg = c.purple, bold = true })

hl("Identifier",     { fg = c.fg })
hl("Function",       { fg = c.blue })

-- SIGNATURE: keywords / storage / control-flow are BOLD pink.
hl("Statement",      { fg = c.pink, bold = true })
hl("Conditional",    { fg = c.pink, bold = true })
hl("Repeat",         { fg = c.pink, bold = true })
hl("Label",          { fg = c.pink, bold = true })
hl("Operator",       { fg = c.cyan })
hl("Keyword",        { fg = c.pink, bold = true })
hl("Exception",      { fg = c.pink, bold = true })

hl("PreProc",        { fg = c.purple })
hl("Include",        { fg = c.pink, bold = true })
hl("Define",         { fg = c.purple })
hl("Macro",          { fg = c.purple })
hl("PreCondit",      { fg = c.purple })

hl("Type",           { fg = c.yellow })
hl("StorageClass",   { fg = c.pink, bold = true })
hl("Structure",      { fg = c.yellow })
hl("Typedef",        { fg = c.yellow })

hl("Special",        { fg = c.cyan })
hl("SpecialChar",    { fg = c.cyan })
hl("Tag",            { fg = c.pink, bold = true })
hl("Delimiter",      { fg = "#8B92B0" })
hl("SpecialComment", { fg = "#7E86A8", italic = true })
hl("Debug",          { fg = c.red })

hl("Underlined",     { fg = c.blue, underline = true })
hl("Ignore",         { fg = c.gutter })
hl("Error",          { fg = c.red, bold = true })
hl("Todo",           { fg = c.bg_dark, bg = c.yellow, bold = true })

-- ---------------------------------------------------------------------------
-- Diagnostics (LSP)
-- ---------------------------------------------------------------------------
hl("DiagnosticError",          { fg = c.red })
hl("DiagnosticWarn",           { fg = c.yellow })
hl("DiagnosticInfo",           { fg = c.blue })
hl("DiagnosticHint",           { fg = c.cyan })
hl("DiagnosticOk",             { fg = c.green })
hl("DiagnosticUnderlineError", { undercurl = true, sp = c.red })
hl("DiagnosticUnderlineWarn",  { undercurl = true, sp = c.yellow })
hl("DiagnosticUnderlineInfo",  { undercurl = true, sp = c.blue })
hl("DiagnosticUnderlineHint",  { undercurl = true, sp = c.cyan })
hl("DiagnosticVirtualTextError", { fg = c.red, bg = "#2A1E28" })
hl("DiagnosticVirtualTextWarn",  { fg = c.yellow, bg = "#2A281E" })
hl("DiagnosticVirtualTextInfo",  { fg = c.blue, bg = "#1E2530" })
hl("DiagnosticVirtualTextHint",  { fg = c.cyan, bg = "#1E2A28" })

-- LSP references / semantic base
hl("LspReferenceText",  { bg = c.sel })
hl("LspReferenceRead",  { bg = c.sel })
hl("LspReferenceWrite", { bg = c.sel })
hl("LspInlayHint",      { fg = c.comment, bg = c.bg_hi })
hl("LspCodeLens",       { fg = c.comment, italic = true })
hl("LspSignatureActiveParameter", { fg = c.pink, bold = true })

-- ---------------------------------------------------------------------------
-- Diff / Git
-- ---------------------------------------------------------------------------
hl("DiffAdd",        { bg = "#1E2A1A" })
hl("DiffChange",     { bg = "#1A2430" })
hl("DiffDelete",     { fg = c.red, bg = "#2A1A20" })
hl("DiffText",       { bg = "#22384A" })
hl("diffAdded",      { fg = c.green })
hl("diffRemoved",    { fg = c.red })
hl("diffChanged",    { fg = c.blue })
hl("diffFile",       { fg = c.yellow })
hl("diffLine",       { fg = c.comment })

hl("GitSignsAdd",    { fg = c.green })
hl("GitSignsChange", { fg = c.blue })
hl("GitSignsDelete", { fg = c.red })

-- ---------------------------------------------------------------------------
-- Spelling
-- ---------------------------------------------------------------------------
hl("SpellBad",   { undercurl = true, sp = c.red })
hl("SpellCap",   { undercurl = true, sp = c.yellow })
hl("SpellRare",  { undercurl = true, sp = c.purple })
hl("SpellLocal", { undercurl = true, sp = c.cyan })

-- ---------------------------------------------------------------------------
-- Treesitter (@captures)
-- ---------------------------------------------------------------------------
-- Comments
hl("@comment",             { fg = c.comment, italic = true })
hl("@comment.documentation", { fg = "#7E86A8", italic = true })
hl("@comment.error",       { fg = c.bg_dark, bg = c.red, bold = true })
hl("@comment.warning",     { fg = c.bg_dark, bg = c.yellow, bold = true })
hl("@comment.todo",        { fg = c.bg_dark, bg = c.cyan, bold = true })
hl("@comment.note",        { fg = c.bg_dark, bg = c.blue, bold = true })

-- Strings
hl("@string",              { fg = c.green })
hl("@string.documentation", { fg = "#7E86A8", italic = true })
hl("@string.regexp",       { fg = c.cyan })
hl("@string.escape",       { fg = c.cyan })
hl("@string.special",      { fg = c.cyan })
hl("@string.special.symbol", { fg = c.orange })
hl("@string.special.url",  { fg = c.blue, underline = true })
hl("@character",           { fg = c.green })
hl("@character.special",   { fg = c.cyan })

-- Numbers / booleans / constants
hl("@number",              { fg = c.orange })
hl("@number.float",        { fg = c.orange })
hl("@boolean",             { fg = c.purple, bold = true })
hl("@constant",            { fg = c.orange })
hl("@constant.builtin",    { fg = c.purple, bold = true })
hl("@constant.macro",      { fg = c.purple })

-- SIGNATURE: keywords / control-flow / storage → BOLD pink
hl("@keyword",             { fg = c.pink, bold = true })
hl("@keyword.function",    { fg = c.pink, bold = true })
hl("@keyword.operator",    { fg = c.pink, bold = true })
hl("@keyword.return",      { fg = c.pink, bold = true })
hl("@keyword.import",      { fg = c.pink, bold = true })
hl("@keyword.export",      { fg = c.pink, bold = true })
hl("@keyword.conditional", { fg = c.pink, bold = true })
hl("@keyword.conditional.ternary", { fg = c.cyan })
hl("@keyword.repeat",      { fg = c.pink, bold = true })
hl("@keyword.exception",   { fg = c.pink, bold = true })
hl("@keyword.coroutine",   { fg = c.pink, bold = true })
hl("@keyword.debug",       { fg = c.pink, bold = true })
hl("@keyword.directive",   { fg = c.purple })
hl("@keyword.directive.define", { fg = c.purple })
hl("@keyword.storage",     { fg = c.pink, bold = true })
hl("@keyword.modifier",    { fg = c.pink, bold = true })
hl("@conditional",         { fg = c.pink, bold = true }) -- legacy capture name
hl("@repeat",              { fg = c.pink, bold = true }) -- legacy capture name
hl("@exception",           { fg = c.pink, bold = true }) -- legacy capture name
hl("@include",             { fg = c.pink, bold = true }) -- legacy capture name

-- Operators / punctuation
hl("@operator",            { fg = c.cyan })
hl("@punctuation.delimiter", { fg = "#8B92B0" })
hl("@punctuation.bracket", { fg = "#8B92B0" })
hl("@punctuation.special", { fg = c.cyan })

-- Functions / methods
hl("@function",            { fg = c.blue })
hl("@function.builtin",    { fg = c.blue, italic = true })
hl("@function.call",       { fg = c.blue })
hl("@function.macro",      { fg = c.purple })
hl("@function.method",     { fg = c.blue })
hl("@function.method.call", { fg = c.blue })
hl("@constructor",         { fg = c.yellow })

-- Variables / parameters / fields
hl("@variable",            { fg = c.fg })
hl("@variable.builtin",    { fg = c.purple, italic = true, bold = true })
hl("@variable.parameter",  { fg = c.param, italic = true })
hl("@variable.parameter.builtin", { fg = c.param, italic = true, bold = true })
hl("@variable.member",     { fg = c.blue_lt })
hl("@property",            { fg = c.blue_lt })
hl("@field",               { fg = c.blue_lt })

-- Types / classes / namespaces
hl("@type",                { fg = c.yellow })
hl("@type.builtin",        { fg = c.yellow, italic = true })
hl("@type.definition",     { fg = c.yellow, bold = true })
hl("@type.qualifier",      { fg = c.pink, bold = true })
hl("@structure",           { fg = c.yellow })
hl("@storageclass",        { fg = c.pink, bold = true })
hl("@namespace",           { fg = c.yellow })
hl("@module",              { fg = c.yellow })
hl("@module.builtin",      { fg = c.yellow, italic = true })

-- Labels / attributes / decorators
hl("@label",               { fg = c.cyan })
hl("@attribute",           { fg = c.purple, italic = true })
hl("@attribute.builtin",   { fg = c.purple, italic = true })
hl("@decorator",           { fg = c.purple, italic = true })

-- Markup (markdown, etc.)
hl("@markup.heading",         { fg = c.pink, bold = true })
hl("@markup.heading.1",       { fg = c.pink, bold = true })
hl("@markup.heading.2",       { fg = c.orange, bold = true })
hl("@markup.heading.3",       { fg = c.yellow, bold = true })
hl("@markup.strong",          { fg = c.orange, bold = true })
hl("@markup.italic",          { fg = c.yellow, italic = true })
hl("@markup.strikethrough",   { fg = c.comment, strikethrough = true })
hl("@markup.underline",       { underline = true })
hl("@markup.link",            { fg = c.blue })
hl("@markup.link.label",      { fg = c.cyan })
hl("@markup.link.url",        { fg = c.blue, underline = true })
hl("@markup.raw",             { fg = c.green })
hl("@markup.raw.block",       { fg = c.green })
hl("@markup.quote",           { fg = c.comment, italic = true })
hl("@markup.list",            { fg = c.pink })
hl("@markup.list.checked",    { fg = c.green })
hl("@markup.list.unchecked",  { fg = c.comment })

-- Tags (HTML / JSX / XML)
hl("@tag",                 { fg = c.pink, bold = true })
hl("@tag.builtin",         { fg = c.pink, bold = true })
hl("@tag.attribute",       { fg = c.yellow, italic = true })
hl("@tag.delimiter",       { fg = "#8B92B0" })

-- Diff captures
hl("@diff.plus",           { fg = c.green })
hl("@diff.minus",          { fg = c.red })
hl("@diff.delta",          { fg = c.blue })

-- ---------------------------------------------------------------------------
-- LSP semantic tokens (@lsp.type.* / @lsp.mod.*)
-- ---------------------------------------------------------------------------
hl("@lsp.type.keyword",       { fg = c.pink, bold = true })
hl("@lsp.type.modifier",      { fg = c.pink, bold = true })
hl("@lsp.type.namespace",     { fg = c.yellow })
hl("@lsp.type.class",         { fg = c.yellow })
hl("@lsp.type.enum",          { fg = c.yellow })
hl("@lsp.type.interface",     { fg = c.yellow })
hl("@lsp.type.struct",        { fg = c.yellow })
hl("@lsp.type.type",          { fg = c.yellow })
hl("@lsp.type.typeParameter", { fg = c.yellow, italic = true })
hl("@lsp.type.function",      { fg = c.blue })
hl("@lsp.type.method",        { fg = c.blue })
hl("@lsp.type.macro",         { fg = c.purple })
hl("@lsp.type.property",      { fg = c.blue_lt })
hl("@lsp.type.variable",      { fg = c.fg })
hl("@lsp.type.parameter",     { fg = c.param, italic = true })
hl("@lsp.type.enumMember",    { fg = c.orange })
hl("@lsp.type.decorator",     { fg = c.purple, italic = true })
hl("@lsp.mod.readonly",       { fg = c.orange })
hl("@lsp.mod.deprecated",     { strikethrough = true })
hl("@lsp.typemod.keyword.controlFlow", { fg = c.pink, bold = true })
hl("@lsp.typemod.function.declaration", { fg = c.blue, bold = true })
hl("@lsp.typemod.variable.readonly",    { fg = c.orange })

-- ---------------------------------------------------------------------------
-- Common plugin groups (Telescope / NvimTree / Neo-tree / WhichKey / Notify)
-- ---------------------------------------------------------------------------
hl("TelescopeNormal",       { fg = c.fg, bg = c.bg_alt })
hl("TelescopeBorder",       { fg = c.border, bg = c.bg_alt })
hl("TelescopePromptNormal", { fg = c.fg, bg = c.bg_hi })
hl("TelescopePromptBorder", { fg = c.bg_hi, bg = c.bg_hi })
hl("TelescopePromptTitle",  { fg = c.bg_dark, bg = c.pink, bold = true })
hl("TelescopeResultsTitle", { fg = c.bg_alt, bg = c.bg_alt })
hl("TelescopePreviewTitle", { fg = c.bg_dark, bg = c.green, bold = true })
hl("TelescopeSelection",    { fg = c.pink, bg = c.bg_hi, bold = true })
hl("TelescopeMatching",     { fg = c.yellow, bold = true })

hl("NvimTreeNormal",        { fg = c.fg_dim, bg = c.bg_alt })
hl("NvimTreeFolderName",    { fg = c.blue })
hl("NvimTreeFolderIcon",    { fg = c.blue })
hl("NvimTreeOpenedFolderName", { fg = c.blue, bold = true })
hl("NvimTreeRootFolder",    { fg = c.pink, bold = true })
hl("NvimTreeGitDirty",      { fg = c.yellow })
hl("NvimTreeSpecialFile",   { fg = c.purple, underline = true })
hl("NvimTreeIndentMarker",  { fg = c.border })

hl("NeoTreeNormal",         { fg = c.fg_dim, bg = c.bg_alt })
hl("NeoTreeNormalNC",       { fg = c.fg_dim, bg = c.bg_alt })
hl("NeoTreeDirectoryName",  { fg = c.blue })
hl("NeoTreeRootName",       { fg = c.pink, bold = true })
hl("NeoTreeGitModified",    { fg = c.yellow })
hl("NeoTreeGitUntracked",   { fg = c.green })

hl("WhichKey",              { fg = c.pink, bold = true })
hl("WhichKeyGroup",         { fg = c.blue })
hl("WhichKeyDesc",          { fg = c.fg })
hl("WhichKeySeparator",     { fg = c.comment })
hl("WhichKeyFloat",         { bg = c.bg_alt })

hl("NotifyERRORBorder",     { fg = c.red })
hl("NotifyWARNBorder",      { fg = c.yellow })
hl("NotifyINFOBorder",      { fg = c.blue })
hl("NotifyERRORTitle",      { fg = c.red, bold = true })
hl("NotifyWARNTitle",       { fg = c.yellow, bold = true })
hl("NotifyINFOTitle",       { fg = c.blue, bold = true })

hl("IndentBlanklineChar",       { fg = c.border })
hl("IblIndent",                 { fg = c.border })
hl("IblScope",                  { fg = c.gutter })

-- ---------------------------------------------------------------------------
-- Terminal ANSI colors
-- ---------------------------------------------------------------------------
vim.g.terminal_color_0  = c.bg_dark
vim.g.terminal_color_1  = c.red
vim.g.terminal_color_2  = c.green
vim.g.terminal_color_3  = c.yellow
vim.g.terminal_color_4  = c.blue
vim.g.terminal_color_5  = c.purple
vim.g.terminal_color_6  = c.cyan
vim.g.terminal_color_7  = c.fg_dim
vim.g.terminal_color_8  = c.comment
vim.g.terminal_color_9  = c.red_lt
vim.g.terminal_color_10 = "#B9E88F"
vim.g.terminal_color_11 = "#FFDD85"
vim.g.terminal_color_12 = c.blue_lt
vim.g.terminal_color_13 = "#D7A8F0"
vim.g.terminal_color_14 = "#7EE3D3"
vim.g.terminal_color_15 = "#FFFFFF"

return M
