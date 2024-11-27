import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# BJT 시뮬레이터

st.title("BJT Common-Base Configuration Simulator")

default_params = {
    "I_S": 1e-14,
    "V_T": 0.026,
    "V_CB_min": 0,
    "V_CB_max": 20,
    "I_E_min": 0.001,
    "I_E_max": 0.005
}


st.sidebar.header("Adjust Input Characteristics Parameters")
I_S = st.sidebar.slider("Saturation Current (I_S, pA)", 0.001, 1.0, default_params["I_S"], step=0.001)
V_T = st.sidebar.slider("Thermal Voltage (V_T, V)", 0.01, 0.05, default_params["V_T"], step=0.001)
V_CB_min = st.sidebar.slider("Min Collector-Base Voltage (V_CB, V)", 0, 20, default_params["V_CB_min"], step=1)
V_CB_max = st.sidebar.slider("Max Collector-Base Voltage (V_CB, V)", 0, 20, default_params["V_CB_max"], step=1)
I_E_min = st.sidebar.slider("Min Emitter Current (I_E, A)", 1e-4, 0.01, default_params["I_E_min"], step=1e-4, format="%.4f")
I_E_max = st.sidebar.slider("Max Emitter Current (I_E, A)", 1e-4, 0.01, default_params["I_E_max"], step=1e-4, format="%.4f")

col1, col2 = st.columns(2)

# Input Characteristics
with col1:
    st.subheader("Input Characteristics")
    fig, ax = plt.subplots()
    V_BE_values = np.linspace(0, 1, 200)
    V_CB_values = np.linspace(V_CB_min, V_CB_max, 3)

    for V_CB in V_CB_values:
        I_E_values = I_S * 1e-12 * (np.exp(V_BE_values / V_T) - 1) * (1 + V_CB / (V_CB + V_T))
        ax.plot(V_BE_values, I_E_values * 1e3, label=f"V_CB = {V_CB:.1f} V")

    ax.set_xlabel("V_BE (V)")
    ax.set_ylabel("I_E (mA)")
    ax.set_title("V_BE - I_E Curve")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# Output Characteristics
with col2:
    st.subheader("Output Characteristics")
    fig, ax = plt.subplots()
    V_CB_values = np.linspace(0, 10, 200)
    I_E_values = np.linspace(I_E_min, I_E_max, 3)

    for I_E in I_E_values:
        I_C_values = I_E * (1 - np.exp(-V_CB_values / V_T))
        ax.plot(V_CB_values, I_C_values * 1e3, label=f"I_E = {I_E * 1e3:.1f} mA")

    ax.set_xlabel("V_CB (V)")
    ax.set_ylabel("I_C (mA)")
    ax.set_title("V_CB - I_C Curve")
    ax.legend()
    ax.grid()
    st.pyplot(fig)