-- [Architecture]: Unified UI & Performance Engine (2026 SOTA Corrected)
-- [Rationale]: Explicitly return modified opts table to ensure lazy.nvim applies overrides.
-- [Rationale]: Enforce kitty protocol for SOTA image rendering in WezTerm/Ghostty.
-- [Reference]: https://github.com/folke/snacks.nvim/blob/main/docs/image.md

return {
  {
    "catppuccin/nvim",
    lazy = false,
    name = "catppuccin",
    priority = 1000,
    opts = {
      flavour = "mocha",
      transparent_background = true,
      integrations = {
        mini = true,
        native_lsp = {
          enabled = true,
          underlines = {
            errors = { "undercurl" },
            hints = { "undercurl" },
            warnings = { "undercurl" },
            information = { "undercurl" },
          },
        },
      },
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "catppuccin",
    },
  },
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      if type(opts.ensure_installed) == "table" then
        vim.list_extend(opts.ensure_installed, {
          -- --- Infrastructure & Data ---
          "bash",
          "lua",
          "python",
          "sql",
          "json",
          "json5",
          "toml",
          "yaml",
          -- --- Git SRE Workflow ---
          "diff",
          "gitcommit",
          "git_rebase",
          "git_config",
          "gitattributes",
          -- --- Modern Documentation ---
          "markdown",
          "markdown_inline",
          "norg",
          "latex",
          "typst",
          "mermaid",
          -- --- Web & Frontend (Minimal) ---
          "css",
          "html",
          "scss",
          "svelte",
          "vue",
          -- --- Neovim Internal ---
          "vim",
          "vimdoc",
          "query",
          "regex",
        })
      end

      return opts
    end,
  },
  {
    "folke/snacks.nvim",
    opts = function(_, opts)
      -- [Architecture]: Image Rendering Pipeline
      -- [Rationale]: Deep merge ensures these survive LazyVim's internal defaults.
      opts.image = vim.tbl_deep_extend("force", opts.image or {}, {
        enabled = true,
        doc = {
          inline = true, -- Re-enable inline image rendering
        },
      })
      opts.markdown = vim.tbl_deep_extend("force", opts.markdown or {}, {
        enabled = true,
      })
      -- [Architecture]: UI Component Activation
      opts.animate = { enabled = true }
      opts.profiler = { enabled = true }
      opts.notifier = { enabled = true }
      opts.picker = { enabled = true }

      -- [Critical]: Must return the modified table
      return opts
    end,
  },
  {
    "Saghen/blink.cmp",
    opts = {
      appearance = {
        use_nvim_cmp_as_default = false,
        nerd_font_variant = "mono",
      },
    },
  },
}
