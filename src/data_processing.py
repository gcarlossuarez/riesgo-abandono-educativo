import pandas as pd
import sys

def load_data(input_path):
    """Carga y valida los datos de entrada"""
    try:
        df = pd.read_csv(input_path, encoding='utf-8')
        required_columns = ['Estado Final', 'Asistencia (%)', 'Participación', 
                          'Tareas Entregadas (10)', 'Promedio Notas']
        
        if not all(col in df.columns for col in required_columns):
            print(f"Error: Faltan columnas requeridas. Necesarias: {required_columns}")
            print(f"Columnas encontradas: {df.columns.tolist()}")
            return None
            
        print("\nDatos cargados correctamente. Columnas disponibles:", df.columns.tolist())
        return df
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return None

def calculate_risk(df):
    """Calcula columna de riesgo"""
    df['Riesgo'] = df['Estado Final'].apply(
        lambda x: 1 if x in ['Retirado', 'Reprobado'] else 0
    )
    return df

''''
def generate_early_alerts(df, thresholds):
    """Genera alertas tempranas basadas en reglas"""
    df['Alerta_Temprana'] = 0
    #df.loc[(df['Asistencia (%)'] < 60) & (df['Participación'] == 'Baja'), 'Alerta_Temprana'] = 1
    #df.loc[(df['Tareas Entregadas (10)'] < 3), 'Alerta_Temprana'] = 1
    #df.loc[df['Promedio Notas'] < 50, 'Alerta_Temprana'] = 1
    df.loc[(df['Asistencia (%)'] < thresholds['asistencia_threshold']) & (df['Participación'] == 'Baja'), 'Alerta_Temprana'] = 1
    df.loc[(df['Tareas Entregadas (10)'] < thresholds['tareas_threshold']), 'Alerta_Temprana'] = 1
    df.loc[df['Promedio Notas'] < thresholds['notas_threshold'], 'Alerta_Temprana'] = 1
    return df
'''
from decision_tree_rules import apply_decision_tree_rules

def generate_early_alerts(df, thresholds):
    """
    Genera alertas tempranas basadas en reglas aprendidas por el árbol de decisión.
    """
    # Aplicar las reglas aprendidas por el árbol de decisión
    df = apply_decision_tree_rules(df, thresholds)
    return df

def process_data(input_path, output_path=None):
    """Función principal de procesamiento"""
    df = load_data(input_path)
    if df is None:
        return None
        
    df = calculate_risk(df)
    thresholds = calculate_thresholds(df) # Calcula los umbrales
    df = generate_early_alerts(df, thresholds)
    
    if output_path:
        df.to_csv(output_path, index=False)
        print(f"\nDatos procesados guardados en {output_path}")
    
    # Mostrar resumen
    print("\nResumen de alertas tempranas:")
    print(df['Alerta_Temprana'].value_counts())
    
    return df, thresholds



def calculate_thresholds(df):
    """
    Calcula umbrales óptimos para las condiciones de alerta temprana
    basándose en estadísticas descriptivas y percentiles.
    """
    try:
        # Cargar datos
        #df = pd.read_csv(input_path, encoding='utf-8')
        
        # Verificar que las columnas necesarias estén presentes
        required_columns = ['Asistencia (%)', 'Participación', 'Tareas Entregadas (10)', 'Promedio Notas', 'Riesgo']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Faltan columnas requeridas. NECESARIAS: {required_columns}. ENCONTRADAS: {df.columns.tolist()}")
        
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


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python data_processing.py <input_file.csv> <output_file.csv>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_data(input_file, output_file)