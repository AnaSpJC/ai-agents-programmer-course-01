# 📂 Reporte de Incidente: Configuración de Base de Datos de Vectores (ChromaDB)

**Proyecto:** Tech-Nova AI Agent  
**Entorno:** GitHub Codespaces / Python 3.12 (.venv)  
**Fecha:** Abril 2026  

---

## ⚠️ Problema: Error `404 NOT_FOUND` en Embeddings
Al intentar inicializar la base de datos de vectores con la librería `langchain-google-genai`, el sistema arrojó errores persistentes de "Modelo no encontrado", impidiendo la conversión de texto a vectores (Embeddings).

---

## 📋 Evolución de las Versiones (Autopsia Técnica)

### 1. `test_chroma_v1.py`: El Modelo Legacy
* **Intento:** Usar `models/embedding-001`.
* **Error:** `google.genai.errors.ClientError: 404 NOT_FOUND`.
* **Causa Probable:** El nombre del modelo estaba depreciado en la versión de la API (`v1beta`) invocada por la librería.

### 2. `test_chroma_v2.py`: El Modelo Moderno
* **Intento:** Actualizar a `models/text-embedding-004` (estándar de la industria en 2026).
* **Error:** `404 NOT_FOUND`.
* **Diagnóstico Presuntivo:** Incompatibilidad de nombres entre la cuenta de Google Cloud/AI Studio y los prefijos esperados por LangChain.

### 3. Script de Diagnóstico: `listar_modelos.py`
Para resolver la incertidumbre, se ejecutó un script utilizando `google.generativeai` para consultar directamente al servidor de Google qué modelos de tipo `embedContent` estaban habilitados para la API Key actual.
* **Resultado del Diagnóstico:** Se descubrió que los únicos nombres válidos eran:
    * `models/gemini-embedding-001`
    * `models/gemini-embedding-2-preview`

### 4. `test_chroma_v3.py`: Solución Final
* **Intento:** Configurar `GoogleGenerativeAIEmbeddings` con el nombre exacto: `models/gemini-embedding-001`.
* **Resultado:** **ÉXITO.**
* **Validación Semántica:** El sistema logró relacionar la pregunta *"¿Puedo pagar con Ethereum el martes?"* con la política de *"Criptomonedas los jueves"*, confirmando que la base de datos de vectores está operativa.

---

## 💡 Lecciones Aprendidas (Senior Insights)

1.  **Naming Over Documentation:** En el desarrollo de IA, los nombres de los modelos en la API cambian más rápido que los tutoriales. Si hay un 404, **no adivines**, consultá la lista de modelos del proveedor (`list_models`).
2.  **Importancia del "Upsert":** Cambiar `add()` por `upsert()` en ChromaDB evita errores de ejecución al re-correr scripts, permitiendo actualizar vectores existentes sin romper la base de datos.
3.  **Persistencia Local:** La carpeta `./chroma_db` creada en el entorno es el cerebro del agente. Se debe asegurar su exclusión en `.gitignore` para evitar subir datos binarios pesados al repositorio.

---