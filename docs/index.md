# tcn-ae

A temporal convolutional autoencoder (TCN-AE) for unsupervised anomaly detection in
multivariate time series.

This package provides a reference implementation of the algorithm described in:

> Markus Thill, Wolfgang Konen, Hao Wang, Thomas Bäck.
> *Temporal convolutional autoencoder for unsupervised anomaly detection in time series.*
> Applied Soft Computing, 2021.

!!! warning "Not ready for use"

    The package currently contains no model implementation — it is packaging and
    infrastructure only, and installing it gives you nothing usable yet. The released
    versions exist to validate the release pipeline, not to be depended on. The TCN-AE
    implementation and a stable public API are still to come.

## Installation

```bash
pip install tcn-ae
```

This installs Keras with the **TensorFlow backend**, matching the paper's original
implementation.

Keras 3 is multi-backend, so PyTorch can be used instead:

```bash
pip install "tcn-ae[torch]"
KERAS_BACKEND=torch python your_script.py
```

TensorFlow is a required dependency rather than an extra, so `tcn-ae[torch]` installs both.
To make the backend choice permanent, set `"backend": "torch"` in `~/.keras/keras.json`.

There is one implementation, written against the Keras 3 API — the backend is chosen at
install and run time, not by a separate code path.

## Status

No model code yet. The installation instructions above describe how the package *will* be
used once the implementation lands; today `tcn_ae` exposes only `__version__`.

See the [API reference](reference.md) for what is currently available.
