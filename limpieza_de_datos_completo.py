import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================================================
#   ANALISIS EXPLORATORIO - ONLINE RETAIL DATASET
#   Dataset: online_retail.xlsx (2009-2011)
#   Autor: Felipe
# ================================================

# LEER Y COMBINAR HOJAS
hojas = pd.read_excel("online_retail.xlsx", sheet_name=["2009-2010", "2010-2011"])
df = pd.concat(hojas.values(), ignore_index=True)

# INGENIERIA DE FEATURES
df["Total_price"] = df["Quantity"] * df["Price"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Fecha"] = df["InvoiceDate"].dt.date
df["Año"] = df["InvoiceDate"].dt.year
df["Hora"] = df["InvoiceDate"].dt.time
df["Mes"] = df["InvoiceDate"].dt.month
df["Dia_semana"] = pd.to_datetime(df["Fecha"]).dt.day_name()
df["Hora_num"] = pd.to_datetime(df["Hora"].astype(str)).dt.hour

# LIMPIEZA DE DATOS
df = df.drop_duplicates()
df["Description"] = df["Description"].fillna("Unknown").replace("?", "Unknown")
df["Customer_ID"] = df["Customer_ID"].fillna("Unknown")

# SEGMENTACION DE DATOS
df_filtrado = df[(df["Quantity"] > 0) & (df["Quantity"] < 1000)]
devoluciones = df[df["Quantity"] < 0]

datasets = [("COMPLETO", df), ("FILTRADO", df_filtrado), ("DEVOLUCIONES", devoluciones)]

# ================================================
#   1. INFORMACION GENERAL
# ================================================
print("\nINFORMACION GENERAL\n")
print(df.info())
print("\nPRIMEROS REGISTROS:\n")
print(df.head())

# ================================================
#   2. RESUMEN ESTADISTICO
# ================================================
print("\n=== RESUMEN ESTADISTICO ===\n")
for nombre, data in datasets:
    print(f"\n{nombre}:")
    print(data[["Quantity", "Price", "Total_price"]].describe().T)

# ================================================
#   3. TOP VENTAS
# ================================================
print("\n=== TOP VENTAS ===\n")
for nombre, data in datasets:
    print(f"\nTop 5 productos por cantidad - {nombre}:")
    print(data.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(5))

    print(f"\nTop 5 paises por ingresos - {nombre}:")
    print(data.groupby("Country").agg({"Total_price": "sum"}).sort_values("Total_price", ascending=False).head(5))

    print(f"\nTop 5 productos por ingresos - {nombre}:")
    print(data.groupby("Description").agg({"Total_price": "sum"}).sort_values("Total_price", ascending=False).head(5))

    print(f"\nTop 10 clientes por ingresos - {nombre}:")
    print(data.groupby("Customer_ID")["Total_price"].sum().sort_values(ascending=False).head(10))

# ================================================
#   4. GRAFICOS - DISTRIBUCION Y OUTLIERS
# ================================================
for nombre, data in datasets:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=data["Quantity"])
    plt.title(f"Distribución de Quantity - {nombre}")
    plt.tight_layout()
    plt.show()

