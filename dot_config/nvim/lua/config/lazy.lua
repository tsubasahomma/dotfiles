local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- [Rationale]: Detect CI environment to disable non-deterministic background tasks.
local is_ci = os.getenv("CI") == "true"

-- Initialize lazy.nvim with correct path conventions and noise suppression.
require("lazy").setup({
  spec = {
    -- Core LazyVim framework.
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },

    -- [Rationale]: Prettier extra ensures Neovim uses the 'prettier' binary
    -- from $PATH (provided via mise) for Markdown, JSON, and YAML.
    { import = "lazyvim.plugins.extras.formatting.prettier" },

    -- Language-specific extras for 2026 SOTA workflows.
    { import = "lazyvim.plugins.extras.lang.python" },
    { import = "lazyvim.plugins.extras.lang.typescript" },
    { import = "lazyvim.plugins.extras.lang.json" },
    { import = "lazyvim.plugins.extras.lang.toml" },
    { import = "lazyvim.plugins.extras.lang.yaml" },
    { import = "lazyvim.plugins.extras.lang.git" },
    { import = "lazyvim.plugins.extras.lang.rust" },
    { import = "lazyvim.plugins.extras.lang.markdown" },
    { import = "lazyvim.plugins.extras.lang.docker" },

    -- Test workflow extra.
    { import = "lazyvim.plugins.extras.test.core" },

    -- Debug workflow extra.
    { import = "lazyvim.plugins.extras.dap.core" },

    -- [Architecture]: 2026 SOTA Engines
    -- [Rationale]: Replaces legacy mini-animate, fzf-lua, and nvim-cmp with
    -- unified, Rust-backed, or native-speed alternatives.
    -- [Reference]: https://www.lazyvim.org/extras/editor/snacks_picker
    { import = "lazyvim.plugins.extras.editor.snacks_picker" },
    { import = "lazyvim.plugins.extras.coding.blink" },

    -- Custom plugin overrides.
    { import = "plugins" },
  },
  defaults = {
    lazy = false,
    version = false,
  },
  rocks = {
    enabled = false,
    hererocks = false,
  },
  -- [Rationale]: Disable auto-checker in CI to maintain absolute idempotency.
  checker = { enabled = not is_ci },
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
})
