```markdown
# Manual del Usuario: Proceso de Análisis y Predicción de Riesgo de Abandono

## **1. Validación del Modelo**
1. Obtén un **DataSet** con los datos de los estudiantes.
2. Ejecuta el script `data_processing_training_rules.py` para validar el modelo.
   - Este script generará automáticamente las reglas a aplicar en el árbol de decisión, infiriéndolas de los datos de entrada.
   - Las reglas generadas se guardarán en el archivo `decision_tree_rules.py`.

3. **Validación de las Reglas**:
   - Las reglas generadas deben ser revisadas y validadas por un experto antes de ejecutar `data_processing.py`.
   - Si se desea, las reglas pueden ajustarse manualmente editando el archivo `decision_tree_rules.py`.

## **2. Procesamiento de Datos**
1. Ejecuta el script `data_processing.py` con el archivo de entrada y el archivo de salida como argumentos:
   ```bash
   python data_processing.py <input_file.csv> <output_file.csv>
   ```
   - Este script aplicará las reglas generadas en decision_tree_rules.py para procesar los datos.
   - El archivo de salida (por ejemplo, `datos_procesados.csv`) contendrá las alertas tempranas generadas.

## **3. Entrenamiento del Modelo**
1. Una vez generado el archivo de salida, procede a entrenar el modelo ejecutando el script model_training.py:
   ```bash
   python model_training.py
   ```
   - Este script entrenará el modelo de predicción de riesgo utilizando los datos procesados.

## **4. Predicción del Riesgo**
1. Ejecuta el script app.py para levantar un servidor web:
   ```bash
   python app.py
   ```
   - Esto habilitará la interfaz web para la predicción del riesgo de abandono.

2. Abre el archivo `dashboard.html` en un navegador web.
   - Este archivo actúa como la interfaz para que el docente interactúe con el sistema.

## **5. Uso del Dashboard**
1. El docente debe subir un archivo `.csv` con los datos de los estudiantes.
   - Este archivo puede ser obtenido desde la plataforma institucional o desde un reporte generado por el Centro de Procesamiento de Datos de la institución educativa.

2. Una vez cargado el archivo en `dashboard.html`, pulsa el botón **"Analizar"**.
   - El sistema procesará los datos y generará un dashboard en pantalla con un gráfico para una mejor visualización.

3. El dashboard generado puede ser exportado a un archivo `.csv` para su análisis posterior por parte del docente.

## **Notas Importantes**
- **Validación de Reglas**: Aunque las reglas se generan automáticamente, es altamente recomendable validarlas con un experto antes de su uso.
- **Modificación de Reglas**: Si es necesario, las reglas pueden ajustarse manualmente editando el archivo decision_tree_rules.py.
- **Exportación de Resultados**: Los resultados del análisis pueden ser exportados para su estudio detallado.


## Flujo del proceso de predicción, una vez que el docente sube sus datos

**No se depende de la columna `Estado Final` para realizar las predicciones**. A continuación, se detalla cómo funciona el flujo del archivo y cómo se generan las predicciones:

---

### **1. Flujo del archivo app.py**

#### **Carga del archivo CSV**
- El docente sube un archivo `.csv` a través del formulario en `dashboard.html`.
- El archivo se procesa en la ruta `/analizar` mediante el método `POST`.
- El sistema verifica que el archivo tenga las columnas mínimas requeridas:
  ```python
  required_cols = ['Asistencia (%)', 'Participación', 'Promedio Notas', 'Tareas Entregadas (10)']
  missing_cols = [col for col in required_cols if col not in df.columns]
  ```
  - Si faltan columnas, se devuelve un error indicando cuáles son las columnas faltantes.

#### **Predicción del riesgo**
- Si el modelo está cargado correctamente (`model` no es `None`), se realizan las predicciones.
- El sistema utiliza las siguientes columnas para generar las predicciones:
  ```python
  X = df[['Asistencia (%)', 'Promedio Notas', 'Tareas Entregadas (10)', 'Participación_encoded']]
  ```
  - **`Participación_encoded`**: Si el modelo incluye un encoder para la columna `Participación`, esta se transforma antes de ser utilizada.

- Las predicciones se generan utilizando el método `predict_proba` del modelo:
  ```python
  df['Probabilidad_Riesgo'] = model.predict_proba(X)[:, 1]
  ```

- Los niveles de alerta se asignan en función de la probabilidad de riesgo:
  ```python
  df['Nivel_Alerta'] = pd.cut(
      df['Probabilidad_Riesgo'],
      bins=[0, 0.4, 0.7, 1],
      labels=['Normal', 'Riesgo Moderado', 'Alto Riesgo']
  )
  ```

#### **Devolución de resultados**
- Los resultados se convierten a un formato JSON para ser enviados al cliente:
  ```python
  result = df.to_dict('records')
  return jsonify(result)
  ```

---

### **2. Verificación de la dependencia de `Estado Final`**

- En ningún lugar del código de app.py se utiliza la columna **`Estado Final`** para realizar las predicciones.
- Las predicciones dependen únicamente de las siguientes columnas:
  - **`Asistencia (%)`**
  - **`Promedio Notas`**
  - **`Tareas Entregadas (10)`**
  - **`Participación_encoded`** (si el modelo incluye un encoder para esta columna).

Esto significa que el sistema puede generar predicciones durante el semestre, siempre que se cuente con datos actualizados de asistencia, tareas entregadas, participación y calificaciones parciales.

---

### **3. Observaciones importantes**

1. **Entrenamiento del modelo**:
   - Aunque el archivo app.py no depende de `Estado Final`, para la predicción en abase a los datos actuales, si fue creado utilizándolo columna como parte del proceso de obtención de la columna `Riesgo`. Esto es algo que se puede verificar en el script de entrenamiento (`data_processing.py`).

2. **Predicciones en tiempo real**:
   - El sistema está diseñado para realizar predicciones basadas en los datos disponibles en el archivo `.csv` subido por el docente. Esto significa que puede generar alertas tempranas durante el semestre, siempre que los datos estén actualizados.

3. **Validación de columnas**:
   - El sistema valida que las columnas mínimas requeridas estén presentes en el archivo subido. Esto asegura que las predicciones se realicen correctamente.

---

### **4. Conclusión**

El archivo app.py **no depende de la columna `Estado Final` para realizar las predicciones**. Las predicciones se basan únicamente en las columnas de características (`Asistencia (%)`, `Promedio Notas`, `Tareas Entregadas (10)`, y opcionalmente `Participación_encoded`).

