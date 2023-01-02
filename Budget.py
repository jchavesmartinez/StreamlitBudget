import streamlit as st
import time
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide")
st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

path= "https://raw.githubusercontent.com/jchavesmartinez/StreamlitBudget/main/Budget.csv"
Budget2023 = pd.read_csv(path, encoding='latin-1',index_col=0)

path2= "https://raw.githubusercontent.com/jchavesmartinez/StreamlitBudget/main/Diario.csv"
Diario = pd.read_csv(path2, encoding='utf8',index_col=0)
#Diario['Monto'] = Diario['Monto'].astype(float)

with st.expander("Presupuesto 2023"):
    st.dataframe(Budget2023,use_container_width=True)
    
with st.expander("Ingresos"):
    number1 = st.number_input('Salario mensual neto Jose',1207000)
    number2 = st.number_input('Salario mensual neto Aline',600000)

    if st.checkbox("Registrar ingreso"):
        with st.form("my_form"):
            motivo_option = st.selectbox('Motivo',('Salario Jose', 'Salario Aline', 'Ingreso extra'))
            cuenta_option = st.selectbox('Cuenta Bancaria',('Tarjeta debito AAA', 'Tarjeta debito BBB', 'Tarjeta credito AAA','Tarjeta de credito BBB'))            
            monto_ingreso = st.number_input('Monto')
            currency_option = st.selectbox('Moneda',('Colones', 'Pesos', 'USD'))
            nota_input = st.text_input('Comentario')
            
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.write("slider")


with st.expander("Gastos"):
    if st.checkbox("Registrar gasto"):
        with st.form("my_form2"):
            motivo_option2 = st.selectbox('Motivo',('Hipoteca', 'Cuota Condominio', 'Tasa 0','Boltos','Celular','Regalos','Ahorro','Entretenimiento','Mascotas','Marchamo y seguros','Ropa','Gas','Comida','Viajes','Cuota carro','Internet','Eletricidad','Comidas afuera','Agua'))
            cuenta_option2 = st.selectbox('Cuenta Bancaria',('Tarjeta debito AAA', 'Tarjeta debito BBB', 'Tarjeta credito AAA','Tarjeta de credito BBB'))            
            monto_ingreso2 = st.number_input('Monto')
            currency_option2 = st.selectbox('Moneda',('Colones', 'Pesos', 'USD'))
            nota_input2 = st.text_input('Comentario')
            
            submitted2 = st.form_submit_button("Submit")
        
        if submitted2:
            st.write("slider")

with st.expander("Metricas y resultados"):
    
    
    mes_option = st.selectbox('Seleccione un mes',('Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre'))
    quicena_option = st.selectbox('Seleccione la quincena',('Ambas','Primera quincena', 'Segunda quincena'))
    if  quicena_option=='Primera quincena':
        fechafiltrar= mes_option + ' I '
        DiarioFinal=Diario[Diario['Fecha']==fechafiltrar]
    elif quicena_option=='Segunda quincena':
        fechafiltrar= mes_option + ' II '
        DiarioFinal=Diario[Diario['Fecha']==fechafiltrar]
    elif quicena_option=='Ambas':
        DiarioFinal=Diario[Diario['Fecha'].str.contains(mes_option)]
    
    DiarioFinalPresupuesto=DiarioFinal[DiarioFinal['Escenario']=='1. Presupuesto']
    DiarioFinalPresupuesto = DiarioFinalPresupuesto.groupby(['Motivo'])['Monto'].sum()
    DiarioFinalActual=DiarioFinal[DiarioFinal['Escenario']=='2. Actual']
    DiarioFinalActual = DiarioFinalActual.groupby(['Motivo'])['Monto'].sum()
    DiarioFinal2 = DiarioFinal.groupby(['Motivo'])['Monto'].sum()

    DiarioFinal1 = pd.merge(DiarioFinal2, DiarioFinalPresupuesto, on=["Motivo"])
    DiarioFinal1 = pd.merge(DiarioFinal1, DiarioFinalActual, on=["Motivo"])
    DiarioFinal1=DiarioFinal1.rename(columns={"Monto_x": "Saldo Disponible", "Monto_y": "Saldo Presupuestado", "Monto": "Saldo Consumido"}, errors="raise")

    temp_cols=DiarioFinal1.columns.tolist()
    new_cols=temp_cols[1:] + temp_cols[0:1]
    DiarioFinal1=DiarioFinal1[new_cols]

    DiarioFinal1['Saldo Consumido %'] = 100 - (DiarioFinal1['Saldo Disponible']/DiarioFinal1['Saldo Presupuestado']*100)


    tab1, tab2= st.tabs(["Metricas", "Resumen"])

    with tab1:
        st.dataframe(DiarioFinal1,use_container_width=True)

    with tab2:
        st.write("Proximamente grafiquitos bonitos")
  

with st.expander("Saldos"):
    st.write("Holi")

