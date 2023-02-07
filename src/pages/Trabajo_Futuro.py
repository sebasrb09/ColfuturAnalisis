import streamlit as st

st.header('Trabajo Futuro')
st.write('Hay muchas cosas que se pueden mejorar en este tablero. Varias relacionadas con los datos. Los que se usaron en este proyecto son los datos abiertos accesibles desde la página oficial. ' + 
        'El problema es que solo se tiene acceso a los datos de aquellos que son beneficiarios o fueron seleccionados. Si se tuviera acceso a los datos de toda la convocatoria, se podría comparar '+
        'cuantas personas aplicaron, a donde, y cual es el porcentaje de aprovación.')
st.write('Así mismo, con esos datos se podría aplicar un modelo de regresión para saber cuales son las probabilidades de un candidato. Si se tienen los datos de puntaje final, y los diferentes criterios que se evaluaron. Muchos de esos datos son internos y privados de colfuturo, pero se podría estimar basados en otras caracteristicas y en heuristicas.')