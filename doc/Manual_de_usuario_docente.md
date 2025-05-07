# Manual del Usuario: Sistema de Predicción de Riesgo de Abandono

## **Introducción**
Este sistema está diseñado para ayudar a los docentes a identificar estudiantes en riesgo de abandono académico. Utiliza datos históricos y actuales de los estudiantes para generar predicciones basadas en un modelo de aprendizaje automático. Es importante tener en cuenta que las mejores predicciones se obtendrán después de contar con las notas de la primera evaluación, ya que sin información suficiente, el sistema no puede realizar análisis precisos.

---

## **Pasos para Utilizar el Sistema**

### **1. Preparar los Datos**
1. Obtén un archivo `.csv` con los datos de los estudiantes desde la plataforma institucional o desde un reporte generado por el Centro de Procesamiento de Datos de la institución educativa.
2. Asegúrate de que el archivo contenga las siguientes columnas:
   - **Asistencia (%)**: Porcentaje de asistencia del estudiante.
   - **Participación**: Nivel de participación del estudiante (por ejemplo, "Alta", "Media", "Baja").
   - **Tareas Entregadas (10)**: Número de tareas entregadas de un total de 10.
   - **Promedio Notas**: Promedio de las calificaciones obtenidas.

---

### **2. Subir los Datos al Sistema**
1. Abre el archivo `dashboard.html` en tu navegador web.
2. En la interfaz del sistema, selecciona el archivo `.csv` que contiene los datos de los estudiantes.
3. Pulsa el botón **"Analizar"**.

---

### **3. Interpretar los Resultados**
1. El sistema procesará los datos y generará un **dashboard interactivo** con gráficos que muestran:
   - Distribución de los estudiantes según su nivel de riesgo.
   - Factores clave que influyen en el riesgo de abandono.
2. Los resultados se mostrarán en pantalla para facilitar la interpretación.

---

### **4. Exportar los Resultados**
1. Si deseas guardar los resultados para un análisis posterior, puedes exportar el dashboard generado a un archivo `.csv`.
2. Este archivo contendrá las predicciones de riesgo para cada estudiante, junto con las características analizadas.

---

## **Notas Importantes**
- **Mejor momento para usar el sistema**:
  - Las predicciones serán más precisas después de contar con las notas de la primera evaluación.
  - Sin información suficiente, el sistema no podrá realizar análisis efectivos.

- **Confidencialidad de los datos**:
  - Asegúrate de manejar los datos de los estudiantes con responsabilidad y de acuerdo con las políticas de privacidad de la institución.

- **Limitaciones del sistema**:
  - El sistema no reemplaza el juicio del docente. Las predicciones deben ser utilizadas como una herramienta complementaria para la toma de decisiones.

---

## **Preguntas Frecuentes**

### **1. ¿Qué hago si el sistema no genera resultados?**
- Verifica que el archivo `.csv` cargado tenga las columnas requeridas y que los datos estén completos.

### **2. ¿Puedo usar el sistema antes de la primera evaluación?**
- Sí, pero las predicciones serán menos precisas debido a la falta de información clave como las calificaciones.

### **3. ¿Qué hago si quiero ajustar las reglas del sistema?**
- Las reglas del sistema son generadas automáticamente por el modelo. Si necesitas ajustes específicos, consulta con el equipo técnico.

---

## **Contacto**
Si tienes dudas o necesitas soporte, contacta al equipo técnico de tu institución educativa.