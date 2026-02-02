import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Plotador Universal", layout="wide", page_icon="📈")

st.title("🧮 Plotador de Funções Matemáticas Avançado")
st.markdown("""
Digite qualquer equação matemática usando **x** como variável.
Exemplos: `x**2`, `sin(x)`, `exp(x)`, `log(x)`, `x**3 - 2*x + 1`
""")

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Configurações do Gráfico")

# 1. Entrada da Função
st.sidebar.subheader("1. Equação")
raw_equation = st.sidebar.text_input("Digite f(x):", value="sin(x) * x")

# 2. Intervalo do Eixo X
st.sidebar.subheader("2. Domínio (Eixo X)")
col1, col2 = st.sidebar.columns(2)
x_min = col1.number_input("Mínimo", value=-10.0, step=1.0)
x_max = col2.number_input("Máximo", value=10.0, step=1.0)
num_points = st.sidebar.slider("Resolução (nº pontos)", 100, 2000, 500)

# 3. Intervalo do Eixo Y (Opcional)
st.sidebar.subheader("3. Imagem (Eixo Y)")
use_ylim = st.sidebar.checkbox("Limitar Eixo Y manually?")
y_lim = (None, None)
if use_ylim:
    y_min_val = st.sidebar.number_input("Y Mínimo", value=-5.0)
    y_max_val = st.sidebar.number_input("Y Máximo", value=5.0)
    y_lim = (y_min_val, y_max_val)

# 4. Estilização Visual
st.sidebar.subheader("4. Estilo")
plot_color = st.sidebar.color_picker("Cor da linha", "#1f77b4")
line_style = st.sidebar.selectbox("Estilo da linha", ["-", "--", "-.", ":"])
show_grid = st.sidebar.checkbox("Mostrar Grade", value=True)
theme_style = st.sidebar.selectbox("Tema do Matplotlib", plt.style.available, index=plt.style.available.index('seaborn-v0_8-darkgrid'))

# --- LÓGICA DE PROCESSAMENTO (SYMPY) ---
def process_function(equation_str, x_range):
    """Converte string em função numérica e calcula Y."""
    try:
        # Prepara a string (substitui ^ por ** para potências se usuário esquecer)
        equation_str = equation_str.replace('^', '**')
        
        # Define o símbolo matemático
        x_sym = sp.symbols('x')
        
        # Converte string para expressão simbólica
        expr = sp.sympify(equation_str)
        
        # Cria uma função Python "lambdify" (compila para numpy)
        # 'numpy' permite que funcione com vetores inteiros de uma vez
        f = sp.lambdify(x_sym, expr, modules=['numpy'])
        
        # Calcula Y
        y_vals = f(x_range)
        
        # Retorna a expressão formatada em LaTeX e os valores
        return sp.latex(expr), y_vals, None
        
    except Exception as e:
        return None, None, str(e)

# --- PLOTAGEM ---
try:
    # 1. Gerar dados X
    x = np.linspace(x_min, x_max, num_points)
    
    # 2. Processar Y
    latex_expr, y, error = process_function(raw_equation, x)
    
    if error:
        st.error(f"Erro ao interpretar a equação: {error}")
        st.info("Dica: Use sintaxe Python. Ex: `2*x` em vez de `2x`. Use `np.sin`, `np.sqrt` ou apenas `sin`, `sqrt`.")
    else:
        # Mostra a equação formatada bonitinha
        st.latex(f"f(x) = {latex_expr}")
        
        # Configura o tema
        plt.style.use(theme_style)
        
        # Cria a figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plota os dados
        ax.plot(x, y, label=f'f(x) = {raw_equation}', color=plot_color, linestyle=line_style, linewidth=2)
        
        # Configurações dos eixos
        ax.set_title(f'Gráfico de: ${latex_expr}$', fontsize=16)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('f(x)', fontsize=12)
        
        # Grid e Linhas Centrais
        if show_grid:
            ax.grid(True, linestyle='--', alpha=0.6)
            
        ax.axhline(0, color='black', linewidth=1.2) # Eixo X
        ax.axvline(0, color='black', linewidth=1.2) # Eixo Y
        
        # Limites manuais de Y se selecionado
        if use_ylim:
            ax.set_ylim(y_lim)
        else:
            # Auto-ajuste inteligente para evitar gráficos explodidos (assíntotas)
            # Filtra valores infinitos para definir limites razoáveis se não houver manual
            finite_y = y[np.isfinite(y)]
            if len(finite_y) > 0:
                y_range = finite_y.max() - finite_y.min()
                if y_range > 1000: # Se a variação for gigante (assíntota vertical)
                    ax.set_ylim(np.percentile(finite_y, 1), np.percentile(finite_y, 99))

        ax.legend()
        
        # Exibe no Streamlit
        st.pyplot(fig)

except Exception as main_error:
    st.error(f"Ocorreu um erro inesperado: {main_error}")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Dica: Tente funções como `tan(x)`, `exp(-x**2)`, ou `abs(x)`.")
