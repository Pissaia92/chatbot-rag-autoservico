import gradio as gr
import os
import shutil
import tempfile
from ingest import extract_text, chunk_text
from vector_db import add_chunks_to_collection

# Usar diretório temporário para uploads
UPLOAD_DIR = tempfile.mkdtemp()
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_document(file):
    if not file:
        return "Nenhum arquivo fornecido."
    
    temp_path = None
    try:
        # Usar caminho temporário seguro
        temp_path = os.path.join(UPLOAD_DIR, os.path.basename(file.name))
        
        # Copiar o arquivo para o diretório temporário
        with open(temp_path, "wb") as f:
            with open(file.name, "rb") as source_file:
                shutil.copyfileobj(source_file, f)
        
        # Processar o documento
        raw_text = extract_text(temp_path)        
        chunks = chunk_text(raw_text)        
        num_added = add_chunks_to_collection(chunks)        
        
        # Limpar arquivo temporário
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return f"✅ Documento processado!\n\nBlocos gerados: {len(chunks)}\nAdicionados ao banco: {num_added}"
    
    except Exception as e:
        # Limpeza em caso de erro
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return f"❌ Erro: {str(e)}"

# Configuração otimizada para Hugging Face Spaces
with gr.Blocks(
    title="Chatbot RAG Autosserviço"
) as demo:
    
    gr.Markdown("# 🤖 Chatbot RAG de Autosserviço")
    gr.Markdown("Faça upload de documentos (PDF, TXT, DOCX, CSV) para alimentar o conhecimento do chatbot.")

    with gr.Row():
        with gr.Column():
            file_input = gr.File(
                label="Upload de documento",
                file_types=[".pdf", ".txt", ".docx", ".csv"]
            )
            submit_btn = gr.Button("Processar Documento", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(label="Resultado", lines=10, interactive=False)

    submit_btn.click(fn=process_document, inputs=file_input, outputs=output)

# Para Hugging Face Spaces
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)