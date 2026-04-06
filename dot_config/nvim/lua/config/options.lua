-- Global leader keys for structured keybindings.
vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

local opt = vim.opt

-- System integration and persistence.
opt.clipboard = "unnamedplus" -- Synchronize with the system clipboard.
opt.undofile = true -- Maintain undo history across sessions.
opt.undolevels = 10000

-- Indentation and tab behavior (standardized to 2 spaces).
opt.expandtab = true -- Use spaces instead of tabs.
opt.shiftwidth = 2 -- Number of spaces for each indentation level.
opt.tabstop = 2 -- Number of spaces that a <Tab> counts for.
opt.smartindent = true -- Insert indents automatically where appropriate.

-- User Interface settings for high-performance visual feedback.
opt.number = true -- Show absolute line numbers.
opt.relativenumber = true -- Show relative line numbers for efficient motion.
opt.cursorline = true -- Highlight the current line.
opt.scrolloff = 8 -- Keep at least 8 lines above/below the cursor.
opt.signcolumn = "yes" -- Always show the sign column to prevent layout shifts.
opt.termguicolors = true -- Enable 24-bit RGB color in the TUI.

-- Search behavior.
opt.ignorecase = true -- Ignore case in search patterns.
opt.smartcase = true -- Override 'ignorecase' if the search pattern contains upper case characters.
