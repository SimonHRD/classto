import os
import shutil
from typing import List

from flask import Flask, render_template, request, jsonify, send_from_directory

from classto.utils import generate_suffix, sanitize_label, get_next_image_from_folder, log_classification_to_csv


def create_flask_app(
    classes: List[str], 
    delete_button: bool, 
    image_folder: str, 
    shuffle: bool, 
    suffix: bool, 
    log_to_csv: bool = False
) -> Flask:
    """
    Create and configure the Flask app for Classto.

    This app serves a web interface to manually classify images 
    into custom categories. Images are moved into per-label folders, 
    optionally renamed with a unique suffix, and optionally logged to a CSV file.

    Args:
        classes (List[str]): The list of classification labels (e.g. ["Model", "Product Only"]).
        delete_button (bool): Whether to include a delete button in the UI.
        image_folder (str): Path to the input image directory.
        shuffle (bool): Whether to show images in random order.
        suffix (bool): Whether to add a random suffix to filenames.
        log_to_csv (bool, optional): Whether to log classification results to CSV. Defaults to False.

    Returns:
        Flask: A configured Flask app instance ready to run.
    """
    
    package_dir = os.path.dirname(__file__)

    app = Flask(
        __name__,
        static_folder=os.path.join(package_dir, "static"),
        static_url_path="/static",
        template_folder=os.path.join(package_dir, "templates")
    )


    CLASSIFIED_FOLDER = os.path.join(image_folder, "..", "classified")
    LOG_FILE = os.path.join(CLASSIFIED_FOLDER, "labels.csv")


    @app.route('/')
    def index():
        image_filename = get_next_image_from_folder(image_folder=image_folder, shuffle=shuffle)
        return render_template(
            'index.html',
            image_filename=image_filename,
            classes=classes,
            delete_button=delete_button,
            image_folder=image_folder
        )

    @app.route('/images/<filename>')
    def serve_image(filename):
        return send_from_directory(image_folder, filename)

    @app.route('/classify', methods=['POST'])
    def classify():
        data = request.json
        label = data.get("label")
        filename = data.get("image")
        src = os.path.join(image_folder, filename)

        # If it's a delete action, remove the image and skip the rest
        if label.lower() in ["delete", "delete image", "🗑️ delete image"] and os.path.exists(src):
            os.remove(src)
            print(f"Deleted image: {filename}")
            next_image = get_next_image_from_folder(image_folder=image_folder, shuffle=shuffle)
            return jsonify({"next_image": next_image})

        # Sanitize the label
        safe_label = sanitize_label(label)

        # Create label-specific folder on-demand
        dest_folder = os.path.join(CLASSIFIED_FOLDER, safe_label)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Determine destination filename
        if not suffix:
            dst = os.path.join(dest_folder, filename)
            final_filename = filename
        else:
            name, ext = os.path.splitext(filename)
            random_suffix = generate_suffix()
            final_filename = f"{name}__{random_suffix}{ext}"
            dst = os.path.join(dest_folder, final_filename)

            while os.path.exists(dst):
                random_suffix = generate_suffix()
                final_filename = f"{name}__{random_suffix}{ext}"
                dst = os.path.join(dest_folder, final_filename)

        # Move image
        if os.path.exists(src):
            shutil.move(src, dst)

            # Optional: Log to CSV
            if log_to_csv:
                log_classification_to_csv(
                    log_file=LOG_FILE, 
                    original_filename=filename, 
                    final_filename=final_filename,
                    label=label
                )

        next_image = get_next_image_from_folder(image_folder=image_folder, shuffle=shuffle)
        return jsonify({"next_image": next_image})


    return app
