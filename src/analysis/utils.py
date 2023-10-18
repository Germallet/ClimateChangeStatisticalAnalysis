import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/"

def read_csv(filename):
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    return df

def plot(x_values, y_values, x_label, y_label, title, filename, periods = 10):
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values)
    plt.xlabel(x_label)
    plt.xticks(rotation=45)
    plt.ylabel(y_label)
    plt.title(title)
    if isinstance(x_values, np.ndarray):
        plt.xticks(np.linspace(x_values.min(), x_values.max(), periods))
    elif isinstance(x_values, pd.DatetimeIndex):
        plt.xticks(pd.date_range(start=x_values.min(), end=x_values.max(), periods=periods))
    else:
        plt.xticks(np.arange(0, x_values.size, np.floor(x_values.size/periods)))
    plt.xlim(x_values.min(), x_values.max())
    plt.grid(True)
    plt.savefig(os.path.join(IMG_DIR, f"{filename}.png"))
    plt.show()

def plot_ft(y_values, x_label, y_label, title, filename, periods = 10):
    fft = np.fft.fft(y_values)
    frequencies = np.fft.fftfreq(len(fft))
    plot(frequencies[frequencies > 0], np.abs(fft[frequencies > 0]), x_label, y_label, title, filename, periods)

def plot_all(x_values, y_values, x_label, y_label, title, filename, periods = 10):
    plot(x_values, y_values, x_label, y_label, title, filename, periods)
    plot_ft(y_values, "Frequency", "Amplitude", f"{title} (FT)", f"{filename} FT")
