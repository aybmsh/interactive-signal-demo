
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
st.title("Interactive Analog to Digital Signal Demo")

# Upload or use default CSVs
st.sidebar.title("Upload CSV Data")
full_signal_file = st.sidebar.file_uploader("Signal original (CSV)", type="csv")
sampled_signal_file = st.sidebar.file_uploader("Signal échantillonné (CSV)", type="csv")

@st.cache_data
def load_csv(file):
    df = pd.read_csv(file)
    return df

if full_signal_file and sampled_signal_file:
    df_full = load_csv(full_signal_file)
    df_sampled = load_csv(sampled_signal_file)

    bit_depth = st.slider("Bit Depth", min_value=2, max_value=8, value=8, step=1)
    step_size = 2 / (2 ** bit_depth)
    levels = np.linspace(-1, 1, 2 ** bit_depth)

    # Apply quantization
    quantized_y = [min(levels, key=lambda l: abs(l - val)) for val in df_sampled["amplitude_sampled"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_full["time"], y=df_full["amplitude"],
                             mode="lines", name="Signal original", line=dict(color="lightgray")))
    fig.add_trace(go.Scatter(x=df_sampled["sample_time"], y=df_sampled["amplitude_sampled"],
                             mode="markers", name="Signal échantillonné", marker=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df_sampled["sample_time"], y=quantized_y,
                             mode="lines+markers", name=f"Signal quantifié ({bit_depth} bits)",
                             line=dict(shape="hv", color="green"), marker=dict(color="green")))

    fig.update_layout(title="Conversion Analogique vers Numérique",
                      xaxis_title="Temps (s)", yaxis_title="Amplitude",
                      yaxis=dict(range=[-1.1, 1.1]), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Téléversez les deux fichiers CSV pour commencer.")
