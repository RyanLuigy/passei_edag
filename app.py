import streamlit as st

opcoes = ["A", "B", "C", "D", "E"]

tp_prova = st.selectbox("Tipo de Prova", ["I","II","III", "IV", "V", "VI", "VII"])

if tp_prova == "I":
    n_linhas = 9  # só objetiva? sem discursiva específica
    peso_discursivas = [35, 0]  # Formação Geral Discursiva, Conhecimento Específico Discursiva
    peso_obj = [65, 0]          # Formação Geral Objetivas, Conhecimento Específico Objetivas

elif tp_prova == "II":
    n_linhas = 14  # ajustar conforme número de questões objetivas
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

col1_vals = []
col2_vals = []
acertos = []
nota_gerais = 0
nota_espec = 0

col1, col2 = st.columns(2)  # cria duas colunas lado a lado
with col1:
        st.header("Resposta")
with col2:
        st.header("Gabarito")

for i in range(n_linhas):
  
    with col1:
        val1 = st.selectbox(f"Resposta da Questão{i+1}", opcoes, key=f"c1_{i}")
    with col2:
        val2 = st.selectbox(f"Gabarito da Questão {i+1}", opcoes, key=f"c2_{i}")
    
    col1_vals.append(val1)
    col2_vals.append(val2)
    acertos.append(col1_vals[i] == col2_vals[i])

discursiva1 = st.select_slider("Discursiva 1:", options=list(range(peso_discursivas[0]+1)))
if(peso_discursivas[1]!=0):
    discursiva2 = st.select_slider("Discursiva 2:", options=list(range(peso_discursivas[1]+1)))

for i in range(9):
    if(acertos[i]):
         nota_gerais += peso_obj[0]/9
for i in range(9,n_linhas):
    if(acertos[i]):
         nota_espec += peso_obj[1]/9

if(tp_prova != "I" | "II"):
    total = nota_gerais + nota_espec + discursiva1 + discursiva2
else:
     total = nota_gerais + discursiva1

st.title(total)
