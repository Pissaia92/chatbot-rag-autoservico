import pipeline_rag
from supabase_client import supabase, EMPRESA_TOKEN

# Teste simples
def test_pipeline():
    question = "Qual é a política de devolução?"
    context = pipeline_rag.pipeline(question)
    print(f"Contexto encontrado: {context}")
    
    # Salva interação (opcional)
    empresa_id = supabase.table('empresas').select('id').eq('token', EMPRESA_TOKEN).execute().data[0]['id']
    data = {
        "question": question,
        "answer": "Resposta gerada pelo Qwen",
        "context": context,
        "feedback": True,
        "empresa_id": empresa_id
    }
    supabase.table('interactions').insert(data).execute()

# Execute o teste
test_pipeline()