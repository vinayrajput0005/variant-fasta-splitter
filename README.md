# 🧬 FAST Variant Group FASTA Splitter

## Overview
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/2014ffea-e121-46f4-8583-dc1dd8158ac3" />

This tool splits large SARS-CoV-2 FASTA datasets (e.g., GISAID) into variant-specific FASTA files using PANGO lineage definitions and custom variant group mappings.

It is optimized for:

* ⚡ Very large datasets (millions of sequences)
* 💻 HPC environments
* 📦 Low memory usage (streaming)
* 🚀 Fast execution (buffered I/O)

---

## 📥 Data Download Guide

### 1️⃣ GISAID FASTA Sequences

🔗 https://www.gisaid.org/

#### Steps:

1. Login to your GISAID account
2. Go to **EpiCoV Database**
3. Apply filters (optional):

   * Host: Human
   * Complete sequences
   * High coverage
4. Click **Download packages → FASTA**

You will get a file like:

```
gisaid_epicov_*.fasta
```

(Optional) Compress:

```
gzip gisaid_epicov_*.fasta
```

Rename (recommended):

```
mv gisaid_epicov_*.fasta.gz data/gisaid.fa.gz
```

---

### 2️⃣ PANGO Lineage File

🔗 https://github.com/cov-lineages/pango-designation

#### Download:

```
git clone https://github.com/cov-lineages/pango-designation.git
```

File used:

```
pango-designation/lineages.csv
```

---

### 3️⃣ Variant Groups File

Example format:

```
variant_group    pango_lineages
Alpha            B.1.1.7,Q.4,Q.8,Q.6,Q.1
Delta            B.1.617.2,AY.1,AY.2
Omicron          BA.1,BA.2,BA.5,XBB
```

Save as:

```
data/variant_groups.tsv
```

---

## 📂 Recommended Directory Structure

```
data/
├── gisaid.fa.gz
├── variant_groups.tsv
└── pango-designation/
    └── lineages.csv
```

---

## ⚙️ Installation

```
git clone https://github.com/<your-username>/variant-fasta-splitter.git
cd variant-fasta-splitter
pip install -r requirements.txt
```

---

## ▶️ Usage

```
python scripts/split_fasta_variant_groups_fast.py \
-f data/gisaid.fa.gz \
-v data/variant_groups.tsv \
-l data/pango-designation/lineages.csv \
-o outputs/fasta_lineages
```

---

## 📂 Input Files (Detailed)

### FASTA file (`-f`)

* GISAID sequences (.fa or .fa.gz)
* Header format:

```
>hCoV-19/India/XYZ/2021|EPI_ISL_123456|2021-05-01
```

### Variant groups (`-v`)

* TSV file mapping lineages to variant groups

### Lineages file (`-l`)

* PANGO lineage mapping file (`lineages.csv`)

---

## 📤 Output

```
outputs/fasta_lineages/

Alpha.fa.gz
Delta.fa.gz
Omicron.fa.gz
...
```

Each file contains sequences belonging to a specific variant group.

---

## ⚠️ Notes

* GISAID data access requires registration
* Do not redistribute raw GISAID data
* Always acknowledge GISAID contributors

---

## ⚡ Performance

| Dataset       | Runtime |
| ------------- | ------- |
| 1M sequences  | ~30 sec |
| 10M sequences | ~5 min  |
| 20M sequences | ~10 min |

---

## 🧬 Method

Sequences are assigned to variant groups by:

1. Mapping FASTA headers to PANGO lineage
2. Mapping lineage to variant group
3. Writing sequences using buffered I/O

---

## 📜 License

MIT License

---

## 👤 Author

Vinay Rajput
National Institute of Virology (NIV), Pune
