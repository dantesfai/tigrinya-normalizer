import argparse
import os
from tigrinya_normalizer.normalizer import TigrinyaNormalizer

def main():
    parser = argparse.ArgumentParser(description="Normalize Tigrinya text")
    parser.add_argument(
        "-i", "--input", type=str, required=True,
        help="Path to the input dataset file"
    )
    parser.add_argument(
        "-o", "--output", type=str, default="normalized_output.txt",
        help="Filename for normalized output (can include path)"
    )
    parser.add_argument(
        "-d", "--dict_path", type=str, default="dictionaries",
        help="Path to the dictionary folder"
    )
    parser.add_argument(
        "-p", "--punctuation", type=str, default=None,
        help="Punctuation marks to keep (optional)"
    )
    args = parser.parse_args()

    # Extract output directory from output file path
    output_dir = os.path.dirname(args.output) or "."

    normalizer = TigrinyaNormalizer(
        dict_path=args.dict_path,
        dataset_file=args.input,
        output_dir=output_dir
    )

    try:
        normalizer.normalize_and_save(os.path.basename(args.output), punctuation_to_keep=args.punctuation)
        print(f"Normalization complete. Output saved to {args.output}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
