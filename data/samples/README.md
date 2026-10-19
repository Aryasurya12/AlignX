# AlignX Sample Biological Datasets

This directory provides curated, real-world biological sequences from standard NCBI reference databases to benchmark and demonstrate AlignX on genuine genomic data.

## Datasets

### 1. Beta-Globin (HBB) Homology
- **Reference:** `human_hbb.fasta` (NCBI `NM_000518.5`, Homo sapiens hemoglobin subunit beta CDS, 444 bp)
- **Query:** `chimp_hbb.fasta` (NCBI `XM_001148411.5`, Pan troglodytes ortholog CDS, 444 bp)
- **Characteristics:** High homology (~99% identity), isolated single-nucleotide differences, long uninterrupted exact anchors. Demonstrates huge speedups with banded gap resolution.

### 2. SARS-CoV-2 Spike RBD Variants
- **Reference:** `sars_cov2_wuhan_rbd.fasta` (NCBI `NC_045512.2`, isolate Wuhan-Hu-1 Spike RBD fragment, 360 bp)
- **Query:** `sars_cov2_omicron_rbd.fasta` (NCBI `OL815965.1`, Omicron BA.1 Spike RBD fragment, 360 bp)
- **Characteristics:** Real-world viral lineage divergence with multiple substitution mutations in receptor binding motifs.

### 3. TP53 Tumor Suppressor Exon 7
- **Reference:** `tp53_wildtype.fasta` (NCBI `NM_000546.6`, exon 7 wild-type, 276 bp)
- **Query:** `tp53_mutant.fasta` (Human oncogenic R248W hotspot substitution + localized in-frame deletion, 271 bp)
- **Characteristics:** Indel plus substitution, demonstrating adaptive band width expansion and structural variant mutation detection.
