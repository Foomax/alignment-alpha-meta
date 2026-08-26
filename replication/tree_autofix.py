#!/usr/bin/env python3
"""Read an experiment's run.log / node.out and print pip package names that would fix the failure
(environment-class only): missing Python modules (ModuleNotFoundError / ImportError) and a missing
jupyter/nbconvert for notebook entrypoints. Prints nothing if no environment fix is recognisable.
Usage: tree_autofix.py <logfile> [<logfile> ...]
"""
import re, sys

NAME_MAP = {
    "sklearn": "scikit-learn", "PIL": "pillow", "yaml": "pyyaml", "cv2": "opencv-python-headless",
    "transformer_lens": "transformer-lens", "sae_lens": "sae-lens", "circuitsvis": "circuitsvis",
    "jaxtyping": "jaxtyping", "einops": "einops", "datasets": "datasets", "matplotlib": "matplotlib",
    "seaborn": "seaborn", "plotly": "plotly", "tqdm": "tqdm", "scipy": "scipy", "pandas": "pandas",
    "numpy": "numpy", "torch": "torch", "transformers": "transformers", "accelerate": "accelerate",
    "peft": "peft", "wandb": "wandb", "huggingface_hub": "huggingface_hub", "umap": "umap-learn",
    "nnsight": "nnsight", "openai": "openai", "anthropic": "anthropic", "tiktoken": "tiktoken",
    "sentencepiece": "sentencepiece", "safetensors": "safetensors", "bitsandbytes": "bitsandbytes",
    "IPython": "ipython", "ipywidgets": "ipywidgets", "nbformat": "nbformat", "jupyter": "jupyter",
    "dotenv": "python-dotenv", "attr": "attrs", "attrs": "attrs", "rich": "rich", "typer": "typer",
    "fire": "fire", "hydra": "hydra-core", "omegaconf": "omegaconf", "networkx": "networkx",
    "statsmodels": "statsmodels", "plotnine": "plotnine", "jax": "jax", "flax": "flax", "optax": "optax",
    "sympy": "sympy", "nltk": "nltk", "spacy": "spacy", "gensim": "gensim", "h5py": "h5py",
    "zstandard": "zstandard", "orjson": "orjson", "pyarrow": "pyarrow", "polars": "polars",
    "lightning": "lightning", "pytorch_lightning": "pytorch-lightning", "torchvision": "torchvision",
    "kaleido": "kaleido", "adjustText": "adjusttext", "tabulate": "tabulate", "loguru": "loguru",
}
SKIP = {"src", "utils", "lib", "config", "configs", "models", "data", "experiments", "scripts", "notebooks"}

text = ""
for f in sys.argv[1:]:
    try: text += open(f, errors="replace").read()
    except OSError: pass
pk = []
for m in re.finditer(r"(?:ModuleNotFoundError|ImportError): No module named '?([A-Za-z0-9_\.]+)'?", text):
    top = m.group(1).split(".")[0]
    if top in SKIP or top.startswith("_"): continue
    pk.append(NAME_MAP.get(top, top.replace("_", "-")))
if re.search(r"No module named '?jupyter|nbconvert|No such kernel|jupyter: command not found|ipykernel", text):
    pk += ["jupyter", "nbconvert", "ipykernel"]
seen = []
for p in pk:
    if p not in seen: seen.append(p)
print(" ".join(seen))
