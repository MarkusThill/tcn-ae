# tcn-ae

A temporal convolutional autoencoder (TCN-AE) for unsupervised anomaly detection in
multivariate time series.

This package provides a reference implementation of the algorithm described in:

> Markus Thill, Wolfgang Konen, Hao Wang, Thomas Bäck.
> *Temporal convolutional autoencoder for unsupervised anomaly detection in time series.*
> Applied Soft Computing, 2021.

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

Early development. The public API is not yet stable.

See the [API reference](reference.md) for what is currently available.
