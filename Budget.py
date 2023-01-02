import streamlit as st
import time
import pandas as pd
import numpy as np


st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

with st.container():
    with st.expander("Presupuesto 2023"):
        df = pd.DataFrame(
        np.random.randn(50, 20),
        columns=('col %d' % i for i in range(20)))

        st.dataframe(df)  # Same as st.write(df)
    with st.expander("Ingresos"):
        st.write("Holi")
    with st.expander("Gastos"):
        st.write("Holi")

