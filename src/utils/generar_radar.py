import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def crear_grafico_radar():
    ruta_datos = os.path.join("data", "processed", "delanteros_analizados.csv")
    
    if not os.path.exists(ruta_datos):
        print("Error: Primero debes ejecutar el script de procesamiento.")
        return

    # 1. Cargar los datos procesados
    df = pd.read_csv(ruta_datos)

    # 2. Configurar métricas y jugadores
    metricas = ["npxG_per90", "tiros_puerta_per90", "toques_area_per90", "duelos_aereos_ganados_pct", "conversion_goles_pct"]
    etiquetas = ["Goles Esperados\n(npxG)", "Tiros a Puerta", "Toques en Area", "% Duelos Aereos", "% Conversion\nGoles"]
    
    jugador_1 = "Ariete Barakaldo"
    jugador_2 = "Ganga SegundaRFEF"

    # 3. Extraer valores y normalizarlos (para que todos escalen de 0 a 1 de forma justa en el gráfico)
    # npxG(0-0.6), Tiros(0-2), Toques(0-6), Duelos(0-100), Conversión(0-25)
    maximos = [0.6, 2.0, 6.0, 100.0, 25.0]
    
    valores_j1 = df[df["jugador"] == jugador_1][metricas].values[0] / maximos
    valores_j2 = df[df["jugador"] == jugador_2][metricas].values[0] / maximos

    # Cerrar el círculo del radar repitiendo el primer valor al final
    valores_j1 = np.append(valores_j1, valores_j1[0])
    valores_j2 = np.append(valores_j2, valores_j2[0])

    # Calcular los ángulos de cada línea del radar
    angulos = np.linspace(0, 2 * np.pi, len(metricas), endpoint=False).tolist()
    angulos += angulos[:1]

    # 4. Diseñar el gráfico (Estética gualdinegra de Lasesarre)
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#121212")
    ax.set_facecolor("#1E1E1E")

    # Dibujar las líneas del radar para cada jugador
    # Amarillo (#FFD700) para el Barakaldo CF y Cian (#00FFFF) para el candidato
    ax.plot(angulos, valores_j1, color="#FFD700", linewidth=2, label=jugador_1)
    ax.fill(angulos, valores_j1, color="#FFD700", alpha=0.3)

    ax.plot(angulos, valores_j2, color="#00FFFF", linewidth=2, label=jugador_2)
    ax.fill(angulos, valores_j2, color="#00FFFF", alpha=0.2)

    # Configurar las etiquetas de los ejes
    ax.set_xticks(angulos[:-1])
    ax.tick_params(pad=15) 
    ax.set_xticklabels(etiquetas, color="#FFFFFF", fontsize=9)
    ax.set_yticklabels([]) # Ocultamos los números internos para una estética limpia estilo Scout

    # Título y Leyenda
    plt.title(f"Comparativa Táctica: {jugador_1} vs {jugador_2}", color="#FFFFFF", fontsize=12, pad=20, weight="bold")
    ax.legend(loc="upper left", bbox_to_anchor=(1.15, 1.0))

    # 5. Guardar el gráfico en la carpeta de la app web
    ruta_guardar = os.path.join("app", "radar_scouting.png")
    os.makedirs(os.path.dirname(ruta_guardar), exist_ok=True)
    plt.savefig(ruta_guardar, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    
    print(f"🎯 Grafico de radar guardado con exito en: {ruta_guardar}")

if __name__ == "__main__":
    crear_grafico_radar()