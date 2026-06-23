import os
import pandas as pd

# 1. Definir rutas absolutas/relativas del proyecto
RUTA_ENTRADA = os.path.join("data", "raw", "delanteros.csv")
RUTA_SALIDA = os.path.join("data", "processed", "delanteros_analizados.csv")

def cargar_y_procesar_datos():
    # Verificar si el archivo origen existe
    if not os.path.exists(RUTA_ENTRADA):
        print(f"Error: No se encuentra el archivo en {RUTA_ENTRADA}")
        return

    # 2. Cargar los datos en bruto con Pandas
    df = pd.read_csv(RUTA_ENTRADA)
    print("⚽ Datos en bruto cargados correctamente.")

    # 3. Algoritmo: Calcular el Score de Eficiencia Goleadora (de 0 a 100)
    # Combinamos las 3 métricas clave dándoles un peso equilibrado
    df["score_eficiencia"] = (
        (df["npxG_per90"] * 40) + 
        (df["conversion_goles_pct"] * 2) + 
        (df["toques_area_per90"] * 6)
    )
    
    # Redondear a un decimal para que quede limpio
    df["score_eficiencia"] = df["score_eficiencia"].round(1)

    # 4. Clasificar el perfil del delantero según su edad y rendimiento
    # Un club de Primera busca revalorizar activos, la edad es clave
    def clasificar_perfil(row):
        if row["edad"] <= 21 and row["score_eficiencia"] >= 40:
            return "Talento Sub-21 Proyección"
        elif row["score_eficiencia"] >= 45:
            return "Objetivo Prioritario Mercado"
        else:
            return "Perfil Regular / Complementario"

    df["perfil_scouting"] = df.apply(clasificar_perfil, axis=1)

    # 5. Ordenar los resultados de mejor a peor rendimiento
    df = df.sort_values(by="score_eficiencia", ascending=False)

    # 6. Guardar los datos limpios en la carpeta processed
    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
    df.to_csv(RUTA_SALIDA, index=False)
    print(f"📊 Procesamiento completado. Archivo guardado en: {RUTA_SALIDA}")
    
    # Mostrar el resultado final por consola de forma estética
    print("\n--- INFORME PRELIMINAR DE SCOUTING ---")
    print(df[["jugador", "equipo", "edad", "score_eficiencia", "perfil_scouting"]].to_string(index=False))

if __name__ == "__main__":
    cargar_y_procesar_datos()