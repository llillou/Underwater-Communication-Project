# Underwater Acoustic BPSK Communication System

This repository contains a Python simulation of a digital communication link designed for underwater environments, focusing on BPSK modulation and physical channel constraints.

## Project Description
Underwater communication is limited by frequency-dependent absorption and ambient noise. This study models a complete transceiver chain to analyze Bit Error Rate (BER) performance under varying SNR and distance conditions.

## Technical Specifications
* **Modulation:** Binary Phase Shift Keying (BPSK)
* **Carrier Frequency:** 15 kHz
* **Sampling Rate:** 100 kHz
* **Channel Model:** Thorp’s Absorption Formula
* **Receiver Type:** Coherent Correlation Receiver

## Implementation Details
1. **Transmitter:** Converts digital bits into phase-modulated (BPSK) acoustic signals.
2. **Channel:** Simulates signal attenuation based on Thorp’s model and adds AWGN to represent sea state noise.
3. **Receiver:** Recovers the original data by multiplying the signal with a local carrier reference and integrating over bit duration.

## Usage
Ensure `numpy` and `matplotlib` are installed, then run:
```bash
python main.py
