import pandas as pd

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

# Utilisation de la fonction
file_path = 'D:\TP\ALL0000\F0000CH1.CSV'  # Chemin vers le fichier
params, signal_data = lire_csv_oscilloscope(file_path)

# Affichage des paramètres de l'oscilloscope
print("Paramètres de l'oscilloscope :")
for key, value in params.items():
    print(f"{key}: {value}")

# Affichage des premières lignes des données extraites
print("\nDonnées de signal (temps et tension) :")
print(signal_data.head())
