-- Configure prose and shell linting without replacing LazyVim setup hooks.
-- The opts pattern keeps custom Vale settings across LazyVim's markdown extra
-- merging while maintaining path-agnostic parsing.
-- [Reference]: https://github.com/mfussenegger/nvim-lint

return {
  {
    "mfussenegger/nvim-lint",
    -- [Note]: LazyVim handles the 'config' and triggers. We only provide the 'opts'.
    opts = {
      linters_by_ft = {
        bash = { "shellcheck" },
        gitcommit = { "vale" },
        markdown = { "vale" },
        sh = { "shellcheck" },
      },
      -- [Critical]: Define linter overrides in 'linters' table to allow
      -- LazyVim's internal setup function to merge them correctly.
      linters = {
        vale = {
          stdin = false,
          ignore_exitcode = true,
          args = {
            "--config",
            vim.env.VALE_CONFIG_PATH,
            "--ext",
            ".md",
            "--output",
            "JSON",
          },
          -- [Path-Agnostic Parser]: Robust decoding for symlinks/absolute paths.
          -- Ensures diagnostics are attached to the current buffer even if Vale
          -- returns absolute paths that don't match the buffer name string exactly.
          parser = function(output, _)
            local diagnostics = {}
            local ok, decoded = pcall(vim.json.decode, output)
            if not ok or not decoded then
              return diagnostics
            end

            for _, messages in pairs(decoded) do
              for _, msg in ipairs(messages) do
                table.insert(diagnostics, {
                  lnum = msg.Line - 1,
                  col = msg.Span[1] - 1,
                  end_lnum = msg.Line - 1,
                  end_col = msg.Span[2],
                  severity = vim.diagnostic.severity[msg.Severity:upper()]
                    or vim.diagnostic.severity.INFO,
                  source = "vale",
                  message = msg.Message,
                  code = msg.Check,
                })
              end
            end
            return diagnostics
          end,
        },
      },
    },
  },
}
