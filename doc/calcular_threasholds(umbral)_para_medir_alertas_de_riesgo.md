### iAlgoritmo en Python que calcula los umbrales óptimos para las condiciones de alerta temprana basándose en un análisis estadístico de los datos del archivo CSV. Este algoritmo utiliza percentiles y estadísticas descriptivas para determinar los valores adecuados.

### **Algoritmo para calcular umbrales**

```python
import pandas as pd

def calculate_thresholds(input_path):
    """
    Calcula umbrales óptimos para las condiciones de alerta temprana
    basándose en estadísticas descriptivas y percentiles.
    """
    try:
        # Cargar datos
        df = pd.read_csv(input_path, encoding='utf-8')
        
        # Verificar que las columnas necesarias estén presentes
        required_columns = ['Asistencia (%)', 'Participación', 'Tareas Entregadas (10)', 'Promedio Notas', 'Riesgo']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Faltan columnas requeridas. Necesarias: {required_columns}")
        
        # Filtrar datos de estudiantes en riesgo
        riesgo_df = df[df['Riesgo'] == 1]
        
        # Calcular umbrales basados en percentiles para estudiantes en riesgo
        asistencia_threshold = riesgo_df['Asistencia (%)'].quantile(0.25)  # Percentil 25
        tareas_threshold = riesgo_df['Tareas Entregadas (10)'].quantile(0.25)  # Percentil 25
        notas_threshold = riesgo_df['Promedio Notas'].quantile(0.25)  # Percentil 25
        
        # Mostrar resultados
        print("Umbrales calculados para alerta temprana:")
        print(f"Asistencia (%) < {asistencia_threshold}")
        print(f"Tareas Entregadas (10) < {tareas_threshold}")
        print(f"Promedio Notas < {notas_threshold}")
        
        return {
            'asistencia_threshold': asistencia_threshold,
            'tareas_threshold': tareas_threshold,
            'notas_threshold': notas_threshold
        }
    
    except Exception as e:
        print(f"Error al calcular umbrales: {e}")
        return None

# Ejemplo de uso
input_file = "datos_procesados.csv"  # Reemplaza con la ruta a tu archivo CSV
thresholds = calculate_thresholds(input_file)
```

---

### **Explicación del algoritmo**

1. **Carga de datos**:
   - Se carga el archivo CSV con los datos de los estudiantes.

2. **Filtrado de estudiantes en riesgo**:
   - Se seleccionan únicamente los estudiantes que están en "Riesgo" (`Riesgo == 1`), ya que los umbrales deben basarse en este grupo.

3. **Cálculo de umbrales**:
   - Se calculan los **percentiles** (por ejemplo, el percentil 25) para las columnas relevantes:
     - `Asistencia (%)`
     - `Tareas Entregadas (10)`
     - `Promedio Notas`
   - El percentil 25 se utiliza como umbral porque representa el límite inferior del rendimiento de los estudiantes en riesgo.

4. **Resultados**:
   - Los umbrales calculados se imprimen y se devuelven como un diccionario.

---

### **Ejemplo de salida**

Si el archivo `datos_procesados.csv` contiene los siguientes datos:

```csv
Estado Final,Asistencia (%),Participación,Tareas Entregadas (10),Promedio Notas,Riesgo
Aprobado,85,Alta,8,75,0
Reprobado,50,Baja,2,45,1
Retirado,40,Baja,1,30,1
Aprobado,95,Media,10,90,0
Aprobado,60,Alta,5,55,0
```

El programa podría generar la siguiente salida:

```plaintext
Umbrales calculados para alerta temprana:
Asistencia (%) < 45.0
Tareas Entregadas (10) < 1.5
Promedio Notas < 37.5
```

---

### **Cómo usar los umbrales calculados**

Puedes reemplazar las condiciones actuales en `generate_early_alerts` con los umbrales calculados dinámicamente:

```python
def generate_early_alerts(df, thresholds):
    """Genera alertas tempranas basadas en umbrales calculados"""
    df['Alerta_Temprana'] = 0
    df.loc[(df['Asistencia (%)'] < thresholds['asistencia_threshold']) & 
           (df['Participación'] == 'Baja'), 'Alerta_Temprana'] = 1
    df.loc[(df['Tareas Entregadas (10)'] < thresholds['tareas_threshold']), 'Alerta_Temprana'] = 1
    df.loc[df['Promedio Notas'] < thresholds['notas_threshold'], 'Alerta_Temprana'] = 1
    return df
```

---

