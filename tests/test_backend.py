"""The package targets Keras with the TensorFlow backend by default."""

import os

import pytest


@pytest.mark.skipif(
    os.environ.get("KERAS_BACKEND", "tensorflow") != "tensorflow",
    reason="KERAS_BACKEND overridden to a non-default backend",
)
def test_default_keras_backend_is_tensorflow():
    import keras

    assert keras.backend.backend() == "tensorflow"


def test_keras_imports_without_manual_backend_setup():
    """Regression guard: Keras 3 raises ImportError when no framework is installed."""
    import keras

    assert keras.__version__.startswith("3.")
