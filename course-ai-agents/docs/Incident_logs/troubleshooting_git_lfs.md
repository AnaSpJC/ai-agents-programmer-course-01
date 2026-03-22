# Troubleshooting Log: Resolución de Conflicto de Tamaño de Archivos en Git

**ID del Incidente:** 002  
**Fecha:** 22 de marzo de 2026  
**Autor:** AnaSpJC  
**Estado:** Resuelto  

---

## 1. Descripción del Problema
Al intentar realizar un `git push` desde GitHub Codespaces hacia el repositorio remoto, el proceso falló con una advertencia de seguridad técnica debido al tamaño de los archivos.

### Mensaje de Error de GitHub:
> `remote: warning: File course-ai-agents/.venv/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so is 52.41 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB`

El sistema identificó archivos binarios dentro del entorno virtual (`.venv`) que exceden el límite de gestión estándar de Git, sugiriendo el uso de Git LFS (Large File Storage).

---

## 2. Diagnóstico Técnico
El problema no residía en el código del agente, sino en la **arquitectura del repositorio**.

1.  **Fuga del Entorno Virtual:** La carpeta `.venv` (donde se instalan las librerías como `ChromaDB` y `LlamaIndex`) estaba siendo rastreada por Git por error.
2.  **Fallo en la Exclusión:** El archivo `.gitignore` inicial contenía la instrucción `venv/`, pero la carpeta física se llamaba `.venv/`. En sistemas Linux (Codespaces), la diferencia de un punto (`.`) hace que las rutas sean totalmente distintas.
3.  **Dependencias Compiladas:** Librerías de IA modernas utilizan archivos `.so` (Shared Objects) compilados en Rust para optimizar la velocidad. Estos archivos son binarios pesados que no deben versionarse en Git.

---

## 3. Información Recopilada para la Solución
Para abordar el problema sin riesgo de pérdida de datos, se extrajo la siguiente información del sistema:

* **Listado de Dependencias (pip freeze):** Confirmó la presencia de paquetes pesados (ChromaDB, LangChain, LlamaIndex).
* **Mapeo de Directorios (ls -R):** Validó que los archivos de datos (/docs) y los scripts del agente estaban fuera de la zona de riesgo.
* **Gestión de Secretos:** Se confirmó que las API Keys residían en un archivo .env para asegurar que permanecieran privadas.
* **Validación de Ejecución:** Se confirmó que el agente leía archivos correctamente antes de iniciar la limpieza.

---

## 4. Solución Implementada
Se optó por una **limpieza de historial y desvinculación de dependencias**.

### Paso 1: Corrección del .gitignore
Se actualizó el archivo para ignorar explícitamente el entorno virtual y los binarios:
- .venv/
- __pycache__/
- .env
- *.so

### Paso 2: Remoción del Índice (Cache)
Se ejecutó el comando para "olvidar" la carpeta pesada sin borrarla del disco local:
`git rm -r --cached .venv`

### Paso 3: Consolidación y Respaldo
* Se realizó un `commit` de limpieza y un `push origin main` exitoso.
* Se generó un archivo `requirements.txt` para permitir la reconstrucción del entorno en cualquier momento ejecutando `pip freeze > requirements.txt`.

---

## 5. Conclusión y Mejores Prácticas
1.  **Portabilidad:** Un repositorio profesional solo debe contener código y configuración. Las librerías se instalan bajo demanda usando el requirements.txt.
2.  **Higiene de Git:** El uso correcto del punto en las rutas del .gitignore es crítico para evitar el rastreo accidental de archivos de sistema o dependencias pesadas.
3.  **Integridad:** El agente sigue funcionando perfectamente en el entorno local (Codespace), mientras que el repositorio en la nube ahora es ligero y eficiente.