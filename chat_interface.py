import gradio as gr
from pipeline_rag import pipeline

def chat_fn(message, history):
    response = pipeline(message)
    return response

with gr.Blocks(title="Chatbot RAG") as demo:
    gr.Markdown("# 🤖 Chatbot de Atendimento")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Sua mensagem")
    clear = gr.Button("Limpar")
    
    def respond(message, chat_history):
        bot_message = pipeline(message)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=True)