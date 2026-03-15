"""
Underwater Acoustic Communication Simulator
Author: Lara Dogan
Description: BPSK modulation performance over underwater channels
using the Thorp attenuation model and AWGN.
"""
import numpy as np
import matplotlib.pyplot as plt


fs = 100000
fc = 15000
bit_rate = 5000
num_bits_demo = 5000
num_bits_ber = 1000
k = 1.5


def calculate_thorp(f_hz):

    f_khz = f_hz / 1000
    f2 = f_khz ** 2
    return (0.11 * (f2 / (1 + f2)) + 44 * (f2 / (4100 + f2)) + 0.000275 * f2 + 0.003)


def run_detailed_report(dist_km=5.0, snr_db=0, report_title="ACOUSTIC LINK ANALYSIS"):

    print(f"\n--- RUNNING ANALYSIS: {dist_km}km at {snr_db}dB SNR ---")
    alpha = calculate_thorp(fc)


    path_loss_db = (10 * k * np.log10(dist_km * 1000)) + (alpha * dist_km)
    gain = 10 ** (-path_loss_db / 20)


    bits = np.random.randint(0, 2, num_bits_demo)
    t_bit = np.arange(0, 1 / bit_rate, 1 / fs)

    tx_signal = []
    for bit in bits:
        phase = 0 if bit == 1 else np.pi
        tx_signal.extend(np.sin(2 * np.pi * fc * t_bit + phase))
    tx_signal = np.array(tx_signal)


    rx_weak = tx_signal * gain
    sig_pwr = np.mean(rx_weak ** 2)
    noise_pwr = sig_pwr / (10 ** (snr_db / 10))
    rx_signal = rx_weak + np.sqrt(noise_pwr) * np.random.randn(len(rx_weak))


    received_bits = []
    samples_per_bit = len(t_bit)
    ref = np.sin(2 * np.pi * fc * t_bit)
    for i in range(num_bits_demo):
        seg = rx_signal[i * samples_per_bit: (i + 1) * samples_per_bit]
        received_bits.append(1 if np.sum(seg * ref) > 0 else 0)

    received_bits = np.array(received_bits)
    errors = np.sum(bits != received_bits)
    ber = (errors / num_bits_demo) * 100

    print("\n" + "-" * 30)
    print("  COMMUNICATION LINK METRICS")
    print("-" * 30)
    print(f"  Distance        : {dist_km} km")
    print(f"  Channel SNR     : {snr_db} dB")
    print(f"  Data Rate       : {bit_rate} bps")
    print(f"  Path Loss       : {path_loss_db:.2f} dB")
    print(f"  Calculated BER  : {ber:.4f}%")
    print("-" * 30)
    # -------------------------



    plt.figure(figsize=(12, 7))
    plt.clf()


    plt.subplot(2, 1, 1)
    plt.plot(tx_signal[:500])
    plt.title("Transmitted Signal (First 5 Bits) - " + str(report_title))
    plt.grid(True, alpha=0.3)


    plt.subplot(2, 1, 2)

    bit_count_for_visualization = 5
    start_sample = 0
    end_sample = samples_per_bit * bit_count_for_visualization

    plt.plot(rx_signal[start_sample:end_sample], color='red', alpha=0.8)
    dynamic_label = "Received Signal (Dist: " + str(dist_km) + "km, SNR: " + str(snr_db) + "dB)"
    plt.title(dynamic_label)
    plt.xlabel("Samples")
    plt.grid(True, alpha=0.3)


    if snr_db > 5:
        plt.ylim([-gain * 2.5, gain * 2.5])

    plt.tight_layout()

    filename = f"figures/received_signal_{dist_km}km_{snr_db}dB.png"
    plt.savefig(filename, dpi=300)
    print(f"Görsel kaydedildi: {filename}")
    plt.show()


def run_ber_comparisons():

    print("\n--- GENERATING PERFORMANCE CURVES ---")
    snr_range = np.arange(-5, 16, 2)
    distances = [1.0, 3.0, 5.0]

    plt.figure(figsize=(10, 6))
    for d in distances:
        alpha = calculate_thorp(fc)
        path_loss = (10 * k * np.log10(d * 1000)) + (alpha * d)
        gain = 10 ** (-path_loss / 20)

        ber_list = []
        for snr in snr_range:
            bits = np.random.randint(0, 2, num_bits_ber)
            t_bit = np.arange(0, 1 / bit_rate, 1 / fs)

            tx = []
            for b in bits:
                tx.extend(np.sin(2 * np.pi * fc * t_bit + (0 if b == 1 else np.pi)))
            tx = np.array(tx) * gain

            spwr = np.mean(tx ** 2)
            npwr = spwr / (10 ** (snr / 10))
            rx = tx + np.sqrt(npwr) * np.random.randn(len(tx))

            ref = np.sin(2 * np.pi * fc * t_bit)
            received = []
            for i in range(num_bits_ber):
                seg = rx[i * len(t_bit): (i + 1) * len(t_bit)]
                received.append(1 if np.sum(seg * ref) > 0 else 0)

            err = np.sum(bits != np.array(received))
            ber_list.append(err / num_bits_ber)

        plt.semilogy(snr_range, ber_list, 'o-', label=f'Distance: {d}km')

    plt.title("BER Performance vs SNR (Distance Comparison)")
    plt.xlabel("SNR (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig("figures/ber_waterfall_comparison.png", dpi=300)
    print("BER Waterfall grafiği kaydedildi: figures/ber_waterfall_comparison.png")
    plt.show()


if __name__ == "__main__":

    run_detailed_report(dist_km=12,snr_db=-10)




    run_ber_comparisons()