### **Ventajas del enfoque**
1. **Basado en datos**: Los umbrales se calculan dinámicamente a partir de los datos históricos.
2. **Personalización**: Los umbrales se ajustan automáticamente según las características de los estudiantes en riesgo.
3. **Flexibilidad**: Puedes cambiar el percentil utilizado (por ejemplo, usar el percentil 10 o 50) según las necesidades del análisis.

## Fundamentación del uso del percentil 25

La elección del **percentil 25** como umbral tiene una base teórica en estadísticas descriptivas y análisis de datos. Aquí te explico su fundamento y por qué es útil en este contexto:

---

### **1. ¿Qué es el percentil 25?**
El percentil 25 (también conocido como el **primer cuartil, Q1**) es el valor por debajo del cual se encuentra el 25% de los datos en una distribución ordenada. En otras palabras:
- Representa el límite inferior del 25% de los valores más bajos en un conjunto de datos.
- Es útil para identificar valores que están significativamente por debajo de la media o mediana.

---

### **2. Fundamento teórico**
El percentil 25 se utiliza comúnmente en análisis de datos para identificar **valores bajos o atípicos** en una distribución. Esto tiene sentido en el contexto de la educación, donde los estudiantes con características en el rango más bajo (por ejemplo, baja asistencia o calificaciones) suelen estar en mayor riesgo.

#### **Aplicaciones teóricas del percentil 25:**
- **Análisis de riesgo**:
  - En problemas de clasificación, los valores en el percentil 25 pueden indicar un rendimiento insuficiente o un comportamiento que requiere atención.
- **Identificación de outliers**:
  - En combinación con el rango intercuartílico (IQR), el percentil 25 se utiliza para detectar valores atípicos.
- **Segmentación de datos**:
  - Divide los datos en cuartiles para analizar diferentes grupos (por ejemplo, estudiantes con bajo, medio y alto rendimiento).

---

### **3. Por qué usar el percentil 25 en este caso**
En el contexto de tu proyecto, el percentil 25 es útil porque:
1. **Identifica estudiantes en el rango más bajo**:
   - Los estudiantes con asistencia, tareas entregadas o calificaciones en el percentil 25 o inferior probablemente estén en riesgo académico.
2. **Basado en datos históricos**:
   - Si los datos históricos muestran que los estudiantes en riesgo suelen tener valores en este rango, el percentil 25 es un umbral razonable.
3. **Evita la arbitrariedad**:
   - En lugar de elegir umbrales fijos (como `60%` de asistencia o `50` de promedio), el percentil 25 se ajusta dinámicamente según los datos.

---

### **4. Limitaciones del percentil 25**
Aunque el percentil 25 es útil, tiene algunas limitaciones:
- **Generalización**:
  - Puede no ser adecuado para todos los contextos. Por ejemplo, si los datos están sesgados o tienen una distribución no uniforme, el percentil 25 podría no reflejar correctamente el riesgo.
- **Dependencia de los datos**:
  - Si los datos históricos no son representativos, los umbrales calculados podrían no ser precisos.

---

### **5. Alternativas al percentil 25**
Si el percentil 25 no es adecuado para tu caso, puedes considerar otras opciones:
- **Percentil 10 o 5**:
  - Para identificar a los estudiantes con el rendimiento más bajo (los casos más extremos).
- **Percentil 50 (mediana)**:
  - Para dividir a los estudiantes en dos grupos: por debajo y por encima de la mediana.
- **Análisis basado en la media y desviación estándar**:
  - Por ejemplo, considerar estudiantes con valores por debajo de la media menos una desviación estándar.

#### Ejemplo:
```python
# Umbral basado en la media y desviación estándar
asistencia_threshold = riesgo_df['Asistencia (%)'].mean() - riesgo_df['Asistencia (%)'].std()
```

---

### **6. Recomendación**
La elección del percentil 25 es un buen punto de partida, pero es importante validar su efectividad:
- **Análisis exploratorio**:
  - Visualiza los datos para asegurarte de que el percentil 25 captura correctamente a los estudiantes en riesgo.
- **Pruebas empíricas**:
  - Evalúa el desempeño del modelo con diferentes percentiles (por ejemplo, 10, 25, 50) y selecciona el que mejor se ajuste a tus necesidades.

---

### **Conclusión**
El percentil 25 tiene una base teórica sólida en estadísticas descriptivas y es útil para identificar estudiantes en el rango más bajo de rendimiento. Sin embargo, su efectividad depende de los datos y del contexto. Es recomendable validar esta elección con análisis exploratorios y pruebas empíricas para garantizar que los umbrales sean adecuados para este proyecto.