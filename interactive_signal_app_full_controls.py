
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import interp1d

st.set_page_config(layout="wide")
st.title("Analog to Digital Signal Conversion – Interactive Demo")

# Load original signal
@st.cache_data
def load_original():
    return pd.read_csv("signal_original_20ms.csv")

df_full = load_original()

# User input controls
sampling_rate = st.slider("Sampling Rate (Hz)", min_value=400, max_value=44100, value=8000, step=100)
bit_depth = st.slider("Quantization Bit Depth", min_value=2, max_value=8, value=8, step=1)

# Step 1 – Sampling
st.subheader("1. Sampling")
full_time = df_full["time"].to_numpy()
full_ampl = df_full["amplitude"].to_numpy()
duration = full_time[-1] - full_time[0]
num_samples = int(duration * sampling_rate)

sample_times = np.linspace(full_time[0], full_time[-1], num_samples)
interp_func = interp1d(full_time, full_ampl, kind='linear')
sampled_amplitudes = interp_func(sample_times)

fig_sampling = go.Figure()
fig_sampling.add_trace(go.Scatter(x=full_time, y=full_ampl,
                                  mode="lines", name="Original Signal", line=dict(color="lightgray")))
fig_sampling.add_trace(go.Scatter(x=sample_times, y=sampled_amplitudes,
                                  mode="markers", name=f"Sampled ({sampling_rate} Hz)", marker=dict(color="blue")))
fig_sampling.update_layout(title="Step 1: Sampling",
                           xaxis_title="Time (s)", yaxis_title="Amplitude", height=400)
st.plotly_chart(fig_sampling, use_container_width=True)

# Step 2 – Quantization
st.subheader("2. Quantization")
levels = np.linspace(-1, 1, 2 ** bit_depth)
quantized_amplitudes = [min(levels, key=lambda l: abs(val - l)) for val in sampled_amplitudes]

fig_quant = go.Figure()
fig_quant.add_trace(go.Scatter(x=sample_times, y=sampled_amplitudes,
                               mode="markers", name="Sampled", marker=dict(color="blue")))
fig_quant.add_trace(go.Scatter(x=sample_times, y=quantized_amplitudes,
                               mode="markers+lines", name=f"Quantized ({bit_depth} bits)",
                               marker=dict(color="green"), line=dict(color="green", shape="hv")))
fig_quant.update_layout(title="Step 2: Quantization",
                        xaxis_title="Time (s)", yaxis_title="Amplitude", height=400)
st.plotly_chart(fig_quant, use_container_width=True)

# Step 3 – Encoding
st.subheader("3. Encoding")
binary_codes = [format(levels.tolist().index(q), f'0{bit_depth}b') for q in quantized_amplitudes]

fig_encode = go.Figure()
fig_encode.add_trace(go.Scatter(x=sample_times, y=quantized_amplitudes,
                                mode="markers", name="Quantized", marker=dict(color="green")))
for i in range(0, len(sample_times), max(1, len(sample_times)//32)):
    fig_encode.add_annotation(x=sample_times[i], y=quantized_amplitudes[i] + 0.05,
                              text=binary_codes[i], showarrow=False, font=dict(size=9))

fig_encode.update_layout(title="Step 3: Binary Encoding",
                         xaxis_title="Time (s)", yaxis_title="Amplitude", height=400)
st.plotly_chart(fig_encode, use_container_width=True)
