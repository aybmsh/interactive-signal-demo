
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
st.title("Analog to Digital Signal Conversion – Full Interactive Demo")

# Load data
@st.cache_data
def load_csv(filename):
    return pd.read_csv(filename)

df_full = load_csv("signal_original_20ms.csv")
df_sampled = load_csv("signal_échantillonné_quantifié_8000Hz.csv")

bit_depth = st.slider("Bit Depth", 2, 8, 8)
levels = np.linspace(-1, 1, 2 ** bit_depth)
step_size = 2 / (2 ** bit_depth)

quantized_y = [min(levels, key=lambda l: abs(l - val)) for val in df_sampled["amplitude_sampled"]]
binary_codes = [format(levels.tolist().index(q), f'0{bit_depth}b') for q in quantized_y]

# --- Sampling stage ---
st.subheader("1. Sampling")
fig_sampling = go.Figure()
fig_sampling.add_trace(go.Scatter(x=df_full["time"], y=df_full["amplitude"],
                                  mode="lines", name="Original Signal", line=dict(color="lightgray")))
fig_sampling.add_trace(go.Scatter(x=df_sampled["sample_time"], y=df_sampled["amplitude_sampled"],
                                  mode="markers", name="Sampled Points", marker=dict(color="blue")))
fig_sampling.update_layout(title="Step 1: Sampling at 8000 Hz",
                           xaxis_title="Time (s)", yaxis_title="Amplitude", height=400)
st.plotly_chart(fig_sampling, use_container_width=True)

# --- Quantization stage ---
st.subheader("2. Quantization")
fig_quant = go.Figure()
fig_quant.add_trace(go.Scatter(x=df_full["time"], y=df_full["amplitude"],
                               mode="lines", name="Original Signal", line=dict(color="lightgray")))
fig_quant.add_trace(go.Scatter(x=df_sampled["sample_time"], y=quantized_y,
                               mode="markers+lines", name="Quantized Signal",
                               marker=dict(color="green"), line=dict(color="green", shape="hv")))
fig_quant.update_layout(title=f"Step 2: Quantization with {bit_depth} bits ({2**bit_depth} levels)",
                        xaxis_title="Time (s)", yaxis_title="Amplitude", height=400)
st.plotly_chart(fig_quant, use_container_width=True)

# --- Encoding stage ---
st.subheader("3. Encoding")
fig_encode = go.Figure()
fig_encode.add_trace(go.Scatter(x=df_sampled["sample_time"], y=quantized_y,
                                mode="markers", name="Quantized Values", marker=dict(color="green")))
for i in range(0, len(df_sampled), max(1, len(df_sampled)//32)):  # label only a few to keep it readable
    fig_encode.add_annotation(x=df_sampled["sample_time"][i],
                              y=quantized_y[i] + 0.05,
                              text=binary_codes[i],
                              showarrow=False,
                              font=dict(size=9), align="center")
fig_encode.update_layout(title="Step 3: Binary Encoding of Quantized Values",
                         xaxis_title="Time (s)", yaxis_title="Amplitude", height=400)
st.plotly_chart(fig_encode, use_container_width=True)

