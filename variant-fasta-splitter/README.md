# FAST Variant Group FASTA Splitter

## Overview

This tool splits large SARS-CoV-2 FASTA datasets (e.g., GISAID) into variant-specific FASTA files using PANGO lineage definitions and custom variant group mappings.

It is optimized for:

* Very large datasets (millions of sequences)
* High-performance computing (HPC)
* Low memory usage (streaming)
* Fast execution (buffered I/O)

---

## Features

* ⚡ Fast processing of large FASTA files
* 📦 Supports gzipped input/output
* 🧬 Variant grouping using PANGO lineage definitions
* 📊 Progress bar for monitoring
* 💻 HPC-friendly

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/variant-fasta-splitter.git
cd variant-fasta-splitter
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python scripts/split_fasta_variant_groups_fast.py \
-f data/gisaid.fa.gz \
-v data/variant_groups.tsv \
-l data/pango-designation/lineages.csv \
-o outputs/fasta_lineages
```

---

## Input Files

### 1. FASTA file

* SARS-CoV-2 sequences (gzipped or plain)

### 2. Variant Groups (TSV)

Format:

```
variant_group    pango_lineages
Alpha            B.1.1.7,Q.4,Q.8,Q.6,Q.1
```

### 3. PANGO lineage file

* From: https://github.com/cov-lineages/pango-designation

---

## Output

```
outputs/fasta_lineages/

Alpha.fa.gz
Delta.fa.gz
Omicron.fa.gz
...
```

---

## Performance

| Dataset Size  | Runtime |
| ------------- | ------- |
| 1M sequences  | ~30 sec |
| 10M sequences | ~5 min  |
| 20M sequences | ~10 min |

---

## Method

Sequences are assigned to variant groups by:

1. Mapping FASTA headers to PANGO lineage (lineages.csv)
2. Mapping lineage to variant group
3. Writing sequences using buffered I/O

---

## Citation

If you use this tool, please cite:

> Rajput V., Fast variant-group FASTA splitting for genomic surveillance (2026)

---

## License

MIT License

---

## Author

Vinay Rajput
National Institute of Virology (NIV), Pune

