import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# --- Título ---
st.title("Dashboard Predictivo de Liquidez y Rentabilidad")
st.write("Simula la proyección de tu flujo de caja y rentabilidad mensual basada en tus ingresos y costes estimados.")

# --- Formulario de entrada ---
with st.form("finanzas_form"):
    meses = st.slider("Número de meses a proyectar", 3, 24, 12)
    ingresos_iniciales = st.number_input("Ingresos mensuales iniciales (€)", value=8000)
    crecimiento_ingresos = st.slider("Crecimiento mensual de ingresos (%)", -10, 20, 2)
    costes_fijos = st.number_input("Costes fijos mensuales (€)", value=3000)
    costes_variables_pct = st.slider("Costes variables (% de ingresos)", 0, 100, 35)

    submitted = st.form_submit_button("Generar proyección")

# --- Calcular proyección ---
def proyectar_flujo(meses, ingresos_0, crecimiento_pct, fijos, var_pct):
    ingresos = [ingresos_0 * ((1 + crecimiento_pct/100) ** i) for i in range(meses)]
    variables = [i * (var_pct/100) for i in ingresos]
    costes = [fijos + v for v in variables]
    flujo = [ing - c for ing, c in zip(ingresos, costes)]
    rentabilidad = [f / i * 100 if i != 0 else 0 for f, i in zip(flujo, ingresos)]
    return pd.DataFrame({
        "Mes": list(range(1, meses+1)),
        "Ingresos": ingresos,
        "Costes Totales": costes,
        "Flujo Neto": flujo,
        "Rentabilidad (%)": rentabilidad
    })

# --- Mostrar resultados ---
if submitted:
    df = proyectar_flujo(meses, ingresos_iniciales, crecimiento_ingresos, costes_fijos, costes_variables_pct)

    st.subheader("Tabla de Proyección")
    st.dataframe(df.style.format({"Ingresos": "{:,.0f}", "Costes Totales": "{:,.0f}", "Flujo Neto": "{:,.0f}", "Rentabilidad (%)": "{:.1f}%"}))

    st.subheader("Gráficos")
    fig1, ax1 = plt.subplots()
    ax1.plot(df["Mes"], df["Ingresos"], label="Ingresos", marker='o')
    ax1.plot(df["Mes"], df["Costes Totales"], label="Costes Totales", marker='o')
    ax1.plot(df["Mes"], df["Flujo Neto"], label="Flujo Neto", marker='o')
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("€")
    ax1.set_title("Proyección Financiera Mensual")
    ax1.legend()
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.bar(df["Mes"], df["Rentabilidad (%)"], color='green')
    ax2.set_xlabel("Mes")
    ax2.set_ylabel("Rentabilidad (%)")
    ax2.set_title("Rentabilidad proyectada")
    st.pyplot(fig2)

    st.info("Para un análisis financiero más profundo, puedes exportar estos datos y combinarlos con KPIs personalizados de tu empresa.")
