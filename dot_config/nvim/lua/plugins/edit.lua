-- [Architecture]: High-Fidelity Search, Replace, and Edit Engine
-- [Reference]: https://github.com/echasnovski/mini.surround

return {
  {
    "folke/persistence.nvim",
    enabled = false,
  },
  {
    "nvim-mini/mini.surround",
    opts = {
      mappings = {
        add = "gsa",
        delete = "gsd",
        find = "gsf",
        find_left = "gsF",
        highlight = "gsh",
        replace = "gsr",
        update_n_lines = "gsn",
      },
    },
  },
  {
    "MagicDuck/grug-far.nvim",
    opts = {
      headerMaxWidth = 80,
    },
    keys = {
      { "<leader>sr", "<cmd>GrugFar<cr>", desc = "Search and Replace (Grug)" },
    },
  },
}
