#!/usr/bin/env python3
"""Make a *_repl.ipynb copy of a notebook with google.colab stubbed via sys.modules (prepended cell),
google.colab import lines commented, and %pip/!pip lines left intact. Prints the copy path.
Usage: nb_colab_stub.py <notebook.ipynb>   (no-op copy if the notebook never mentions google.colab)"""
import json, re, sys, os
p = sys.argv[1]; nb = json.load(open(p))
STUB = ("import types as _t, sys as _s\n_g=_t.ModuleType('google'); _c=_t.ModuleType('google.colab')\n"
        "class _F:\n    def download(self,*a,**k): print('[replication] skipped Colab files.download', a)\n    def upload(self,*a,**k): return {}\n"
        "_c.files=_F(); _c.drive=_t.SimpleNamespace(mount=lambda *a,**k: print('[replication] skipped drive.mount'))\n"
        "_c.userdata=_t.SimpleNamespace(get=lambda *a,**k: None)\n_g.colab=_c; _s.modules['google']=_g; _s.modules['google.colab']=_c  # replication env fix\n")
n = 0
for c in nb["cells"]:
    if c["cell_type"] != "code": continue
    src = c["source"]; lines = src.splitlines(keepends=True) if isinstance(src, str) else src
    new = []
    for l in lines:
        if re.search(r"^\s*(from\s+google\.colab\b.*import|import\s+google\.colab)", l):
            new.append("# " + l.rstrip("\n") + "  # replication: stubbed\n"); n += 1
        else: new.append(l)
    c["source"] = new
out = p[:-6] + "_repl.ipynb" if not p.endswith("_repl.ipynb") else p
if n:
    nb["cells"].insert(0, {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [STUB]})
    json.dump(nb, open(out, "w"), indent=1)
print(f"{out} colab_lines={n}")
