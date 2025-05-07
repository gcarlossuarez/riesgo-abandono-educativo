def apply_decision_tree_rules(df, thresholds):
    """
    Aplica las reglas aprendidas por el árbol de decisión.
    """
    df['Alerta_Temprana'] = 0

    condition = (df['Promedio Notas'] <= 50.3)
    df.loc[condition, 'Alerta_Temprana'] = 1
    

    condition = (df['Promedio Notas'] > 50.3) & (df['Asistencia (%)'] <= 61.5) & (df['Tareas Entregadas (10)'] <= 6.0)
    df.loc[condition, 'Alerta_Temprana'] = 1
    

    condition = (df['Promedio Notas'] > 50.3) & (df['Asistencia (%)'] <= 61.5) & (df['Tareas Entregadas (10)'] > 6.0)
    df.loc[condition, 'Alerta_Temprana'] = 1
    

    condition = (df['Promedio Notas'] > 50.3) & (df['Asistencia (%)'] > 61.5) & (df['Asistencia (%)'] <= 92.0)
    df.loc[condition, 'Alerta_Temprana'] = 0
    

    condition = (df['Promedio Notas'] > 50.3) & (df['Asistencia (%)'] > 61.5) & (df['Asistencia (%)'] > 92.0)
    df.loc[condition, 'Alerta_Temprana'] = 0
    

    return df
