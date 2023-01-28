import streamlit as st
import time
import pandas as pd
import numpy as np
import os
from datetime import datetime, date, time, timedelta, timezone
import pymongo
import pandas as pd
from pandas import json_normalize
import json
import harperdb


st.set_page_config(layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



st.title('Presupuesto 2023 Maldonado Chaves SA de CV')

path= "https://raw.githubusercontent.com/jchavesmartinez/StreamlitBudget/main/Budget.csv"
Budget2023 = pd.read_csv(path, encoding='latin-1',index_col=0)

path= "https://raw.githubusercontent.com/jchavesmartinez/StreamlitBudget/main/Tasas0.csv"
Tasas0 = pd.read_csv(path, encoding='latin-1',index_col=0)

CONNECTION_STRING = 'mongodb://presupuesto2023:CBCE5lRc5JX778aCQVXb9EmUJAnEA76qYuC3XAElUjuhkoJXJoy0pt4C0EZgHEygtT1R2j2iI1mvACDb6ljS4w==@presupuesto2023.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@presupuesto2023@' # Prompts user for connection string
DB_NAME = "Presupuesto"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client[DB_NAME]
cursor = db.COLLECTION_DIARIO # choosing the collection you need

Diario = pd.DataFrame(list(db.COLLECTION_DIARIO.find({})))


hoy=date.today().strftime("%d-%b-%Y")
mes=int(datetime.now().date().month)+1
dia=int(date.today().strftime("%d"))-20

st.write(hoy)

if mes==1:
    mes='Enero'
elif mes==2:
    mes='Febrero'
elif mes==3:
    mes='Marzo'
elif mes==4:
    mes='Abril'
elif mes==5:
    mes='Mayo'
elif mes==6:
    mes='Junio'
elif mes==7:
    mes='Julio'
elif mes==8:
    mes='Agosto'
elif mes==9:
    mes='Setiembre'
elif mes==10:
    mes='Octubre'
elif mes==11:
    mes='Noviembre'
elif mes==12:
    mes='Diciembre'

if int(dia)<15:
    quincena=' I '
if int(dia)>=15:
    quincena=' II '

fecha=mes+quincena


with st.expander("Presupuesto 2023"):
    st.dataframe(Budget2023,use_container_width=True)
    
with st.expander("Ingresos"):
    number1 = st.number_input('Salario mensual neto Jose',1207000)
    number2 = st.number_input('Salario mensual neto Aline',600000)

    if st.checkbox("Registrar ingreso"):
        with st.form("my_form"):
            motivo_option = st.selectbox('Motivo',('Salario', 'Ingreso extra'))
            cuenta_option = st.selectbox('Cuenta Bancaria',('Tarjeta debito Jose', 'Tarjeta debito Aline'))            
            monto_ingreso = st.number_input('Monto')
            #currency_option = st.selectbox('Moneda',('Colones', 'Pesos', 'USD'))
            nota_input = st.text_input('Comentario')
            
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            db.COLLECTION_DIARIO.insert_one({"_id": len(Diario)+13, "Motivo": motivo_option, "Tipo": 'Ingreso', "Monto": -monto_ingreso, "Fecha": fecha, "Escenario": '2. Actual', "Cuenta": cuenta_option, "Nota": nota_input})
            st.success('This is a success message!!', icon="✅")
            st.experimental_rerun()

with st.expander("Gastos"):
    
    if st.checkbox("Registrar gasto"):
        
        with st.form("my_form2"):
            motivo_option2 = st.selectbox('Motivo',('Hipoteca', 'Cuota Condominio', 'Tasa 0','Boletos','Celular','Regalos','Ahorro','Entretenimiento','Mascotas','Marchamo y seguros','Ropa','Gas','Comida','Viajes','Cuota Carro','Internet','Electricidad','Comida afuera','Agua','Casa Mantenimiento','Carro Mantenimiento'))
            cuenta_option2 = st.selectbox('Cuenta Bancaria',('Tarjeta debito Jose', 'Tarjeta debito Aline', 'Tarjeta credito Jose','Tarjeta credito Aline'))            
            monto_ingreso2 = st.number_input('Monto')
            #currency_option2 = st.selectbox('Moneda',('Colones', 'Pesos', 'USD'))
            nota_input2 = st.text_input('Comentario')
            submitted2 = st.form_submit_button("Submit")
        
        if submitted2:
            db.COLLECTION_DIARIO.insert_one({"_id": len(Diario)+13, "Motivo": motivo_option2, "Tipo": 'Gasto', "Monto": -monto_ingreso2, "Fecha": fecha, "Escenario": '2. Actual', "Cuenta": cuenta_option2, "Nota": nota_input2})
            st.success('This is a success message!!', icon="✅")
            st.experimental_rerun()


with st.expander("Metricas y resultados"):
    
    mes_option = st.selectbox('Seleccione un mes',('Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre'),key="mes1")
    quicena_option = st.selectbox('Seleccione la quincena',('Ambas','Primera quincena', 'Segunda quincena'),key='quincena1')
    if  quicena_option=='Primera quincena':
        fechafiltrar= mes_option + ' I '
        DiarioFinal=Diario[Diario['Fecha']==fechafiltrar]
    elif quicena_option=='Segunda quincena':
        fechafiltrar= mes_option + ' II '
        DiarioFinal=Diario[Diario['Fecha']==fechafiltrar]
    elif quicena_option=='Ambas':
        DiarioFinal=Diario[Diario['Fecha'].str.contains(mes_option)]
    
    DiarioFinalPresupuesto=DiarioFinal[DiarioFinal['Escenario']=='1. Presupuesto']
    DiarioFinalPresupuesto1=DiarioFinalPresupuesto
    DiarioFinalPresupuesto = DiarioFinalPresupuesto.groupby(['Motivo'])['Monto'].sum()
    DiarioFinalActual=DiarioFinal[DiarioFinal['Escenario']=='2. Actual']
    DiarioFinalActual1=DiarioFinalActual
    DiarioFinalActual = DiarioFinalActual.groupby(['Motivo'])['Monto'].sum()
    DiarioFinal2 = DiarioFinal.groupby(['Motivo'])['Monto'].sum()

    DiarioFinal1 = pd.merge(DiarioFinal2, DiarioFinalPresupuesto, on=["Motivo"])
    DiarioFinal1 = pd.merge(DiarioFinal1, DiarioFinalActual, on=["Motivo"])
    DiarioFinal1=DiarioFinal1.rename(columns={"Monto_x": "Saldo Disponible", "Monto_y": "Saldo Presupuestado", "Monto": "Saldo Consumido"}, errors="raise")

    temp_cols=DiarioFinal1.columns.tolist()
    new_cols=temp_cols[1:] + temp_cols[0:1]
    DiarioFinal1=DiarioFinal1[new_cols]

    DiarioFinal1['Saldo Consumido %'] = 100 - (DiarioFinal1['Saldo Disponible']/DiarioFinal1['Saldo Presupuestado']*100)

    DiarioCalculosP=DiarioFinalPresupuesto1[(DiarioFinalPresupuesto1.Motivo != "Salario")]
    DiarioCalculosP=DiarioCalculosP[(DiarioCalculosP.Motivo != "Ingresos Extra")]

    DiarioCalculosA=DiarioFinalActual1[(DiarioFinalActual1.Motivo != "Salario")]
    DiarioCalculosA=DiarioCalculosA[(DiarioCalculosA.Motivo != "Ingresos Extra")]

    Superavit=DiarioFinal1[DiarioFinal1['Saldo Presupuestado'] < 600000]
    Superavit=Superavit[Superavit['Saldo Disponible'] > 0]
    Superavit1=Superavit['Saldo Disponible'].sum()

    Deficit=DiarioFinal1[DiarioFinal1['Saldo Presupuestado'] < 600000]
    Deficit=Deficit[Deficit['Saldo Disponible'] < 0]
    Deficit1=Deficit['Saldo Disponible'].sum()

    genre = st.radio(
    "What\'s your favorite movie genre",
    ('Todo', 'Deficit', 'Superavit'))

    if genre == 'Todo':
        Mostrar=DiarioFinal1
        indicador=''
        Etiqueta=''
    elif genre == 'Superavit':
        Mostrar=Superavit
        indicador=int(Superavit1)
        Etiqueta='Gastos por cubrir'
    elif genre == 'Deficit':
        Mostrar=Deficit
        indicador=int(Deficit1)
        Etiqueta='Gastos excedidos'

    tab1, tab2= st.tabs(["Metricas", "Resumen"])

    with tab1:
        col1, col2, col3, col4,col5 = st.columns([1,1,1,1,1])
        col1.metric(Etiqueta, indicador)
        col2.metric("Saldo Presupuestado", int(DiarioCalculosP['Monto'].sum()))
        col3.metric("Saldo Consumido", int(DiarioCalculosA['Monto'].sum()))
        col4.metric("Saldo Disponible", int(DiarioCalculosP['Monto'].sum())+int(DiarioCalculosA['Monto'].sum()))
        col5.metric("Saldo Consumido", str(-int(DiarioCalculosA['Monto'].sum()/DiarioCalculosP['Monto'].sum()*100))+'%')
        #st.dataframe(DiarioFinal1,use_container_width=True)
        st.dataframe(Mostrar,use_container_width=True)

    with tab2:
        st.write("Proximamente grafiquitos bonitos")
  
with st.expander("Saldos"):
    tab3, tab4, tab5= st.tabs(["Debito", "Credito", 'Tasas 0'])

    with tab3:
        mes_option2 = st.selectbox('Seleccione un mes',('Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre'),key='mes2')
        quicena_option2 = st.selectbox('Seleccione la quincena',('Ambas','Primera quincena', 'Segunda quincena'),key='quincena2')
        cuenta_option2 = st.selectbox('Seleccione una cuenta',('Ambas','Tarjeta debito Jose', 'Tarjeta debito Aline'),key='cuenta')
        if  quicena_option2=='Primera quincena':
            fechafiltrar2= mes_option2 + ' I '
            DiarioFinal2=Diario[Diario['Fecha']==fechafiltrar2]
        elif quicena_option2=='Segunda quincena':
            fechafiltrar2= mes_option2 + ' II '
            DiarioFinal2=Diario[Diario['Fecha']==fechafiltrar2]
        elif quicena_option2=='Ambas':
            DiarioFinal2=Diario[Diario['Fecha'].str.contains(mes_option2)]      
        
        if cuenta_option2 !='Ambas':
            DiarioFinal2=DiarioFinal2[DiarioFinal2['Cuenta']==cuenta_option2]
        
        DiarioFinal2=DiarioFinal2[DiarioFinal2['Escenario']=='2. Actual']
        DiarioFinal2=DiarioFinal2.drop(columns=['Escenario', 'Fecha'])
        DiarioFinal2=DiarioFinal2[DiarioFinal2['Cuenta'].str.contains('debito')]

        debitototal=(DiarioFinal2[DiarioFinal2['Tipo']=='Ingreso']['Monto'].sum())*-1+DiarioFinal2[DiarioFinal2['Tipo']=='Gasto']['Monto'].sum()
        col7, col8, col9, col10,col11 = st.columns([1,1.2,1,1,1])
        col9.metric("Saldo Debito", int(debitototal), "4%")
        
        st.dataframe(DiarioFinal2,use_container_width=True)

    with tab4:
        mes_option2 = st.selectbox('Seleccione un mes',('Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre'),key='mes3')
        quicena_option2 = st.selectbox('Seleccione la quincena',('Ambas','Primera quincena', 'Segunda quincena'),key='quincena3')
        cuenta_option2 = st.selectbox('Seleccione una cuenta',('Ambas','Tarjeta credito Jose', 'Tarjeta credito Aline'),key='cuenta3')
        if  quicena_option2=='Primera quincena':
            fechafiltrar2= mes_option2 + ' I '
            DiarioFinal2=Diario[Diario['Fecha']==fechafiltrar2]
        elif quicena_option2=='Segunda quincena':
            fechafiltrar2= mes_option2 + ' II '
            DiarioFinal2=Diario[Diario['Fecha']==fechafiltrar2]
        elif quicena_option2=='Ambas':
            DiarioFinal2=Diario[Diario['Fecha'].str.contains(mes_option2)]      
            
        DiarioFinal2=DiarioFinal2[DiarioFinal2['Escenario']=='2. Actual']
        DiarioFinal2=DiarioFinal2.drop(columns=['Escenario', 'Fecha'])
        DiarioFinal2=DiarioFinal2[DiarioFinal2['Cuenta'].str.contains('credito')]

        if cuenta_option2=='Ambas':
            saldoinicial=-(322862.82+59581.35)
            debitototal=DiarioFinal2['Monto'].sum()
            col27, col28, col29, col210,col211 = st.columns([1,1.2,1,1,1])
            col29.metric("Saldo Credito",abs(debitototal+saldoinicial), "%")

        if cuenta_option2=='Tarjeta credito Jose':
            DiarioFinal2=DiarioFinal2[DiarioFinal2['Cuenta']==cuenta_option2]
            saldoinicial=-322862.82-176,914.08

            debitototal=DiarioFinal2['Monto'].sum()
            col17, col18, col19, col110,col111 = st.columns([1,1.2,1,1,1])
            col19.metric("Saldo Credito",abs(debitototal+saldoinicial), "%")

            if st.checkbox("Pagar tarjeta Jose"):
                
                with st.form('PagoJose'):
                    cuenta_option21 = st.selectbox('Cuenta Bancaria',('Tarjeta debito Jose', 'Tarjeta debito Aline'),key='pagojose1')            
                    monto_ingreso21 = st.number_input('Monto',key='pagojose2')
                    submitted31 = st.form_submit_button("Confirmar pago Jose")
                
                if submitted31:
                    db.COLLECTION_DIARIO.insert_one({"_id": len(Diario)+13, "Motivo": 'Tasa 0', "Tipo": 'Gasto', "Monto": monto_ingreso21, "Fecha": fecha, "Escenario": '2. Actual', "Cuenta": 'Tarjeta credito Jose', "Nota": 'Pago tarjeta de credito Jose'})
                    db.COLLECTION_DIARIO.insert_one({"_id": len(Diario)+14, "Motivo": 'Tasa 0', "Tipo": 'Gasto', "Monto": -monto_ingreso21, "Fecha": fecha, "Escenario": '2. Actual', "Cuenta": cuenta_option21, "Nota": 'Pago tarjeta de credito Jose'})
                    st.success('This is a success message!!', icon="✅")
                    st.experimental_rerun()



        if cuenta_option2=='Tarjeta credito Aline':
            DiarioFinal2=DiarioFinal2[DiarioFinal2['Cuenta']==cuenta_option2]
            saldoinicial=-59581.35
            debitototal=DiarioFinal2['Monto'].sum()
            col37, col338, col39, col310,col311 = st.columns([1,1.2,1,1,1])
            col39.metric("Saldo Credito",int(abs(debitototal+saldoinicial)), "%")

            if st.checkbox("Pagar tarjeta Aline"):

                with st.form("PagoAline"):
                    cuenta_option2 = st.selectbox('Cuenta Bancaria',('Tarjeta debito Jose', 'Tarjeta debito Aline'),key='pagoaline1')            
                    monto_ingreso2 = st.number_input('Monto',key='pagoaline2')
                    submitted4 = st.form_submit_button("Confirmar pago Aline")
                
                if submitted4:
                    db.COLLECTION_DIARIO.insert_one({"_id": len(Diario)+13, "Motivo": 'Tasa 0', "Tipo": 'Gasto', "Monto": monto_ingreso2, "Fecha": fecha, "Escenario": '2. Actual', "Cuenta": 'Tarjeta credito Aline', "Nota": 'Pago tarjeta de credito Aline'})
                    db.COLLECTION_DIARIO.insert_one({"_id": len(Diario)+14, "Motivo": 'Tasa 0', "Tipo": 'Gasto', "Monto": -monto_ingreso2, "Fecha": fecha, "Escenario": '2. Actual', "Cuenta": cuenta_option2, "Nota": 'Pago tarjeta de credito Aline'})
                    st.success('This is a success message!!', icon="✅")
                    st.experimental_rerun()
        
        st.dataframe(DiarioFinal2,use_container_width=True)

    with tab5:
        st.dataframe(Tasas0,use_container_width=True)
