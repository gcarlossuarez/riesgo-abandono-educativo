## ANÁLISIS DE LAS REGLAS APRENDIDAS POR EL ÁRBOL DE DECISIÓN

- **Promedio Notas <= 50.30**
  - **class: 1**
- **Promedio Notas > 50.30**
  - **Asistencia (%) <= 60.00**
    - **class: 1**
  - **Asistencia (%) > 60.00**
    - **Asistencia (%) <= 63.50**
      - **class: 0**
    - **Asistencia (%) > 63.50**
      - **class: 0**


El árbol de decisión ha aprendido reglas basadas en los datos proporcionados. se van a analizar las reglas aprendidas y lo que significan:

---

### **Reglas aprendidas por el árbol de decisión**
```plaintext
|--- Promedio Notas <= 50.30
|   |--- class: 1
|--- Promedio Notas >  50.30
|   |--- Asistencia (%) <= 60.00
|   |   |--- class: 1
|   |--- Asistencia (%) >  60.00
|   |   |--- Asistencia (%) <= 63.50
|   |   |   |--- class: 0
|   |   |--- Asistencia (%) >  63.50
|   |   |   |--- class: 0
```

---

### **Interpretación de las reglas**

1. **Primera regla: `Promedio Notas <= 50.30`**
   - Si el promedio de notas de un estudiante es menor o igual a **50.30**, el árbol clasifica al estudiante como en **riesgo** (`class: 1`).
   - Esto indica que el promedio de notas es un factor clave para identificar a los estudiantes en riesgo.

2. **Segunda regla: `Promedio Notas > 50.30`**
   - Si el promedio de notas es mayor a **50.30**, el árbol evalúa la asistencia para tomar una decisión.

3. **Subregla: `Asistencia (%) <= 60.00`**
   - Si la asistencia es menor o igual a **60%**, el estudiante se clasifica como en **riesgo** (`class: 1`).
   - Esto refuerza la importancia de la asistencia como indicador de riesgo.

4. **Subregla: `Asistencia (%) > 60.00`**
   - Si la asistencia es mayor a **60%**, el árbol evalúa un umbral adicional:
     - **`Asistencia (%) <= 63.50`**:
       - Si la asistencia está entre **60% y 63.50%**, el estudiante se clasifica como **no en riesgo** (`class: 0`).
     - **`Asistencia (%) > 63.50`**:
       - Si la asistencia es mayor a **63.50%**, el estudiante también se clasifica como **no en riesgo** (`class: 0`).

---

### **Conclusiones**

1. **Factores clave identificados por el árbol**:
   - **Promedio Notas**:
     - Es el factor más importante. Un promedio menor o igual a **50.30** es un indicador directo de riesgo.
   - **Asistencia (%)**:
     - Es el segundo factor más importante. Una asistencia menor o igual a **60%** también indica riesgo.
     - Para estudiantes con asistencia entre **60% y 63.50%**, el riesgo es menor.

2. **Umbrales aprendidos**:
   - **Promedio Notas <= 50.30**: Umbral crítico para identificar estudiantes en riesgo.
   - **Asistencia (%) <= 60.00**: Umbral importante para evaluar el riesgo.
   - **Asistencia (%) <= 63.50**: Umbral adicional para diferenciar entre riesgo y no riesgo.

3. **Reglas claras y simples**:
   - El árbol ha aprendido reglas claras y fáciles de interpretar, lo que es ideal para comunicar los resultados a docentes o administradores.

---

### **Próximos pasos**

1. **Validar las reglas aprendidas**:
   - Evalúa el desempeño del árbol utilizando métricas como precisión, recall y F1-score.
   - Por ejemplo:
     ```python
     from sklearn.metrics import classification_report
     y_pred = tree.predict(X)
     print(classification_report(y, y_pred))
     ```

2. **Comparar con las reglas actuales**:
   - Compara las reglas aprendidas por el árbol con las reglas definidas manualmente (por ejemplo, los umbrales actuales de asistencia y promedio de notas).
   - Ajusta las reglas manuales si es necesario.

