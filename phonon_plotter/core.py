from typing import List


class Plotter:
    def __init__(self, band_yaml_files: List[str]) -> None:
        self._band_yaml_files = band_yaml_files

    def load_data(self) -> None:
        pass
