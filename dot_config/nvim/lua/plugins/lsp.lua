-- [Architecture]: LSP Provider & Binary Orchestration.
-- Configures Harper (Contextual) and Typos (Source-level) as primary audit engines.
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        -- Python: Dynamic venv resolution for 'uv' managed monorepos.
        pyright = {
          before_init = function(_, config)
            local uv_path = vim.fn.trim(vim.fn.system("uv python find 2>/dev/null"))
            if vim.v.shell_error == 0 and uv_path ~= "" then
              config.settings.python.pythonPath = uv_path
            end
          end,
        },
        ruff = {},

        -- Harper: High-fidelity grammar and contextual spell checker.
        harper_ls = {
          filetypes = { "markdown", "gitcommit", "text" },
          settings = {
            ["harper-ls"] = {
              userDictPath = vim.fn.expand("~/.config/harper/dictionary.txt"),
            },
          },
        },

        -- Typos: Zero-speculation spell checking for code and comments.
        typos_lsp = {},
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
