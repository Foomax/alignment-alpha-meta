#!/usr/bin/env python3
"""Print the pip packages implied by the top-level imports in a repo (.py and .ipynb), minus stdlib
and local modules, so a venv can be prepared in one install instead of one auto-fix round per module.
Usage: tree_imports.py <repo_dir> [--exclude name,name]   -> space-separated package names on stdout
"""
import ast, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_autofix import NAME_MAP  # module -> pip name map

root = sys.argv[1]
excl = set(sys.argv[sys.argv.index("--exclude") + 1].split(",")) if "--exclude" in sys.argv else set()
stdlib = set(getattr(sys, "stdlib_module_names", set())) | {"__future__"}
local = set()
for dp, dn, fn in os.walk(root):
    if "/.git" in dp or "/.venv" in dp: continue
    for d in dn: local.add(d)
    for f in fn:
        if f.endswith(".py"): local.add(f[:-3])
mods = set()
def scan_source(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        for m in re.finditer(r"^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", src, re.M):
            mods.add((m.group(1) or m.group(2)).split(".")[0])
        return
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names: mods.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            mods.add(n.module.split(".")[0])
for dp, dn, fn in os.walk(root):
    if "/.git" in dp or "/.venv" in dp or "site-packages" in dp: continue
    for f in fn:
        p = os.path.join(dp, f)
        try:
            if f.endswith(".py"):
                scan_source(open(p, errors="replace").read())
            elif f.endswith(".ipynb"):
                nb = json.load(open(p, errors="replace"))
                for c in nb.get("cells", []):
                    if c.get("cell_type") == "code":
                        src = "".join(c.get("source", []))
                        src = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("%", "!")))
                        scan_source(src)
        except Exception:
            pass
SKIP = {"torch", "src", "utils", "lib", "config", "configs", "models", "data", "experiments", "scripts", "notebooks", "tests", "test", "setup"}
pk = []
for m in sorted(mods):
    if m in stdlib or m in local or m in SKIP or m in excl or m.startswith("_"): continue
    pk.append(NAME_MAP.get(m, m.replace("_", "-")))
print(" ".join(dict.fromkeys(pk)))
