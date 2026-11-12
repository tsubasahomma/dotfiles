-- Adapter for lazy.nvim 85c7ff3711b730b4030d03144f6db6375044ae82.
-- Restore repository revisions without normal startup. Builds may load plugin config.
local function main()
  local engine = "85c7ff3711b730b4030d03144f6db6375044ae82"
  local config = vim.fn.stdpath("config")
  local root = vim.fn.stdpath("data") .. "/lazy"
  local lockfile = config .. "/lazy-lock.json"
  local function read(path)
    local f = assert(io.open(path, "rb"))
    local bytes = f:read("*a")
    f:close()
    return bytes
  end
  local original = read(lockfile)
  local adopted = vim.json.decode(original)
  assert(adopted["lazy.nvim"] and adopted["lazy.nvim"].commit == engine, "Unsupported lazy.nvim lock")
  for name, entry in pairs(adopted) do
    assert(type(name) == "string" and name:match("^[%w_.-]+$") and name ~= "." and name ~= ".."
      and type(entry) == "table" and type(entry.commit) == "string"
      and #entry.commit == 40 and entry.commit:match("^[0-9a-f]+$"), "Invalid lock entry")
  end
  local worklock = assert(vim.env.DOTFILES_RESTORE_LOCK)
  local f = assert(io.open(worklock, "wb")); f:write(original); f:close()
  local function git(dir, args)
    local command = { "git" }
    if dir then vim.list_extend(command, { "-C", dir }) end
    vim.list_extend(command, args)
    local result = vim.system(command, { text = true }):wait()
    assert(result.code == 0, "Git failed: " .. table.concat(args, " ") .. "\n" .. (result.stderr or ""))
    return vim.trim(result.stdout)
  end
  local function bootstrap(name, url)
    local entry = assert(adopted[name], "Missing lock: " .. name)
    local dir = root .. "/" .. name
    local missing = not vim.uv.fs_stat(dir)
    if missing then
      vim.fn.mkdir(root, "p")
      git(nil, { "clone", "--filter=blob:none", "--no-checkout", "--", url, dir })
    else
      assert(git(dir, { "remote", "get-url", "origin" }) == url, "Unexpected origin: " .. name)
      assert(git(dir, { "status", "--porcelain" }) == "", "Local changes: " .. name)
      if name == "lazy.nvim" then
        assert(git(dir, { "rev-parse", "HEAD" }) == engine, "Installed lazy.nvim engine is unsupported")
      end
    end
    if missing or git(dir, { "rev-parse", "HEAD" }) ~= entry.commit then
      git(dir, { "fetch", "origin", entry.commit })
      git(dir, { "checkout", "--no-recurse-submodules", "--detach", entry.commit })
    end
  end
  bootstrap("lazy.nvim", "https://github.com/folke/lazy.nvim.git")
  bootstrap("LazyVim", "https://github.com/LazyVim/LazyVim.git")
  vim.o.eventignore = "all"
  vim.o.loadplugins = true
  vim.opt.rtp:prepend(root .. "/lazy.nvim")
  local errors = {}
  vim.notify = function(message, level)
    if (level or 0) >= vim.log.levels.ERROR then errors[#errors + 1] = tostring(message) end
  end
  local lazy = require("lazy")
  require("lazy.core.loader").startup = function() end
  local setup, called = lazy.setup, false
  lazy.setup = function(opts)
    assert(not called and type(opts) == "table" and type(opts.spec) == "table", "Unsupported lazy setup")
    called = true
    assert(not opts.root and not opts.lockfile, "Custom root/lockfile is unsupported")
    assert(opts.rocks and opts.rocks.enabled == false, "Rocks are unsupported")
    opts.lockfile = worklock
    opts.install = { missing = false }
    opts.local_spec = false
    opts.checker = { enabled = false }
    opts.change_detection = { enabled = false }
    opts.headless = { process = false, colors = false }
    opts.concurrency = 8
    setup(opts)
  end
  dofile(config .. "/init.lua")
  assert(called, "Configuration did not call lazy.setup")
  local C = require("lazy.core.config")
  local Plugin = require("lazy.core.plugin")
  local Git = require("lazy.manage.git")
  local Lock = require("lazy.manage.lock")
  local function check(final)
    assert(C.spec:report() == 0, "Plugin spec contains errors")
    for name, p in pairs(C.plugins) do
      assert(adopted[name], "Active plugin absent from adopted lock: " .. name)
      assert(not p._.is_local and not p.virtual and not p.dev and p.dir == root .. "/" .. name,
        "Unsupported plugin location: " .. name)
      assert(not Plugin.has_errors(p), "Plugin task failed: " .. name)
      if p._.installed then
        assert(Git.get_origin(p.dir) == p.url, "Unexpected plugin origin: " .. name)
      end
      if final then
        assert(p._.installed and Git.info(p.dir).commit == adopted[name].commit,
          "Adopted lock/checkout mismatch: " .. name)
      end
    end
    vim.wait(600)
    assert(#errors == 0, table.concat(errors, "\n"))
    assert(read(lockfile) == original, "Adopted lock changed during restore")
  end
  check(false)
  local Task = require("lazy.manage.task")
  local spawn = assert(Task.spawn)
  Task.spawn = function(self, command, opts)
    -- Clone without checking out today's branch/submodules before the locked commit.
    if command == "git" and opts.args and opts.args[1] == "clone" then
      opts.args = vim.tbl_filter(function(arg) return arg ~= "--recurse-submodules" end, opts.args)
      table.insert(opts.args, 2, "--no-checkout")
    end
    local ok = spawn(self, command, opts)
    if not ok then self:error("Subprocess failed: " .. command) end
    return ok
  end
  local checkout = require("lazy.manage.task.git").checkout
  local run = checkout.run
  checkout.run = function(self, opts)
    if self.plugin._.cloned then
      self:spawn("git", { args = { "checkout", "--no-recurse-submodules", "--detach", assert(adopted[self.plugin.name]).commit },
        cwd = self.plugin.dir })
      if Plugin.has_errors(self.plugin) then return end
    end
    run(self, opts)
    if not Plugin.has_errors(self.plugin) and self.plugin.submodules ~= false then
      self:spawn("git", { args = { "submodule", "update", "--init", "--recursive" }, cwd = self.plugin.dir })
    end
  end
  -- Upstream writes only the work copy. Restore must still use the original input
  -- even if an install wrote different entries into its in-memory lock table.
  Lock.lock, Lock._loaded = vim.deepcopy(adopted), true
  lazy.install({ wait = true, show = false, lockfile = true, clear = false })
  check(false)
  Lock.lock, Lock._loaded = vim.deepcopy(adopted), true
  lazy.restore({ wait = true, show = false, clear = false })
  check(true)
  print("Restored active plugin revisions; adopted lock unchanged. Editor/provider readiness is not checked.")
end
local ok, err = xpcall(main, debug.traceback)
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd("cquit 1")
else
  vim.cmd("qa!")
end
