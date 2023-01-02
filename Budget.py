import streamlit as st
import time
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide")
st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

path= "https://raw.githubusercontent.com/jchavesmartinez/StreamlitBudget/main/Budget.csv"
Budget2023 = pd.read_csv(path, encoding='latin-1',index_col=0)

with st.expander("Presupuesto 2023"):
    st.dataframe(Budget2023,use_container_width=True)
    
with st.expander("Ingresos"):
    number1 = st.number_input('Salario mensual neto Jose',1207000)
    number2 = st.number_input('Salario mensual neto Aline',600000)

    if st.checkbox("Registrar ingreso"):
        with st.form("my_form"):
            motivo_option = st.selectbox('Motivo',('Salario Jose', 'Salario Aline', 'Ingreso extra'))
            monto_ingreso = st.number_input('Monto')
            currency_option = st.selectbox('Moneda',('Colones', 'Pesos', 'USD'))
            nota_input = st.text_input('Comentario')
            
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.write("slider")


with st.expander("Gastos"):
    if st.checkbox("Registrar gasto"):
        with st.form("my_form2"):
            motivo_option2 = st.selectbox('Motivo',('Salario Jose', 'Salario Aline', 'Ingreso extra'))
            monto_ingreso2 = st.number_input('Monto')
            currency_option2 = st.selectbox('Moneda',('Colones', 'Pesos', 'USD'))
            nota_input2 = st.text_input('Comentario')
            
            submitted2 = st.form_submit_button("Submit")
        
        if submitted2:
            st.write("slider")

with st.expander("Metricas y resultados"):
    st.write("Holi")

with st.expander("Saldos"):
    st.write("Holi")

