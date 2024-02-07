import streamlit as st
import requests
import os
import re

# Reemplaza "tu_clave_de_api_aqui" con tu clave de API real
API_KEY = "fcbfdfe8-e9ed-41f3-a7d8-b6587538e84e"

def get_api_response(question):
    url = "https://api.afforai.com/api/api_completion"
    payload = {
        "apiKey": API_KEY,
        "sessionID": "65489d7c9ad727940f2ab26f",
        "history": [{"role": "user", "content": question}],
        "powerful": True,
        "google": True
    }

    response = requests.post(url, json=payload)
    return response.json()

def extract_source(completion):
    # Busca el patrón 【3†source】 y extrae la información de la fuente
    source_pattern = "【\\d+†source】"
    source_match = re.search(source_pattern, completion)
    
    if source_match:
        source_text = source_match.group(0)
        source_number = re.search(r"\d+", source_text).group(0)
        source_name = f"NombreFuente{source_number}"
        source_url = f"https://URLFuente{source_number}.com"
        return source_name, source_url, source_number  # Agregado source_number

    return None, None, None

def main():
    st.title("Preguntas sobre las leyes de Guatemala")
    question = st.text_input("Escribe tu pregunta")
    
    if st.button("Enviar"):
        response = get_api_response(question)
        completion = response.get('output', {}).get('completion', '')
        
        # Extraer información de la fuente
        source_name, source_url, source_number = extract_source(completion)  # Agregado source_number

        # Reemplazar la cadena en el texto de completitud
        if source_name and source_url:
            completion = completion.replace(f"【{source_number}†source】", f"Fuente: [{source_name}]({source_url})")

        st.markdown(completion)

if __name__ == "__main__":
    main()
 
