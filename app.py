from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: chave GROQ_API_KEY não definida no .env")

chat = ChatGroq(model="llama-3.3-70b-versatile")

documento = None

def carregar_documento():
    global documento
    if documento is None:
        loader = WebBaseLoader("https://fsn-5-grupo-02-autopecas.vercel.app/")
        documentos_site = loader.load()
        documento = ""
        for doc in documentos_site:
            documento += doc.page_content

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return "O chatbot OlimpIA está online. Use /chat para interagir."

def resposta_bot(mensagens, documento):
    try:
        message_system = """Você é um assistente amigável chamado OlimpIA que utiliza as seguintes informações para formular as suas respostas de forma simples, resumida e direta, mas com os detalhes necessários: {informacoes}."""
        mensagens_modelo = [("system", message_system)]
        for msg in mensagens:
            if isinstance(msg, dict):
                sender = msg.get('sender', 'user')
                content = msg.get('content', '')
                if sender == 'bot':
                    sender = 'assistant'
                mensagens_modelo.append((sender, content))
            else:
                print(f"Mensagem inválida: {msg}")
        template = ChatPromptTemplate.from_messages(mensagens_modelo)
        chain = template | chat
        resposta = chain.invoke({"informacoes": documento}).content
        return resposta
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, houve um erro ao processar sua mensagem."

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    try:
        if documento is None:
            carregar_documento()
        data = request.json
        mensagens = data.get("mensagens", [])
        resposta = resposta_bot(mensagens, documento)
        return jsonify({"resposta": resposta})
    except Exception as e:
        print(f"Erro ao processar requisição: {e}")
        return jsonify({"resposta": "Erro no servidor."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
