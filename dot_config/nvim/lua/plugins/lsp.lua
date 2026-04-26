-- [Architecture]: Environment-Inherited LSP Configuration
-- [Rationale]: Eliminates runtime shell execution (uv python find) inside Lua.
-- Relies on the parent shell environment established by 'mise activate'.
-- [Reference]: https://docs.basedpyright.com/latest/configuration/language-server-settings/

return {
  {
    "folke/lazydev.nvim",
    ft = "lua",
    cmd = "LazyDev",
    opts = {
      library = {
        { path = "${3rd}/luv/library", words = { "vim%.uv" } },
        { path = "snacks.nvim", words = { "Snacks" } },
      },
    },
  },
  {
    "neovim/nvim-lspconfig",
    opts = {
      diagnostics = {
        virtual_text = {
          severity = { min = vim.diagnostic.severity.WARN },
          spacing = 4,
          prefix = "●",
        },
        severity_sort = true,
        update_in_insert = false,
        signs = {
          severity = { min = vim.diagnostic.severity.HINT },
        },
        underline = {
          severity = { min = vim.diagnostic.severity.HINT },
        },
      },
      servers = {
        pyright = { enabled = false },
        basedpyright = {
          enabled = true,
          -- [Interop]: Mason-managed binary names.
          cmd = { "basedpyright-langserver", "--stdio" },
          -- [Architecture]: Zero-Speculation Path Resolution
          -- [Rationale]: By omitting settings.python.pythonPath, BasedPyright
          -- defaults to the 'python' binary available in the current PATH,
          -- which is correctly set by mise during the shell session.
          settings = {
            basedpyright = {
              analysis = {
                typeCheckingMode = "standard",
                diagnosticMode = "workspace",
              },
            },
          },
        },
        ruff = {},
        typos_lsp = {
          init_options = {
            diagnosticSeverity = "Hint",
          },
        },
        harper_ls = {
          filetypes = { "markdown", "gitcommit", "text" },
          settings = {
            ["harper-ls"] = {
              userDictPath = vim.fn.expand("~/.config/harper/dictionary.txt"),
              diagnosticSeverity = "information",
              linters = {
                SpelledNumbers = false,
                AnA = true,
                SentenceCapitalization = false,
                SpellCheck = false,
              },
            },
          },
        },
      },
    },
  },
  {
    "mason-org/mason.nvim",
    opts = {
      ensure_installed = {
        "basedpyright",
        "debugpy",
        "harper-ls",
        "typos-lsp",
      },
    },
  },
}
