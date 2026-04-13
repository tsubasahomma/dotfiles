-- [Architecture]: Deterministic Chezmoi Integration
-- [Rationale]: Enable high-fidelity syntax highlighting via Treesitter gotmpl
-- and provide seamless source-target synchronization.
-- [Reference]: https://www.chezmoi.io/user-guide/advanced/ide-integration/#neovim

return {
  {
    "xvzc/chezmoi.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    init = function()
      -- [Architecture]: Deterministic Filetype Detection
      -- [Rationale]: Force Neovim to recognize all .tmpl files as Go templates
      -- during the startup phase. This guarantees that Treesitter attaches
      -- correctly before the buffer is fully initialized.
      vim.filetype.add({
        extension = {
          tmpl = "gotmpl",
        },
      })
    end,
    config = function()
      require("chezmoi").setup({
        -- [Rationale]: Use direct edit mode for operational determinism.
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
        -- [Rationale]: 'gotmpl' is the definitive parser for Go templates.
        vim.list_extend(opts.ensure_installed, { "gotmpl" })
      end
    end,
  },
}
