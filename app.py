import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# 페이지 제목
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>반도체 시뮬레이터</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>MOSFET 및 BJT의 동작 특성을 시뮬레이션하고 3D 구조를 시각화합니다.</p>", unsafe_allow_html=True)