# ================================================
#   5. MATRIZ DE CORRELACION
# ================================================
for nombre, data in datasets:
    plt.figure(figsize=(7, 5))
    corr = data[["Quantity", "Price", "Total_price"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title(f"Correlación entre variables numéricas - {nombre}")
    plt.tight_layout()
    plt.show()

# ================================================
#   6. VENTAS TEMPORALES
# ================================================
for nombre, data in datasets:
    # Ventas diarias
    ventas_diarias = data.groupby("Fecha")["Total_price"].sum()
    plt.figure(figsize=(12, 6))
    ventas_diarias.plot()
    plt.title(f"Ventas diarias - {nombre}")
    plt.tight_layout()
    plt.show()

    # Ventas por dia de semana
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Dia_semana", y="Total_price", data=data, estimator=sum,
                order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.title(f"Ingresos por día de la semana - {nombre}")
    plt.tight_layout()
    plt.show()

    # Ventas mensuales por año
    ventas_mensuales = data.groupby(["Mes", "Año"])["Total_price"].sum().reset_index()
    plt.figure(figsize=(10, 6))
    for año in sorted(ventas_mensuales["Año"].unique()):
        datos = ventas_mensuales[ventas_mensuales["Año"] == año]
        plt.plot(datos["Mes"], datos["Total_price"], marker="o", label=str(año))
    plt.title(f"Ventas mensuales por año - {nombre}")
    plt.xlabel("Mes")
    plt.ylabel("Ingresos totales")
    plt.xticks(range(1, 13))
    plt.legend(title="Año")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ================================================
#   7. PRODUCTOS Y PAISES
# ================================================
for nombre, data in datasets:
    # Top 10 productos mas vendidos
    top_productos = data.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_productos.values, y=top_productos.index, palette="viridis")
    plt.title(f"Top 10 productos más vendidos - {nombre}")
    plt.xlabel("Cantidad total")
    plt.ylabel("Producto")
    plt.tight_layout()
    plt.show()

    # Top 10 paises por ingresos
    top_paises = data.groupby("Country")["Total_price"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_paises.values, y=top_paises.index, palette="magma")
    plt.title(f"Top 10 países por ingresos - {nombre}")
    plt.xlabel("Ingresos totales")
    plt.ylabel("País")
    plt.tight_layout()
    plt.show()

    # Ventas por hora
    plt.figure(figsize=(10, 6))
    sns.histplot(data, x="Hora_num", weights="Total_price", bins=24, color="steelblue")
    plt.title(f"Distribución de ventas por hora - {nombre}")
    plt.xlabel("Hora del día")
    plt.ylabel("Ingresos totales")
    plt.tight_layout()
    plt.show()

    # Heatmap ventas por mes y producto (Top 20)
    top20 = data.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(20).index
    ventas_mes_producto = (data[data["Description"].isin(top20)]
                           .groupby(["Mes", "Description"])["Quantity"].sum().reset_index())
    pivot = ventas_mes_producto.pivot(index="Description", columns="Mes", values="Quantity").fillna(0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap="YlGnBu", cbar_kws={"label": "Cantidad"})
    plt.title(f"Ventas por mes y producto (Top 20) - {nombre}")
    plt.tight_layout()
    plt.show()

    # Participacion de productos en ingresos (Pie chart)
    ingresos_productos = (data[data["Total_price"] > 0]
                          .groupby("Description")["Total_price"].sum().sort_values(ascending=False))
    top5 = ingresos_productos.head(5)
    otros = ingresos_productos.iloc[5:].sum()
    pie_data = pd.concat([top5, pd.Series({"Otros": otros})])
    plt.figure(figsize=(8, 8))
    plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
    plt.title(f"Participación de productos en ingresos - {nombre}")
    plt.tight_layout()
    plt.show()

# ================================================
#   8. ANALISIS RFM (Recencia, Frecuencia, Valor)
# ================================================
print("\n=== ANALISIS RFM ===\n")
for nombre, data in datasets:
    fecha_max = data["InvoiceDate"].max()
    fecha_referencia = fecha_max + pd.Timedelta(days=1)
    print(f"\n{nombre} - Fecha de referencia: {fecha_referencia.date()}")

    df_rfm = (data.groupby("Customer_ID")
              .agg({"InvoiceDate": ["count", "max"], "Total_price": "sum"})
              .reset_index())
    df_rfm = df_rfm[df_rfm["Customer_ID"] != "Unknown"]
    df_rfm.columns = ["Customer_ID", "Frecuencia", "Ultima_Compra", "Valor_Monetario"]
    df_rfm["Recencia"] = (fecha_referencia - df_rfm["Ultima_Compra"]).dt.days

    print(df_rfm.head())
    print("\nEstadísticas RFM:")
    print(df_rfm[["Recencia", "Frecuencia", "Valor_Monetario"]].describe().T)

    # Graficos RFM
    for col, titulo in [("Recencia", "Días desde última compra"),
                        ("Frecuencia", "Número de transacciones"),
                        ("Valor_Monetario", "Ingresos totales por cliente")]:
        plt.figure(figsize=(10, 3))
        sns.histplot(df_rfm[col], bins=50, kde=True)
        plt.title(f"Distribución de {titulo} - {nombre}")
        plt.tight_layout()
        plt.show()

    # Curva de Pareto
    ingresos_clientes = df_rfm.groupby("Customer_ID")["Valor_Monetario"].sum().sort_values(ascending=False)
    porcentaje = ingresos_clientes.cumsum() / ingresos_clientes.sum()
    clientes_80 = (porcentaje <= 0.8).sum()

    plt.figure(figsize=(10, 6))
    porcentaje.reset_index(drop=True).plot()
    plt.axhline(0.8, color="red", linestyle="--")
    plt.text(clientes_80, 0.82, f"{clientes_80} clientes ≈ 80% ingresos", color="red")
    plt.title(f"Curva de Pareto - Concentración de ingresos por cliente - {nombre}")
    plt.xlabel("Clientes ordenados por ingresos")
    plt.ylabel("Porcentaje acumulado")
    plt.tight_layout()
    plt.show()
