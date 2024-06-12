from data.Data import Data

class DataSet:
    def __init__(self):
        self._dataset = {}

    def get(self, k):
        """Ottiene il set di informazioni legate alla chiave k.

        Args:
            k (str): La chiave per il dato.

        Returns:
            dict: Set di informazioni legate alla chiave k.
        """
        return self._dataset.get(k, None)

    def set(self, data: Data):
        self._dataset[data.name] = data
        return data