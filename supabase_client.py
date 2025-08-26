from supabase import create_client
from dotenv import load_dotenv
import os
import sys

def load_env(company_token):
    # Define o caminho relativo para o .env
    dotenv_path = os.path.join(os.path.dirname(__file__), 'config', f'{company_token}.env')
    
    # Carrega o .env
    load_dotenv(dotenv_path)
    
    # Define variáveis globais
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    EMPRESA_TOKEN = os.getenv("EMPRESA_TOKEN")
    
    if not SUPABASE_URL or not SUPABASE_KEY or not EMPRESA_TOKEN:
        raise ValueError("Variáveis do .env estão faltando.")
    
    return SUPABASE_URL, SUPABASE_KEY, EMPRESA_TOKEN

# Cria cliente Supabase
SUPABASE_URL, SUPABASE_KEY, EMPRESA_TOKEN = load_env('empresa1')  # Altere para 'empresa2' se necessário
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate(token):
    try:
        result = supabase.table('empresas').select('id').eq('token', token).execute()
        return bool(result.data)
    except Exception as e:
        print(f"Erro na autenticação: {e}", file=sys.stderr)
        return False
