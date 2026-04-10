-- [Naming]: Leader keys must be set before any plugin loads.
vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

local opt = vim.opt

-- General Preferences
opt.clipboard = "unnamedplus"
opt.undofile = true
opt.undolevels = 10000
opt.scrolloff = 8

-- Indentation (Standard: 2 spaces)
opt.expandtab = true
opt.shiftwidth = 2
opt.tabstop = 2
opt.smartindent = true

-- UI Improvements
opt.number = true
opt.relativenumber = true
opt.cursorline = true
opt.signcolumn = "yes"
opt.termguicolors = true

-- Search Logic
opt.ignorecase = true
opt.smartcase = true

-- [Strategy]: 2026 Sovereign Spell Enforcement
-- [Rationale]: Deprecate native 'spell' to eliminate UI noise (red underlines).
-- Shift to Contextual LSPs (Harper/Typos) for non-destructive grammar/typo audit.
opt.spell = false
opt.spelllang = { "en" }
opt.spelloptions = "camel"