3. **Visualizar el árbol**:
   - Puedes visualizar el árbol de decisión para comunicar mejor las reglas aprendidas:
     ```python
     from sklearn.tree import plot_tree
     import matplotlib.pyplot as plt

     plt.figure(figsize=(12, 8))
     plot_tree(tree, feature_names=X.columns, class_names=["No Riesgo", "Riesgo"], filled=True)
     plt.show()
     ```

4. **Incorporar las reglas aprendidas**:
   - Si las reglas aprendidas son mejores que las actuales, puedes incorporarlas en tu sistema de alertas tempranas.

---

### **Conclusión**
El árbol de decisión ha identificado reglas claras y basadas en datos para clasificar a los estudiantes en riesgo. Estas reglas refuerzan la importancia del promedio de notas y la asistencia como indicadores clave.

## Evaluación del desempeño de las reglas
```plaintext
                precision    recall  f1-score   support

           0       0.85      1.00      0.92        29
           1       1.00      0.76      0.86        21

    accuracy                           0.90        50
   macro avg       0.93      0.88      0.89        50
weighted avg       0.91      0.90      0.90        50
```






## AJUSTE

El ajuste realizado al agregar el parámetro `class_weight={0: 1, 1: 2}` en el árbol de decisión ha mejorado el balance entre las clases, especialmente para la clase "Riesgo" (`1`). Vamos a analizar los resultados:

---

```plaintext
Reglas aprendidas por el árbol de decisión:
|--- Promedio Notas <= 50.30
|   |--- class: 1
|--- Promedio Notas >  50.30
|   |--- Asistencia (%) <= 61.50
|   |   |--- Tareas Entregadas (10) <= 6.00
|   |   |   |--- class: 1
|   |   |--- Tareas Entregadas (10) >  6.00
|   |   |   |--- class: 1
|   |--- Asistencia (%) >  61.50
|   |   |--- Asistencia (%) <= 92.00
|   |   |   |--- class: 0
|   |   |--- Asistencia (%) >  92.00
|   |   |   |--- class: 0
```
### **1. Métricas por clase**

#### **Clase 0 (No Riesgo)**:
- **Precisión (precision)**: **0.88**
  - De todas las predicciones que el modelo hizo como "No Riesgo", el **88%** fueron correctas.
- **Recall (recall)**: **0.97**
  - El modelo identificó correctamente al **97%** de los estudiantes que realmente no estaban en riesgo.
- **F1-Score**: **0.92**
  - Indica un buen balance entre precisión y recall para esta clase.

#### **Clase 1 (Riesgo)**:
- **Precisión (precision)**: **0.94**
  - De todas las predicciones que el modelo hizo como "Riesgo", el **94%** fueron correctas.
- **Recall (recall)**: **0.81**
  - El modelo identificó correctamente al **81%** de los estudiantes que realmente estaban en riesgo.
- **F1-Score**: **0.87**
  - Indica un buen balance entre precisión y recall, aunque el recall sigue siendo más bajo que la precisión.

---

### **2. Métricas generales**

#### **Accuracy (Exactitud)**: **0.90**
- El modelo clasificó correctamente al **90%** de los estudiantes en general.

#### **Macro Avg (Promedio Macro)**:
- **Precisión (precision)**: **0.91**
  - Promedio de la precisión para ambas clases.
- **Recall (recall)**: **0.89**
  - Promedio del recall para ambas clases.
- **F1-Score**: **0.89**
  - Promedio del F1-Score para ambas clases.

#### **Weighted Avg (Promedio Ponderado)**:
- **Precisión (precision)**: **0.90**
  - Promedio ponderado de la precisión, considerando el número de ejemplos en cada clase.
- **Recall (recall)**: **0.90**
  - Promedio ponderado del recall.
- **F1-Score**: **0.90**
  - Promedio ponderado del F1-Score.

---

### **3. Comparación con los resultados anteriores**

