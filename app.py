from flask import Flask, render_template, request, jsonify
import requests
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from stella_data import SYSTEM_PROMPT, QUESTION_PROGRESSION, COMPANY_INFO, DESTINATIONS_DATA

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar Perplexity
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

conversations = {}

class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "messages": [],
            "question_count": 0,
            "responses": {
                "ciudad": None,
                "clima": None,
                "cultura": None,
                "objetivo": None,
                "presupuesto": None
            },
            "lead_data": None,
            "created_at": datetime.now().isoformat()
        }
        return session_id
    
    def get_session(self, session_id):
        return self.sessions.get(session_id)
    
    def add_message(self, session_id, role, content):
        if session_id in self.sessions:
            self.sessions[session_id]["messages"].append({
                "role": role,
                "content": content
            })
    
    def get_messages(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]["messages"]
        return []

manager = SessionManager()

def call_perplexity(system_prompt, user_prompt):
    """Llamar a Perplexity API directamente"""
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    except requests.exceptions.Timeout:
        return "Lo siento, la respuesta tardó demasiado. ¿Podrías intentar de nuevo? ⏱️"
    except requests.exceptions.RequestException as e:
        print(f"Error en Perplexity: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        print(f"Error general: {e}")
        return "Lo siento, tuve un problema. ¿Intentamos de nuevo? 🤖"

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/api/stella/start", methods=["POST"])
def start():
    session_id = manager.create_session()
    
    messages = [
        "¡Hola! Soy **Stella**, tu guía de STUNET. 🌍",
        "Te ayudaré a encontrar tu destino internacional ideal con unas breves preguntas.",
        "**Primera pregunta:** ¿Prefieres estudiar o vivir en una **ciudad grande**, **mediana**, **pequeña**, o **te adaptas a cualquier lugar**?"
    ]
    
    for msg in messages:
        manager.add_message(session_id, "assistant", msg)
        
    manager.sessions[session_id]["question_count"] = 1
    
    return jsonify({
        "session_id": session_id,
        "messages": messages
    })

@app.route("/api/stella/message", methods=["POST"])
def message():
    data = request.json
    sid = data["session_id"]
    user_msg = data["message"]
    
    session = manager.get_session(sid)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    # Guardar mensaje del usuario
    manager.add_message(sid, "user", user_msg)
    
    # Obtener contexto
    messages = manager.get_messages(sid)
    question_count = session["question_count"]
    
    # Construir historial
    chat_history = "\n".join([
        f"Usuario: {m['content']}" if m['role'] == 'user' 
        else f"Stella: {m['content']}" 
        for m in messages[-10:]
    ])
    
    # Determinar qué hacer
    if question_count < 5:
        current_question = QUESTION_PROGRESSION[question_count]["question"]
        next_question = QUESTION_PROGRESSION[question_count + 1]["question"]
        
        prompt = f"""Eres Stella, asistente de STUNET. El usuario está respondiendo a la pregunta {question_count}.
        
Pregunta actual: "{current_question}"
Respuesta del usuario: "{user_msg}"

Tu tarea:
1. Analiza si la respuesta del usuario es acorde a lo que se le preguntó (aunque sea breve o informal).
2. Si la respuesta es VÁLIDA: responde con "VALID: [Tu comentario natural y amable] + [Siguiente pregunta: {next_question}]"
3. Si la respuesta es INVÁLIDA o no tiene sentido en el contexto: responde con "INVALID: [Comentario amable explicando por qué necesitas esa información] + [Repite la pregunta: {current_question}]"

IMPORTANTE: Empieza SIEMPRE con "VALID:" o "INVALID:". Sé breve y amigable."""
    
    elif question_count == 5:
        current_question = QUESTION_PROGRESSION[5]["question"]
        prompt = f"""Eres Stella. El usuario respondió la última pregunta (5).
        
Pregunta actual: "{current_question}"
Respuesta del usuario: "{user_msg}"

Tu tarea:
1. Analiza si la respuesta es válida para el presupuesto.
2. Si es VÁLIDA: responde con "VALID: [Comento sobre su presupuesto] + [Recomienda 3 destinos ideales (España, Australia, Nueva Zelanda, Malta, Irlanda, Canadá) con por qué, costo, trabajo] + [Pide datos: '¿Me compartes tus datos para poder ayudarte mejor?']"
3. Si es INVÁLIDA: responde con "INVALID: [Comentario amable] + [Repite la pregunta: {current_question}]"

IMPORTANTE: Empieza SIEMPRE con "VALID:" o "INVALID:"."""
    
    else:
        prompt = f"""Eres Stella. El usuario está compartiendo sus datos.

Respuesta: {user_msg}

Tu tarea:
Responde con "VALID: [Reconoce datos, agradece y dile que STUNET se contactará pronto]"

IMPORTANTE: Empieza con "VALID:"."""
    
    # Llamar a Perplexity
    raw_response = call_perplexity(SYSTEM_PROMPT, prompt)
    
    # Procesar lógica de validación
    is_valid = raw_response.startswith("VALID:")
    assistant_msg = raw_response.replace("VALID:", "").replace("INVALID:", "").strip()
    
    # Limpiar posibles citas tipo [1][2] que Perplexity a veces incluye por error
    import re
    assistant_msg = re.sub(r'\[\d+\]', '', assistant_msg)
    
    # Asegurar que no queden referencias residuales
    assistant_msg = assistant_msg.replace("[1]", "").replace("[2]", "").replace("[3]", "").replace("[4]", "").replace("[5]", "")
    
    # Detectar si estamos en el cierre de recomendaciones o pidiendo datos
    is_recommendation = any(kw in assistant_msg.lower() for kw in ["recomiendo", "estos son", "mejores opciones", "puedes estudiar"])
    requesting_data = any(kw in assistant_msg.lower() for kw in ["compartes tus datos", "tus datos", "formulario", "tu correo"])
    
    # Guardar respuesta limpia
    manager.add_message(sid, "assistant", assistant_msg)
    
    # Incrementar contador SOLO si es válido y no estamos en el final
    if is_valid and question_count < 5:
        manager.sessions[sid]["question_count"] += 1
    elif is_valid and question_count == 5:
        manager.sessions[sid]["question_count"] = 6 # Pasar a etapa de datos
    
    return jsonify({
        "response": assistant_msg,
        "session_id": sid,
        "question_number": manager.sessions[sid]["question_count"],
        "requesting_lead": requesting_data,
        "is_recommendation": is_recommendation,
        "is_valid": is_valid
    })

@app.route("/api/stella/lead", methods=["POST"])
def capture_lead():
    data = request.json
    sid = data["session_id"]
    
    lead_data = {
        "session_id": sid,
        "nombre": data.get("nombre"),
        "email": data.get("email"),
        "whatsapp": data.get("whatsapp"),
        "pais": data.get("pais"),
        "timestamp": datetime.now().isoformat()
    }
    
    # Guardar
    session = manager.get_session(sid)
    if session:
        session["lead_data"] = lead_data
    
    print(f"✅ Lead: {lead_data['nombre']} ({lead_data['email']})")
    
    return jsonify({
        "status": "success",
        "message": "¡Perfecto! 🎉 Gracias. El equipo de STUNET te contactará pronto. 🌍"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
