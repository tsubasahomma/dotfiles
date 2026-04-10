-- [Architecture]: High-performance Search Engine
-- [Rationale]: Replaces Telescope with fzf-lua for sub-millisecond
-- response times in massive repositories.
return {
  {
    "ibhagwan/fzf-lua",
    -- [Note]: LazyVim will automatically use this for many pickers
    -- if configured as a dependency or extra.
    opts = {
      -- Standard 2026 profile: Adaptive floating window.
      "fzf-native",
    },
    keys = {
      { "<leader>ff", "<cmd>FzfLua files<cr>", desc = "Find Files (fzf)" },
      { "<leader>fg", "<cmd>FzfLua live_grep<cr>", desc = "Live Grep (fzf)" },
      { "<leader>fb", "<cmd>FzfLua buffers<cr>", desc = "Find Buffers (fzf)" },
    },
  },
}
