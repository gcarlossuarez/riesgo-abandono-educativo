```markdown
# Manual Técnico: Configuración de Reglas para el Árbol de Decisión

## **Introducción**
El sistema permite configurar las reglas del árbol de decisión de 2 maneras:
1. **Codificación directa en Python**: El equipo técnico, junto con el experto, puede codificar las reglas directamente en un archivo Python (`decision_tree_rules.py`).
2. **Especificación en un archivo `.txt`**: El experto puede definir las reglas en un archivo de texto plano, siguiendo un formato específico. Posteriormente, el equipo técnico puede convertir estas reglas en código Python utilizando el script `generate_decision_tree_rules_from_txt_file.py`.

## NOTA. - En caso de no estar de acuerdo con las reglas o quere investigar optras opciones, se puede dejar que el Sistema busque las mejores reglas, a través del script `data_processing_training_rules.py`.

Cada vez que se ejecuta el script `generate_decision_tree_rules_from_txt_file.py` o el script `data_processing_training_rules.py`, se crea una copia del archivo `decision_tree_rules.py` en el directorio `bkp_decision_tree_rules` y se antepone el prefijo bkpyyyymmddhhssff a `decision_tree_rules.py`. ejemplo: `bkpy20250420144345ffdecision_tree_rules.py`, donde yyyymmddhhssff corresponde a año, mes, día, hora, minbuto, segundo y milisegundo. Esto se hace con el fin de tener un backup en caso de quere utilizar otra vez una regla anterior. Lo único que se tien que hacer es reemkplazar, por ejmplo, `bkpy20250420144345ffdecision_tree_rules.py` en el directorio src y quitar el prefijo, dejando el nombre `decision_tree_rules.py`.
---

## **Formato del Archivo `.txt`**
El archivo `.txt` debe seguir un formato jerárquico que represente las condiciones y decisiones del árbol de decisión. Cada nivel de indentación indica una condición o regla, y las hojas del árbol (nodos finales) especifican la clase asignada.

### **Ejemplo de Archivo `.txt`**
```plaintext
|--- Promedio Notas <= 50.40
|   |--- class: 1
|--- Promedio Notas >  50.40
|   |--- Asistencia (%) <= 61.50
|   |   |--- Tareas Entregadas (10) <= 6.00
|   |   |   |--- Asistencia (%) >  65.50
|   |   |   |   |--- class: 1
|   |   |--- Tareas Entregadas (10) >  6.00
|   |   |   |--- class: 1
|   |--- Asistencia (%) >  61.50
|   |   |--- Asistencia (%) <= 90.00
|   |   |   |--- class: 0
|   |   |--- Asistencia (%) >  90.00
|   |   |   |--- class: 0
```

### **Descripción del Formato**
1. **Condiciones**:
   - Cada condición está precedida por `|---` y especifica una característica, un operador lógico y un valor.
   - Ejemplo: `|--- Promedio Notas <= 50.40`.

2. **Niveles de indentación**:
   - Cada nivel de indentación (representado por `|   `) indica una condición anidada dentro de la anterior.

3. **Clases finales**:
   - Las hojas del árbol (nodos finales) están marcadas con `|--- class: X`, donde `X` es la clase asignada (por ejemplo, `1` para riesgo o `0` para no riesgo).

---

## **Conversión del Archivo `.txt` a Código Python**
Una vez que el archivo `.txt` con las reglas ha sido completado, se puede convertir en un archivo Python utilizando el script `generate_decision_tree_rules_from_txt_file.py`.

### **Pasos para la Conversión**
1. **Crear el archivo `.txt`**:
   - Asegúrate de que el archivo `.txt` siga el formato especificado anteriormente.
   - Guarda el archivo con un nombre descriptivo, por ejemplo, `rules_input.txt`.

2. **Ejecutar el script de conversión**:
   - Usa el siguiente comando para convertir el archivo `.txt` en un archivo Python:
     ```bash
     python generate_decision_tree_rules_from_txt_file.py rules_input.txt
     ```
   - Esto generará un archivo llamado decision_tree_rules.py en el mismo directorio.

3. **Verificar el archivo generado**:
   - El archivo decision_tree_rules.py contendrá las reglas convertidas en código Python.

---

## **Ejemplo de Salida Generada**
Si el archivo rules_input.txt contiene las reglas del ejemplo anterior, el archivo decision_tree_rules.py generado será similar a este:

```python
def apply_decision_tree_rules(df, thresholds):
    """
    Aplica las reglas aprendidas por el árbol de decisión.
    """
    df['Alerta_Temprana'] = 0

    condition = (df['Promedio Notas'] <= 50.40)
    df.loc[condition, 'Alerta_Temprana'] = 1

    condition = (df['Promedio Notas'] > 50.40) & (df['Asistencia (%)'] <= 61.50) & (df['Tareas Entregadas (10)'] <= 6.00) & (df['Asistencia (%)'] > 65.50)
    df.loc[condition, 'Alerta_Temprana'] = 1

    condition = (df['Promedio Notas'] > 50.40) & (df['Asistencia (%)'] <= 61.50) & (df['Tareas Entregadas (10)'] > 6.00)
    df.loc[condition, 'Alerta_Temprana'] = 1

    condition = (df['Promedio Notas'] > 50.40) & (df['Asistencia (%)'] > 61.50) & (df['Asistencia (%)'] <= 90.00)
    df.loc[condition, 'Alerta_Temprana'] = 0

    condition = (df['Promedio Notas'] > 50.40) & (df['Asistencia (%)'] > 61.50) & (df['Asistencia (%)'] > 90.00)
    df.loc[condition, 'Alerta_Temprana'] = 0

    return df
```

---

## **Opciones para el Usuario**
1. **Equipo Técnico**:
   - Si el experto no está familiarizado con el formato `.txt`, el equipo técnico puede trabajar junto a él para codificar las reglas directamente en Python.

2. **Archivo `.txt`**:
   - Si el experto prefiere trabajar de manera independiente, puede llenar el archivo `.txt` siguiendo el formato especificado. Posteriormente, el equipo técnico puede convertirlo en código Python utilizando el script de conversión.

---

## **Notas Importantes**
- **Validación del archivo `.txt`**:
  - Asegúrate de que el archivo `.txt` siga estrictamente el formato especificado para evitar errores durante la conversión.
- **Colaboración con el experto**:
  - Es recomendable que el equipo técnico y el experto trabajen juntos para garantizar que las reglas reflejen correctamente las necesidades del modelo.
- **Pruebas del archivo generado**:
  - Después de generar el archivo Python, realiza pruebas para verificar que las reglas se aplican correctamente a los datos.

Con este flujo, el sistema permite flexibilidad tanto para el equipo técnico como para el experto en la configuración de las reglas del árbol de decisión.
