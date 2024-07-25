from typing import List

import matplotlib.pyplot as plt
import yaml

COLORS = ["r", "C0", "C1"]


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

        # Create list of label and list of label distance
        self._labels = []
        self._label_dists = []
        for point in data[0]["phonon"]:
            if "label" not in point:
                continue

            self._labels.append(point["label"])
            self._label_dists.append(point["distance"])
        if len(self._labels) == 0:
            # Create list of label
            for cnt, (i, j) in enumerate(data[0]["labels"]):
                if cnt == 0:
                    self._labels.append(i)
                self._labels.append(j)

            # Create list of label distance
            step = data[0]["segment_nqpoint"][0]
            n_dists = len(self._dists[0])
            self._label_dists = [self._dists[0][i] for i in range(0, n_dists, step)]
            self._label_dists.append(self._dists[0][-1])

    def plot(self, label_size: int = 28, tick_size: int = 24) -> None:
        """Plot phonon bands

        Args:
            label_size (int, optional): The size of axis labels. Defaults to 28.
            tick_size (int, optional): The size of ticks. Defaults to 24.
        """
        if self._n_band > 1:
            self._fig, self._ax = plt.subplots(figsize=(16, 12))
        else:
            self._fig, self._ax = plt.subplots(figsize=(12.6, 12))

        # Fix the appearance of phonon bands
        self._ax.set_xlabel("Wave vector", fontsize=label_size)
        self._ax.set_ylabel("Frequency (THz)", fontsize=label_size)
        self._ax.set_xlim(0, self._label_dists[-1])
        self._ax.set_xticks(self._label_dists, self._labels)
        self._ax.tick_params(labelsize=tick_size)
        self._ax.tick_params(axis="x", bottom=False)

        if self._n_band > 1:
            for i in range(self._n_band):
                self._ax.plot(
                    self._dists[0],
                    self._eigenvalues[i],
                    linewidth=1.5,
                    color=COLORS[i],
                )
        else:
            self._ax.plot(
                self._dists[0], self._eigenvalues[0], linewidth=1.5, color="r"
            )
        self._ax.axhline(linewidth=1, color="black")
        for dist in self._label_dists:
            self._ax.axvline(x=dist, linewidth=1, color="black")
