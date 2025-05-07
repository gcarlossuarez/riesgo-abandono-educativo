### JUSTIFICACIÓN DE LAS REGLAS PARA DETERMINAR LOS TIPOS DE ALERTA

Para sustentar las reglas que determinan los tipos de alerta, se puede seguir un enfoque basado en datos y análisis estadístico. Aquí te detallo cómo hacerlo:

---

### **1. Análisis exploratorio de los datos**
Antes de definir reglas, es importante analizar cómo se distribuyen las características (`Asistencia (%)`, `Tareas Entregadas (10)`, `Promedio Notas`, etc.) en los estudiantes con diferentes niveles de alerta.

#### **Pasos**:
- **Visualización de datos**:
  - Usae gráficos para observar cómo se comportan las características en los estudiantes con y sin alertas.
- **Estadísticas descriptivas**:
  - Calcular la media, mediana, percentiles y desviación estándar para cada característica.

#### **Ejemplo en Python**:
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Visualizar distribución de Asistencia (%) por Riesgo
sns.boxplot(data=df, x='Riesgo', y='Asistencia (%)')
plt.title("Distribución de Asistencia (%) por Riesgo")
plt.show()

# Estadísticas descriptivas por nivel de riesgo
print(df.groupby('Riesgo')[['Asistencia (%)', 'Tareas Entregadas (10)', 'Promedio Notas']].describe())
```

---

### **2. Validar las reglas actuales**
Las reglas actuales para determinar las alertas son:
- **`Asistencia (%) < thresholds['asistencia_threshold']` y `Participación == 'Baja'`**.
- **`Tareas Entregadas (10) < thresholds['tareas_threshold']`**.
- **`Promedio Notas < thresholds['notas_threshold']`**.

#### **Cómo validarlas**:
- **Correlación**:
  - Calcula la correlación entre estas características y la variable `Riesgo` para verificar si realmente están relacionadas.
- **Análisis de impacto**:
  - Evalúa cuántos estudiantes cumplen con cada regla y si están correctamente clasificados como en riesgo.

#### **Ejemplo en Python**:
```python
# Correlación entre características y Riesgo
correlation = df[['Asistencia (%)', 'Tareas Entregadas (10)', 'Promedio Notas', 'Riesgo']].corr()
print("Correlación con Riesgo:")
print(correlation['Riesgo'])

# Verificar cuántos estudiantes cumplen con cada regla
regla1 = df[(df['Asistencia (%)'] < thresholds['asistencia_threshold']) & (df['Participación'] == 'Baja')]
regla2 = df[df['Tareas Entregadas (10)'] < thresholds['tareas_threshold']]
regla3 = df[df['Promedio Notas'] < thresholds['notas_threshold']]

print(f"Estudiantes que cumplen con la regla 1: {len(regla1)}")
print(f"Estudiantes que cumplen con la regla 2: {len(regla2)}")
print(f"Estudiantes que cumplen con la regla 3: {len(regla3)}")
```

---

### **3. Ajustar las reglas con modelos predictivos**
En lugar de reglas fijas, se puede usar un modelo predictivo (como un árbol de decisión o regresión logística) para identificar automáticamente las combinaciones de características que mejor predicen el riesgo.

#### **Ejemplo con un árbol de decisión**:
```python
from sklearn.tree import DecisionTreeClassifier, export_text

# Entrenar un árbol de decisión
X = df[['Asistencia (%)', 'Tareas Entregadas (10)', 'Promedio Notas']]
y = df['Riesgo']
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X, y)

# Mostrar las reglas aprendidas por el árbol
rules = export_text(tree, feature_names=X.columns.tolist())
print("Reglas aprendidas por el árbol de decisión:")
print(rules)
```

Esto permitirá ver reglas como:
```plaintext
|--- Asistencia (%) <= 60.00
|   |--- Promedio Notas <= 50.00
|   |   |--- class: Riesgo
|   |--- Promedio Notas > 50.00
|   |   |--- class: No Riesgo
|--- Asistencia (%) > 60.00
|   |--- class: No Riesgo
```

---

### **4. Validar las reglas con métricas de desempeño**
Una vez definidas las reglas, evaluar su desempeño utilizando métricas como:
- **Precisión**: Qué porcentaje de las predicciones son correctas.
- **Recall**: Qué porcentaje de los estudiantes en riesgo fueron correctamente identificados.
- **F1-Score**: Una combinación de precisión y recall.

#### **Ejemplo en Python**:
```python
from sklearn.metrics import classification_report

# Predicciones basadas en las reglas
df['Predicción'] = 0
df.loc[(df['Asistencia (%)'] < thresholds['asistencia_threshold']) & (df['Participación'] == 'Baja'), 'Predicción'] = 1
df.loc[(df['Tareas Entregadas (10)'] < thresholds['tareas_threshold']), 'Predicción'] = 1
df.loc[df['Promedio Notas'] < thresholds['notas_threshold'], 'Predicción'] = 1

# Evaluar desempeño
print(classification_report(df['Riesgo'], df['Predicción']))
```

---

### **5. Consultar con expertos en el dominio**
Además del análisis estadístico, es importante validar las reglas con expertos en educación. Preguntas clave:
- ¿Qué niveles de asistencia, tareas entregadas o calificaciones suelen asociarse con el riesgo académico?
- ¿Existen políticas institucionales que definan estos umbrales?

---

### **6. Ajustar dinámicamente los niveles de alerta**
Se pueden definir diferentes niveles de alerta (por ejemplo, "Moderado" y "Alto") basándose en los percentiles de las características.

#### **Ejemplo**:
```python
# Definir niveles de alerta basados en percentiles
df['Nivel_Alerta'] = 'Normal'
df.loc[(df['Asistencia (%)'] < thresholds['asistencia_threshold']) & (df['Participación'] == 'Baja'), 'Nivel_Alerta'] = 'Moderado'
df.loc[(df['Tareas Entregadas (10)'] < thresholds['tareas_threshold']) & (df['Promedio Notas'] < thresholds['notas_threshold']), 'Nivel_Alerta'] = 'Alto'
```

---

### **Conclusión**
Para sustentar las reglas de alerta:
1. **Analiza los datos históricos** para validar las relaciones entre características y riesgo.
2. **Usa modelos predictivos** para identificar reglas basadas en datos.
3. **Evaluar el desempeño** de las reglas con métricas como precisión y recall.
4. **Consultar con expertos** para alinear las reglas con el contexto educativo.
5. **Ajustar dinámicamente** los niveles de alerta según los datos.
