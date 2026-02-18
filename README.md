# 📊 Análisis Exploratorio - Online Retail Dataset

## Descripción
Análisis exploratorio de datos (EDA) aplicado a un dataset de retail online con transacciones entre 2009 y 2011. El proyecto incluye limpieza de datos, análisis de ventas, segmentación de clientes y análisis RFM.

## Dataset
- **Fuente:** [UCI Machine Learning Repository - Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **Período:** 2009 - 2011
- **Contenido:** Transacciones de una tienda de retail del Reino Unido

## Estructura del proyecto
```
├── online_retail.xlsx                              # Dataset original
├── limpieza_de_datos_completo.py                   # EDA dataset completo
├── limpieza_de_datos_filtrados_y_devoluciones.py   # EDA filtrado y devoluciones
└── README.md
```

## Tecnologías utilizadas
- Python 3.x
- pandas
- matplotlib
- seaborn

## Análisis realizados

### 🧹 Limpieza de datos
- Eliminación de duplicados
- Tratamiento de valores nulos
- Corrección de valores negativos en cantidad
- Separación de devoluciones

### 📈 Análisis exploratorio
- Resumen estadístico por dataset (completo, filtrado, devoluciones)
- Top productos más vendidos por cantidad e ingresos
- Top países por ingresos
- Top clientes por ingresos

### 📅 Análisis temporal
- Ventas diarias
- Ventas por día de la semana
- Ventas mensuales por año

### 🗺️ Visualizaciones
- Boxplot de distribución de cantidades
- Matriz de correlación (heatmap)
- Gráficos de barras por producto y país
- Distribución de ventas por hora
- Heatmap de ventas por mes y producto (Top 20)
- Gráfico de torta: participación de productos en ingresos

### 👥 Análisis RFM
- **Recencia:** días desde la última compra
- **Frecuencia:** número de transacciones por cliente
- **Valor Monetario:** ingresos totales por cliente
- Curva de Pareto: concentración de ingresos en clientes clave

```

## Autor
**Felipe** — Estudiante de Ingeniería en Ciencia de Datos  
Profesor de Matemática y Computación | En transición hacia Data Science
