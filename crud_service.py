from utils.file_manager import FileManager


class CRUDService:
    """Generic CRUD operations for JSON-list resources."""
    def __init__(self, filename, id_field):
        self.storage = FileManager(filename)
        self.id_field = id_field

    def all(self):
        return self.storage.load_data([])

    def find(self, item_id):
        for row in self.all():
            if str(row.get(self.id_field)) == str(item_id):
                return row
        return None

    def search(self, term):
        rows = self.all()
        if term is None:
            return rows

        term = str(term).strip().lower()
        if not term:
            return rows

        return [row for row in rows
                if any(term in str(value).lower() for value in row.values())]

    def add(self, row):
        if self.find(row.get(self.id_field)) is not None:
            raise ValueError(f"Duplicate {self.id_field}: {row.get(self.id_field)}")
        self.storage.append_data(row)
        return row

    def update(self, item_id, changes, protected=()):
        rows = self.all()
        for index, row in enumerate(rows):
            if str(row.get(self.id_field)) == str(item_id):
                for key, value in changes.items():
                    if key not in protected and value is not None:
                        row[key] = value
                self.storage.update_data(index, row)
                return row
        raise ValueError(f"{self.id_field} not found.")

    def delete(self, item_id):
        rows = self.all()
        for index, row in enumerate(rows):
            if str(row.get(self.id_field)) == str(item_id):
                return self.storage.delete_data(index)
        raise ValueError(f"{self.id_field} not found.")
