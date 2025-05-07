
## 1) python src/data_processing.py data/raw/estudiantes.csv data/processed/datos_procesados.csv

El archivo de salida datos_procesados.csv debe crearse en data/processed/

Debe contener las nuevas columnas:

Riesgo (1 para Retirado/Reprobado, 0 para Aprobado)

Alerta_Temprana (1 si cumple algún criterio de alerta)


## 2) python src/model_training.py data/processed/datos_procesados.csv

Qué verificar:

El archivo modelo_riesgo.pkl debe crearse

En consola deben aparecer las precisiones de entrenamiento y prueba (deben ser > 0.7)

No deben aparecer errores durante el proceso


## 3) python src/app.py

Pruebas en el Navegador (http://localhost:5000)
Prueba 1: Subir archivo CSV

Ve a http://localhost:5000 en tu navegador

Haz clic en "Seleccionar archivo" y elige tu estudiantes.csv

Verifica que:

Se muestre una tabla con los resultados

Aparezcan las columnas de predicción

Los estudiantes con bajo rendimiento aparezcan destacados

Prueba 2: Datos incorrectos

Intenta subir un archivo con:

Columnas faltantes

Formato incorrecto

Verifica que muestre mensajes de error claros


Datos de Prueba Recomendados
Crea un archivo test_data.csv con este contenido mínimo:

csv
Copy
ID_Estudiante,Asistencia (%),Participación,Tareas Entregadas (10),Promedio Notas,Estado Final
EST100,85,Alta,8,75,Aprobado
EST101,45,Baja,2,48,Reprobado
EST102,90,Media,5,82,Aprobado
EST103,30,Baja,1,35,Retirado
Verificación de Resultados
Para alertas tempranas:

EST101 y EST103 deben tener Alerta_Temprana = 1

EST100 y EST102 deben tener Alerta_Temprana = 0

Para predicciones del modelo:

EST103 debería tener alta probabilidad de riesgo (>70%)

EST100 debería tener baja probabilidad de riesgo (<30%)

### Pruebas Avanzadas
Prueba con nuevos datos:

Crea un archivo con 5-10 estudiantes nuevos

Verifica que el modelo genere predicciones coherentes

Prueba de rendimiento:

Sube un archivo con 100+ registros

Verifica que responda en menos de 5 segundos

Solución de Problemas Comunes
Si algo no funciona:

Verifica los logs en la terminal donde ejecutas app.py

Revisa los archivos generados:

datos_procesados.csv (¿tiene las columnas esperadas?)

modelo_riesgo.pkl (¿tiene tamaño > 1MB?)

Prueba cada módulo por separado antes de usar la app web completa