import argparse
from pathlib import Path
import zipfile
from tqdm import tqdm

def is_data_downloaded(resource_url: str, expected_file: Path, resource_name: str):
    if expected_file.exists():
        return True
    print(f"{resource_name} is missing. Download {expected_file.name} from {resource_url} and place it in the {expected_file.parent} directory.")
    return False

def extract_zip(src, dst):
    with zipfile.ZipFile(src, "r") as zf:
        for member in tqdm(zf.infolist(), desc="Extracting "):
            try:
                zf.extract(member, dst)                    
            except zipfile.error as err:
                print(err)

def prepare_datasets(path):
    # Datasets folder
    dataset_path = Path(path)
    dataset_path.mkdir(parents=True, exist_ok=True)

    market_path = dataset_path / "Market-1501-v15.09.15.zip"
    market_present = is_data_downloaded(
        "https://drive.google.com/file/d/0B8-rUzbwVRk0c054eEozWG9COHM/view?resourcekey=0-8nyl7K9_x37HlQm34MmrYQ",
        market_path,
        "Market-1501"
    )

    pa100k_path = dataset_path / "data.zip"
    pa100k_present = is_data_downloaded(
        "https://drive.google.com/file/d/1Bod3MrbdCRiSvpR7NSOYi-rF3-ushwtj/",
        pa100k_path,
        "PA100k"
    )

    peta_path = dataset_path / "PETA.zip"
    peta_present = is_data_downloaded(
        "https://www.dropbox.com/s/52ylx522hwbdxz6/PETA.zip?dl=1",
        peta_path,
        "PETA"
    )
    
    annotations_path = dataset_path / "2024_phase1.zip"
    annotations_present = is_data_downloaded(
        "https://drive.google.com/file/d/1FMX9nUrXArxW4wkORO6Z7zp7xy7JBjUM/view?usp=sharing",
        annotations_path,
        "Annotations"
    )

    templates_path = dataset_path / "2024_submission_templates.zip"
    templates_present = is_data_downloaded(
        "https://drive.google.com/file/d/11ZxT8kixkV-vAj8aixS8n2aGJ5Rw0OQy/view",
        templates_path,
        "Submission templates"
    )

    if not all([market_present, pa100k_present, peta_present, annotations_present, templates_present]):
        raise RuntimeError("Missing downloaded zipfiles. Download the data and try again.")

    extract_zip(market_path, dataset_path)
    extract_zip(pa100k_path, dataset_path)
    extract_zip(peta_path, dataset_path)
    extract_zip(annotations_path, dataset_path)
    extract_zip(templates_path, dataset_path)

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