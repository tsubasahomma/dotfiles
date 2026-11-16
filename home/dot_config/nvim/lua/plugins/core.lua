-- UI and performance plugin overrides.
-- Return the modified opts table so lazy.nvim applies overrides.
-- [Reference]: https://github.com/folke/snacks.nvim

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
          "bash",
          "lua",
          "python",
          "sql",
          "json",
          "json5",
          "yaml",
          "just",
          "kdl",
          "csv",
          "diff",
          "markdown",
          "markdown_inline",
          "latex",
          "typst",
          "mermaid",
          "css",
          "html",
          "scss",
          "svelte",
          "vue",
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
      opts.image = vim.tbl_deep_extend("force", opts.image or {}, {
        enabled = true,
        doc = { inline = true },
      })
      opts.markdown = vim.tbl_deep_extend("force", opts.markdown or {}, {
        enabled = true,
      })

      opts.animate = { enabled = true }
      opts.profiler = { enabled = true }
      opts.notifier = { enabled = true }
      opts.picker = { enabled = true }
      opts.dashboard = { enabled = true }
      opts.indent = { enabled = true }
      opts.scroll = { enabled = true }
      opts.words = { enabled = true }

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
