#  Football Data Analysis – Bootcamp Data Science

##  Descripción del proyecto

Este proyecto analiza datos históricos de partidos internacionales de fútbol utilizando Python y pandas.
El objetivo es identificar patrones de rendimiento de equipos, torneos y jugadores a través de métricas clave.



##  Dataset

Se trabajó con múltiples fuentes de datos:

https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017/data

* **results.csv** → resultados de partidos
* **goalscorers.csv** → detalle de goleadores
* **shootouts.csv** → tandas de penales
* **former_names.csv** → historial de nombres de equipos



##  Limpieza y preparación de datos

Se realizaron las siguientes etapas:

* Eliminación de valores nulos en variables críticas
* Conversión de fechas a formato datetime
* Validación y eliminación de duplicados
* Estandarización de nombres de equipos
* Creación de variables derivadas (goles totales, métricas de victoria, etc.)



## Preguntas de análisis

El análisis se enfocó en responder:

1. ¿Cuál es el **Top 15 de equipos en la historia con mejor win rate** (mínimo 20 partidos)?
2. ¿Qué **torneos han tenido más goles por partido** en los últimos 5 años?
3. ¿Cuál es el **Top 20 de jugadores con mayor número de goles** en diferentes torneos durante los últimos 5 años?



## Tecnologías utilizadas

* Python
* pandas
* Jupyter Notebook



## Principales análisis realizados

### Rendimiento de equipos

* Cálculo de win rate (% de victorias)
* Filtro de equipos con al menos 20 partidos
* Ranking de los equipos más consistentes históricamente

### Análisis de torneos

* Cálculo de goles totales y promedio por partido
* Filtrado de los últimos 5 años
* Identificación de torneos más ofensivos

### Análisis de jugadores

* Conteo de goles por jugador
* Análisis por torneo
* Ranking de máximos goleadores recientes



##  Cómo ejecutar el proyecto

1. Clonar el repositorio:

```
git clone https://github.com/tu-usuario/BootcampDataScience_ZaidaLopez.git
```

2. Instalar dependencias:

```
pip install pandas
```

3. Ejecutar los notebooks o scripts



##  Conclusiones

* Se identificaron equipos con alta consistencia histórica en términos de victorias
* Algunos torneos presentan mayor promedio de goles, lo que sugiere estilos de juego más ofensivos
* Los rankings de goleadores recientes permiten identificar jugadores con alto impacto en diferentes competiciones



##  Autor

Zaida Lopez
Proyecto realizado como parte de Bootcamp de Data Science
