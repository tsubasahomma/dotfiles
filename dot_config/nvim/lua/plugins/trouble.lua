-- Diagnostic and LSP reference aggregation.
-- Trouble centralizes code issues and references in a reviewable list,
-- reducing the chance of hidden diagnostics.
return {
  {
    "folke/trouble.nvim",
    opts = {}, -- Default options are sufficient for this integration.
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
