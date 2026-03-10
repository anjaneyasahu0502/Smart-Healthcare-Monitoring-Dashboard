import wfdb
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

record_path = r"E:\6th sem\fog\project\dataset\100"
record = wfdb.rdrecord(record_path)

signal = record.p_signal[:,0]
fs = record.fs

peaks,_ = find_peaks(signal, distance=fs*0.6)

rr = np.diff(peaks) / fs
hr = 60 / rr
hr = hr[(hr>40)&(hr<180)]

# Desired dataset size
n = 2000

# Sample HR values from ECG-derived heart rates
hr_samples = np.random.choice(hr, n)

# Generate realistic variations
spo2 = np.random.normal(97, 1.2, n)
spo2 = np.clip(spo2, 90, 100)

temp = np.random.normal(36.8, 0.4, n)
temp = np.clip(temp, 35.8, 39.5)

acc = np.random.normal(1.2, 0.3, n)

# Simulate occasional fall / motion spikes
spike_indices = np.random.choice(n, size=int(n*0.15), replace=False)
acc[spike_indices] = np.random.uniform(20,25,len(spike_indices))

# Simulate tachycardia events
hr_spike_indices = np.random.choice(n, size=int(n*0.1), replace=False)
hr_samples[hr_spike_indices] = np.random.uniform(145,180,len(hr_spike_indices))

df = pd.DataFrame({
    "hr": np.round(hr_samples,1),
    "spo2": np.round(spo2,1),
    "temp": np.round(temp,1),
    "acc_mag": np.round(acc,2)
})

df.to_csv("mitbih_hr.csv", index=False)

print("Dataset generated with", n, "samples")