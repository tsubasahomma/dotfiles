-- [Architecture]: Proactive Audit Logic & Noise Suppression (2026 Standard)
-- [Reference]: https://docs.basedpyright.com/
-- [Reference]: https://github.com/folke/lazydev.nvim

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
          -- [Architecture]: 明示的に有効化し、他設定との競合を排除
          enabled = true,
          -- [Interop]: Masonのバイナリ名を指定。あなたの環境の bin/basedpyright-langserver に対応
          cmd = { "basedpyright-langserver", "--stdio" },
          root_dir = function(fname)
            local util = require("lspconfig.util")
            return util.root_pattern(
              "pyproject.toml",
              "setup.py",
              "setup.cfg",
              "requirements.txt",
              "Pipfile",
              ".git"
            )(fname)
          end,
          before_init = function(_, config)
            local uv_path = vim.fn.trim(vim.fn.system("uv python find 2>/dev/null"))
            if vim.v.shell_error == 0 and uv_path ~= "" then
              config.settings.python.pythonPath = uv_path
            end
          end,
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
        "harper-ls",
        "typos-lsp",
      },
    },
  },
}
