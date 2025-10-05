import streamlit as st
import numpy as np

opcoes = ["A", "B", "C", "D", "E"]

# Seleção do tipo de prova
tp_prova = st.selectbox("Tipo de Prova", ["I","II","III", "IV", "V", "VI", "VII"])

# Definição de pesos e número de questões por tipo de prova
if tp_prova == "I":
    n_linhas = 9
    peso_discursivas = [35, 0]
    peso_obj = [65, 0]

elif tp_prova == "II":
    n_linhas = 14
    peso_discursivas = [35, 0]
    peso_obj = [37.8, 27.2]

elif tp_prova == "III":
    n_linhas = 18
    peso_discursivas = [17, 14]
    peso_obj = [30.06, 38.94]

elif tp_prova == "IV":
    n_linhas = 23
    peso_discursivas = [14.5, 11.5]
    peso_obj = [24.48, 49.52]

elif tp_prova == "V":
    n_linhas = 28
    peso_discursivas = [11.5, 9.5]
    peso_obj = [21.15, 57.85]

elif tp_prova == "VI":
    n_linhas = 33
    peso_discursivas = [8.75, 7.5]
    peso_obj = [18.72, 65.03]

elif tp_prova == "VII":
    n_linhas = 38
    peso_discursivas = [8.75, 7.5]
    peso_obj = [16.25, 67.5]

# Inicialização de listas e variáveis
col1_vals, col2_vals, acertos = [], [], []
nota_gerais = 0
nota_espec = 0

# Layout das colunas
col1, col2 = st.columns(2)
with col1:
    st.header("Resposta")
with col2:
    st.header("Gabarito")

# Loop para cada questão
for i in range(n_linhas):
    with col1:
        val1 = st.selectbox(f"Resposta da Questão {i+1}", opcoes, key=f"c1_{i}")
    with col2:
        val2 = st.selectbox(f"Gabarito da Questão {i+1}", opcoes, key=f"c2_{i}")
    col1_vals.append(val1)
    col2_vals.append(val2)
    acertos.append(val1 == val2)

# Sliders para notas discursivas
discursiva1 = st.select_slider(
    "Discursiva 1:",
    options=list(np.round(np.arange(0, peso_discursivas[0] + 0.1, 0.1), 1))
)

discursiva2 = 0  # valor padrão
if peso_discursivas[1] != 0:
    discursiva2 = st.select_slider(
        "Discursiva 2:",
        options=list(np.round(np.arange(0, peso_discursivas[1] + 0.1, 0.1), 1))
    )

# Cálculo da nota objetiva
num_gerais = 9
for i in range(num_gerais):
    if acertos[i]:
        nota_gerais += peso_obj[0] / num_gerais

num_espec = n_linhas - num_gerais
if num_espec > 0:
    for i in range(num_gerais, n_linhas):
        if acertos[i]:
            nota_espec += peso_obj[1] / num_espec

# Cálculo da nota total
if tp_prova == "I":
    total = nota_gerais + discursiva1
elif tp_prova == "II":
    total = nota_gerais + nota_espec + discursiva1
else:
    total = nota_gerais + nota_espec + discursiva1 + discursiva2

st.title(f"Nota Total: {total:.2f}")
