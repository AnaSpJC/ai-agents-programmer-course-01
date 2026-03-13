# Registro de Incidencias y Resolución (Marzo 2026)

Este documento detalla los errores encontrados durante el desarrollo del proyecto, sus causas técnicas y las soluciones aplicadas para asegurar la estabilidad del entorno.

---

## 1. Error de Librería Depreciada
* **Problema:** `google.generativeai` lanzó un `FutureWarning` y fallos de conexión.
* **Causa:** Google migró la librería oficial a una versión más moderna y ligera.
* **Solución:** Desinstalación del paquete antiguo e instalación de `google-genai`.

```python
# Importación actualizada
from google import genai
```

## 2. Error de Importación (`ModuleNotFoundError`)
* **Problema:** Python no encontraba el módulo `genai`, a pesar de haber ejecutado la instalación.
* **Causa:** Desincronización entre la instalación global y el entorno virtual (`.venv`) en Codespaces, sumado a la confusión entre el nombre del paquete (`google-genai`) y el módulo (`genai`).
* **Solución:** Instalación forzada a través del módulo de Python para asegurar el destino en el entorno activo.

```bash
python3 -m pip install google-genai
```

## 3. Error 404 - Modelo No Encontrado (`NOT_FOUND`)
* **Problema:** El servidor indicaba que modelos como `gemini-1.5-flash` no existían.
* **Causa:** * Errores tipográficos (ej. `105` en lugar de `1.5`).
    * Retiro del modelo `1.5-flash` de la cuota gratuita para priorizar versiones más nuevas (`2.5` y `3`).
* **Solución:** Implementación de un script de diagnóstico (`listar_modelos.py`) para verificar los modelos disponibles en tiempo real.
## 4. Error 429 - Recurso Agotado (`RESOURCE_EXHAUSTED`)
* **Problema:** El modelo `gemini-2.0-flash` rechazaba las peticiones por falta de cuota.
* **Causa:** Las cuentas gratuitas tienen límites estrictos (o nulos) para modelos específicos en fase de alta demanda.
* **Solución:** Cambiamos el modelo a `gemini-2.5-flash`, que según la lista de diagnóstico, es el modelo estándar con cuota activa para este proyecto.

---

## Configuración Final Exitosa

|   Componente | Detalle |
|   ---------- | ------- |
| **Librería** | `google-genai` (v1.66.0+)   |
| **Cliente**  | `genai.Client(api_key=...)` |
| **Modelo Utilizado** | `gemini-2.5-flash`  |
