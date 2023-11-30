import numpy as np
import pandas as pd  # Import pandas for handling Excel files

def calculate_noise(data):
    noise = np.std(data)
    return noise

def calculate_snr_db(low_data, high_data):
    means = []
    stds = []
    means.append(np.mean(low_data))
    means.append(np.mean(high_data))
    print(means)

    stds.append(np.std(low_data))  
    stds.append(np.std(high_data))
    print(stds)
    
    snr = np.ptp(means) / np.ptp(stds)
    snr_db  = np.log10(snr) * 20

    return snr_db

# User input for the Excel file name
file_name = input("Enter the name of the .xlsx file: ") + (".xlsx")

# # Read the Excel file
# df = pd.read_excel(file_name, header=None)
# print(df)

# Read the Excel file
df = pd.read_excel(file_name)

# Extracting the signal data from column B
signal_data = df['y0000']

# Parsing the low and high data
low_data = signal_data[30:60]  # excel rows (B32:B61)  
high_data = signal_data[60:90]  # # excel rows (B62:B91) 

# Calculate SNR and SNR in dB
snr_db = calculate_snr_db(low_data, high_data)

print(f"SNR: {snr_db} dB")
