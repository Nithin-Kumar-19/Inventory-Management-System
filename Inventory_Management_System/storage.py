import json
import os


class JSONStorage:
    """
    Simple JSON file storage helper.

    Stores and loads a Python list (e.g., list of products, customers, or sales).
    """

    def __init__(self, filename):
        self.filename = filename

    def load(self):
        """Load data from JSON file. Returns a list."""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, OSError):
            print(f"Warning: Could not read {self.filename}. Starting with empty data.")
            return []

    def save(self, data):
        """Save a list to JSON file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"Error saving to {self.filename}: {e}")
