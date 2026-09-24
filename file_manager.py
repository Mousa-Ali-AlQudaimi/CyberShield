"""
CyberShield - File Manager
Stage 1

Responsible for saving and loading project data as JSON files.
"""

import json
from pathlib import Path


class FileManager:
    """Utility class for JSON file storage."""

    DATA_DIR = Path(__file__).resolve().parent.parent / "data"

    def __init__(self, filename):
        if not isinstance(filename, str):
            raise TypeError("Filename must be text.")

        if not filename.strip():
            raise ValueError("Filename cannot be empty.")

        if not filename.endswith(".json"):
            filename += ".json"

        self.filename = filename
        self.file_path = self.DATA_DIR / filename

        self.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def save_data(self, data):
        """Replace file contents with data."""
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except TypeError as error:
            raise TypeError(f"Data cannot be converted to JSON: {error}")

    def load_data(self, default=None):
        """Load JSON data. Return default if file does not exist."""
        if default is None:
            default = []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return default
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON data in {self.filename}: {error}"
            )

    def append_data(self, item):
        """Append one item to a JSON list."""
        data = self.load_data(default=[])

        if not isinstance(data, list):
            raise TypeError(
                f"{self.filename} must contain a JSON list."
            )

        data.append(item)
        self.save_data(data)

    def update_data(self, index, new_item):
        """Update one item by its list index."""
        data = self.load_data(default=[])

        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")

        if index < 0 or index >= len(data):
            raise IndexError("Item index is out of range.")

        data[index] = new_item
        self.save_data(data)

    def delete_data(self, index):
        """Delete one item by its list index."""
        data = self.load_data(default=[])

        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")

        if index < 0 or index >= len(data):
            raise IndexError("Item index is out of range.")

        deleted_item = data.pop(index)
        self.save_data(data)

        return deleted_item

    def clear_data(self):
        """Delete all stored records."""
        self.save_data([])

    def file_exists(self):
        """Return True when the JSON file exists."""
        return self.file_path.exists()

    def __str__(self):
        return f"FileManager({self.filename})"
