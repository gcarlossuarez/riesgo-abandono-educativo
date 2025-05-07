import pandas as pd
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import sys
import os

# Agregar el directorio raíz del proyecto al PYTHONPATH, para poder importar módulos que no están en el mismo directorio
# Esto es útil si se está ejecutando el script desde un directorio diferente
dir_scriptdata_processing = os.path.join(os.path.dirname(__file__), '../')
print("Directorio script data_processing_training_rules.py", dir_scriptdata_processing)
sys.path.append(os.path.abspath(dir_scriptdata_processing))

from data_processing import process_data


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
    
def analyze_distribution(df):
    # Visualizar distribución de Asistencia (%) por Riesgo
    sns.boxplot(data=df, x='Riesgo', y='Asistencia (%)')
    plt.title("Distribución de Asistencia (%) por Riesgo")
    plt.show()

    # Estadísticas descriptivas por nivel de riesgo
    print(df.groupby('Riesgo')[['Asistencia (%)', 'Tareas Entregadas (10)', 'Promedio Notas']].describe())


def analyze_correlation(df, thresholds):
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

def train_decision_tree(df):
    from sklearn.tree import DecisionTreeClassifier, export_text

    # Entrenar un árbol de decisión
    X = df[['Asistencia (%)', 'Tareas Entregadas (10)', 'Promedio Notas']]
    y = df['Riesgo']
    #tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    tree = DecisionTreeClassifier(max_depth=3, random_state=42, class_weight={0: 1, 1: 2})
    tree.fit(X, y)

    # Mostrar las reglas aprendidas por el árbol
    rules = export_text(tree, feature_names=X.columns.tolist())
    print("Reglas aprendidas por el árbol de decisión:")
    print(rules)

    # Generar el archivo decision_tree_rules.py
    generate_rules_script(tree, X.columns.tolist())

    # Evaluar el desempeño del árbol utilizando métricas como precisión, recall y F1-score
    print("\nMétricas de desempeño del árbol de decisión:")
    #from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from sklearn.metrics import classification_report
    y_pred = tree.predict(X)
    print(classification_report(y, y_pred))

    from sklearn.tree import plot_tree
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 8))
    plot_tree(tree, feature_names=X.columns, class_names=["No Riesgo", "Riesgo"], filled=True)
    plt.show()


def get_parts_from_sentence(line):
    """
    Explicación:
    r".*\|---\s*(.*?)\s*(<=|<|>=|>|==)\s*(.*)": Este patrón de expresión regular busca:

    .*: .*\|---\s*: Esta parte del patrón .* permite que haya cualquier conjunto de caracteres (incluyendo ninguno,
    debido al operador *) antes de la secuencia |---. El .* es una expresión que coincide con cualquier carácter
    (excepto saltos de línea) cualquier número de veces.
    \|---: La secuencia literal "|---".
    \s*: Cualquier cantidad de espacios en blanco.
    (.*?): Captura el operando izquierdo (cualquier texto antes del operador) de forma no codiciosa.
    (<=|<|>=|>|==): Captura el operador entre las opciones especificadas.
    (.*): Captura el operando derecho (cualquier cosa después del operador).

    match.group(1), match.group(2), match.group(3): Obtienen las partes capturadas (operando izquierdo, operador, operando derecho) de la línea.
    Este script te proporcionará las tres partes especificadas con base en un formato similar al que has descrito.
    """

    if not line or not isinstance(line, str):
        return None, None, None

    import re

    # Expresión regular para capturar operando izquierdo, operador y operando derecho
    pattern = r".*\|---\s*(.*?)\s*(<=|<|>=|>|==)\s*(.*)"

    match = re.match(pattern, line)
    if match:
        left_operand = match.group(1)
        operator = match.group(2)
        right_operand = match.group(3)
        return left_operand, operator, right_operand
    return None, None, None

