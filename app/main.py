import os
import pandas as pd
import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="Lasesarre Intelligence", page_icon="⚽", layout="wide")

# Título de la herramienta
st.title("⚽ Lasesarre Intelligence: Recruitment System")
st.markdown("Plataforma avanzada de scouting e identificación de talento para el **Barakaldo CF**.")
st.write("---")

# Ruta de los datos procesados
ruta_datos = os.path.join("data", "processed", "delanteros_analizados.csv")

if os.path.exists(ruta_datos):
    df = pd.read_csv(ruta_datos)
    
    # 1. Filtros Interactivos en la barra lateral (Sidebar)
    st.sidebar.header("Filtros de Búsqueda")
    edad_max = st.sidebar.slider("Edad Máxima", int(df["edad"].min()), 35, 25)
    
    # Filtrar el dataframe según el input del usuario
    df_filtrado = df[df["edad"] <= edad_max]
    
    # 2. Diseño de la pantalla principal en 2 columnas
    col1, col2 = st.columns([1.2, 1]) # Columna 1 un poco más ancha para la tabla
    
    with col1:
        st.subheader("🎯 Candidatos Recomendados")
        # Mostrar tabla interactiva sin el índice aburrido de Pandas
        st.dataframe(
            df_filtrado[["jugador", "equipo", "liga", "edad", "score_eficiencia", "perfil_scouting"]],
            use_container_width=True,
            hide_index=True
        )
        st.info("💡 El 'Score de Eficiencia' pondera npxG, toques en área y acierto de cara a puerta.")
        
    with col2:
        st.subheader("📊 Comparativa Táctica Avanzada")
        ruta_radar = os.path.join("app", "radar_scouting.png")
        if os.path.exists(ruta_radar):
            # Cargar la imagen del radar gualdinegro que acabas de generar
            st.image(ruta_radar, use_container_width=True)
else:
    st.error("No se han encontrado datos procesados en la carpeta. Ejecuta primero los scripts de procesamiento.")