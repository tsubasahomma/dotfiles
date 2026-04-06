-- API Client and Data Operations.
-- Transforms Neovim into a high-performance HTTP client for GTM Ops workflows.
return {
  {
    "mistweaverco/kulala.nvim",
    ft = { "http", "rest" }, -- Only load for .http files to save memory.
    keys = {
      -- Standardized keymaps for API execution.
      { "<leader>R", "", desc = "+Rest/API" },
      { "<leader>Rs", "<cmd>lua require('kulala').run()<cr>", desc = "Send Request" },
      { "<leader>Ra", "<cmd>lua require('kulala').run_all()<cr>", desc = "Send All Requests" },
      {
        "<leader>Rt",
        "<cmd>lua require('kulala').toggle_view()<cr>",
        desc = "Toggle Headers/Body",
      },
      { "<leader>Rc", "<cmd>lua require('kulala').copy()<cr>", desc = "Copy Request as cURL" },
    },
    opts = {
      -- Formatting the response directly with jq/yq if available.
      formatters = {
        json = { "jq", "." },
        xml = { "xmllint", "--format", "-" },
        html = { "prettier", "--parser", "html" },
      },
      -- Ensure responses are opened in a vertical split for easy reading.
      default_winopts = {
        split = "right",
      },
    },
  },
}
