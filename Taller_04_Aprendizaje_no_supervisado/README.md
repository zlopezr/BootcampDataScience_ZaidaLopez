# Taller 04: Descubriendo Patrones Musicales con Spotify

Análisis de clustering sobre un dataset de 1000 canciones de Spotify, aplicando reducción de dimensionalidad (PCA) y dos algoritmos de agrupamiento no supervisado: **K-Means** y **DBSCAN**.

## Descripción del caso

El objetivo es identificar grupos de canciones que comparten características musicales similares (energía, acústica, ritmo, etc.), sin depender de etiquetas de género previamente definidas. Esto simula un escenario real de una plataforma de streaming que busca mejorar su sistema de recomendación a partir de patrones "ocultos" en los datos de audio.

## Dataset

- **Archivo:** `spotifydataset.csv`
- **Tamaño:** 1000 canciones, 23 columnas
- **Características de audio usadas:** `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`

## Estructura del notebook

| Bloque | Contenido |
|---|---|
| 1 | Configuración y carga de datos |
| 2 | Limpieza y selección de las columnas de audio (features) |
| 3 | Reducción de dimensionalidad con **PCA** (escalado previo con `StandardScaler`, 2 componentes ≈ 48% de varianza explicada) |
| 4 | Modelado con **K-Means** (método del codo para elegir K=5) |
| 4b | Modelado alternativo con **DBSCAN** (exploración de `eps` y `min_samples`) |
| 5 | Visualización e interpretación de los clusters (perfiles promedio, heatmaps, proyección PCA) |

## Metodología

1. Se seleccionaron únicamente columnas numéricas de audio, descartando texto, identificadores y metadatos no relevantes para el "sonido" de la canción.
2. Se estandarizaron los datos (`StandardScaler`) para que todas las características tuvieran la misma escala antes de aplicar PCA y los algoritmos de clustering.
3. Se aplicó **PCA** para visualizar los datos en 2D, identificando que las 2 primeras componentes capturan ~48% de la variabilidad total.
4. Se aplicó **K-Means**, usando el método del codo para elegir K=5, obteniendo 5 grupos de tamaños desiguales (379, 54, 331, 99 y 137 canciones).
5. Se aplicó **DBSCAN** sobre los mismos datos escalados, explorando distintos valores de `eps` para entender la densidad de los datos.
6. Se compararon ambos enfoques cruzando sus resultados (tabla de contingencia).

## Resultados principales

- **K-Means (K=5)** encontró grupos con perfiles musicales reconocibles: canciones acústicas/experimentales, rap/hip-hop (alto `speechiness`), baladas tipo piano-voz, y dos grupos de pop/rock de alta energía que dominan el dataset (>70% de las canciones).
- **DBSCAN** no encontró múltiples grupos medianos —en su lugar, identificó un cluster principal denso y marcó ~13.4% de las canciones como ruido (outliers).
- El **ruido detectado por DBSCAN coincide casi por completo** con el cluster más pequeño y distintivo de K-Means (el grupo acústico/experimental), validando ese hallazgo con dos métodos independientes.

## Conclusiones

1. **Los clusters reflejan estilos musicales reconocibles**, aunque el modelo nunca recibió información de artista o género — las características de audio por sí solas son suficientes para diferenciar estilos.
2. **DBSCAN "redescubrió" el mismo grupo atípico que K-Means**, mostrando que los datos forman una nube continua de estilos pop/rock mainstream, con un pequeño grupo claramente diferenciado (acústico/experimental).
3. **El estilo "mainstream" domina el dataset**: más del 70% de las canciones caen en los dos clusters de mayor energía y bailabilidad, típicos de listas de popularidad.

## Tecnologías utilizadas

- Python 3
- `pandas`, `numpy`
- `scikit-learn` (`StandardScaler`, `PCA`, `KMeans`, `DBSCAN`, `NearestNeighbors`)
- `matplotlib`, `seaborn`

## Cómo ejecutar

1. Asegúrate de tener instaladas las librerías mencionadas (`pip install pandas numpy scikit-learn matplotlib seaborn`).
2. Coloca `spotifydataset.csv` en la misma carpeta que el notebook.
3. Abre `Actividad_Spotify_clustering.ipynb` y ejecuta todas las celdas en orden (Kernel → Restart & Run All).
