-- Lock generation only. Adapter verified against lazy.nvim 85c7ff3711b730b4030d03144f6db6375044ae82.
local function main()
  local phase = assert(vim.env.DOTFILES_LAZY_PHASE)
  local root = vim.fn.stdpath("data") .. "/lazy"
  local errors = {}
  vim.notify = function(message, level)
    if (level or 0) >= vim.log.levels.ERROR then errors[#errors + 1] = tostring(message) end
  end
  -- Do not run editor events, plugin init/config, builds, Mason or parsers.
  vim.o.eventignore = "all"
  vim.o.loadplugins = true -- -u NONE otherwise makes lazy.setup return without setup.
  vim.opt.rtp:prepend(root .. "/lazy.nvim")
  local lazy = require("lazy")
  local loader = require("lazy.core.loader")
  assert(type(loader.startup) == "function", "Unsupported lazy loader")
  loader.startup = function() end
  local setup = lazy.setup
  local called = false
  lazy.setup = function(opts)
    assert(not called and type(opts) == "table" and type(opts.spec) == "table", "Unsupported lazy setup")
    called = true
    assert(not opts.root and not opts.lockfile, "Custom lazy root/lockfile is unsupported")
    assert(not opts.dev or not next(opts.dev), "Development plugin paths are unsupported")
    assert(not opts.performance or not opts.performance.rtp or not opts.performance.rtp.paths,
      "Additional runtime paths are unsupported")
    assert(opts.rocks and opts.rocks.enabled == false, "Disable rocks in the selected config first")
    opts.install = { missing = false }
    opts.checker = { enabled = false }
    opts.change_detection = { enabled = false }
    opts.local_spec = false
    opts.headless = { process = false, colors = false }
    opts.concurrency = 8
    -- The adapter's engine is intentionally retained; all other active plugins update.
    table.insert(opts.spec, { "folke/lazy.nvim", pin = true })
    setup(opts)
  end
  dofile(vim.fn.stdpath("config") .. "/init.lua")
  assert(called, "Selected init did not call lazy.setup")
  local C = require("lazy.core.config")
  local Plugin = require("lazy.core.plugin")
  local function check(require_installed)
    assert(C.spec:report() == 0, "Plugin spec contains errors")
    for name, p in pairs(C.plugins) do
      assert(not p._.is_local and not p.virtual and not p.dev, "Unsupported local/dev/virtual plugin: " .. name)
      assert(p.dir == root .. "/" .. name and not name:find("[/\\]"), "Plugin outside isolated root: " .. name)
      assert(not Plugin.has_errors(p), "Plugin task failed: " .. name)
      if require_installed then assert(p._.installed, "Plugin not installed: " .. name) end
    end
    -- LazyVim delays notifications; no editor events can run with eventignore=all.
    vim.wait(600)
    assert(#errors == 0, table.concat(errors, "\n"))
  end
  check(false)
  local tasks = require("lazy.manage.task.plugin")
  assert(type(tasks.build.run) == "function", "Unsupported lazy build task")
  tasks.build.run = function() end
  -- Upstream drops silent process failures from task logs. Observe just this boundary.
  local Task = require("lazy.manage.task")
  local spawn = assert(Task.spawn)
  Task.spawn = function(self, command, opts)
    local ok = spawn(self, command, opts)
    if not ok then self:error("Subprocess failed: " .. command) end
    return ok
  end
  local function downloads_only()
    -- Locks record repository commits, not build-time submodule checkouts.
    for _, p in pairs(C.plugins) do p.submodules = false end
  end
  if phase ~= "verify" then
    downloads_only()
    lazy.install({ wait = true, show = false, lockfile = true, clear = false })
    check(true)
  end
  if phase == "update" then
    local names = {}
    for name in pairs(C.plugins) do if name ~= "lazy.nvim" then names[#names + 1] = name end end
    downloads_only()
    lazy.update({ plugins = names, wait = true, show = false, clear = false })
  end
  check(true)
  local lock = vim.json.decode(table.concat(vim.fn.readfile(C.options.lockfile), "\n"))
  local active = {}
  for name, p in pairs(C.plugins) do
    local Git = require("lazy.manage.git")
    local info = assert(Git.info(p.dir))
    assert(lock[name] and lock[name].commit == info.commit, "Lock/checkout mismatch: " .. name)
    if phase == "verify" then
      assert(Git.get_origin(p.dir) == p.url, "Spec/origin mismatch: " .. name)
      if not p.pin then
        local target = assert(Git.get_target(p))
        local resolved = vim.system({ "git", "-C", p.dir, "rev-parse", "--verify",
          "--end-of-options", assert(target.commit, "Missing spec target: " .. name) .. "^{commit}" },
          { text = true }):wait()
        assert(resolved.code == 0 and vim.trim(resolved.stdout) == info.commit
          and lock[name].branch == target.branch, "Updated spec target differs from candidate: " .. name)
      end
    end
    active[name] = { commit = info.commit, url = p.url }
  end
  for name in pairs(lock) do
    assert(active[name] or C.spec.disabled[name] or C.spec.ignore_installed[name], "Unexplained lock entry: " .. name)
  end
  vim.fn.writefile({ vim.json.encode({ phase = phase, active = active, imports = C.spec.modules }) },
    assert(vim.env.DOTFILES_LAZY_REPORT))
end
local ok, err = xpcall(main, debug.traceback)
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd("cquit 1")
else
  vim.cmd("qa!")
end
