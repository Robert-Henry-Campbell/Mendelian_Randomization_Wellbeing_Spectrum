import argparse
from pathlib import Path


def main(directory: Path) -> None:
    for file_path in directory.iterdir():
        if file_path.is_file():
            new_file = file_path.with_suffix('.tsv')
            file_path.rename(new_file)
            print(f"Renamed '{file_path}' to '{new_file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename GTEx files to .tsv")
    parser.add_argument("directory", type=Path, help="Directory with GTEx files")
    args = parser.parse_args()
    main(args.directory)
