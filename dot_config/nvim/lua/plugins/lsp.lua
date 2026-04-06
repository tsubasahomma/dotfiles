-- LSP Configuration strictly optimized for uv managed monorepos.
-- This file only contains delta configurations on top of LazyVim's lang.python extra.
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        -- Python (Pyright): Seamlessly resolve virtual environments created by uv.
        pyright = {
          before_init = function(_, config)
            -- Dynamic discovery of the uv interpreter path.
            local uv_venv = vim.fn.trim(vim.fn.system("uv python find 2>/dev/null"))
            if vim.v.shell_error == 0 and uv_venv ~= "" then
              config.settings.python.pythonPath = uv_venv
            end
          end,
        },
        -- Ruff: Configuration inherited from LazyVim extras.
        ruff = {},
      },
    },
  },
}