| Métrica         | Antes del ajuste | Después del ajuste |
|-----------------|------------------|--------------------|
| **Precisión (Clase 1)** | 1.00             | 0.94               |
| **Recall (Clase 1)**    | 0.76             | 0.81               |
| **F1-Score (Clase 1)**  | 0.86             | 0.87               |
| **Accuracy**            | 0.90             | 0.90               |

#### **Observaciones**:
1. **Clase 1 (Riesgo)**:
   - El recall mejoró de **0.76** a **0.81**, lo que significa que el modelo ahora identifica más estudiantes en riesgo.
   - La precisión disminuyó ligeramente de **1.00** a **0.94**, pero sigue siendo alta.
   - El F1-Score aumentó de **0.86** a **0.87**, lo que indica un mejor balance entre precisión y recall.

2. **Clase 0 (No Riesgo)**:
   - El recall aumentó de **1.00** a **0.97**, lo que significa que el modelo sigue siendo muy bueno para identificar a los estudiantes sin riesgo.
   - La precisión disminuyó ligeramente de **0.85** a **0.88**, pero sigue siendo alta.

3. **Balance general**:
   - El modelo ahora está más equilibrado entre las dos clases, gracias al ajuste del peso de la clase "Riesgo".

---

### **4. Interpretación del ajuste**

El parámetro `class_weight={0: 1, 1: 2}` le indicó al modelo que la clase "Riesgo" (`1`) es más importante que la clase "No Riesgo" (`0`). Esto penaliza más los errores en la clase "Riesgo", lo que llevó a un aumento en el recall para esta clase.

---

### **5. Recomendaciones**

1. **Mantener el ajuste**:
   - El modelo ahora tiene un mejor balance entre precisión y recall para ambas clases, lo que es crucial en un contexto educativo donde es importante identificar a los estudiantes en riesgo.

2. **Validación cruzada**:
   - Usa validación cruzada para asegurarte de que el modelo sea consistente en diferentes subconjuntos de datos:
     ```python
     from sklearn.model_selection import cross_val_score
     scores = cross_val_score(tree, X, y, cv=5, scoring='f1_weighted')
     print("F1-Score promedio en validación cruzada:", scores.mean())
     ```

3. **Ajustar más hiperparámetros**:
   - Experimenta con otros hiperparámetros, como `max_depth`, `min_samples_split` o `min_samples_leaf`, para mejorar aún más el desempeño.

4. **Evaluar con una matriz de confusión**:
   - Genera una matriz de confusión para visualizar los errores del modelo:
     ```python
     from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
     cm = confusion_matrix(y, y_pred)
     disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Riesgo", "Riesgo"])
     disp.plot()
     ```

5. **Comunicar las reglas aprendidas**:
   - Las reglas aprendidas por el árbol de decisión son claras y fáciles de interpretar. Puedes usarlas para justificar las decisiones del modelo.

---

### **6. Conclusión**

El ajuste del peso de las clases mejoró el balance del modelo, especialmente para la clase "Riesgo". Ahora el modelo identifica más estudiantes en riesgo, manteniendo un buen desempeño general. Si necesitas ayuda para implementar más ajustes o realizar análisis adicionales, ¡puedes pedírmelo! 🚀

## Cambios en las reglas aprendidas

Las reglas aprendidas por el árbol de decisión cambiaron después de ajustar el hiperparámetro `class_weight`. Esto es completamente normal y esperado, ya que el ajuste del peso de las clases afecta cómo el modelo prioriza las decisiones durante el entrenamiento.

---

### **Por qué cambiaron las reglas**
1. **Ajuste del peso de las clases (`class_weight`)**:
   - Al asignar más peso a la clase "Riesgo" (`1`), el modelo penaliza más los errores en esta clase.
   - Esto hace que el árbol busque reglas que sean más efectivas para identificar a los estudiantes en riesgo, incluso si eso significa cambiar los umbrales o incluir nuevas características.

2. **Nuevas características en las reglas**:
   - Ahora el árbol incluye **`Tareas Entregadas (10)`** como parte de las reglas, lo que no estaba presente antes.
   - Esto indica que, al priorizar la clase "Riesgo", el modelo encontró que esta característica es relevante para mejorar la clasificación.

