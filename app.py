import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

opcoesResposta = ["A", "B", "C", "D", "E"]
opcoesGabarito = ["A", "B", "C", "D", "E","Anulada"]

st.title("Calculadora de nota do EDAG")
st.write("Calcule sua nota no Exame de Desempenho dos Alunos de Graduação. Selecione o curso e o tipo de prova. Ao selecionar o curso, o gabarito preliminar será preenchido na coluna Gabarito, no entanto, o usuário é livre para alterar.")
st.write("---")
st.write("\n")
curso = st.selectbox("Curso de Graduação", ["Engenharia da Computação","Engenharia Mecânica", "Engenharia Química", "Engenharia Elétrica", "Engenharia de Controle e Automação"])
tp_prova = st.selectbox("Tipo de Prova", ["I","II","III", "IV", "V", "VI", "VII"])

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

col1_vals, col2_vals, acertos = [], [], []
nota_gerais = 0
nota_espec = 0

gabaritos = {
    "Engenharia da Computação": [
        "B", "A", "A", "B", "A", "D", "E", "C", "E",
        "A", "B", "C", "A", "E", "B", "A", "B", "B",
        "C", "A", "C", "D", "C", "A", "A", "D", "C",
        "C", "D", "D", "E", "A", "C", "D", "C", "B",
        "E", "B"
    ],
    "Engenharia de Controle e Automação": [
        "B","A","A","B","A","D","E","C","E","A",
        "B","C","A","E","B","A","B","B","C","A",
        "C","D","A","E","A","E","E","A","A","C",
        "B","B","D","C","C","C","C","C","A"
    ],
    "Engenharia Elétrica": [
        "B","A","A","B","A","D","E","C","E","A",
        "B","C","A","E","B","A","B","B","C","A",
        "A","D","A","A","E","A","C","B","C","B",
        "D","C","C","C","B","C","B","A","C"
    ],
    "Engenharia Química": [
        "B","A","A","B","A","D","E","C","E","A",
        "B","C","A","E","B","A","B","B","C","A",
        "C","E","A","B","E","E","D","B","E","B",
        "B","B","A","E","E","E","A"
    ],
    "Engenharia Mecânica": [
        "B", "A", "A", "B", "A", "D", "E", "C", "E",
        "A", "B", "C", "A", "E", "B", "A", "C", "E",
        "B", "A", "B", "C", "A", "D", "A", "C", "E",
        "B", "D", "E", "E", "B", "B", "E", "B", "A",
        "C", "B", "E"
    ]
}

if "curso_atual" not in st.session_state or st.session_state.curso_atual != curso:
    st.session_state.curso_atual = curso
    for i in range(n_linhas):
        if i < len(gabaritos[curso]):
            st.session_state[f"c2_{i}"] = gabaritos[curso][i]

if "tp_atual" not in st.session_state or st.session_state.tp_atual != tp_prova:
    last_n = st.session_state.get("n_linhas_antigo", 0)
    st.session_state.tp_atual = tp_prova
    st.session_state.n_linhas_antigo = n_linhas
    for i in range(last_n, n_linhas): 
        if i < len(gabaritos[curso]):
            st.session_state[f"c2_{i}"] = gabaritos[curso][i]

col1, col2 = st.columns(2)
with col1:
    st.header("Resposta")
with col2:
    st.header("Gabarito")

for i in range(n_linhas):
    with col1:
        val1 = st.selectbox(f"Resposta da Questão {i+1}", opcoesResposta, key=f"c1_{i}")
    with col2:
        val2 = st.selectbox(f"Gabarito da Questão {i+1}", opcoesGabarito, key=f"c2_{i}")
    col1_vals.append(val1)
    col2_vals.append(val2)
    acertos.append(val1 == val2)

st.write("\n")

discursiva1 = st.select_slider(
    "Discursiva 1:",
    options=list(np.round(np.arange(0, peso_discursivas[0] + 0.1, 0.1), 1))
)

discursiva2 = 0
if peso_discursivas[1] != 0:
    discursiva2 = st.select_slider(
        "Discursiva 2:",
        options=list(np.round(np.arange(0, peso_discursivas[1] + 0.1, 0.1), 1))
    )

num_gerais_total = 9
acertos_gerais = 0
num_gerais_validas = num_gerais_total
num_espec_total = n_linhas - num_gerais_total

for i in range(num_gerais_total):
    if col2_vals[i] == "Anulada":
        num_gerais_validas -= 1
    elif acertos[i]:
        acertos_gerais += 1

acertos_espec = 0
num_espec_validas = num_espec_total

if num_espec_total > 0:
    for i in range(num_gerais_total, n_linhas):
        if col2_vals[i] == "Anulada":
            num_espec_validas -= 1
        elif acertos[i]:
            acertos_espec += 1

nota_gerais = 0
if num_gerais_validas > 0:
    peso_por_acerto_geral = peso_obj[0] / num_gerais_validas
    nota_gerais = acertos_gerais * peso_por_acerto_geral

nota_espec = 0
if num_espec_validas > 0 and peso_obj[1] != 0:
    peso_por_acerto_espec = peso_obj[1] / num_espec_validas
    nota_espec = acertos_espec * peso_por_acerto_espec

if tp_prova == "I":
    total = nota_gerais + discursiva1
elif tp_prova == "II":
    total = nota_gerais + nota_espec + discursiva1
else:
    total = nota_gerais + nota_espec + discursiva1 + discursiva2

st.title(f"Nota Total: {total:.2f}")

# Montar os dados de acordo com a prova
if tp_prova == "I":
    total = nota_gerais + discursiva1
    dados = {
        "Componente": ["Objetivas Gerais", "Discursiva 1", "Total"],
        "Valor": [nota_gerais, discursiva1, total]
    }

elif tp_prova == "II":
    total = nota_gerais + nota_espec + discursiva1
    dados = {
        "Componente": ["Objetivas Gerais", "Específica", "Discursiva 1", "Total"],
        "Valor": [(nota_gerais), (nota_espec), (discursiva1), total]
    }

else:
    total = nota_gerais + nota_espec + discursiva1 + discursiva2
    dados = {
        "Componente": ["Objetivas Gerais", "Específica", "Discursiva 1", "Discursiva 2", "Total"],
        "Valor": [nota_gerais, nota_espec, discursiva1, discursiva2, total]
    }


df = pd.DataFrame(dados)

df["y"] = "Nota"

cores = {
    "Objetivas Gerais": "#3498db",   # azul
    "Específica": "#2ecc71",         # verde
    "Discursiva 1": "#9b59b6",       # roxo
    "Discursiva 2": "#1abc9c",       # ciano
    "Total": "#e74c3c"             # vermelho
}

fig = px.bar(
    df,
    x="Valor",
    y="y",
    color="Componente",
    orientation="h",
    color_discrete_map=cores,
    text="Valor",
    hover_data={"y": False}
)

fig.update_traces(
    texttemplate="%{x:.2f}",   
    textposition="none",
    insidetextfont=dict(color="white")    
)

fig.update_layout(
    barmode="stack",
    xaxis=dict(range=[0, total], title=None),  
    yaxis=dict(showticklabels=False, title=None),
    height=200
)

st.plotly_chart(fig, use_container_width=True)