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
        with st.container():
            with st.form("my_form"):
                st.write("Inside the form")
                slider_val = st.slider("Form slider")
                checkbox_val = st.checkbox("Form checkbox")

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
            if submitted:
                st.write("slider", slider_val, "checkbox", checkbox_val)

    with st.expander("Metricas y resultados"):
        st.write("Holi")

