import os
import sys
from data_processing_training_rules import convert_rules_in_python_code

def process_rules_from_txt(input_txt_path, output_py_path):
    """
    Lee las reglas desde un archivo .txt y las convierte en código Python.
    """
    try:
        # Leer el contenido del archivo .txt
        with open(input_txt_path, "r", encoding="utf-8") as f:
            rules_text = f.read()
        
        print("📄 Reglas cargadas desde el archivo .txt:")
        print(rules_text)

        # Invocar a convert_rules_in_python_code para generar el archivo Python
        convert_rules_in_python_code(rules_text, output_py_path)
        print(f"✅ Archivo Python generado con éxito en: {output_py_path}")
    
    except FileNotFoundError:
        print(f"❌ Error: El archivo {input_txt_path} no existe.")
    except Exception as e:
        print(f"❌ Error al procesar las reglas: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: generate_decision_tree_rules_from_txt_file.py <input_file.csv>")
        sys.exit(1)

    # Ruta del archivo de entrada (archivo .txt con las reglas)
    input_txt_path = sys.argv[1]

    # Ruta del archivo de salida (archivo Python generado)
    output_py_path = "decision_tree_rules.py"  # Cambia esto si deseas otro nombre o ubicación

    # Procesar las reglas
    process_rules_from_txt(input_txt_path, output_py_path)