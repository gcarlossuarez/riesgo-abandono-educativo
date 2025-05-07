def apply_decision_tree_rules(df, thresholds):
    """Genera alertas tempranas basadas en reglas"""
    df['Alerta_Temprana'] = 0
    #df.loc[(df['Asistencia (%)'] < 60) & (df['Participación'] == 'Baja'), 'Alerta_Temprana'] = 1
    #df.loc[(df['Tareas Entregadas (10)'] < 3), 'Alerta_Temprana'] = 1
    #df.loc[df['Promedio Notas'] < 50, 'Alerta_Temprana'] = 1
    df.loc[(df['Asistencia (%)'] < thresholds['asistencia_threshold']) & (df['Participación'] == 'Baja'), 'Alerta_Temprana'] = 1
    df.loc[(df['Tareas Entregadas (10)'] < thresholds['tareas_threshold']), 'Alerta_Temprana'] = 1
    df.loc[df['Promedio Notas'] < thresholds['notas_threshold'], 'Alerta_Temprana'] = 1
    return df
