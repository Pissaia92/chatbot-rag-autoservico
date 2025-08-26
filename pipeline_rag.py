import requests
import json
from config import HF_TOKEN, MODEL_NAME

class ChatAPI:
    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    def send_message(self, message):
        payload = {
            "inputs": f"Usuário: {message}\nAssistant:",
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            result = response.json()
            
            # Verifica se é uma lista e pega o primeiro resultado
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'Desculpe, não entendi.')
            else:
                return "Desculpe, não consegui processar sua mensagem."
                
        except Exception as e:
            return f"Erro na API: {str(e)}"

# Função principal que será importada pelo chat_interface.py
def pipeline(user_input):
    chat = ChatAPI()
    response = chat.send_message(user_input)
    return response

# Teste local (opcional)
if __name__ == "__main__":
    teste = pipeline("Olá, como você está?")
    print("Resposta:", teste)