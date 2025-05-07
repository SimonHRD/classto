import csv
import os
import tempfile
from classto.utils import generate_suffix, sanitize_label, get_next_image_from_folder, log_classification_to_csv

# --- generate_suffix() ---

# Test: generated suffix has correct custom length and is alphanumeric
def test_generate_suffix_returns_alphanumeric():
    suffix = generate_suffix(length=6)
    assert len(suffix) == 6
    assert suffix.isalnum()

# Test: default length is 5 characters
def test_generate_suffix_default_len():
    suffix = generate_suffix()
    assert len(suffix) == 5
    assert suffix.isalnum()

# --- sanitize_label() ---

# Test: input with only valid characters is unchanged
def test_sanitize_label_no_change():
    label = "Product_Only"
    assert sanitize_label(label) == "Product_Only"

# Test: invalid characters are stripped and leading/trailing spaces removed
def test_sanitize_label_removes_invalid_characters():
    label = "Something@# Included!! "
    assert sanitize_label(label) == "Something Included"

# --- get_next_image_from_folder() ---

# Test: returns first sorted image if shuffle=False 
def test_get_next_image_sorted():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image files
        filenames = ["img1.jpg", "img2.jpg", "img3.png"]
        for name in filenames:
            with open(os.path.join(tmpdir, name), "w") as f:
                f.write("fake image")

        result = get_next_image_from_folder(tmpdir, shuffle=False)
        assert result == "img1.jpg"

# Test: returns any image if shuffle=True
def test_get_next_image_shuffled():
    with tempfile.TemporaryDirectory() as tmpdir:
        filenames = ["a.jpg", "b.jpg", "c.jpg"]
        for name in filenames:
            with open(os.path.join(tmpdir, name), "w") as f:
                f.write("test")

        result = get_next_image_from_folder(tmpdir, shuffle=True)
        assert result in filenames

# --- log_classification_to_csv() ---

# Test: CSV file is created with header and first row    
def test_log_classification_creates_csv_with_header():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "labels.csv")
        
        log_classification_to_csv(
            log_file=log_path,
            original_filename="cat1.jpg",
            final_filename="cat1__Ab123.jpg",
            label="Cat"
        )
        
        with open(log_path, newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        
        assert rows[0] == ["original_filename", "new_filename", "label", "timestamp"]
        assert rows[1][0] == "cat1.jpg"
        assert rows[1][1].startswith("cat1__")
        assert rows[1][2] == "Cat"
        assert "T" in rows[1][3]  # ISO timestamp format check

# Test: second log appends row without rewriting header
def test_log_classification_appends_rows():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "labels.csv")

        # First log
        log_classification_to_csv(log_path, "dog1.jpg", "dog1__Xyz99.jpg", "Dog")

        # Second log
        log_classification_to_csv(log_path, "dog2.jpg", "dog2__Tt341.jpg", "Dog")

        with open(log_path, newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))

        assert len(rows) == 3  # header + 2 entries
        assert rows[2][0] == "dog2.jpg"