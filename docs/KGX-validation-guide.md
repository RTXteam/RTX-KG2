### Validate KGX JSONL with `validate_biolink_kgx.py` (translator-ingests)

Repo: [`https://github.com/NCATSTranslator/translator-ingests`](https://github.com/NCATSTranslator/translator-ingests)

---

## 1) Clone and enter the repo

```bash
git clone https://github.com/NCATSTranslator/translator-ingests
cd translator-ingests
```

Expected result:
- You are in the repo root (you can see `pyproject.toml` and `src/`).

---

## 2) Install Python + dependencies (required)

```bash
uv python install
uv sync
```

Expected result:
- `uv run ...` works inside this repo.

---

## 3) Put your KGX files somewhere (example layout)

Create a folder:

```bash
mkdir -p data/mykg/source_data
```

Copy your files:

```bash
cp /ABS/PATH/to/nodes.jsonl data/mykg/source_data/
cp /ABS/PATH/to/edges.jsonl data/mykg/source_data/
```

Expected result:
- You have:
  - `data/mykg/source_data/nodes.jsonl`
  - `data/mykg/source_data/edges.jsonl`

---

## 4) Run validation (this is the key command)

```bash
uv run python src/translator_ingest/util/validate_biolink_kgx.py \
  --files /ABS/PATH/translator-ingests/data/mykg/source_data/nodes.jsonl \
  --files /ABS/PATH/translator-ingests/data/mykg/source_data/edges.jsonl \
  --output-dir /ABS/PATH/translator-ingests/data/mykg
```

What this does:
- Validates nodes/edges against the current Biolink Model (LinkML plugin)
- Checks edge `subject` and `object` refer to existing node `id`s
- Saves a report to:

```text
data/mykg/validation-report.json
```

Expected result:
- Exit code `0` if validation passes
- Exit code `1` if validation fails
- `data/mykg/validation-report.json` is created either way

---

## 5) Read results (status + counts)

```bash
data/mykg/validation-report.json
```

Expected result:
- Prints `status: PASSED` or `status: FAILED`
- Prints a `statistics` dict including error/warning counts (and sample sizes for large graphs)

---