# Classto

**Classto** is a Python library for building lightweight, browser-based tools to manually classify images into custom categories - ideal for preparing datasets or sorting visual content.

With just a few lines of Python, Classto spins up a local web interface built on [Flask](https://flask.palletsprojects.com/) and styled with [Tailwind CSS](https://tailwindcss.com/) to let you quickly review, label, and organize images - right from your browser.



### Interface Previews

<p align="center">
  <img src="./assets/screenshot_light.png" alt="Classto Light Mode" width="400">
  &nbsp;&nbsp;&nbsp;
  <img src="./assets/screenshot_dark.png" alt="Classto Dark Mode" width="400">
</p>

<p align="center"><em>Classto in Light and Dark Mode</em></p>
&nbsp;

## Features

- Classify images with one click
- Supports custom category lists
- Images are moved into subfolders per label
- Optionally add unique filename suffixes
- CSV logging for ML dataset tracking
- Delete unwanted images during classification
- Dark mode toggle built in

## Installation

You can install Classto via pip:

```bash
pip install classto
```

## Quickstart
```python
import classto as ct

app = ct.ImageLabeler(
    classes=["Model", "Product Only"],
    image_folder="images",          # Path to your images
    delete_button=True,             # Optional delete button
    suffix=True,                    # Add unique suffix to avoid conflicts
    log_to_csv=True                 # Save results to labels.csv
)

app.launch()
```
Then open your browser at http://127.0.0.1:5000.

### Example Folder Structure
Place your images in a folder (e.g. images/) relative to your script:
```
project/
├── images/
│   ├── cat1.jpg
│   ├── cat2.jpg
│   ├── dog1.jpg
│   └── dog2.jpg
├── app.py
```

After classification, images are moved to:

```
project/
├── classified/
│   ├── Cat/
│   │   ├── cat1__K8dLs.jpg
│   │   └── cat2__a7JkL.jpg
│   ├── Dog/
│   │   ├── dog1__Xy4Tz.jpg
│   │   └── dog2__Zx9Pm.jpg
│   └── labels.csv
```



## Parameters

- `classes` (`List[str]`): A list of categories for classification (e.g. `["Dog", "Cat"]`).
- `image_folder` (`str`): Path to the folder containing the images to classify. Defaults to `"images"`.
- `delete_button` (`bool`): If `True`, shows a delete button to remove images. Defaults to `False`.
- `suffix` (`bool`): If `True`, appends a random suffix to filenames to avoid overwriting. Defaults to `False`.
- `log_to_csv` (`bool`): If `True`, logs each classification into a CSV file. Defaults to `False`.
- `shuffle` (`bool`): If `True`, images are shown in random order. Defaults to `False`.


## How it works
1. Classto loads images from your specified folder (e.g. `images/`)
2. Each classification moves the image to `classified/<category>/`
3. Optionally appends a suffix to the filename
4. If enabled, logs the action to a `labels.csv` file in `classified/`

## CSV Logging Format

If `log_to_csv=True` is enabled, each classification is logged to a `labels.csv` file inside the `classified/` directory. The file contains the following columns:

| original_filename | new_filename        | label          | timestamp                |
|-------------------|---------------------|----------------|--------------------------|
| img01.jpg         | img01__4Fg7T.jpg    | Product Only   | 2025-05-05T15:58:00+00:00 |

- `original_filename`: The name of the image before classification.
- `new_filename`: The new name after suffixing (if enabled).
- `label`: The category selected during classification.
- `timestamp`: When the classification occurred, in ISO 8601 format (UTC).