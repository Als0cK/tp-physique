import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def lire_csv_oscilloscope(file_path):
    # Lire les 18 premières lignes du fichier pour extraire les paramètres de l'oscilloscope
    with open(file_path, 'r') as file:
        params = {}
        for i in range(18):
            line = file.readline().strip()
            key_value = line.split(',')
            if len(key_value) >= 2:
                params[key_value[0].strip()] = key_value[1].strip()
    
    # Charger le reste du fichier CSV à partir de la 19e ligne pour les données de temps et de tension
    data = pd.read_csv(file_path, skiprows=18)
    
    # Extraction du temps (colonne 4) et de la tension (colonne 5)
    time_data = pd.to_numeric(data.iloc[:, 3], errors='coerce')  # Colonne 4
    voltage_data = pd.to_numeric(data.iloc[:, 4], errors='coerce')  # Colonne 5

    # Supprimer les lignes contenant des valeurs NaN
    valid_data = pd.DataFrame({'Time (s)': time_data, 'Voltage (V)': voltage_data}).dropna()

    return params, valid_data

def visualiser_et_mesurer(signal_data):
    # Visualisation du signal
    plt.figure(figsize=(10, 6))
    plt.plot(signal_data['Time (s)'], signal_data['Voltage (V)'], label='Tension aux bornes du GBF')
    plt.title("Signal du GBF")
    plt.xlabel("Temps (s)")
    plt.ylabel("Tension (V)")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Mesures de tension
    amplitude_max = signal_data['Voltage (V)'].max()
    amplitude_min = signal_data['Voltage (V)'].min()
    
    # Identification des périodes (temps entre deux pics successifs)
    peak_threshold = amplitude_max * 0.9  # On fixe un seuil pour détecter les pics
    peaks = signal_data[signal_data['Voltage (V)'] >= peak_threshold]
    
    # Calcul des différences de temps entre les pics (période)
    peak_times = peaks['Time (s)'].values
    period_diffs = np.diff(peak_times)
    if len(period_diffs) > 0:
        period = np.mean(period_diffs)
        frequency = 1 / period if period > 0 else None
    else:
        period = None
        frequency = None
    
    # Affichage des mesures
    print(f"Amplitude maximale: {amplitude_max:.3f} V")
    print(f"Amplitude minimale: {amplitude_min:.3f} V")
    if period is not None:
        print(f"Période moyenne: {period:.6f} s")
        print(f"Fréquence: {frequency:.3f} Hz")
    else:
        print("Impossible de calculer la période et la fréquence.")

# Utilisation des fonctions
file_path = "D:\TP\ALL0000\F0000CH1.CSV"  # Chemin vers le fichier
params, signal_data = lire_csv_oscilloscope(file_path)

# Affichage des paramètres de l'oscilloscope
print("Paramètres de l'oscilloscope :")
for key, value in params.items():
    print(f"{key}: {value}")

# Visualisation et mesures sur les données de signal
visualiser_et_mesurer(signal_data)
