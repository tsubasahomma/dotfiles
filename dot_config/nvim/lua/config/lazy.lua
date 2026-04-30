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

-- Detect CI so background update checks can be disabled.
local is_ci = os.getenv("CI") == "true"

-- Initialize lazy.nvim with correct path conventions and noise suppression.
require("lazy").setup({
  spec = {
    -- Core LazyVim framework.
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },

    -- Prettier extra uses the 'prettier' binary from $PATH for Markdown,
    -- JSON, and YAML.
    { import = "lazyvim.plugins.extras.formatting.prettier" },

    -- Use project-local ESLint for diagnostics and code actions
    -- while preserving Prettier as the formatting owner.
    -- [Reference]: https://www.lazyvim.org/extras/linting/eslint
    { import = "lazyvim.plugins.extras.linting.eslint" },

    -- Language-specific extras used by the managed editor baseline.
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

    -- Editor UI and completion extras.
    -- These extras replace legacy mini-animate, fzf-lua, and nvim-cmp with
    -- maintained LazyVim defaults.
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
  -- Disable the auto-checker in CI to keep runs idempotent.
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
