-- Chezmoi integration for source-state template editing.
-- Treesitter gotmpl highlighting keeps source and target syntax easier to review
-- while chezmoi.nvim handles source-target synchronization.
-- [Reference]: https://www.chezmoi.io/user-guide/advanced/ide-integration/#neovim

return {
  {
    "xvzc/chezmoi.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    init = function()
      -- Register .tmpl files as Go templates before buffers finish initializing.
      -- This lets Treesitter attach consistently for chezmoi source files.
      vim.filetype.add({
        extension = {
          tmpl = "gotmpl",
        },
      })
    end,
    config = function()
      require("chezmoi").setup({
        -- Direct edit mode keeps chezmoi source-state edits explicit.
        edit = {
          watch = true,
          force = false,
        },
        notification = {
          on_checkout = true,
          on_apply = true,
        },
      })
    end,
    -- [Event]: Trigger load only when physical files are opened.
    event = { "BufReadPost", "BufNewFile" },
  },
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      if type(opts.ensure_installed) == "table" then
        -- 'gotmpl' is the parser used for Go templates.
        vim.list_extend(opts.ensure_installed, { "gotmpl" })
      end
    end,
  },
}
