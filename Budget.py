import streamlit as st
import time
import pandas as pd
import numpy as np
import os


st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

with st.container():
    with st.expander("Presupuesto 2023"):
        path= "C:\Users\XPC\OneDrive\Desktop"+'\\'
        #Budget2023 = pd.read_csv(path+'Budget.csv', encoding='latin-1')
        st.write(path+'Budget.csv')



    with st.expander("Ingresos"):
        st.write("Holi")
    with st.expander("Gastos"):
        st.write("Holi")

