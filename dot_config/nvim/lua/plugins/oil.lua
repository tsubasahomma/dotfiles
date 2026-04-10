-- [Architecture]: Text-based Directory Editor
-- [Rationale]: Enables bulk renaming and rapid filesystem traversal
-- by treating directories as standard editable buffers.
return {
  {
    "stevearc/oil.nvim",
    opts = {
      -- Default options are sufficient for MVP, adding rationale for UI.
      view_options = {
        show_hidden = true,
      },
    },
    -- [Keybinding]: Using '-' as it is the canonical 'up' motion in oil.nvim.
    keys = {
      { "-", "<CMD>Oil<CR>", desc = "Open parent directory" },
    },
    dependencies = { "nvim-tree/nvim-web-devicons" },
  },
}
