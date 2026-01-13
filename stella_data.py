DESTINATIONS_DATA = {
    "españa": {
        "ciudades": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Málaga"],
        "costo": "EUR 2.500+",
        "trabajo": "30 horas/semana",
        "clima": "Soleado y templado",
        "empleabilidad": "Hostelería, negocios, tech",
        "programas": ["Prácticas", "Cursos cortos", "FP", "Grados", "Másters"],
        "visas": "93% éxito"
    },
    "australia": {
        "ciudades": ["Sídney", "Melbourne", "Brisbane", "Perth"],
        "costo": "AUD 2.900+",
        "trabajo": "20 horas/semana",
        "clima": "Soleado, estaciones marcadas",
        "empleabilidad": "Hospitalidad, administración, construcción, tech",
        "programas": ["Idiomas", "VET", "Grados", "Másters"],
        "visas": "8-16 semanas"
    },
    "nueva zelanda": {
        "ciudades": ["Auckland", "Wellington", "Christchurch", "Queenstown"],
        "costo": "NZD 3.900+",
        "trabajo": "20 horas/semana, tiempo completo en vacaciones",
        "clima": "Templado, muy variado",
        "empleabilidad": "Hospitalidad, turismo, construcción, tech",
        "programas": ["Inglés", "VET", "Grados", "Másters"],
        "visas": "4-8 semanas"
    },
    "malta": {
        "ciudades": ["St. Julian's"],
        "costo": "EUR 2.490+",
        "trabajo": "20 horas/semana (después de 90 días)",
        "clima": "Mediterráneo",
        "empleabilidad": "Turismo, hostelería, iGaming, atención al cliente",
        "programas": ["Inglés", "Cursos cortos", "Formación profesional"],
        "visas": "4-8 semanas"
    },
    "dubai": {
        "ciudades": ["Dubai Marina", "Downtown Dubai"],
        "costo": "USD 2.900+",
        "trabajo": "Depende del programa",
        "clima": "Desértico, cálido todo el año",
        "empleabilidad": "Turismo, hotelería, negocios, tech",
        "programas": ["Inglés", "Inglés para negocios", "Cursos cortos"],
        "visas": "2-4 semanas"
    },
    "irlanda": {
        "ciudades": ["Dublín", "Cork"],
        "costo": "EUR 3.590+",
        "trabajo": "20 horas/semana, 40 en vacaciones",
        "clima": "Oceánico, templado",
        "empleabilidad": "Tech, servicios, hotelería, finanzas",
        "programas": ["Inglés", "Formación profesional", "Grados", "Másters"],
        "visas": "4-8 semanas"
    },
    "reino unido": {
        "ciudades": ["Londres", "Manchester", "Liverpool", "Birmingham"],
        "costo": "GBP 3.900+",
        "trabajo": "Depende del programa",
        "clima": "Templado, variable",
        "empleabilidad": "Finanzas, tech, educación",
        "programas": ["Inglés", "Grados", "Másters"],
        "visas": "Varía según programa"
    },
    "canada": {
        "ciudades": ["Toronto", "Vancouver", "Montreal"],
        "costo": "CAD 3.900+",
        "trabajo": "Varía según programa",
        "clima": "Continental a templado",
        "empleabilidad": "Tech, servicios, administración",
        "programas": ["Inglés", "Grados", "Másters"],
        "visas": "4-12 semanas"
    },
    "Francia": {
        "ciudades": ["París", "Montpellier", "Marsella", "Lyon"],
        "costo": "EUR 3.900+",
        "trabajo": "20 horas/semana",
        "clima": "Templado, mediterráneo en el sur",
        "empleabilidad": "Cultura, arte, negocios",
        "programas": ["Francés", "Grados", "Másters"],
        "visas": "Varía según nacionalidad"
    },
    "alemania": {
        "ciudades": ["Berlín", "Munich", "Hamburgo"],
        "costo": "EUR 2.900+",
        "trabajo": "120 días completos o 240 semi",
        "clima": "Continental, templado",
        "empleabilidad": "Ingeniería, tech, manufactura",
        "programas": ["Inglés", "Grados", "Másters"],
        "visas": "Rápido (4-6 semanas)"
    }
}

QUESTION_PROGRESSION = {
    1: {
        "question": "¿Prefieres una ciudad grande y cosmopolita, mediana, pequeña, o te adaptas a cualquier lugar?",
        "key": "ciudad"
    },
    2: {
        "question": "¿Qué clima prefieres: cálido, templado o frío?",
        "key": "clima"
    },
    3: {
        "question": "¿Qué tipo de cultura buscas: latina, europea, multicultural u otra?",
        "key": "cultura"
    },
    4: {
        "question": "¿Cuál es tu objetivo: estudiar + trabajar, perfeccionar idioma, hacer prácticas o experiencia cultural?",
        "key": "objetivo"
    },
    5: {
        "question": "¿Cómo es tu presupuesto: ajustado, medio o flexible?",
        "key": "presupuesto"
    }
}

COMPANY_INFO = {
    "nombre": "STUNET",
    "estudiantes": "7.500+",
    "satisfaccion": "98%",
    "tasa_visas": "93%",
    "anos": "8+",
    "whatsapp": "+57 302 854 6449",
    "email": "marketing@stunet.com.au",
    "oficinas": ["Sydney, Australia", "Bogotá, Colombia", "CDMX, México"]
}

SYSTEM_PROMPT = """Eres STELLA, asistente de IA de STUNET, una agencia de experiencias internacionales.

Tu misión: Ayudar a estudiantes a encontrar su destino internacional PERFECTO.

## IMPORTANTE - FLUJO CONVERSACIONAL:
- Eres amigable, empático y entusiasta
- Haz UNA pregunta a la vez (no múltiples)
- Escucha activamente y responde naturalmente a lo que dicen
- Usa el nombre de la persona si la preguntó
- Celebra sus respuestas ("¡Excelente!", "Qué genial!", etc.)

## PROCESO (5 PREGUNTAS CLAVE):
Debes hacer estas 5 preguntas en orden:
1. Tipo de ciudad (grande/mediana/pequeña)
2. Clima preferido (cálido/templado/frío)
3. Tipo de cultura (latina/europea/multicultural)
4. Objetivo (estudiar+trabajar/idioma/prácticas/experiencia)
5. Presupuesto (ajustado/medio/flexible)

## DESPUÉS DE LAS 5 PREGUNTAS:
- Analiza sus respuestas
- Recomienda los 3 MEJORES destinos con razones específicas
- Menciona qué pueden estudiar en cada uno
- Cuenta sobre el costo, trabajo y visa

## DESTINOS DISPONIBLES:
España, Australia, Nueva Zelanda, Malta, Dubái, Irlanda, Reino Unido, Canadá, Francia, Alemania, Italia, China, Estados Unidos

## TONO Y ESTILO:
- Conversacional (NO formal)
- Usa emojis ocasionalmente 😊
- Responde en ESPAÑOL
- Sé breve pero acogedor
- Muestra entusiasmo por sus planes

## CIERRE:
Cuando termines las recomendaciones, pide gentilmente:
"Para poder ayudarte mejor con tu próximo paso, ¿me compartes tus datos?"
- Nombre
- Email
- WhatsApp
- País de residencia
"""
