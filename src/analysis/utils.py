import matplotlib as mp
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from typing import Optional

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/"


def read_csv(filename):
    return pd.read_csv(os.path.join(DATA_DIR, filename))


def dataframe_year_filter(dataframe: pd.DataFrame, from_year: Optional[int] = None, to_year: Optional[int] = None):
    filtered_df = dataframe.copy()
    if from_year is not None:
        filtered_df = filtered_df[filtered_df.index >= f"{from_year}-01"]
    if to_year is not None:
        filtered_df = filtered_df[filtered_df.index < f"{to_year}-01"]
    return filtered_df


def dataframe_date_filter(dataframe: pd.DataFrame, from_date: Optional[pd.Timestamp] = None, to_date: Optional[pd.Timestamp] = None):
    filtered_df = dataframe.copy()
    if from_date is not None:
        filtered_df = filtered_df[filtered_df.index >= from_date]
    if to_date is not None:
        filtered_df = filtered_df[filtered_df.index <= to_date]
    return filtered_df


def matching_period_dataframes(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame):
    from_date = max(dataframe1.index.min(), dataframe2.index.min())
    to_date = min(dataframe1.index.max(), dataframe2.index.max())
    return dataframe_date_filter(dataframe1, from_date, to_date), dataframe_date_filter(dataframe2, from_date, to_date)


def set_fig_style(fig):
    font_size = 20
    font_color = "black"
    mp.rcParams['ytick.color'] = font_color
    mp.rcParams['xtick.color'] = font_color
    mp.rcParams['axes.labelcolor'] = font_color
    mp.rcParams['axes.edgecolor'] = font_color
    mp.rcParams['font.size'] = font_size
    mp.rcParams['lines.linewidth'] = font_size / 4.
    plt.xticks(rotation=45)
    

def plot(x_values, y_values, x_label, y_label, title, filename, periods=10):
    fig = plt.figure(figsize=(12, 14))
    set_fig_style(fig)
    plt.plot(x_values, y_values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if isinstance(x_values, np.ndarray):
        plt.xticks(np.linspace(x_values.min(), x_values.max(), periods))
    elif isinstance(x_values, pd.DatetimeIndex):
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%Y'))
        plt.xticks(pd.date_range(start=x_values.min(),
                   end=x_values.max(), periods=periods))
    else:
        plt.xticks(np.arange(x_values.min(), x_values.max(),
                   np.floor(x_values.size/periods)))
    plt.xlim(x_values.min(), x_values.max())
    plt.grid(True)
    fig.canvas.manager.set_window_title(title)
    plt.savefig(os.path.join(IMG_DIR, f"{filename}.png"), transparent=True)
    plt.show()


def plot_ft(y_values, x_label, y_label, title, filename, periods=10):
    fft = np.fft.fft(y_values)
    frequencies = np.fft.fftfreq(len(fft))
    plot(frequencies[frequencies > 0], np.abs(
        fft[frequencies > 0]), x_label, y_label, title, filename, periods)


def plot_all(x_values, y_values, x_label, y_label, title, filename, periods=10):
    plot(x_values, y_values, x_label, y_label, title, filename, periods)
    plot_ft(y_values, "Frequency", "Amplitude",
            f"{title} (FT)", f"{filename} FT")
