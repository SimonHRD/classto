import os
from typing import List

from .main import create_flask_app

class ImageLabeler:
    """
    A web-based tool for manually labeling images into user-defined categories.

    This class configures and launches a Flask app to classify images
    from a given folder into specified classes. Options include random order,
    filename suffixing, and logging results to a CSV file.
    """
    
    def __init__(
        self, 
        classes: List[str], 
        delete_button: bool = True, 
        image_folder: str = "images", 
        shuffle: bool = False, 
        suffix: bool = False, 
        log_to_csv: bool = False
    ) -> None:
        """
        Initialize the ImageLabeler.

        Args:
            classes (List[str]): The list of labels to classify images into.
            delete_button (bool): Whether to include a delete button. Defaults to True.
            image_folder (str): Path to the folder containing images. Defaults to 'images'.
            shuffle (bool): Whether to show images in random order. Defaults to False.
            suffix (bool): Whether to append a random suffix to saved filenames. Defaults to False.
            log_to_csv (bool): Whether to log classifications to a CSV file. Defaults to False.
        """
        
        self.classes = classes
        self.delete_button = delete_button
        self.image_folder = image_folder
        self.image_folder = os.path.abspath(image_folder)
        self.shuffle = shuffle
        self.suffix = suffix
        self.log_to_csv = log_to_csv


    def launch(self, host: str = "127.0.0.1", port: int = 5000, debug: bool = False) -> None:
        """
        Start the Flask application to label images via the browser.

        Args:
            host (str): The hostname to listen on. Defaults to "127.0.0.1" (localhost).
            port (int): The port to bind to. Defaults to 5000.
            debug (bool): Whether to enable Flask's debug mode. Defaults to False.
        """
        app = create_flask_app(
            self.classes, 
            self.delete_button, 
            self.image_folder, 
            self.shuffle, 
            self.suffix, 
            self.log_to_csv
        )
        app.run(host=host, port=port, debug=debug)