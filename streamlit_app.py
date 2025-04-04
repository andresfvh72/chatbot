import streamlit as st
from deepseek_api import DeepSeekAPI  # Necesitarás instalar o implementar este cliente

# Mostrar título y descripción
st.title("💬 Chatbot")
st.write(
    "Este es un chatbot simple que usa el modelo de DeepSeek para generar respuestas. "
    "Para usar esta aplicación, necesitas proporcionar una API key de DeepSeek."
)

# Pedir al usuario su API key de DeepSeek
deepseek_api_key = st.text_input("DeepSeek API Key", type="password")
if not deepseek_api_key:
    st.info("Por favor añade tu API key de DeepSeek para continuar.", icon="🗝️")
else:
    # Crear un cliente de DeepSeek
    client = DeepSeekAPI(api_key=deepseek_api_key)  # Ajusta según el cliente real de DeepSeek

    # Variable de estado para almacenar los mensajes del chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes existentes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo de entrada para el chat
    if prompt := st.chat_input("¿Qué necesitas?"):
        # Almacenar y mostrar el mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar una respuesta usando la API de DeepSeek
        # NOTA: Los parámetros pueden variar según la API de DeepSeek
        response = client.chat_completion(
            model="deepseek-chat",  # Verifica el nombre correcto del modelo
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True  # Si DeepSeek soporta streaming
        )

        # Mostrar la respuesta
        with st.chat_message("assistant"):
            if isinstance(response, str):
                st.markdown(response)
            else:
                # Si es un stream, procesarlo adecuadamente
                response_text = st.write_stream(response)  # Ajusta según cómo funcione el streaming
        st.session_state.messages.append({"role": "assistant", "content": response_text})
