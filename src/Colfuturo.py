import streamlit as st
import pandas as pd
import plotly.express as px
import webbrowser



@st.cache
def cargar_df():

    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/ColfSelecClean.csv')
    return st.session_state['df']

@st.cache
def query_year(years,df):

    return df[(df['Prom'] >= years[0]) & ((df['Prom'] <= years[1]))]

@st.cache
def query_field_mult(field_name,options,df):
    df2 = pd.DataFrame(columns = df.columns)
    if len(options) > 0:
        for i in options:
            df2 = pd.concat([df2,df[df[field_name] == i]],ignore_index=True)
        return df2
    else:
        return df

def main():

    df = cargar_df()

    st.header(':red[Colfuturo] credito-beca 	:flag-co:')
    st.write('¡Bienvenido! Este es un proyecto donde vas a poder ver los datos de los ganadores del credito beca de Colfuturo de una manera más interactiva. \n' + 
    'En el panel izquierdo podrás filtrar el año de convocatoria, área del estudio y el tipo de estudio.')
    st.write('En el panel izquierdo también vas a encontrar la pagina de comparación, ahí podrás comparar dos paises, ciudades o universidades. También están la página de trabajo futuro, en el cual se discute cuales pueden ser las siguientes mejoras al tablero.')
    st.write('Existen dos tipos de personas en los datos, los beneficiarios y los seleccionados. Lo más probable es que los seleccionados hayan ganado la convocatoria, pero por alguna razón, no llegaron a ser beneficiarios.')
    st.write('Este es un proyecto independiente, no esta vinculado a Colfuturo y fue realizado con los datos abiertos de la entidad')
    st.write('En este momento la convocatoria para el año 2023 esta abierta! Puedes dar en este botón que te va a redirigir a la página oficial para que puedas aplicar :point_down:')
    url = 'https://www.colfuturo.org/programas/credito-beca/convocatoria'
    if st.button('Convocatoria 2023'):
        webbrowser.open_new_tab(url)

    years = st.sidebar.slider(
        label="Selecciona el rango de años",
        min_value=2000,
        max_value=2022,
        value=(2000,2022)
    )

    df = query_year(years,df)

    areas = df['Área'].unique()
    tipos = df['Tipo'].unique()

    selected_areas = st.sidebar.multiselect(
        label='Selecciona el área de estudio',
        options = areas,
        help = 'Puedes escoger más de una área a la vez'
    )

    selected_tipos = st.sidebar.multiselect(
        label='Selecciona el tipo de estudio',
        options = tipos,
        help = 'Puedes escoger más de un tipo a la vez'
    )
    df = query_field_mult('Área',selected_areas,df)
    df = query_field_mult('Tipo',selected_tipos,df)
    
    st.subheader('¿A donde van los Colombianos con la beca? :earth_americas:')
    st.map(data=df,zoom=0.6,use_container_width=True)
    benef = df[df['Estado'] == 'beneficiario']
    select = df[df['Estado'] == 'seleccionado']
    if select.shape[0] > 0:
        cols = st.columns(2)
    else:
        cols = st.columns(1)
    with cols[0]:
        plot_given_state(True,benef)
    
    if select.shape[0] > 0:
        with cols[1]:
            plot_given_state(False,select)


    st.subheader('Analisís en Detalle')

    st.write('¿Cuales son las ciudades preferidas para ir a estudiar?')

    top10 = df.groupby(['Ciudad_Destino']).size().reset_index(name='Conteo').sort_values(by='Conteo',ascending=False).head(10)

    fig = px.bar(top10, x='Ciudad_Destino', y='Conteo')
    st.plotly_chart(fig,theme="streamlit",use_container_width=True)

    st.write('Y, ¿que tal los países?')

    top10 = df.groupby(['País']).size().reset_index(name='Conteo').sort_values(by='Conteo',ascending=False).head(10)

    fig = px.bar(top10, x='País', y='Conteo')
    st.plotly_chart(fig,theme="streamlit",use_container_width=True)

def plot_given_state(estado,df):
    if estado:
        text_labels = 'beneficiarios'
    else:
        text_labels = 'seleccionados'
    texto = "El numero de " + text_labels + " fue: "
    st.metric(
                label= texto,
                value= df.shape[0]
            )
            
    gen_selec = df.groupby(['Género']).size().reset_index(name='Conteo')
    fig = px.pie(gen_selec, values='Conteo', names='Género',
                    title='Género de los ' + text_labels,
                    color='Género',
                    color_discrete_map={'Masculino':px.colors.qualitative.Pastel[8],
                    'Femenino':px.colors.qualitative.Pastel[3],
                    'Otro':px.colors.qualitative.Pastel[1]},
                )
                        
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig,use_container_width=True)
        
main()    