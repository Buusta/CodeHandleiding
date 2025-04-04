# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 17:08:16 2025

@author: jarno
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Werklocatie instellen
os.chdir("C:/Users/jarno/")

# CSV-bestand inlezen
bestand = "pid_log.csv"
data = pd.read_csv(bestand)

# Controleren of de benodigde kolommen aanwezig zijn
required_columns = ["time", "error", "integral", "derivative", "output"]
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"CSV-bestand mist de kolom: {col}")

# Subplots maken
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 12), sharex=True)

# Grafiek voor Error
axes[0].plot(data["time"], data["error"], label="Error", linestyle="-", marker="o", color="r")
axes[0].set_ylabel("Error")
axes[0].legend()
axes[0].grid()

# Grafiek voor Integral
axes[1].plot(data["time"], data["integral"], label="Integral", linestyle="--", color="g")
axes[1].set_ylabel("Integral")
axes[1].legend()
axes[1].grid()

# Grafiek voor Derivative
axes[2].plot(data["time"], data["derivative"], label="Derivative", linestyle="-.", color="b")
axes[2].set_ylabel("Derivative")
axes[2].legend()
axes[2].grid()

# Grafiek voor Output
axes[3].plot(data["time"], data["output"], label="Output", linestyle=":", color="m")
axes[3].set_xlabel("Tijd (s)")
axes[3].set_ylabel("Output")
axes[3].legend()
axes[3].grid()

# Titel toevoegen
fig.suptitle("PID Response Over Tijd", fontsize=14)

# Ruimte tussen grafieken optimaliseren
plt.tight_layout()
plt.show()
