#!/usr/bin/env python3

"""
================================================================================
FAST VARIANT-GROUP FASTA SPLITTER
================================================================================

Description:
------------
This script splits a large SARS-CoV-2 FASTA file (e.g., GISAID dataset)
into multiple FASTA files based on predefined variant groups.

Each sequence is assigned to a variant group using:
1. PANGO lineage designation file (lineages.csv)
2. Variant grouping table (variant_groups.tsv)

The script is optimized for:
- Very large FASTA files (millions of sequences)
- Low memory usage (streaming processing)
- High speed (buffered writing)
- HPC environments

--------------------------------------------------------------------------------
Inputs:
--------------------------------------------------------------------------------
1. FASTA file (gzipped or plain)
2. Variant group mapping (TSV)
3. PANGO lineage designation file (CSV)

--------------------------------------------------------------------------------
Outputs:
--------------------------------------------------------------------------------
- One FASTA file per variant group:
  output_dir/<variant_group>.fa.gz

--------------------------------------------------------------------------------
Example:
--------------------------------------------------------------------------------
python split_fasta_variant_groups_fast.py \
    -f data/gisaid.fa.gz \
    -v data/variant_groups.tsv \
    -l data/pango-designation/lineages.csv \
    -o outputs/fasta_lineages

--------------------------------------------------------------------------------
Author: Vinay Rajput (customized for LCS pipeline)
================================================================================
"""

import gzip
import csv
import re
import os
import argparse
from collections import defaultdict
from tqdm import tqdm

# -----------------------------
# Argument parser
# -----------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Split FASTA sequences into variant groups using lineage mapping",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-f", "--fasta", required=True,
                        help="Input FASTA file (gzipped or plain)")

    parser.add_argument("-v", "--variant_groups", required=True,
                        help="Variant group mapping TSV file")

    parser.add_argument("-l", "--lineages", required=True,
                        help="PANGO lineage designation CSV file")

    parser.add_argument("-o", "--output", required=True,
                        help="Output directory")

    parser.add_argument("-b", "--buffer_size", type=int, default=2000,
                        help="Buffer size for writing sequences")

    return parser.parse_args()

# -----------------------------
# FASTA reader
# -----------------------------

def fasta_reader(handle):
    header = None
    seq = []

    for line in handle:
        if line.startswith(">"):
            if header:
                yield header, "".join(seq)
            header = line.strip()
            seq = []
        else:
            seq.append(line.strip())

    if header:
        yield header, "".join(seq)

# -----------------------------
# Main
# -----------------------------

def main():

    args = parse_args()

    fasta_file = args.fasta
    variant_groups_file = args.variant_groups
    lineage_csv = args.lineages
    out_dir = args.output
    BUFFER_SIZE = args.buffer_size

    os.makedirs(out_dir, exist_ok=True)

    print("\n[INFO] Loading variant groups...")

    lineage_to_group = {}
    groups = []

    with open(variant_groups_file) as f:
        next(f)
        for line in f:
            group, lineages = line.strip().split("\t")
            groups.append(group)

            for l in lineages.split(","):
                lineage_to_group[l.strip()] = group

    print(f"[INFO] Variant groups loaded: {len(groups)}")

    print("\n[INFO] Loading lineage mapping...")

    taxon_to_lineage = {}

    with open(lineage_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            taxon_to_lineage[row["taxon"]] = row["lineage"]

    print(f"[INFO] Lineage mappings loaded: {len(taxon_to_lineage)}")

    print("\n[INFO] Preparing output files...")

    writers = {}
    buffers = defaultdict(list)

    for g in groups:
        writers[g] = gzip.open(f"{out_dir}/{g}.fa.gz", "wt")

    # -----------------------------
    # Count sequences
    # -----------------------------

    print("\n[INFO] Counting sequences...")

    if fasta_file.endswith(".gz"):
        fh = gzip.open(fasta_file, "rt")
    else:
        fh = open(fasta_file)

    total = sum(1 for line in fh if line.startswith(">"))
    fh.close()

    print(f"[INFO] Total sequences: {total}")

    # -----------------------------
    # Process FASTA
    # -----------------------------

    print("\n[INFO] Processing FASTA...")

    if fasta_file.endswith(".gz"):
        fh = gzip.open(fasta_file, "rt")
    else:
        fh = open(fasta_file)

    assigned = 0

    for header, seq in tqdm(fasta_reader(fh), total=total):

        strain = re.sub("^>", "", header)
        strain = re.sub("^hCoV-19/", "", strain)
        strain = strain.split("|")[0]

        lineage = taxon_to_lineage.get(strain)

        if lineage:
            group = lineage_to_group.get(lineage)

            if group:
                buffers[group].append(header + "\n" + seq + "\n")
                assigned += 1

                if len(buffers[group]) >= BUFFER_SIZE:
                    writers[group].write("".join(buffers[group]))
                    buffers[group].clear()

    # flush buffers
    for g in buffers:
        if buffers[g]:
            writers[g].write("".join(buffers[g]))

    # close files
    for w in writers.values():
        w.close()

    print("\n[INFO] Done!")
    print(f"[INFO] Assigned sequences: {assigned}")
    print(f"[INFO] Output directory: {out_dir}")

# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    main()
