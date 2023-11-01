import argparse
from pathlib import Path, PurePosixPath
import zipfile
from tqdm import tqdm
import shutil
import numpy as np


def is_data_downloaded(resource_url: str, expected_file: Path, resource_name: str):
    if expected_file.exists():
        return True
    print(f"{resource_name} is missing. Download {expected_file.name} from {resource_url} and place it in the {expected_file.parent} directory.")
    return False

def extract_zip(src, dst, pwd=None):
    with zipfile.ZipFile(src, "r") as zf:
        for member in tqdm(zf.infolist(), desc="Extracting "):
            try:
                zf.extract(member, dst, pwd=pwd)                    
            except zipfile.error as err:
                print(err)

def prepare_peta(dataset_path):
    # PETA dataset
    peta_path = dataset_path / "PETA"
    peta_path.mkdir(parents=True, exist_ok=True)
    peta_zipfile = peta_path / "peta.zip"
    print("Download PETA dataset")
    url = "https://www.dropbox.com/s/52ylx522hwbdxz6/PETA.zip?dl=1"
    download_url(url, peta_zipfile)
    print("Extract PETA dataset")
    extract_zip(peta_zipfile, peta_path)
    peta_img_path = peta_path / "images"
    peta_img_path.mkdir(parents=True, exist_ok=True)
    mapping = {row[0]: row[1] for row in np.genfromtxt("peta_file_mapping.txt", dtype=str, delimiter=",")}
    for file in tqdm(peta_path.glob("*/*/*/*")):
        if file.suffix == ".txt":
            continue
        shutil.move(file, dataset_path / mapping[str(PurePosixPath(file)).replace(str(dataset_path) + "/", "")])

def prepare_datasets(path):
    # Datasets folder
    dataset_path = Path(path)
    dataset_path.mkdir(parents=True, exist_ok=True)

    market_zip = dataset_path / "Market-1501-v15.09.15.zip"
    market_present = is_data_downloaded(
        "https://drive.google.com/file/d/0B8-rUzbwVRk0c054eEozWG9COHM/view?resourcekey=0-8nyl7K9_x37HlQm34MmrYQ",
        market_zip,
        "Market-1501"
    )

    pa100k_zip = dataset_path / "data.zip"
    pa100k_present = is_data_downloaded(
        "https://drive.google.com/file/d/1Bod3MrbdCRiSvpR7NSOYi-rF3-ushwtj/",
        pa100k_zip,
        "PA100k"
    )

    peta_zip = dataset_path / "PETA.zip"
    peta_present = is_data_downloaded(
        "https://www.dropbox.com/s/52ylx522hwbdxz6/PETA.zip?dl=1",
        peta_zip,
        "PETA"
    )
    
    annotations_zip = dataset_path / "2024_phase1.zip"
    annotations_present = is_data_downloaded(
        "https://drive.google.com/file/d/1FMX9nUrXArxW4wkORO6Z7zp7xy7JBjUM/view?usp=sharing",
        annotations_zip,
        "Annotations"
    )


    if not all([market_present, pa100k_present, peta_present, annotations_present]):
        raise RuntimeError("Missing downloaded zipfiles. Download the data and try again.")

    extract_zip(market_zip, dataset_path)
    extract_zip(pa100k_zip, dataset_path / "PA100k")
    extract_zip(peta_zip, dataset_path / "PETA")
    extract_zip(annotations_zip, dataset_path)

    (dataset_path / "Market-1501-v15.09.15").rename(dataset_path / "Market1501")

    (dataset_path / "PETA" / "images").mkdir(exist_ok=True)
    mapping = {row[0]: row[1] for row in np.genfromtxt("peta_file_mapping.txt", dtype=str, delimiter=",")}
    for file in tqdm((dataset_path / "PETA").glob("*/*/*/*")):
        if file.suffix == ".txt":
            continue
        shutil.move(file, dataset_path / mapping[str(PurePosixPath(file)).replace(str(dataset_path) + "/", "")])


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