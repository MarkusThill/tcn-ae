"""Temporal convolutional autoencoder for anomaly detection in multivariate time series."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("tcn-ae")
except PackageNotFoundError:  # pragma: no cover - only when running from a source tree
    __version__ = "0.0.0.dev0"

__all__ = ["__version__"]
