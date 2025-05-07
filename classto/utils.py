import csv
import os
import random
import string
from datetime import datetime, timezone


def generate_suffix(length: int = 5) -> str:
    """
    Generate a random alphanumeric string for use as a unique suffix.

    Args:
        length (int): The length of the generated string. Defaults to 5.

    Returns:
        str: A randomly generated alphanumeric string.
    """
    
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def sanitize_label(label: str) -> str:
    """
    Sanitize a classification label by removing disallowed characters.

    Only alphanumeric characters, spaces, hyphens, and underscores are preserved.
    Leading and trailing whitespace is removed.

    Args:
        label (str): The raw label input from the user or interface.

    Returns:
        str: A cleaned and safe label string suitable for use as a folder name.
    """
    
    return "".join(c for c in label if c.isalnum() or c in (' ', '-', '_')).strip()


def get_next_image_from_folder(image_folder: str, shuffle: bool = False) -> str | None:
    """
    Retrieve the next image filename from a given folder.

    This function scans the specified folder for image files and returns the next one
    based on alphabetical order or at random if shuffle is enabled. Supported image
    formats include .jpg, .jpeg, .png, and .webp.

    Args:
        image_folder (str): Path to the folder containing input images.
        shuffle (bool, optional): If True, returns a random image instead of the first one. Defaults to False.

    Returns:
        str | None: The filename of the next image to classify, or None if no valid images are found.
    """
    
    if not os.path.isdir(image_folder):
        return None
    files = sorted([
        f for f in os.listdir(image_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    ])
    if not files:
        return None
    return random.choice(files) if shuffle else files[0]


def log_classification_to_csv(
    log_file: str,
    original_filename: str,
    final_filename: str,
    label: str
) -> None:
    """
    Append a classification record to a CSV log file.

    If the file does not exist, it is created with the appropriate header.
    Each entry includes the original filename, final filename, label, and UTC timestamp.

    Args:
        log_file (str): Path to the CSV file to write to.
        original_filename (str): The name of the image before renaming.
        final_filename (str): The final name of the image after optional suffixing.
        label (str): The category assigned to the image.
    """
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if os.stat(log_file).st_size == 0:
            writer.writerow(["original_filename", "new_filename", "label", "timestamp"])
        writer.writerow([
            original_filename,
            final_filename,
            label,
            datetime.now(timezone.utc).isoformat()
        ])
