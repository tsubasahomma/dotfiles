local root, source = arg[1], arg[2]
vim.opt.runtimepath:prepend(root .. "/nvim-lint")
local lint = require("lint")
local base = dofile(root .. "/LazyVim/lua/lazyvim/plugins/linting.lua")[1]
local spec = dofile(source .. "/dot_config/nvim/lua/plugins/lint.lua")[1]
local opts = vim.deepcopy(base.opts)
-- Model the inherited markdown extra and an unrelated linter option.
opts.linters_by_ft.markdown = { "markdownlint-cli2" }
opts.linters.shellcheck = { args = { "--format", "json" } }
opts = type(spec.opts) == "function" and spec.opts(nil, opts)
  or vim.tbl_deep_extend("force", opts, spec.opts)
assert(vim.deep_equal(opts.linters_by_ft.fish, { "fish" }))
for _, ft in ipairs({ "bash", "sh" }) do
  assert(vim.deep_equal(opts.linters_by_ft[ft], { "shellcheck" }))
end
for _, ft in ipairs({ "markdown", "gitcommit" }) do
  assert(vim.deep_equal(opts.linters_by_ft[ft], { "vale" }))
end
assert(opts.linters.shellcheck.args[2] == "json")
base.config(nil, opts) -- Adopted LazyVim performs the real deep merge/arg append.
local vale = lint.linters.vale
assert(vale.stdin and not vale.ignore_exitcode)
assert(vim.tbl_contains(vale.args, "--no-exit"))
assert(vale.args[#vale.args - 1] == "--ext" and vale.args[#vale.args] == ".md")
local parse = vale.parser
local ns = lint.get_namespace("vale")
local changed = false
vim.api.nvim_create_autocmd("DiagnosticChanged", {
  callback = function()
    changed = true
  end,
})
local notifications = {}
vim.notify = function(msg)
  table.insert(notifications, msg)
end
local function lint_buffer()
  changed = false
  lint.try_lint("vale")
  assert(
    vim.wait(5000, function()
      return changed and #lint.get_running() == 0
    end, 10),
    "lint timed out"
  )
  return vim.diagnostic.get(0, { namespace = ns })
end
local function buffer(name, lines)
  local path = root .. "/files/" .. name
  vim.fn.mkdir(vim.fn.fnamemodify(path, ":h"), "p")
  vim.fn.writefile({ "clean disk text" }, path)
  local b = vim.api.nvim_create_buf(true, false)
  vim.api.nvim_set_current_buf(b)
  vim.api.nvim_buf_set_name(b, path)
  vim.api.nvim_buf_set_lines(b, 0, -1, false, lines)
  vim.bo.filetype = name:match("COMMIT_EDITMSG$") and "gitcommit" or "markdown"
  return b, path
end
local function check_diagnostics(ds, expected)
  local actual = {}
  for _, d in ipairs(ds) do
    assert(d.source == "vale" and d.end_lnum == d.lnum)
    local token = ({ Error = "test", Warning = "日", Suggestion = "😀" })[d.code:match(
      "Local%.(.+)"
    )]
    assert(d.message == d.code:sub(7) .. ": " .. token)
    table.insert(actual, { d.lnum, d.col, d.end_col, d.severity })
  end
  table.sort(actual, function(a, b)
    return a[1] < b[1] or a[1] == b[1] and a[2] < b[2]
  end)
  assert(vim.deep_equal(actual, expected), vim.inspect({ actual = actual, expected = expected }))
end
-- Literal expected byte ranges; distinct cases cover format, positions and config selection.
local cases = {
  { "notes.md", { "日😀 test" }, true, { { 0, 0, 3, 2 }, { 0, 3, 7, 4 }, { 0, 8, 12, 1 } } },
  {
    "日本 空白 😀/COMMIT_EDITMSG",
    { "ASCII test 日 😀" },
    true,
    { { 0, 6, 10, 1 }, { 0, 11, 14, 2 }, { 0, 15, 19, 4 } },
  },
  { "COMMIT_EDITMSG", { "😀 日 test" }, false, { { 0, 9, 13, 1 } } },
  {
    "日本 空白.markdown",
    { "日", "", "test", "", "😀" },
    true,
    { { 0, 0, 3, 2 }, { 2, 0, 4, 1 }, { 4, 0, 4, 4 } },
  },
}
for _, case in ipairs(cases) do
  vim.env.VALE_CONFIG_PATH = case[3] and root .. "/config 日本 space.ini" or nil
  local b, path = buffer(case[1], case[2])
  check_diagnostics(lint_buffer(), case[4])
  assert(vim.bo.modified and vim.deep_equal(vim.fn.readfile(path), { "clean disk text" }))
  -- A subsequent clean buffer must clear previous Vale diagnostics without saving.
  vim.api.nvim_buf_set_lines(b, 0, -1, false, { "clean buffer text" })
  assert(#lint_buffer() == 0)
  vim.api.nvim_buf_delete(b, { force = true })
end
assert(#notifications == 0, vim.inspect(notifications))

-- Check the explicit target buffer, not whichever buffer is currently selected.
local target = buffer("other/COMMIT_EDITMSG", { "日😀 test" })
local other = buffer("current.md", { "unrelated" })
local function output(item)
  return vim.json.encode({ ["stdin.md"] = { item } })
end
local item = {
  Line = 1,
  Span = { 2, 2 },
  Severity = "suggestion",
  Check = "Local.Suggestion",
  Message = "Suggestion: 😀",
}
check_diagnostics(parse(output(item), target), { { 0, 3, 7, 4 } })
assert(#parse("", target) == 0 and #parse("{}", target) == 0)
vim.api.nvim_buf_set_lines(target, 0, -1, false, { "" })
local document = parse(
  output({
    Line = 1,
    Span = { 1, 1 },
    Severity = "suggestion",
    Check = "Document",
    Message = "document",
  }),
  target
)
assert(#document == 1 and document[1].col == 0 and document[1].end_col == 0)

local function assert_parse_error(raw)
  vim.diagnostic.set(ns, target, { { lnum = 0, col = 0, message = "previous result" } })
  local accumulated = require("lint.parser").accumulate_chunks(parse)
  local done = false
  accumulated.on_chunk(raw)
  accumulated.on_done(function(ds, b)
    vim.diagnostic.set(ns, b, ds)
    done = true
  end, target, root)
  assert(vim.wait(1000, function()
    return done
  end))
  local ds = vim.diagnostic.get(target, { namespace = ns })
  assert(#ds == 1 and ds[1].severity == vim.diagnostic.severity.ERROR)
  assert(ds[1].message:find("Parser failed", 1, true), ds[1].message)
end
assert_parse_error("{invalid JSON")
assert_parse_error(output({
  Line = 99,
  Span = { 1, 1 },
  Severity = "error",
  Check = "Invalid",
  Message = "invalid line",
}))
assert_parse_error(output({
  Line = 1,
  Span = vim.NIL,
  Severity = "error",
  Check = "Invalid",
  Message = "invalid span",
}))
vim.api.nvim_buf_delete(target, { force = true })
vim.api.nvim_buf_delete(other, { force = true })

-- Known observed Vale 3.14.2 limitation: bad Line from repeated multiline tokens
-- remains a visible parser error, not an invented location or a clean result.
vim.env.VALE_CONFIG_PATH = root .. "/config 日本 space.ini"
local bad =
  buffer("repeat.md", { "日😀 test", "ASCII test 日 😀", "😀 日 test", "", "test日😀" })
local failures = lint_buffer()
assert(#failures == 1 and failures[1].severity == vim.diagnostic.severity.ERROR)
assert(failures[1].message:find("Parser failed", 1, true), vim.inspect(failures))
vim.api.nvim_buf_delete(bad, { force = true })
print(
  "PASS: 4 native cases, clean-result clearing, explicit bufnr, document-level/empty output, malformed JSON/coordinates, real Vale error propagation"
)
