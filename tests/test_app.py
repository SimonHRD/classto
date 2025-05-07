import os
import tempfile
import shutil
import pytest

from classto.main import create_flask_app


@pytest.fixture
def client():
    tmpdir = tempfile.mkdtemp()
    image_path = os.path.join(tmpdir, "test.jpg")

    with open(image_path, "wb") as f:
        f.write(b"fake image data")

    app = create_flask_app(
        classes=["Product", "Model"],
        delete_button=True,
        image_folder=tmpdir,
        shuffle=False,
        suffix=False,
        log_to_csv=False
    )
    app.config["TESTING"] = True
    app.image_folder = tmpdir  # expose it for tests

    client = app.test_client()

    yield client

    shutil.rmtree(tmpdir)


# --- Basic Route Tests ---

# Test: Index route loads and includes classification heading
def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Classify this image" in response.data

# Test: Image route returns the test image
def test_image_serving(client):
    response = client.get("/images/test.jpg")
    assert response.status_code == 200
    assert response.content_type.startswith("image")


# --- Classification Logic ---

# Test: Image gets classified and moved (simulate POST)
def test_classify_image(client):
    response = client.post("/classify", json={
        "label": "Product",
        "image": "test.jpg"
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "next_image" in json_data


# Test: Delete label deletes image file
def test_delete_image(client):
    image_path = os.path.join(client.application.image_folder, "test.jpg")
    assert os.path.exists(image_path)

    response = client.post("/classify", json={
        "label": "Delete Image",
        "image": "test.jpg"
    })
    assert response.status_code == 200
    assert not os.path.exists(image_path)


# --- Edge Cases ---

# Test: Classify with missing image file
def test_classify_nonexistent_image(client):
    response = client.post("/classify", json={
        "label": "Model",
        "image": "missing.jpg"
    })
    assert response.status_code == 200
    # Should still return next image (or None), but file was not found
    assert "next_image" in response.get_json()
