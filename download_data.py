"""
This file is used to download the data from the competition's repository on GitHub and save it in the data/statbomb directory.
Alternatively, you can download the data manually from the following link: https://github.com/statsbomb/open-data
and save competition.json, events and matches in the data/statbomb directory.
"""

import os
import requests
from tqdm import tqdm

# Define the URL of the data on GitHub
URL = "https://github.com/statsbomb/open-data"

# Define the directory where the data will be saved
PATH_STATBOMB = "data"

# Create the directory if it doesn't exist
os.makedirs(PATH_STATBOMB, exist_ok=True)

# Define the files to download
files = [
    "data/competitions.json",
]

# Define the folders to download
folders = [
    "data/events",
]

# Define the folders containing subfolders to download
subfolder = [
    "data/matches",
]

# =============================================================================
# # Define the function to download the data


def download_file(url, file_path):
    """
    This function downloads a file from a URL and saves it to the specified file path.

    Parameters
    ----------
    url : str
        The URL of the file to download.

    file_path : str
        The file path where the file will be saved.
    """

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in tqdm(r.iter_content(chunk_size=8192)):
                f.write(chunk)


def download_folder(url, folder_path):
    """
    This function downloads a folder from a URL and saves it to the specified folder path.

    Parameters
    ----------
    url : str
        The URL of the folder to download.

    folder_path : str
        The folder path where the folder will be saved.
    """
    # Create the directory if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Download the files
    r = requests.get(url)
    r.raise_for_status()

    for file in r.json()["payload"]["tree"]["items"]:
        name = file["name"]
        download_file(f"{url}/{name}", os.path.join(folder_path, name))


def download_subfolder(url, folder_path):
    """
    This function downloads a folder containing subfolders from a URL and saves it to the specified folder path.

    Parameters
    ----------
    url : str
        The URL of the folder to download.

    folder_path : str
        The folder path where the folder will be saved.
    """
    # Create the directory if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Download the files
    r = requests.get(url)
    r.raise_for_status()

    for subbolders in r.json()["payload"]["tree"]["items"]:
        name = subbolders["name"]
        download_folder(f"{url}/{name}", os.path.join(folder_path, name))


if __name__ == "__main__":
    # Download the files
    print("Downloading data...")
    for file in tqdm(files):
        download_file(f"{URL}/raw/master/{file}", file)

    # Download the folders
    for folder in tqdm(folders):
        download_folder(f"{URL}/tree/master/{folder}", folder)

    # Download the subfolders from the folder
    for folder in tqdm(subfolder):
        download_subfolder(f"{URL}/tree/master/{folder}", folder)

    print("Data downloaded successfully.")