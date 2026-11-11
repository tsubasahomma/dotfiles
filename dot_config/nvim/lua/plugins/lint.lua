-- Keep LazyVim's setup and nvim-lint's Vale stdin, severity and error handling.
return {
  {
    "mfussenegger/nvim-lint",
    opts = function(_, opts)
      local parse = require("lint.linters.vale").parser
      return vim.tbl_deep_extend("force", opts, {
        linters_by_ft = {
          bash = { "shellcheck" },
          gitcommit = { "vale" },
          markdown = { "vale" },
          sh = { "shellcheck" },
        },
        linters = {
          vale = {
            -- Adopted LazyVim appends these, so the last --ext wins. Keep
            -- Markdown rules for extensionless commit buffers as well.
            -- Vale reads VALE_CONFIG_PATH itself; unset uses its normal search.
            prepend_args = { "--ext", ".md" },
            parser = function(output, bufnr, ...)
              local ext = "." .. vim.fn.fnamemodify(vim.api.nvim_buf_get_name(bufnr), ":e")
              if ext ~= ".md" and vim.trim(output) ~= "" then
                local decoded = vim.json.decode(output)
                -- Upstream selects stdin by the buffer's extension, whereas
                -- our forced Markdown input is always returned as stdin.md.
                decoded["stdin" .. ext] = decoded["stdin.md"]
                output = vim.json.encode(decoded)
              end
              local diagnostics = parse(output, bufnr, ...)
              for _, diagnostic in ipairs(diagnostics) do
                local line =
                  vim.api.nvim_buf_get_lines(bufnr, diagnostic.lnum, diagnostic.lnum + 1, false)[1]
                -- nvim-lint 5259819 converts the 1-based start then subtracts
                -- one byte, landing inside a multibyte character. Move only
                -- that start back to its UTF-8 boundary; the end is exclusive.
                if diagnostic.col >= 0 and diagnostic.col < #line then
                  diagnostic.col = diagnostic.col + vim.str_utf_start(line, diagnostic.col + 1)
                end
              end
              return diagnostics
            end,
          },
        },
      })
    end,
  },
}
