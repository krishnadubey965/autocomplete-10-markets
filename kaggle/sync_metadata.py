"""Push title, subtitle, description, licence and tags to the live Kaggle dataset.

The Data Card description is NOT set by `kaggle datasets create` or by
`dataset_create_version`. Both read a `description` key from the metadata file, but
only `dataset_metadata_update` writes it to the Data Card -- and `create` ignores
`licenses` entirely, which is why a dataset created from a metadata file saying
"CC BY 4.0" still reports `{"name": "unknown"}` until this runs.

So the description lives in description.md (one copy, readable, diffable) and this
script folds it into the metadata before updating. Run it after any edit to
description.md or dataset-metadata.json:

    python kaggle/sync_metadata.py

Kaggle's Markdown renderer silently drops "> " blockquotes, so the script refuses to
push a description containing one rather than letting it vanish on the page.
"""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "krishnadubeyyy/autocomplete-keywords-10-english-markets"


def description():
    text = io.open(os.path.join(HERE, "description.md"), encoding="utf-8").read()
    lines = text.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]          # Kaggle prints "About Dataset" above it already
    for line in lines:
        if line.strip().startswith(">"):
            raise SystemExit("description.md contains a blockquote; Kaggle drops those silently")
    return "\n".join(lines).strip() + "\n"


def main():
    meta_path = os.path.join(HERE, "dataset-metadata.json")
    meta = json.load(io.open(meta_path, encoding="utf-8"))
    meta["description"] = description()
    meta["isPrivate"] = False

    staging = os.path.join(HERE, "meta")
    os.makedirs(staging, exist_ok=True)
    out = os.path.join(staging, "dataset-metadata.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

    print(f"description: {len(meta['description']):,} chars, licence: {meta['licenses']}")
    result = subprocess.run(["kaggle", "datasets", "metadata", "--update", "-p", staging, SLUG],
                            capture_output=True, text=True, shell=True)
    print(result.stdout.strip() or result.stderr.strip())
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
