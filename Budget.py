import streamlit as st
import time 

st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

import streamlit as st

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")