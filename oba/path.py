class Path:
    def __init__(self, path=None, vi=None):
        self._path = path or []
        self._valid_index = vi

    def mark(self):
        if self._valid_index is None:
            self._valid_index = len(self._path) - 1

    def __truediv__(self, other: str):
        if not isinstance(other, str):
            raise ValueError("Path components must be strings")
        return Path(self._path.copy() + [other], vi=self._valid_index)

    def __call__(self):
        return '→'.join(self._path)

    def __len__(self):
        return len(self._path)

    def __str__(self):
        valid_path = self._path[:self._valid_index]
        invalid_path = self._path[self._valid_index:]
        valid_path = list(map(lambda x: f'✓{x}', valid_path))
        invalid_path = list(map(lambda x: f'✗{x}', invalid_path))
        return ' → '.join(valid_path + invalid_path)
