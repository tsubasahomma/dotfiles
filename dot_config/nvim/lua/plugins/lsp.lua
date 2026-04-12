-- [Architecture]: Proactive Audit Logic & Noise Suppression (2026 Standard)
-- [Rationale]: Replaces deprecated vim.lsp.diagnostic handlers with native
-- server-side severity configurations and modern vim.diagnostic.config.
-- [Reference]: https://neovim.io/doc/user/diagnostic.html#vim.diagnostic.config()

return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      -- Global Diagnostic UI Configuration
      diagnostics = {
        -- [Architecture]: Signal-to-Noise Optimization (SNR)
        -- ERROR/WARN: Immediate action required -> Visible via Virtual Text.
        -- INFO/HINT: Stylistic suggestions -> Deferred to Signs, Underlines, and Trouble.
        virtual_text = {
          severity = { min = vim.diagnostic.severity.WARN },
          spacing = 4,
          prefix = "●",
        },
        severity_sort = true,
        update_in_insert = false, -- Prevent visual shifts and UI jank during active typing.
        signs = {
          severity = { min = vim.diagnostic.severity.HINT },
        },
        underline = {
          severity = { min = vim.diagnostic.severity.HINT },
        },
      },
      servers = {
        pyright = {
          before_init = function(_, config)
            local uv_path = vim.fn.trim(vim.fn.system("uv python find 2>/dev/null"))
            if vim.v.shell_error == 0 and uv_path ~= "" then
              config.settings.python.pythonPath = uv_path
            end
          end,
        },
        ruff = {},

        typos_lsp = {
          init_options = {
            diagnosticSeverity = "Hint",
          },
        },

        -- [Component]: Harper LS
        -- [Rationale]: Focus on grammar only. Use strict PascalCase for linter keys
        -- as per official documentation to prevent silent configuration failure.
        -- [Reference]: https://writewithharper.com/docs/integrations/neovim
        harper_ls = {
          filetypes = { "markdown", "gitcommit", "text" },
          settings = {
            ["harper-ls"] = {
              userDictPath = vim.fn.expand("~/.config/harper/dictionary.txt"),
              diagnosticSeverity = "information",
              linters = {
                SpelledNumbers = false,
                AnA = true,
                SentenceCapitalization = false, -- Defers to Vale (Google Style)
                SpellCheck = false, -- Defers to Typos LSP / Vale
              },
            },
          },
        },
      },
    },
  },

  {
    -- [Rationale]: Transitioned to 'mason-org/mason.nvim' to align with
    -- 2026 upstream organization naming and avoid deprecation noise.
    "mason-org/mason.nvim",
    opts = {
      ensure_installed = {
        "harper-ls",
        "typos-lsp",
      },
    },
  },
}
