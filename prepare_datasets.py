import argparse
from pathlib import Path

def ensure_downloaded():
    pass

def prepare_datasets(path):
    # Datasets folder
    dataset_path = Path(path)
    dataset_path.mkdir(parents=True, exist_ok=True)

    # Download & extract datasets
    prepare_market(dataset_path)
    prepare_pa100k(dataset_path)
    prepare_peta(dataset_path)

    # Download & extract annotations
    prepare_annotations(dataset_path)

    # Download & extract submission templates
    prepare_templates(Path("./"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ensure datasets are downloaded and prepared in a common format",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="./data",
        help="Dataset directory. Downloaded datasets are stored in this directory.",
    )
    args = parser.parse_args()

    prepare_datasets(args.data_dir)