def get_rules_list(rules_text):
    rules_code = ""
    rules_stack = []
    final_rules_list = []
    level = 0
    previous_was_class = False

    for line in rules_text.split("\n"):
        if "|---" in line:
            indent_level = line.count("|   ")  # Contar niveles de indentación
            condition = line.split("|---")[-1].strip()

            if "class:" in condition:
                # Es una hoja del árbol (clasificación final)
                previous_was_class = True

                class_label = condition.split(":")[-1].strip()
                rule = f"df.loc[condition, 'Alerta_Temprana'] = {class_label}"
                rules_code += "    " + "    " * indent_level + f"{rule}\n"
                #  Técnica para agregar todos los elementos de la pila a la lista
                # Primero, invertimos la pila para mantener el orden de pila LIFO (last-in, first-out)
                #inverted_rules_stack = rules_stack[::-1]
                #inverted_rules_stack = rules_stack

                # Luego, extendemos la lista con los elementos invertidos de la pila
                rules_list = []
                rules_list.extend(rules_stack)

                # Se itera sobre la lisa y se concatenan las condiciones
                #  Usar string.join() para concatenar elementos de la lista con "&" como delimitador
                result = f"condition = "
                result += " & ".join(rules_list)
                #result += "\n" + rule
                final_rules_list.append(result)
                final_rules_list.append(rule)
                final_rules_list.append("\n")

                # Se saca la última regla de la pila; ya que, debería haber una sola clase por regla al
                # final de cada rama del árbol
                rules_stack.pop()
            else:
                act_level_number = line.count('|')
                if len(rules_stack) == act_level_number and len(rules_stack) > 0 and previous_was_class:
                    # Condición en la misma jerarquía; por lo tanto, es otra regla
                    rules_stack.pop()

                previous_was_class = False

                # Es una condición intermedia
                level += 1
                #feature, operator, value = condition.split()
                feature, operator, value = get_parts_from_sentence(line)

                if feature is not None and operator is not None and value is not None:
                    value = float(value)
                    condition = f"(df['{feature}'] {operator} {value})"
                    rule = f"condition = {condition}"
                    rules_code += "    " + "    " * indent_level + f"{rule})\n"
                    rules_stack.append(condition)

    return final_rules_list

def generate_rules_script(tree, feature_names):
    """
    Genera un archivo Python con las reglas aprendidas por el árbol de decisión.
    """

    make_backup_decision_tree_rules_py()

    from sklearn.tree import export_text

    # Exportar las reglas como texto
    rules_text = export_text(tree, feature_names=feature_names)

    # Obtener la ruta absoluta del directorio donde está el script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Especificar el subdirectorio donde se guardará el archivo
    output_directory = os.path.join(script_dir, "../")
    os.makedirs(output_directory, exist_ok=True)

    # Ruta completa del archivo de salida
    output_path = os.path.join(output_directory, "decision_tree_rules.py")

    # Convertir las reglas en código Python
    convert_rules_in_python_code(rules_text, output_path)

    print("\nArchivo decision_tree_rules.py generado con éxito.")

def convert_rules_in_python_code(rules_text, output_path):
    rules_code = "def apply_decision_tree_rules(df, thresholds):\n"
    rules_code += "    \"\"\"\n    Aplica las reglas aprendidas por el árbol de decisión.\n    \"\"\"\n"
    rules_code += "    df['Alerta_Temprana'] = 0\n\n"

    rules_list = get_rules_list(rules_text)
    for element in rules_list:
        rules_code += f"    {element}\n"

    rules_code += "    return df\n"

    # Guardar las reglas en un archivo Python
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rules_code)

def make_backup_decision_tree_rules_py():
    import os
    import shutil
    from datetime import datetime

    # Nombre del archivo original
    file_name = "decision_tree_rules.py"

    # Directorio actual y subdirectorio de destino
    #current_directory = os.getcwd()
    subdirectory = ".\\bkp_decision_tree_rules"

    # Asegúrate de que el subdirectorio exista
    os.makedirs(subdirectory, exist_ok=True)

    # Generar marca de tiempo en el formato yyyymmddhhmmss
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Nombre de la copia de seguridad
    backup_file_name = f"bkpy{timestamp}ff{file_name}"

    # Crear la ruta completa para la copia de seguridad
    backup_file_path = os.path.join(subdirectory, backup_file_name)

    # Hacer una copia de seguridad del archivo
    shutil.copy(file_name, backup_file_path)
    print(f"Backup creado: {backup_file_path}")

    '''
    # Mover el archivo original al subdirectorio
    destination_path = os.path.join(subdirectory, file_name)
    shutil.move(file_name, destination_path)
    print(f"Archivo movido a subdirectorio: {destination_path}")
    '''


def analyze_processed_data(df):
    """Realiza el análisis del DataFrame procesado"""
    print("\nAnálisis del DataFrame procesado:")
    print(df.head())  # Muestra las primeras filas del DataFrame
    print("\nResumen de alertas tempranas:")
    print(df['Alerta_Temprana'].value_counts())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python data_processing_training_rules.py <input_file.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Ejecutar el procesamiento de datos
    print("Procesando datos...")
    df, thresholds = process_data(input_file)  # Llama a la función de data_processing.py
    
    if df is not None:
        # Realizar análisis en el DataFrame procesado
        analyze_processed_data(df)
        analyze_distribution(df)  # Llama a la función de análisis de distribución
        analyze_correlation(df, thresholds)  # Llama a la función de análisis de correlación
        train_decision_tree(df)
    else:
        print("Error al procesar los datos.")
