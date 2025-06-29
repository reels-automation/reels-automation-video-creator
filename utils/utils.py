import json
import requests
import os 
import unicodedata
import re
from dotenv import load_dotenv  

load_dotenv()

model = os.getenv("OLLAMA_MODEL")
OLLAMA_IP = os.getenv("OLLAMA_IP")


import unicodedata
import re

def sanitize_attribute(attribute: str):
    """Sanitiza un input para que no contenga caracteres que no puedan ser parseados

    Args:
        attribute (str):

    Returns:
        (str):
    """
    if attribute is not None:
        result = (
            unicodedata.normalize("NFKD", attribute)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
        # Modify the regex to exclude dots
        result = re.sub(r"[^a-zA-Z0-9._-]", " ", result)
        result = result.strip()
        return result
    return None

    

def generate(prompt:str, context:list[str]=[]) -> str:
    """Genera un prompt de Ollama

    Args:
        prompt (str): El prompt que se le pasa al modelo de lenguaje
        context (list[str]): El contexto que se tiene de otros mensajes

    Returns:
        Response(str): El texto que generó el modelo de lenguaje
    """
    r = requests.post(OLLAMA_IP,
                      json={
                          'model': model,
                          'prompt': prompt,
                          'context': context,
                      },
                      stream=True, timeout=100)
    
    r.raise_for_status()

    full_response = ""  # To store the concatenated text response

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        # the response streams one token at a time, print that as we receive it
        print(response_part, end='', flush=True)

        # Append each part of the response to the full text
        full_response += response_part

        if 'error' in body:
            raise Exception(body['error']) 

        if body.get('done', False):
            return full_response  # Return the full response as text


def get_keywords(keywords:list[str]):
    print("here kwyword", keywords)

    keywords = str(keywords)
    prompt = f"""
            
    GGenera 5 frases separadas que enfatizan el contenido relacionado con las siguientes palabras {keywords}. Cada frase debe ser relevante y representar bien el tema de las palabras que se te dan. Estas frases se usarán para generar búsquedas de GIFs. Asegúrate de que las frases sean concisas y útiles para encontrar GIFs en un motor de búsqueda como Giphy o Tenor. Cada frase debe estar separada por comas y seguir este formato:

[FRASE 1, FRASE 2, FRASE 3, FRASE 4, FRASE 5]

Ejemplo de salida esperada:

["Las mejores bandas de rock", "El renacimiento del punk rock", "Conciertos icónicos de Green Day", "La evolución del punk a lo largo de las décadas", "Recuerdos de los años 90 con Green Day"]

Instrucciones adicionales:

    Las frases deben ser claras, concisas y fáciles de buscar.
    No incluyas mensajes extra como "Aquí están tus frases" o similares.
    Las frases deben estar separadas por comas, tal como se indica en el formato.
            
            """
    
    return generate(prompt)

def clean_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*,()\[\]]', ' ', filename)
    filename = ' '.join(filename.split())
    return filename

def create_folders():
    folders = ['./temp_vids', './temp_storage_web', './temp_storage_minio_public', './temp_storage_minio','./temp_images'  ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)