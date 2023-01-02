import streamlit as st
import time
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide")
st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

with st.container():
    with st.expander("Presupuesto 2023"):
        path= "https://raw.githubusercontent.com/jchavesmartinez/StreamlitBudget/main/Budget.csv"
        Budget2023 = pd.read_csv(path, encoding='latin-1',index_col=0)
        st.dataframe(Budget2023,use_container_width=True)
        
    with st.expander("Ingresos"):
        number1 = st.number_input('Salario mensual neto Jose')
        number2 = st.number_input('Salario mensual neto Aline')
    with st.expander("Gastos"):
        st.write("Holi")
    with st.expander("Metricas y resultados"):
        st.write("Holi")

