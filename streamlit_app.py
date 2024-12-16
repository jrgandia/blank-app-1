import streamlit as st
from datetime import datetime
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq

# Configuración
QDRANT_HOST = "http://localhost:6333"  # Cambia si usas un servidor remoto
COLLECTION_NAME = "pdf_embeddings"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 5  # Número de documentos relevantes a recuperar
GROQ_API_KEY="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"

# Inicialización de modelos y cliente
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
qdrant_client = QdrantClient(QDRANT_HOST)
groq_client = Groq(api_key=GROQ_API_KEY)

def query_qdrant(collection_name, query_text, top_k=TOP_K):
    """
    Realiza una búsqueda en Qdrant utilizando embeddings.
    """
    query_embedding = embedding_model.encode(query_text).tolist()
    
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )
    
    # Extraer texto relevante de los resultados
    documents = [hit.payload["text"] for hit in results]

    return documents
    



def generate_answer_with_groq(context, question):

    chat_completion = groq_client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[{
            "role": "user",
            "content": f"""
            Use the following CONTEXT to answer the QUESTION at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            CONTEXT: {context}
            QUESTION: {question}
            """
        }],

        # The language model which will generate the completion.
        model="llama-3.1-8b-instant",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Devolver la respuesta generada
    return chat_completion.choices[0].message.content

def responder_pregunta(query):
    # Recuperar documentos relevantes
    documents = query_qdrant(COLLECTION_NAME, query, top_k=TOP_K)

    # Combinar los documentos en un contexto
    context = "\n".join(documents)
    
    # Generar respuesta
    try:
        answer = generate_answer_with_groq(context, query)
        print("\nRespuesta:")
        print(answer)
    except Exception as e:
        answer = "Error generando respuesta: {e}"
        print(f""+answer) 
        
    
    return answer

def inicializa_formulario():
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

def main():
    inicializa_formulario()


if __name__ == "__main__":
    main()
