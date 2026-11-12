"""Native Lua failure gates; upstream network/plugin behavior is tested in CI."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
NVIM = os.environ.get('NVIM_BIN') or shutil.which('nvim')
ENGINE = '85c7ff3711b730b4030d03144f6db6375044ae82'


class Restore(unittest.TestCase):
    def run_case(self, mode):
        with tempfile.TemporaryDirectory(prefix='restore-test-') as directory:
            root = Path(directory).resolve()
            config = root / 'config/nvim'; config.mkdir(parents=True)
            plugins = root / 'data/nvim/lazy'
            for name in ('lazy.nvim', 'LazyVim', 'example'):
                (plugins / name).mkdir(parents=True)
            lock = {name: {'branch': 'main', 'commit': ENGINE if name == 'lazy.nvim' else '1' * 40}
                    for name in ('lazy.nvim', 'LazyVim', 'example')}
            original = json.dumps(lock).encode()
            (config / 'lazy-lock.json').write_bytes(original)
            (config / 'init.lua').write_text('require("lazy").setup({spec={}, rocks={enabled=false}})')
            script = root / 'test.lua'
            script.write_text('local mode = ' + json.dumps(mode) + '\n' + r'''
local root = vim.fn.stdpath("data") .. "/lazy"
local engine = "85c7ff3711b730b4030d03144f6db6375044ae82"
local target = string.rep("1", 40)
local config = {plugins = {example={name="example", dir=root.."/example", url="https://example.invalid/plugin", _={installed=true}}},
  spec = {report=function() return mode == "spec" and 1 or 0 end}}
local fault, head = false, target
local lock = {lock={}}
local loader = {startup=function() error("editor startup executed") end}
package.preload["mason"] = function() return {setup=function(opts)
  assert(opts.registry_fixture == "preserved")
  vim.g.mason_setup = true
end} end
package.preload["mason-registry"] = function() error("editor provisioning executed") end
local task = {spawn=function(self, command, opts)
  if mode == "silent" then return false end
  if opts.args[1] == "clone" then
    assert(vim.tbl_contains(opts.args, "--no-checkout"))
    assert(not vim.tbl_contains(opts.args, "--recurse-submodules"))
  elseif opts.args[1] == "submodule" then
    assert(head == target, "submodules before locked parent checkout")
    vim.g.submodules = true
    if mode == "submodule" then return false end
  elseif opts.args[1] == "checkout" then
    assert(opts.args[2] == "--no-recurse-submodules" and opts.args[3] == "--detach" and opts.args[4] == target)
    head = target
  end
  return true
end}
local checkout = {run=function() assert(head == target) end}
local self = {plugin=config.plugins.example, error=function() fault=true end}
setmetatable(self, {__index=task})
vim.system = function(args)
  local dir = args[3] or ""
  local out = ""
  if vim.tbl_contains(args, "rev-parse") then out = dir:find("lazy.nvim", 1, true) and engine or target end
  if vim.tbl_contains(args, "remote") then
    out = dir:find("lazy.nvim", 1, true) and "https://github.com/folke/lazy.nvim.git" or "https://github.com/LazyVim/LazyVim.git"
  end
  if vim.tbl_contains(args, "status") and mode == "dirty" then out = " M local.lua" end
  if vim.tbl_contains(args, "rev-parse") and mode == "engine" then out = string.rep("2", 40) end
  return {wait=function() return {code=0, stdout=out, stderr=""} end}
end
package.preload["lazy.core.loader"] = function() return loader end
package.preload["lazy.core.config"] = function() return config end
package.preload["lazy.core.plugin"] = function() return {has_errors=function() return fault end} end
package.preload["lazy.manage.lock"] = function() return lock end
package.preload["lazy.manage.task"] = function() return task end
package.preload["lazy.manage.task.git"] = function() return {checkout=checkout} end
package.preload["lazy.manage.git"] = function() return {
  get_origin=function(p) return mode == "origin" and "unexpected" or config.plugins.example.url end,
  info=function() return {commit=head} end,
} end
package.preload["lazy"] = function() return {
  setup=function(opts)
    assert(opts.install.missing == false and opts.local_spec == false)
    assert(opts.lockfile ~= vim.fn.stdpath("config") .. "/lazy-lock.json")
    local override = opts.spec[#opts.spec]
    assert(override[1] == "mason-org/mason.nvim" and override.optional == true)
    override.config(nil, {registry_fixture="preserved"})
    assert(vim.g.mason_setup)
    loader.startup()
  end,
  install=function(opts)
    assert(opts.lockfile and opts.wait)
    self:spawn("git", {args={"clone", "url", "--recurse-submodules"}})
    self.plugin._.cloned = true
    head = string.rep("3", 40)
    checkout.run(self, {})
    if mode == "build" then fault=true end
    if mode == "new-plugin" then config.plugins.unknown=config.plugins.example end
    if mode == "notify" then vim.notify("async failure", vim.log.levels.ERROR) end
    if mode == "callback" then vim.schedule(function() error("fixture async callback") end) end
    -- Model upstream's destructive lock writer: adopted file must be independent.
    lock.lock = {example={commit=string.rep("2", 40)}}
    vim.fn.writefile({"{}"}, vim.env.DOTFILES_RESTORE_LOCK)
  end,
  restore=function(opts)
    assert(lock.lock.example.commit == target, "install output became restore input")
    assert(opts.wait and opts.clear == false and vim.g.submodules)
    if mode == "drift" then head=string.rep("2", 40) end
  end,
} end
''' + '\ndofile(' + json.dumps(str(REPO / '.chezmoitemplates/lazy_restore.lua')) + ')\n')
            env = {'HOME': str(root), 'PATH': '/usr/bin:/bin', 'XDG_CONFIG_HOME': str(root / 'config'),
                   'XDG_DATA_HOME': str(root / 'data'), 'XDG_STATE_HOME': str(root / 'state'),
                   'XDG_CACHE_HOME': str(root / 'cache'), 'DOTFILES_RESTORE_LOCK': str(root / 'work-lock.json')}
            result = subprocess.run([NVIM, '--headless', '-u', 'NONE', '-i', 'NONE', '-n', '-l', str(script)],
                                    cwd=root, env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual((config / 'lazy-lock.json').read_bytes(), original)
            return result

    def test_success_preserves_input_and_initializes_pinned_submodules(self):
        result = self.run_case('success')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_failures_are_nonzero_and_preserve_adopted_lock(self):
        for mode in ('silent', 'submodule', 'build', 'spec', 'dirty', 'engine', 'origin', 'new-plugin', 'notify', 'callback', 'drift'):
            with self.subTest(mode=mode):
                result = self.run_case(mode)
                self.assertNotEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
