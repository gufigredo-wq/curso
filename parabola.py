import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configurações da página
st.set_page_config(page_title="Plotador de Funções", layout="centered")

st.title("📈 Plotador de Função de Primeiro Grau")
st.markdown("Visualize a equação $y = ax + b$ de forma interativa.")

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("Parâmetros da Função")
a = st.sidebar.number_input("Digite o valor de 'a' (angular):", value=1.0, step=0.5)
b = st.sidebar.number_index = st.sidebar.number_input("Digite o valor de 'b' (linear):", value=0.0, step=0.5)

# --- LÓGICA DO GRÁFICO ---
# Gera pontos para o eixo x
x = np.linspace(-10, 10, 400) 

# Calcula os valores de y
y = a * x + b

# Criação da figura Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, label=f'y = {a}x + {b}', color='dodgerblue', linewidth=2)

# Detalhes do gráfico
ax.set_title('Gráfico da Função de Primeiro Grau', fontsize=15)
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.grid(True, linestyle='--', alpha=0.7)
ax.axhline(0, color='black', linewidth=1) # Eixo X
ax.axvline(0, color='black', linewidth=1) # Eixo Y
ax.legend()

# --- EXIBIÇÃO NO STREAMLIT ---
st.pyplot(fig)

# Exibe a equação formatada
st.info(f"**Equação atual:** $y = {a}x + ({b})$")
