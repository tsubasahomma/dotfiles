-- Text-based directory editing.
-- Treating directories as editable buffers enables bulk renaming
-- and rapid filesystem traversal.
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
