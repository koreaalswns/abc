import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# MOSFET 3D 시뮬레이터
st.markdown("<h1 style='text-align: center; color: #000000;'>MOSFET 시뮬레이터</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Vt = 1V, T = 300K</h2>", unsafe_allow_html=True)

st.sidebar.header("⚙️ MOSFET 파라미터")
st.sidebar.markdown("---")
W = st.sidebar.slider("채널 폭 (W) [µm]", 0.1, 20.0, 1000.0, step=0.5)
L = st.sidebar.slider("채널 길이 (L) [µm]", 0.01, 20.0, 10.0, step=0.5)
Vgs = st.sidebar.slider("Gate-Source Voltage (Vgs) [V]", 0.0, 5.0, 1.5, step=0.1)

N_A = st.sidebar.slider(
"p형 도핑 농도 (cm^-3)", 
min_value=1e15, max_value=1e17, value=1e16, format="%.1e"
)

# 특정 n형 도핑 농도 선택
N_D_selected = st.sidebar.slider(
"n형 도핑 농도 (cm^-3)", 
min_value=1e13, max_value=1e20, value=1e19, format="%.1e"
)
T = 300
Vds_values = np.linspace(0, 5, 100)

# 도핑 농도 및 온도 범위 생성
N_D_values = np.logspace(np.log10(1e13), np.log10(1e20), 100)



# 이동도 계산 함수
def calculate_mobility_sic(N_D, N_A, T, mu_1_e=950, mu_0_e=950, mu_1_h=120, mu_0_h=120, 
                        N_ref=1e17, alpha_e=2.5, alpha_h=2.1, gamma=1.5):
    """
    SiC의 전자 및 정공 이동도 계산 함수.

    Parameters:
    - N_D: n형 도핑 농도 (cm^-3)
    - N_A: p형 도핑 농도 (cm^-3)
    - T: 온도 (K)
    - mu_1_e: 전자 격자 이동도 상수 (cm^2/V·s)
    - mu_0_e: 전자 최대 이동도 (cm^2/V·s)
    - mu_1_h: 정공 격자 이동도 상수 (cm^2/V·s)
    - mu_0_h: 정공 최대 이동도 (cm^2/V·s)
    - N_ref: 불순물 산란 기준 농도 (cm^-3)
    - alpha_e: 전자 격자 산란 온도 계수
    - alpha_h: 정공 격자 산란 온도 계수
    - gamma: 불순물 산란 계수

    Returns:
    - 전자 이동도 (μ_e)와 정공 이동도 (μ_h)
    """
    N_total = N_D + N_A  # 총 도핑 농도

    # 전자 이동도 계산
    mu_lattice_e = mu_1_e * (T / 300) ** (-alpha_e)
    mu_impurity_e = mu_0_e / (1 + (N_total / N_ref) ** gamma)
    mu_e = 1 / (1 / mu_lattice_e + 1 / mu_impurity_e)

    # 정공 이동도 계산
    mu_lattice_h = mu_1_h * (T / 300) ** (-alpha_h)
    mu_impurity_h = mu_0_h / (1 + (N_total / N_ref) ** gamma)
    mu_h = 1 / (1 / mu_lattice_h + 1 / mu_impurity_h)

    return mu_e, mu_h

# 효과적인 이동도 계산 함수 (전자의 이동도와 정공의 이동도를 이용)
def effective_mobility(mu_e, mu_h):
    """
    전자 이동도(mu_e)와 정공 이동도(mu_h)를 입력받아,
    효과적인 이동도(mu_eff)를 계산하는 함수.
    """
    mu_eff = (mu_e * mu_h) / (mu_e + mu_h)
    return mu_eff


    
# 선택된 n형 도핑 농도에서의 전자 및 정공 이동도 계산
mu_e_selected, mu_h_selected = calculate_mobility_sic(N_D_selected, N_A, T)

# 효과적인 이동도 계산
mu_eff_selected = effective_mobility(mu_e_selected, mu_h_selected)

# 드레인 전류 계산 함수
def calculate_id(Vgs, Vds, W, L, N_D, N_A):
    Cox = 2.3e-8  # 산화막 캐패시턴스 (F/cm^2)
    W_cm = W * 1e-4  # µm to cm
    L_cm = L * 1e-4  # µm to cm
    mu_eff = mu_eff_selected  # 이동도에 농도 영향을 반영
    if Vgs < 1.0:  # 임계 전압 Vth
        return 0
    elif Vds < Vgs - 1.0:
        return mu_eff * Cox * (W_cm / L_cm) * ((Vgs - 1.0) * Vds - (Vds ** 2) / 2)
    else:
        return 0.5 * mu_eff * Cox * (W_cm / L_cm) * (Vgs - 1.0) ** 2



# 드레인 전류 계산 및 그래프 생성
Id_values = [calculate_id(Vgs, Vds, W, L, N_D_selected, N_A) for Vds in Vds_values]

fig, ax = plt.subplots()
ax.plot(Vds_values, Id_values, label=f"Vgs = {Vgs} V, W = {W:.1f} µm, L = {L:.1f} µm")
ax.set_xlabel("Drain-Source Voltage (Vds) [V]")
ax.set_ylabel("Drain Current (Id) [A]")
ax.set_title("MOSFET Output Characteristics")
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend()
st.pyplot(fig)
