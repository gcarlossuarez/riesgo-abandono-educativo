## ANÁLISIS DE LOS PRIMEROS RESULTADOS PARA EL PRIMER GRUPO DE TEST DE 50 ESTUDIANTES

El resultado que se obtuvo proporciona información valiosa sobre las características de los estudiantes en relación con el riesgo académico. Vamos a analizar cada parte del resultado:

---

### **1. Estadísticas descriptivas por nivel de riesgo**
```plaintext
Riesgo                                                         ...
0                29.0  80.068966  11.032196  61.0  73.0  82.0  ...      16.313227  50.4  60.7  73.0  87.4  99.8  
1                21.0  66.333333  16.374777  40.0  56.0  64.0  ...      20.042171  40.3  43.8  50.2  78.6  98.5  
```

#### **Interpretación**:
- **Riesgo = 0 (sin riesgo)**:
  - **Asistencia (%)**:
    - Promedio: **80.07%**.
    - Desviación estándar: **11.03%** (los valores están más concentrados alrededor de la media).
    - Percentil 25: **73%**.
    - Percentil 50 (mediana): **82%**.
    - Percentil 75: **87.4%**.
  - Esto indica que los estudiantes sin riesgo tienen una asistencia generalmente alta.

- **Riesgo = 1 (en riesgo)**:
  - **Asistencia (%)**:
    - Promedio: **66.33%**.
    - Desviación estándar: **16.37%** (los valores están más dispersos).
    - Percentil 25: **56%**.
    - Percentil 50 (mediana): **64%**.
    - Percentil 75: **78.6%**.
  - Los estudiantes en riesgo tienen una asistencia significativamente más baja en promedio, con mayor dispersión.

#### **Conclusión**:
- La asistencia es un indicador importante del riesgo académico, ya que los estudiantes en riesgo tienen una asistencia promedio más baja y un rango más amplio.

---

### **2. Correlación con el riesgo**
```plaintext
Correlación con Riesgo:
Asistencia (%)           -0.455646
Tareas Entregadas (10)   -0.051215
Promedio Notas           -0.353808
Riesgo                    1.000000
```

#### **Interpretación**:
- **Asistencia (%)**:
  - Correlación: **-0.4556**.
  - Esto indica una correlación negativa moderada: a medida que disminuye la asistencia, aumenta la probabilidad de estar en riesgo.
- **Tareas Entregadas (10)**:
  - Correlación: **-0.0512**.
  - Esto indica una correlación muy débil con el riesgo. Podría no ser un buen indicador por sí solo.
- **Promedio Notas**:
  - Correlación: **-0.3538**.
  - Esto indica una correlación negativa moderada: a medida que disminuyen las calificaciones, aumenta la probabilidad de estar en riesgo.

#### **Conclusión**:
- La asistencia y el promedio de notas son los indicadores más relevantes para predecir el riesgo.
- Las tareas entregadas tienen una correlación débil, por lo que podrían no ser tan útiles como regla independiente.

---

### **3. Estudiantes que cumplen con cada regla**
```plaintext
Estudiantes que cumplen con la regla 1: 3
Estudiantes que cumplen con la regla 2: 10
Estudiantes que cumplen con la regla 3: 5
```

#### **Interpretación**:
- **Regla 1**: `Asistencia (%) < thresholds['asistencia_threshold']` y `Participación == 'Baja'`:
  - Solo **3 estudiantes** cumplen con esta regla.
  - Esto indica que esta regla es muy específica y podría estar subestimando el riesgo.

- **Regla 2**: `Tareas Entregadas (10) < thresholds['tareas_threshold']`:
  - **10 estudiantes** cumplen con esta regla.
  - Aunque la correlación de las tareas entregadas con el riesgo es débil, esta regla identifica a un grupo más amplio.

- **Regla 3**: `Promedio Notas < thresholds['notas_threshold']`:
  - **5 estudiantes** cumplen con esta regla.
  - Esto es consistente con la correlación moderada entre el promedio de notas y el riesgo.

#### **Conclusión**:
- La **Regla 1** podría ser demasiado restrictiva y necesitar ajustes (por ejemplo, aumentar el umbral de asistencia o considerar otros factores).
- La **Regla 2** identifica a más estudiantes, pero su relevancia debe ser validada debido a la baja correlación.
- La **Regla 3** parece ser un buen indicador, ya que está respaldada por la correlación con el riesgo.

---

### **4. Recomendaciones**

1. **Ajustar las reglas**:
   - **Regla 1**:
     - Considera aumentar el umbral de asistencia o eliminar la condición de participación para incluir a más estudiantes.
   - **Regla 2**:
     - Evalúa si las tareas entregadas son realmente un buen indicador del riesgo. Podrías combinar esta regla con otras características.
   - **Regla 3**:
     - Mantén esta regla, ya que el promedio de notas tiene una correlación moderada con el riesgo.

2. **Definir umbrales dinámicos**:
   - Usa los percentiles para ajustar los umbrales de las reglas. Por ejemplo:
     ```python
     asistencia_threshold = df[df['Riesgo'] == 1]['Asistencia (%)'].quantile(0.25)
     print(f"Nuevo umbral para Asistencia (%): {asistencia_threshold}")
     ```

3. **Validar las reglas**:
   - Calcula métricas como precisión, recall y F1-score para evaluar la efectividad de las reglas.

4. **Visualizar los resultados**:
   - Genera gráficos para observar cómo las reglas afectan la clasificación de los estudiantes. Por ejemplo:
     ```python
     sns.boxplot(data=df, x='Riesgo', y='Asistencia (%)')
     plt.title("Distribución de Asistencia (%) por Riesgo")
     plt.show()
     ```

---

### **Conclusión**
El análisis muestra que la asistencia y el promedio de notas son los indicadores más relevantes del riesgo académico. Las reglas actuales funcionan, pero podrían ajustarse para incluir más estudiantes en riesgo.
