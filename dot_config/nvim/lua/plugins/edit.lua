-- [Architecture]: High-Fidelity Search and Replace Engine
-- [Rationale]: Replaces brittle manual refactoring with a
-- deterministic preview-based UI.
return {
  {
    "MagicDuck/grug-far.nvim",
    opts = {
      headerMaxWidth = 80,
      -- 2026 optimized: ensures results are always synchronized with disk.
    },
    keys = {
      { "<leader>sr", "<cmd>GrugFar<cr>", desc = "Search and Replace (Grug)" },
    },
  },
}
