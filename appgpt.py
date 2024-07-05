import streamlit as st
import pandas as pd


def calcular_dividendo(precio_uf, pie_uf, tasa_interes_anual, años):
    monto_prestamo = precio_uf - pie_uf
    tasa_mensual = tasa_interes_anual / 12 / 100
    n = años * 12
    dividendo = (monto_prestamo * tasa_mensual) / (1 - (1 + tasa_mensual) ** -n)
    return dividendo


def obtener_arriendo_promedio(metros_cuadrados, dormitorios):
    # Placeholder: Aquí se puede realizar un web scraping o API call para obtener la información real.
    # Por ahora, vamos a usar un valor estimado.
    return 20 * metros_cuadrados  # Valor estimado por metro cuadrado


# Título de la aplicación
st.title("Recomendador de Departamentos para Inversión en Santiago")

# Cargar el archivo CSV
file_path = '/Users/tomasortiz/Documents/Magister Negocios Digitales/Inteligencia Artificial/departamentos_en_venta.csv'
departamentos = pd.read_csv(file_path)

# Preguntar al usuario sobre el pie y dividendo esperado
pie_uf = st.number_input("¿Cuánto pie puede pagar en UF?", min_value=0.0, step=0.1)
dividendo_esperado_clp = st.number_input("¿Cuál es el dividendo esperado para pagar en CLP?", min_value=0, step=1000)

if st.button("Buscar Departamentos"):
    # Convertir las columnas relevantes a tipos adecuados
    departamentos['Precio (UF)'] = departamentos['Precio (UF)'].str.replace('.', '').astype(float)
    departamentos['Metros Cuadrados'] = departamentos['Metros Cuadrados'].str.extract('(\d+)').astype(float)

    # Parámetros de la tasa de interés y años de crédito
    tasa_interes_anual = 4.0  # Ejemplo, esta tasa debe obtenerse de www.siii.cl
    años_credito = 25

    resultados = []
    for idx, row in departamentos.iterrows():
        precio_uf = row['Precio (UF)']
        metros_cuadrados = row['Metros Cuadrados']
        dormitorios = int(row['Dormitorios'].split()[0])
        baños = int(row['Baños'].split()[0])
        link = row['Link']

        if pie_uf >= precio_uf:
            continue

        dividendo_mensual_uf = calcular_dividendo(precio_uf, pie_uf, tasa_interes_anual, años_credito)
        dividendo_mensual_clp = dividendo_mensual_uf * 30000  # Ejemplo de conversión, ajustar según tasa real

        arriendo_promedio = obtener_arriendo_promedio(metros_cuadrados, dormitorios)
        rentabilidad = (arriendo_promedio - dividendo_mensual_clp) / dividendo_mensual_clp

        if dividendo_mensual_clp <= dividendo_esperado_clp and arriendo_promedio > dividendo_mensual_clp:
            resultados.append({
                'Precio Total (UF)': precio_uf,
                'Pie a Pagar (UF)': pie_uf,
                'Metros Cuadrados': metros_cuadrados,
                'Dormitorios': dormitorios,
                'Baños': baños,
                'Dividendo Mensual (UF)': dividendo_mensual_uf,
                'Dividendo Mensual (CLP)': dividendo_mensual_clp,
                'Arriendo Promedio (CLP)': arriendo_promedio,
                'Rentabilidad Esperada': rentabilidad,
                'Link': link
            })

    if resultados:
        resultados_df = pd.DataFrame(resultados)
        st.write(resultados_df)

        # Descargar los resultados en un archivo CSV
        csv = resultados_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Descargar resultados", data=csv, file_name='resultados_departamentos.csv',
                           mime='text/csv')
    else:
        st.write("No se encontraron departamentos que cumplan con los criterios especificados.")
