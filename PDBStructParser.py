import requests
import argparse
import csv
import time
import numpy as np
import sys

def main():
    args = setup_parser()
    if args.batch:
        try:
            with open(args.batch, "r") as file:
                pdb_ids = file.read().splitlines()
                for id in pdb_ids:
                    time.sleep(1)
                    protein_name, contacts, dist_matrix, coordinates, nodes = contact_finder(id, args.chain, args.threshold, args.weighted)
                    if len(coordinates) == 0:
                        if args.chain:
                            print(f"{id} has no atoms associated with chain {args.chain}")
                        continue
                    contact_output(args.chain, protein_name, contacts, args.threshold)
                    if args.matrix and isinstance(dist_matrix, np.ndarray):
                        matrix_generator(dist_matrix, protein_name, nodes)
        except FileNotFoundError:
            sys.exit("File not found")
    else:
        protein_name, contacts, dist_matrix, coordinates, nodes = contact_finder(args.pdb, args.chain, args.threshold, args.weighted)
        if len(coordinates) == 0:
                sys.exit("Invalid ID and/or invalid chain associated with ID")
        contact_output(args.chain, protein_name, contacts, args.threshold)
        if args.matrix and isinstance(dist_matrix, np.ndarray):
            matrix_generator(dist_matrix, protein_name, nodes)

def setup_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdb", help="Input valid ID from RCSB Protein Data Bank e.g. '1A3N'")
    group.add_argument("--batch", help="Input full name of .txt file including valid PDB ID's e.g. 'PDB.txt'")
    parser.add_argument("--chain", "-c", help="Input chain for parsing (optional)")
    parser.add_argument("--threshold", "-t", type=float, help="Input threshold for contacts (optional, default = 8 Angstroms)")
    parser.add_argument("--matrix", "-m", action="store_true", help="Toggles matrix generator to output binary contact map")
    parser.add_argument("--weighted", "-w", action="store_true", help="Turns contact points in contact map into non-binary distances")
    return parser.parse_args()

def contact_finder(id, chain, threshold, weighted):
    try:
        response = requests.get(f"https://files.rcsb.org/download/{id}.pdb")
        response2 = requests.get(f"https://data.rcsb.org/rest/v1/core/entry/{id}")
        protein_name = response2.json()["struct"]["title"].title()
    except KeyError:
        print(f"ID '{id}' is invalid")
        return 0, 0, 0, [], 0
    lines = response.text.splitlines()
    coordinates = []
    nodes = []

    if chain:
        for line in lines:
            if line.startswith("ATOM") and line[12:15].strip().startswith("CA") and line[21].upper().startswith(chain):
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    residue = line[17:20].strip()
                    coordinates.append([x, y, z])
                    nodes.append(residue)
    else:
        for line in lines:
            if line.startswith("ATOM") and line[12:15].strip().startswith("CA"):
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                residue = line[17:20].strip()
                coordinates.append([x, y, z])
                nodes.append(residue)

    points = len(coordinates)

    try:
        coords_array = np.array(coordinates)
        new_coords = coords_array.reshape(points, 1, 3)
        diff = coords_array - new_coords
        dist_matrix = np.sqrt(((diff ** 2).sum(axis=2)))

        if threshold:
            is_contact = dist_matrix < threshold
            contact_matrix = is_contact.astype(int)
        else:
            is_contact = dist_matrix < 8.0
            contact_matrix = is_contact.astype(int)

    except ValueError:
        return 0, 0, 0, coordinates, 0


    unique_pairs = np.triu(contact_matrix, k=1)
    contacts = np.count_nonzero(unique_pairs)

    if weighted:
        dist_matrix = dist_matrix * contact_matrix
    else:
        dist_matrix = contact_matrix

    return protein_name, contacts, dist_matrix, coordinates, nodes


def contact_output(chain, protein_name, contacts, threshold_input):
    if threshold_input:
        threshold = threshold_input
    else:
        threshold = 8
    if chain:
        print(f"Chain {chain} of {protein_name} has {contacts} contacts at a threshold of {threshold} Angstroms")
    else:
        print(f"{protein_name} has {contacts} contacts at a threshold of {threshold} Angstroms")


def matrix_generator(dist_matrix, protein_name, nodes):

    np.savetxt(fname=f"{protein_name}.csv".replace(' ', ''), X=dist_matrix, delimiter=",", fmt="%.2f")

    print("Contact map has been created")

    with open(f"{protein_name.lower().replace(' ', '')}_nodes.csv", "w") as file:
        writer = csv.writer(file)
        for i, node in enumerate(nodes):
            writer.writerow([f"{i+1} {node}"])

    print("Sequence array has been created")

if __name__ == "__main__":
    main()
