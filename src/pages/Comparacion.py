import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

dicc = {'País':'País','Ciudad':'Ciudad_Destino','Universidad':'UniPos2'}

@st.cache
def cargar_df():
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/ColfSelecClean.csv')
    return st.session_state['df']

@st.cache
def filtrar(opcion_general,opcion1,opcion2,df):

    return df[(df[dicc[opcion_general]] == opcion1) | (df[dicc[opcion_general]] == opcion2)]

@st.cache
def get_opciones(opcion,df):
    return np.sort(df[dicc[opcion]].unique())

def main():
    st.header('Comparación')
    st.write('En esta sección puedes comparar los numeros entre dos países o ciudades o universidades. Las posibilidades son infinitas! Bueno, no del todo :)')

    df = cargar_df()

    opcion_general = st.selectbox(
        label="¿Qué te gustaría comparar?",
        options=('País','Ciudad','Universidad')
    )

    st.subheader('Comparación según ' + opcion_general)

    col1,col2 = st.columns(2)

    ops = get_opciones(opcion_general,df)

    with col1:
        option1 = st.selectbox(
        opcion_general + ' 1',
        ops
        )
    
    with col2:
        option2 = st.selectbox(
        opcion_general + ' 2',
        ops
        )
    
    if option1 and option2:
        df = filtrar(opcion_general,option1,option2,df)

        count_df = df.groupby([dicc[opcion_general],'Prom']).size().reset_index(name='Conteo')

        fig = px.line(count_df, x="Prom", y="Conteo", color=dicc[opcion_general],markers=True)

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        count_pos_df = df.groupby([dicc[opcion_general],'Posgrado']).size().reset_index(name='Conteo')

        count_area_df = df.groupby([dicc[opcion_general],'Área']).size().reset_index(name='Conteo').sort_values(by='Conteo',ascending=False)

        st.subheader('Como se comparan según el área de estudio')
        
        fig = px.histogram(count_area_df, x="Área", y="Conteo",
             color=dicc[opcion_general], barmode='group')

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        st.subheader('Los programas a los que más aplican')

        col3,col4 = st.columns(2)

        with col3:
            st.write(option1)
            st.dataframe(count_pos_df[count_pos_df[dicc[opcion_general]] == option1][['Posgrado','Conteo']].sort_values(by='Conteo',ascending=False).head(10))
        with col4:
            st.write(option2)
            st.dataframe(count_pos_df[count_pos_df[dicc[opcion_general]] == option2][['Posgrado','Conteo']].sort_values(by='Conteo',ascending=False).head(10))

        if opcion_general != 'Universidad':
            count_unis_1 = df[df[dicc[opcion_general]] == option1].groupby([dicc[opcion_general],'UniPos2','url']).size().reset_index(name='Conteo').sort_values(by='Conteo',ascending=False).head()
            st.subheader('Top 5 Universidades a las que aplican en '+option1)
            size = count_unis_1.shape[0]
            cols = st.columns(size)
            for i in range(size):
                with cols[i]:
                    st.write(count_unis_1.iloc[i]['UniPos2'])
                    if count_unis_1.iloc[i]['url'] != 'NotFound':
                        st.write('[Página de la Universidad]('+count_unis_1.iloc[i]['url']+')')
            
            st.subheader('Top 5 Universidades a las que aplican en '+option2)
            count_unis_2 = df[df[dicc[opcion_general]] == option2].groupby([dicc[opcion_general],'UniPos2','url']).size().reset_index(name='Conteo').sort_values(by='Conteo',ascending=False).head()
            size = count_unis_2.shape[0]
            cols = st.columns(size)
            for i in range(size):
                with cols[i]:
                    st.write(count_unis_2.iloc[i]['UniPos2'])
                    if count_unis_2.iloc[i]['url'] != 'NotFound':
                        st.write('[Página de la Universidad]('+count_unis_2.iloc[i]['url']+')')


main()