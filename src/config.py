# Rutas de archivos
DATA_PATHS = {
    'raw': 'data/raw/estudiantes.csv',
    'processed': 'data/processed/datos_procesados.csv',
    'model': 'data/models/modelo_riesgo.pkl'
}

# Umbrales de alerta
ALERT_THRESHOLDS = {
    'high_risk': 0.7,
    'moderate_risk': 0.4,
    'critical': 0.8
}

# Columnas relevantes
FEATURE_COLUMNS = [
    'Asistencia (%)',
    'Promedio Notas', 
    'Tareas Entregadas (10)',
    'Participación'
]