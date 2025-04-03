# 🧠 PR Insight Agent
Este proyecto es un asistente basado en RAG (Retrieval-Augmented Generation) que permite:
- Cargar el contenido de un Pull Request de GitHub
- Analizarlo en el contexto completo del sistema
- Hacer preguntas técnicas sobre el PR o el código base
- Generar code reviews automáticos con trazabilidad vía Langfuse
---
## 🚀 Requisitos
- Python 3.10+
- [Ollama](https://ollama.com/) corriendo localmente (`ollama run mistral`)
- Una cuenta en [Langfuse](https://cloud.langfuse.com/) para trazabilidad
---
## ⚙️ Instalación
```bash
git clone https://github.com/tu-usuario/pr-insight-agent.git
cd pr-insight-agent
# Instalar dependencias
pip install -r requirements.txt
# Configurar credenciales
cp .env.template .env  # y editar con tus claves Langfuse
```

## 🧪 Uso
1. Levantar el backend
```bash
uvicorn chat_api:app --reload
```

2. Iniciar el cliente
```bash
python client.py
```

3. Comandos disponibles
- `load`: Cargar un Pull Request por número, usuario y repo
- `review`: Generar una revisión técnica del PR
- `exit`: Salir del cliente
- Escribí cualquier pregunta técnica sobre el PR o el sistema base

## 📦 Estructura del proyecto
```
.
├── chat_api.py          # Backend FastAPI con endpoints /ask, /load_pr, /review_pr
├── client.py            # CLI para interactuar con el agente
├── ingest_repo.py       # Ingesta código base y PRs a la vectorstore
├── langfuse_config.py   # Configuración global de Langfuse
├── prompting.py         # Prompts base y de revisión
├── memory/              # Descarga y parseo de PRs desde GitHub
├── cognition/           # Ingesta y embebido de código
├── data/vectorstore/    # Base semántica persistente (autogenerada)
├── repos/               # Archivos de PR temporales (autogenerado)
└── .env                 # Tus claves privadas (no subir)
```

## 📊 Langfuse
El proyecto genera trazas automáticas de cada interacción del modelo en:
https://cloud.langfuse.com

Verás:
- Prompts enviados
- Respuestas generadas
- Tiempo de ejecución
- Errores y metadata adicional

## 🛡️ Seguridad
- No subas .env a Git.
- No compartas tu vectorstore si contiene código privado.