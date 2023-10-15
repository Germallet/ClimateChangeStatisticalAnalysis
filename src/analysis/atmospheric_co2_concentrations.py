import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/"

def read_csv(filename):
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    return df

def plot(x_values, y_values, x_label, y_label, title, path, filename):
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values)
    plt.xlabel(x_label)
    plt.xticks(rotation=45)
    plt.ylabel(y_label)
    plt.title(title)
    if isinstance(x_values, np.ndarray):
        plt.xticks(np.linspace(x_values.min(), x_values.max(), 10))
    else:
        plt.xticks(np.arange(0, x_values.size, np.floor(x_values.size/10)))
    plt.xlim(x_values.min(), x_values.max())
    plt.grid(True)
    plt.savefig(os.path.join(IMG_DIR, path, f"{filename}.png"))
    plt.show()

def plot_ft(y_values, x_label, y_label, title, path, filename):
    fft = np.fft.fft(y_values)
    frequencies = np.fft.fftfreq(len(fft))
    plot(frequencies[frequencies > 0], np.abs(fft[frequencies > 0]), x_label, y_label, title, path, filename)

def plot_all(x_values, y_values, x_label, y_label, title, path, filename):
    plot(x_values, y_values, x_label, y_label, title, path, filename)
    plot_ft(y_values, "Frequency", "Amplitude", f"{title} (FT)", path, f"{filename} FT")

df = read_csv("Atmospheric_CO₂_Concentrations.csv")
world_co2_concentrations = df.loc[(df["Country"] == "World") & (df["Unit"] == "Parts Per Million")]
plot_all(world_co2_concentrations["Date"], world_co2_concentrations["Value"], "Date", "CO₂ Parts Per Million", "World Atmospheric CO₂ Concentrations", "", "World CO2 Concentrations")
