import streamlit as st
from datetime import datetime

# Función para procesar la pregunta
def responder_pregunta(pregunta):
    # Obtener la fecha y hora actuales
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Retornar la pregunta y la fecha en formato de respuesta
    return f"Pregunta: {pregunta}\nFecha y hora de la consulta: {fecha_actual}"

# Título de la app
st.title("Formulario de Preguntas")

# Crear el formulario
form = st.form(key="pregunta_form")
pregunta = form.text_input("Introduce tu pregunta:")
submit_button = form.form_submit_button("Obtener Respuesta")

# Mostrar la respuesta cuando se presiona el botón
if submit_button:
    if pregunta:
        respuesta = responder_pregunta(pregunta)
        st.write(respuesta)
    else:
        st.warning("Por favor, introduce una pregunta.")
