import sys
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os
from data_processing import process_data
import config

from flask import send_from_directory

# Configuración absoluta de rutas
base_dir = os.path.abspath(os.path.dirname(__file__))
#template_dir = os.path.join(base_dir, 'templates')
#template_dir = r'D:\Diplomado en Educación Superior UCB\2025-04-12\Actividad 5\ejecutar_sin_jupyter\Proyecto_Analitica_Educativa\templates'
# Retroceder un nivel y luego entrar a 'templates'
template_dir = os.path.join(base_dir, '..', 'templates')

# Verificación de rutas
print(f"Directorio base: {base_dir}")
print(f"Directorio de plantillas: {template_dir}")
print(f"¿Existe dashboard.html? {os.path.exists(os.path.join(template_dir, 'dashboard.html'))}")

app = Flask(__name__, template_folder=template_dir)

#try:
#    model = joblib.load('modelo_riesgo.pkl')
#    print("✅ Modelo cargado correctamente")
#except Exception as e:
#    print(f"❌ Error cargando modelo: {e}")
#    model = None
# Cambia esta parte donde cargas el modelo
try:
    model_data = joblib.load('modelo_riesgo.pkl')  # Carga el diccionario completo
    model = model_data['model']  # Extrae el modelo real
    encoder = model_data.get('encoder')  # Extrae el encoder si existe
    print("✅ Modelo cargado correctamente")
except Exception as e:
    print(f"❌ Error cargando modelo: {e}")
    model = None
    encoder = None

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                           'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    # Verificar si se envió el archivo
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    file = request.files['archivo']
    
    # Verificar nombre de archivo
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    # Procesar archivo CSV
    try:
        df = pd.read_csv(file)
        print("📊 Datos cargados correctamente. Columnas:", df.columns.tolist())
        
        # Verificar columnas mínimas requeridas
        required_cols = ['Asistencia (%)', 'Promedio Notas', 'Tareas Entregadas (10)']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return jsonify({
                'error': f'Faltan columnas requeridas: {missing_cols}',
                'columnas_recibidas': df.columns.tolist()
            }), 400
        
        # Realizar predicciones si el modelo está cargado
        if model:
            try:
                # Preprocesamiento IDÉNTICO al entrenamiento
                if 'encoder' in model_data:  # Si guardaste el encoder
                    df['Participación_encoded'] = model_data['encoder'].transform(df['Participación'])
                
                # Usar EXACTAMENTE las mismas columnas que en el entrenamiento
                X = df[['Asistencia (%)', 'Promedio Notas', 'Tareas Entregadas (10)', 'Participación_encoded']]
                
                df['Probabilidad_Riesgo'] = model.predict_proba(X)[:, 1]
                df['Nivel_Alerta'] = pd.cut(
                    df['Probabilidad_Riesgo'],
                    bins=[0, 0.4, 0.7, 1], # Divide de manera práctica, más o menos, en tercios. Más adelante, se podría validar contra datos hist´poricos, si se quiere hilar más fino.
                    labels=['Normal', 'Riesgo Moderado', 'Alto Riesgo']
                )
                print("🔮 Predicciones generadas correctamente")
            except Exception as e:
                print(f"⚠️ Error en predicciones: {e}")
                # Debug adicional
                print("Columnas disponibles:", df.columns.tolist())
                if 'encoder' in model_data:
                    print("Categorías en encoder:", list(model_data['encoder'].classes_))
        
        # Convertir a formato para DataTables
        result = df.to_dict('records')
        return jsonify(result)
        
    except pd.errors.EmptyDataError:
        return jsonify({'error': 'El archivo CSV está vacío'}), 400
    except pd.errors.ParserError:
        return jsonify({'error': 'El archivo no es un CSV válido'}), 400
    except Exception as e:
        return jsonify({'error': f'Error procesando archivo: {str(e)}'}), 500

if __name__ == '__main__':
    # Forzar codificación UTF-8 en Windows
    if sys.platform == 'win32':
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    app.run(debug=True, port=5000)
