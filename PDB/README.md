# PDB Structural Parser & Contact Map Generator

A Python pipeline for fetching 3D macromolecular structures from the RCSB Protein Data Bank (PDB), extracting CA backbone coordinates, calculating spatial contact matrices using vectorized NumPy operations, and exporting contact maps and sequence node mappings for computational biology applications.

---

## Features

* **RCSB PDB API Integration**: Automatically fetches '.pdb' files and entry metadata directly from the RCSB REST APIs using standard 4-character RCSB PDB IDs.
* **Vectorized Distance Calculations**: Computes full N x N Euclidean distance matrices for N number of CA atoms with the utilization of NumPy broadcasting operations.
* **Flexible Contact Cutoffs**: Identifies residue contacts based on Angstrom thresholds that can be set by the user (default is 8.0 Å).
* **Binary & Weighted Contact Maps**: Supports binary contact matrices (1 for contact, 0 otherwise) or contact matrices with explicit weighted distances.
* **Chain-Specific Filtering**: Singles out individual protein chains or processes full structures across all chains.
* **Batch Processing**: Handles text files containing lists of PDB IDs.
* **CSV Export Pipeline**: Generates CSV files containing node sequences along with distance/contact matrices ready for graph analysis.

---

## Installation

### Prerequisites

* Python 3.8+

### Dependencies

Install the required Python libraries using 'pip':

pip install numpy requests

## Usage

### Command-Line Arguments

| Flag | Short | Description | Required |
| --pdb | | Single 4-character RCSB PDB ID (e.g., '1A3N') | Mutually exclusive with '--batch' |
| --batch | | Text file containing list of PDB IDs (one per line, e.g., 'PDB.txt') | Mutually exclusive with --pdb |
| --chain | -c | Filter parsing by a specific protein chain (e.g., 'A') | No |
| --threshold | -t | Contact threshold in Angstroms (default: '8.0') | No |
| --matrix | -m | Toggle saving the contact matrix and residue nodes to CSV | No |
| --weighted | -w | Use continuous Euclidean distances instead of binary 0/1 values | No |

---

### Examples

#### 1. Quick Contact Count (Single PDB)
Parse a single structure ('1A3N') and count total residue contacts within the 8.0 Å threshold:

python PDBStructParser.py --pdb 1A3N

#### 2. Chain-Specific Analysis with Custom Cutoff
Analyze Chain 'A' of '1A3N' with a contact threshold of 6.5 Å:

python PDBStructParser.py --pdb 1A3N --chain A --threshold 6.5

#### 3. Exporting Contact Map and Sequence Nodes
Generate a binary contact matrix CSV and sequence node index file for Chain 'A':

python PDBStructParser.py --pdb 1A3N --chain A --matrix

#### 4. Exporting Weighted Distance Matrix
Generate a non-binary, distance-weighted matrix for contacts under 10.0 Å:

python PDBStructParser.py --pdb 1A3N --chain A --threshold 10.0 --matrix --weighted

#### 5. Batch Processing Multiple Structures
Process a list of PDB IDs provided in 'PDB.txt' and export matrix files for all valid entries:

python PDBStructParser.py --batch PDB.txt --matrix

---

## Output Files

When '--matrix' ('-m') is enabled, the script outputs two CSV files per processed structure:

1. **Matrix CSV ('{ProteinName}.csv')**: An N x N matrix representing spatial residue contacts/interactions.
   * **Binary Mode (default)**: 1.00 indicates CA - CA distance <= threshold, while 0.00 otherwise.
   * **Weighted Mode ('-w')**: Contains actual Euclidean distances (in Å) for contacts within the threshold.
2. **Nodes CSV ('{proteinname}_nodes.csv')**: Maps each row/column in the matrix to its corresponding amino acid residue (e.g., '1 MET', '2 VAL', '3 LEU').

---

## Methodology

1. **Extraction**: Parses standard PDB file formatting to locate 'ATOM' records and extracts 3D coordinates (x, y, z) for alpha carbons (CA atom types).
2. **Broadcasting**: Formats coordinates into an N x N x 3 array to compute pairwise coordinate differences delta x, delta y, delta z against an N x 3 array.
3. **Distance Matrix**: Computes Euclidean distances:
   d = sqrt((xf - xi)^2 + (yf - yi)^2 + (zf - zi)^2)
4. **Upper Triangle Counting**: Uses 'np.triu(..., k=1)' to count unique non-redundant residue contact pairs, excluding self-interactions and symmetric duplicate pairs.
