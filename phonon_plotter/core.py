from typing import List

import yaml


class Plotter:
    def __init__(self, band_yaml_files: List[str]) -> None:
        self._band_yaml_files = band_yaml_files
        self._n_band = len(band_yaml_files)
        self.load_data()

    def load_data(self) -> None:
        """Load plot data from multiple band.yaml"""
        data = []
        for band_yaml_file in self._band_yaml_files:
            with open(band_yaml_file) as f:
                data.append(yaml.safe_load(f))

        self._dists = [[point["distance"] for point in data[0]["phonon"]]]
        self._eigenvalues = [
            [[e["frequency"] for e in point["band"]] for point in data[i]["phonon"]]
            for i in range(self._n_band)
        ]

        self._labels = []
        self._label_dists = []
        for point in data[0]["phonon"]:
            if "label" not in point:
                continue

            self._labels.append(point["label"])
            self._label_dists.append(point["distance"])
