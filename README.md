
# Interactive Analog-to-Digital Signal Demo

This project provides an interactive interface to demonstrate the conversion of an analog signal to a digital one using:

- Sampling at 8000 Hz
- Quantization at variable bit depths (2–8 bits)
- Real signal data from a 20ms audio segment

## Files included

- `interactive_signal_app.py` – Main Streamlit application
- `signal_original_20ms.csv` – Full resolution signal data
- `signal_échantillonné_quantifié_8000Hz.csv` – Sampled and quantized signal data
- `requirements.txt` – Dependencies for Streamlit Cloud
- `README.md` – Documentation

## How to deploy

1. Fork or upload the files to your own GitHub repo
2. Go to https://streamlit.io/cloud and click "New App"
3. Select your repository and set the app file as: `interactive_signal_app.py`
4. Click Deploy and your app will be live within seconds
