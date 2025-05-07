# Predicción de Riesgo de Abandono Académico por Materia

Este repositorio contiene un sistema para predecir la probabilidad de abandono de los estudiantes en una materia específica, usando modelos de clasificación entrenados con datos históricos de esa misma materia.

Cada materia cuenta con su **propio modelo de riesgo** basado en datos de varios semestres. Los datos provienen del **Centro de Procesamiento de Datos** de la institución educativa.

---

## 📌 Características principales

* Clasificación binaria (`Riesgo` / `No Riesgo`) usando **RandomForestClassifier**.
* Generación dinámica de umbrales basados en percentiles (por defecto, el percentil 25).
* Generación de reglas de decisión personalizadas en Python o desde archivo `.txt`.
* Exportación de resultados y visualización en un dashboard HTML.

---

## 🔁 Flujo del sistema

El flujo completo está documentado en [Flujo\_del\_proceso.md](Flujo_del_proceso.md), incluyendo un diagrama **Mermaid**. En resumen:

1. Se carga el archivo `.csv` con los datos.
2. Se agregan las columnas `Riesgo` y `Alerta_Temprana`.
3. Se calculan umbrales para asistencia, notas y tareas.
4. Se aplican reglas del árbol de decisión.
5. Se generan alertas y se exporta un nuevo `.csv`.

---

## 📁 Archivos relevantes

* `data_processing.py` – Procesamiento de datos y generación de alertas.
* `train_model.py` – Entrenamiento del modelo Random Forest.
* `app.py` – Interfaz web para carga y análisis.
* `dashboard.html` – Frontend HTML para docentes.
* `generate_decision_tree_rules_from_txt_file.py` – Convierte reglas desde `.txt` a código Python.
* `decision_tree_rules.py` – Archivo generado con reglas codificadas.

---

## 📚 Documentación complementaria

* [Manual de Usuario Docente](.\doc\Manual_de_usuario_docente.md)
* [Manual Técnico del Personal](.\doc\Manual_de_usuario_personal_técnico.md)
* [Configuración de Reglas](.\doc\Configuración_manual_de_reglas.md)
* [Minería de Datos en el Proyecto](.\doc\Minería_de_datos_en_el_proyecto.md)
* [Train\_Model.md](.\doc\Train_Model.md) – Cómo trabaja el modelo Random Forest.
* [data\_processing.md](.\doc\data_processing.md) – Detalles de procesamiento.
* [calcular\_threasholds(umbral)\_para\_medir\_alertas\_de\_riesgo.md](.\doc\calcular_threasholds%28umbral%29_para_medir_alertas_de_riesgo.md) – Cálculo dinámico de umbrales.
* [Sugerencias\_para\_afinar\_Criterios\_en\_data\_processing.md](.\doc\Sugerencias_para_afinar_Criterios_en_data_processing.md) – Fundamentos teóricos y prácticos para mejorar los criterios.

---

## 📈 Recomendaciones para publicación

* Incluir capturas del dashboard en funcionamiento.
* Mencionar en LinkedIn que cada materia genera su propio modelo de riesgo.
* Puedes destacar el uso de minería de datos, aprendizaje automático y diseño accesible para docentes.

---

## 🧪 Cómo ejecutar

```bash
# Procesamiento de datos
data_processing.py entrada.csv salida.csv

# Entrenar modelo
train_model.py

# Levantar app web
app.py
```

---

## 🔐 Consideraciones éticas y técnicas

* Los datos deben anonimizarse si se usan fuera de la institución.
* Las alertas son **asistencias a la toma de decisiones** del docente, no juicios definitivos.

---

