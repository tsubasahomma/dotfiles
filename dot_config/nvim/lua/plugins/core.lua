-- Core plugin specifications for UI consistency and theme integration.
-- [Rationale]: Finalized for 2026 professional environment.
-- Ensures deterministic state for inline image rendering and treesitter parsers.
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
      -- [Rationale]: Ensure all professional data and engineering formats are supported.
      if type(opts.ensure_installed) == "table" then
        vim.list_extend(opts.ensure_installed, {
          "css",
          "scss",
          "latex",
          "markdown",
          "markdown_inline",
          "norg",
          "svelte",
          "typst",
          "vue",
        })
      end
    end,
  },
  {
    "folke/snacks.nvim",
    opts = function(_, opts)
      -- [Rationale]: Deep merging ensures 'doc.inline = true' survives
      -- even if LazyVim defaults attempt to disable it.
      opts.image = vim.tbl_deep_extend("force", opts.image or {}, {
        enabled = true,
        doc = {
          inline = true,
        },
      })
      opts.markdown = vim.tbl_deep_extend("force", opts.markdown or {}, {
        enabled = true,
      })
    end,
  },
}
