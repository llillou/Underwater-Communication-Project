# ============================================================
# PROJECT: Underwater Acoustic Communication Simulation
# ENVIRONMENT: Shallow Water, 2km Range, 15kHz Carrier
# MODEL: Thorp Absorption & Practical Spreading (k=1.5)
# MODULATION: Binary Phase Shift Keying (BPSK)
# ============================================================
import numpy as np
import matplotlib.pyplot as plt


fs = 100000
fc = 15000
bit_rate = 5000
num_bits = 50
t_bit = np.arange(0, 1/bit_rate, 1/fs)


bits = np.random.randint(0, 2, num_bits)
print(f"Original Bits (First 10): {bits[:10]}")
tx_signal = np.array([])

for bit in bits:

    phase = 0 if bit == 1 else np.pi
    wave = np.sin(2 * np.pi * fc * t_bit + phase)
    tx_signal = np.concatenate([tx_signal, wave])


plt.figure(figsize=(12, 4))
plt.plot(tx_signal[:500])
plt.title("Transmitted BPSK Signal (Phase 2: Perfect)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

print(f"Generated {num_bits} bits. Ready for the ocean!")

distance_km = 5.0
k = 1.5


f_khz = fc / 1000
f2 = f_khz**2
alpha = (0.11 * (f2 / (1 + f2)) + 44 * (f2 / (4100 + f2)) + 0.000275 * f2 + 0.003)


path_loss_db = (10 * k * np.log10(distance_km * 1000)) + (alpha * distance_km)
gain = 10**(-path_loss_db / 20)


rx_weak = tx_signal * gain


snr_db = 0
sig_pwr = np.mean(rx_weak**2)
noise_pwr = sig_pwr / (10**(snr_db / 10))
noise = np.sqrt(noise_pwr) * np.random.randn(len(rx_weak))


rx_signal = rx_weak + noise


plt.figure(figsize=(12, 4))
plt.plot(rx_signal[:500], color='red')
plt.title(f"Received Signal (Phase 3: After 2km in the Ocean)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

received_bits = []


for i in range(num_bits):

    start = i * len(t_bit)
    end = (i + 1) * len(t_bit)
    bit_segment = rx_signal[start:end]



    clean_reference = np.sin(2 * np.pi * fc * t_bit)
    decision_variable = np.sum(bit_segment * clean_reference)


    if decision_variable > 0:
        received_bits.append(1)
    else:
        received_bits.append(0)

received_bits = np.array(received_bits)


errors = np.sum(bits != received_bits)
ber = errors / num_bits

print("-" * 30)
print(f"Original Bits (First 10): {bits[:10]}")
print(f"Received Bits (First 10): {received_bits[:10]}")
print(f"Total Errors: {errors} out of {num_bits}")
print(f"Bit Error Rate (BER): {ber * 100}%")
print("-" * 30)

print("\n" + "="*50)
print("       UNDERWATER LINK ANALYSIS REPORT")
print("="*50)
results_table = [
    ["Parameter", "Value", "Description"],
    ["-"*15, "-"*15, "-"*20],
    ["Carrier Freq", f"{fc/1000} kHz", "Transmission Pitch"],
    ["Distance", f"{distance_km} km", "Range through water"],
    ["SNR", f"{snr_db} dB", "Signal-to-Noise Ratio"],
    ["Bit Rate", f"{bit_rate} bps", "Data Speed"],
    ["Path Loss", f"{path_loss_db:.2f} dB", "Energy 'eaten' by Ocean"],
    ["Final BER", f"{ber:.2f}%", "Percentage of Errors"]
]

for row in results_table:
    print(f"{row[0]:<18} | {row[1]:<15} | {row[2]}")

print("="*50)


if ber == 0:
    print("ANALYSIS: Link is stable and perfect.")
elif ber < 10:
    print("ANALYSIS: Realistic link. Minor noise interference.")
else:
    print("ANALYSIS: Link Failure. Noise/Distance too high for BPSK.")
print("="*50)