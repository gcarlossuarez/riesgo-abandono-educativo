from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd
import sys
#from dtreeviz.trees import dtreeviz
#import graphviz
#import dtreeviz

def analyze_model(model, X):
    """Analiza el modelo entrenado mostrando reglas del primer árbol y la importancia de características."""
    from sklearn.tree import export_text
    import pandas as pd

    # Inspecciona el primer árbol del bosque
    tree_rules = export_text(model.estimators_[0], feature_names=X.columns.tolist())
    print("Reglas del primer árbol del bosque:")
    print(tree_rules)

    # Calcula la importancia de las características
    feature_importances = pd.DataFrame({
        'Característica': X.columns,
        'Importancia': model.feature_importances_
    }).sort_values(by='Importancia', ascending=False)

    print("\nImportancia de las características:")
    print(feature_importances)

    from sklearn.tree import export_graphviz
    import graphviz

    # Exporta el primer árbol del bosque
    dot_data = export_graphviz(
        model.estimators_[0],
        out_file=None,
        feature_names=X.columns,
        class_names=["No Riesgo", "Sí Riesgo"],
        filled=True,
        rounded=True,
        special_characters=True
    )

    # Visualiza el árbol
    graph = graphviz.Source(dot_data)
    graph.view()



def prepare_features(df):
    """Prepara características para el modelo"""
    # Convertir participación a numérico
    le = LabelEncoder()
    df['Participación_encoded'] = le.fit_transform(df['Participación'])
    
    features = df[['Asistencia (%)', 'Promedio Notas', 'Tareas Entregadas (10)', 'Participación_encoded']]
    return features, le

def train_model(X, y):
    """Entrena el modelo de Random Forest"""
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X, y)
    return model
    

def save_model(model, encoder, output_path):
    """Guarda modelo y preprocesadores"""
    joblib.dump({'model': model, 'encoder': encoder}, output_path)
    print(f"Modelo guardado en {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python model_training.py <datos_procesados.csv>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    try:
        df = pd.read_csv(input_file)
        
        # Preparar datos
        X, encoder = prepare_features(df)
        y = df['Riesgo']
        
        # Entrenar modelo
        model = train_model(X, y)
        
        
        # Llamar a la función para analizar el modelo
        analyze_model(model, X)

        '''
        # Solo tomamos el primer árbol del bosque
        dot_data = export_graphviz(
            model.estimators_[0],
            out_file=None,
            feature_names=X.columns,
            class_names=["No Riesgo", "Riesgo"],
            filled=True,
            rounded=True,
            special_characters=True
        )
        graph = graphviz.Source(dot_data)
        graph.render("primer_arbol", format="png", cleanup=False)
        graph.view()
        '''
        
        '''
        viz = dtreeviz.dtreeviz(
            model.estimators_[0],
            X,
            y,
            feature_names=X.columns.tolist(),
            target_name="Riesgo",
            class_names=["No Riesgo", "Riesgo"]
        )
        viz.save("primer_arbol.svg")
        viz.view()
        '''
        

        # Guardar modelo
        save_model(model, encoder, 'modelo_riesgo.pkl')
        
        # Evaluación rápida
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("\nPrecisión en entrenamiento:", model.score(X_train, y_train))
        print("Precisión en prueba:", model.score(X_test, y_test))
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

