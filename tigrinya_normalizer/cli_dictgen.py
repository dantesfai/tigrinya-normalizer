# tigrinya_normalizer/cli_dictgen.py

import argparse
from tigrinya_normalizer.dictionary_generator import TiDictionary

def main():
    parser = argparse.ArgumentParser(description="Generate Tigrinya normalization dictionaries.")
    parser.add_argument("-i", "--input", required=True, help="Input text file path")
    parser.add_argument("-o", "--output", required=True, help="Output directory for dictionaries")

    args = parser.parse_args()

    ti_dict = TiDictionary(args.input, args.output)
    ti_dict.create_dictionary("clitic_dict.txt", "words_with_fwd_slash.txt", "words_with_dots.txt")
    ti_dict.create_improper_clitic()
    ti_dict.write_clitic_dict(ti_dict.clitic_zipped_dict)

    print("✔ Dictionary generation completed.")
