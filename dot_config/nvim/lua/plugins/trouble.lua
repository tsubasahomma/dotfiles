-- [Architecture]: Diagnostic & LSP Reference Aggregator
-- [Rationale]: Provides a deterministic list of all code issues and
-- references, eliminating "hidden" errors.
return {
  {
    "folke/trouble.nvim",
    opts = {}, -- Default 2026 config is highly optimized.
    keys = {
      { "<leader>xx", "<cmd>Trouble diagnostics toggle<cr>", desc = "Diagnostics (Trouble)" },
      {
        "<leader>xX",
        "<cmd>Trouble diagnostics toggle filter.buf=0<cr>",
        desc = "Buffer Diagnostics (Trouble)",
      },
      { "<leader>cs", "<cmd>Trouble symbols toggle focus=false<cr>", desc = "Symbols (Trouble)" },
      {
        "gr",
        "<cmd>Trouble lsp_references toggle focus=false auto_refresh=true<cr>",
        desc = "LSP References (Trouble)",
      },
    },
  },
}