3. **Cambios en los umbrales**:
   - El umbral para **`Asistencia (%)`** cambió de **60.00** a **61.50** y se introdujo un nuevo rango para valores mayores a **92.00**.
   - Esto refleja que el modelo está ajustando los límites para maximizar el recall de la clase "Riesgo".

---

### **Nuevas reglas aprendidas**
```plaintext
|--- Promedio Notas <= 50.30
|   |--- class: 1
|--- Promedio Notas >  50.30
|   |--- Asistencia (%) <= 61.50
|   |   |--- Tareas Entregadas (10) <= 6.00
|   |   |   |--- class: 1
|   |   |--- Tareas Entregadas (10) >  6.00
|   |   |   |--- class: 1
|   |--- Asistencia (%) >  61.50
|   |   |--- Asistencia (%) <= 92.00
|   |   |   |--- class: 0
|   |   |--- Asistencia (%) >  92.00
|   |   |   |--- class: 0
```

---

### **Interpretación de las nuevas reglas**

1. **Primera regla: `Promedio Notas <= 50.30`**
   - Si el promedio de notas es menor o igual a **50.30**, el estudiante se clasifica como en **riesgo** (`class: 1`).
   - Esto sigue siendo consistente con las reglas anteriores, indicando que el promedio de notas es un factor clave.

2. **Segunda regla: `Promedio Notas > 50.30`**
   - Si el promedio de notas es mayor a **50.30**, el árbol evalúa la asistencia y las tareas entregadas para tomar una decisión.

3. **Subregla: `Asistencia (%) <= 61.50`**
   - Si la asistencia es menor o igual a **61.50%**, el árbol evalúa las tareas entregadas:
     - **`Tareas Entregadas (10) <= 6.00`**:
       - Si el estudiante entregó 6 o menos tareas, se clasifica como en **riesgo** (`class: 1`).
     - **`Tareas Entregadas (10) > 6.00`**:
       - Si el estudiante entregó más de 6 tareas, también se clasifica como en **riesgo** (`class: 1`).

4. **Subregla: `Asistencia (%) > 61.50`**
   - Si la asistencia es mayor a **61.50%**, el árbol evalúa un rango adicional:
     - **`Asistencia (%) <= 92.00`**:
       - Si la asistencia está entre **61.50% y 92.00%**, el estudiante se clasifica como **no en riesgo** (`class: 0`).
     - **`Asistencia (%) > 92.00`**:
       - Si la asistencia es mayor a **92.00%**, el estudiante también se clasifica como **no en riesgo** (`class: 0`).

---

### **Comparación con las reglas anteriores**

| Aspecto                | Reglas anteriores                          | Reglas actuales                              |
|------------------------|--------------------------------------------|---------------------------------------------|
| **Promedio Notas**     | Umbral: **50.30**                         | Umbral: **50.30** (sin cambios)             |
| **Asistencia (%)**     | Umbral: **60.00**, subregla: **63.50**     | Umbral: **61.50**, subregla: **92.00**      |
| **Tareas Entregadas**  | No estaba presente                        | Introducida como nueva característica       |

#### **Observaciones**:
1. **Promedio Notas**:
   - Sigue siendo el factor más importante para identificar a los estudiantes en riesgo.
2. **Asistencia (%)**:
   - El umbral cambió ligeramente, lo que indica que el modelo está ajustando los límites para mejorar la clasificación.
3. **Tareas Entregadas (10)**:
   - Ahora se incluye como un factor relevante, lo que sugiere que esta característica tiene un impacto en la clasificación después del ajuste de pesos.

---

### **Conclusión**

El ajuste del hiperparámetro `class_weight` no solo mejoró el desempeño del modelo, sino que también cambió las reglas aprendidas por el árbol de decisión. Esto es un resultado positivo, ya que las nuevas reglas reflejan un modelo más equilibrado y adaptado a las prioridades de clasificación (identificar a los estudiantes en riesgo).
