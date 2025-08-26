import gradio as gr
from supabase_client import supabase
import numpy as np
import matplotlib.pyplot as plt

def get_metrics():
    # Buscar todas as interações
    response = supabase.table('interactions').select('*').execute()
    interactions = response.data
    
    if not interactions:
        return 0, 0.0, 0.0, 0.0
    
    total_interactions = len(interactions)
    
    # Taxa de deflexão (100% no MVP, já que todas as interações são respondidas pelo bot)
    deflexion_rate = 100.0
    
    # Feedback positivo
    positive_feedback = sum(1 for i in interactions if i['feedback'] is True)
    negative_feedback = total_interactions - positive_feedback
    positive_rate = (positive_feedback / total_interactions) * 100 if total_interactions > 0 else 0.0
    
    # Tempo médio de resposta (simulado, já que não temos dados de tempo real)
    avg_response_time = 2.5  # segundos (valor médio simulado)
    
    return total_interactions, deflexion_rate, positive_rate, avg_response_time

def update_metrics():
    total, deflexion, positive, avg_time = get_metrics()
    return (
        f"{total} interações",
        f"{deflexion:.2f}%",
        f"{positive:.2f}%",
        f"{avg_time:.2f} segundos"
    )

def plot_feedback():
    response = supabase.table('interactions').select('*').execute()
    interactions = response.data
    
    if not interactions:
        return None
    
    positive_feedback = sum(1 for i in interactions if i['feedback'] is True)
    negative_feedback = len(interactions) - positive_feedback
    
    labels = ['Positivo', 'Negativo']
    sizes = [positive_feedback, negative_feedback]
    colors = ['#4CAF50', '#F44336']
    
    plt.figure(figsize=(6, 4))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Feedback dos Usuários')
    
    return plt.gcf()

def handle_like(history):
    # Salva feedback positivo
    if history:
        question, answer = history[-1]
        supabase.table('interactions').update({'feedback': True}).eq('question', question).execute()
    return history

def handle_dislike(history):
    # Salva feedback negativo
    if history:
        question, answer = history[-1]
        supabase.table('interactions').update({'feedback': False}).eq('question', question).execute()
    return history

with gr.Blocks(title="Dashboard de Métricas") as dashboard:
    gr.Markdown("# 📊 Dashboard de Métricas do Chatbot RAG")
    
    gr.Markdown("### Métricas em Tempo Real")
    with gr.Row():
        total_interactions = gr.Textbox(label="Total de Interações", value="0 interações")
        deflexion_rate = gr.Textbox(label="Taxa de Deflexão", value="0.00%")
        positive_rate = gr.Textbox(label="Feedback Positivo", value="0.00%")
        avg_response_time = gr.Textbox(label="Tempo Médio de Resposta", value="0.00 segundos")
    
    with gr.Row():
        like_button = gr.Button("👍", variant="primary")
        dislike_button = gr.Button("👎", variant="primary")
    
    feedback_plot = gr.Plot(label="Feedback dos Usuários")
    
    like_button.click(
        fn=lambda history: handle_like(history) + update_metrics(),
        inputs=gr.State([]),
        outputs=[total_interactions, deflexion_rate, positive_rate, avg_response_time, feedback_plot]
    )
    
    dislike_button.click(
        fn=lambda history: handle_dislike(history) + update_metrics(),
        inputs=gr.State([]),
        outputs=[total_interactions, deflexion_rate, positive_rate, avg_response_time, feedback_plot]
    )

dashboard.launch()