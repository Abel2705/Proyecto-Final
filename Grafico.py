import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from dash import dash_table
import pandas as pd
import plotly.express as px
import mysql.connector
import dash_table
# Función para conectar a la db con mySQL
def conectar():
    try:
        dbConexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="quesadillas1",
            database="datos"
        )
        cursor = dbConexion.cursor()
        return dbConexion, cursor
    except mysql.connector.Error as e:
        print(e)
        return None, None

# Función para sacar los datos de la bd
def obtener_datos(query):
    dbConexion, cursor = conectar()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    dbConexion.close()
    return resultados

# Convertir resultados en DataFrame
def convertir_a_dataframe(resultados, columnas):
    return pd.DataFrame(resultados, columns=columnas)

# Consulta para obtener datos de comparativa de precios
query_comparativa = "SELECT plataforma, promedio_precio FROM comparativa_precios"

# Consulta para obtener el top 10 de productos mejor calificados en Mercado Libre
query_top_10_calificados_mercado = """
SELECT nombre, rating 
FROM top_10_mejor_calificados_mercado 
WHERE nombre LIKE '%Adidas%' OR nombre LIKE '%adidas%'
"""

# Inicializar la aplicación Dash
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

# Definir el sidebar
sidebar = html.Div(
    [
        html.H4("Productos mejor calificados en Mercado Libre", className="display-50"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Top 10 Mejores calificados Mercado Libre", href="/top-10-calificados-mercado", active="exact"),
                dbc.NavLink("Comparativa de Precios por plataforma", href="/comparativa-precios", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="HORIZONTAL_SIDEBAR_STYLE",
)

content = html.Div(id="page-content", className="CONTENT_STYLE")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return html.P("")

    elif pathname == "/top-10-calificados-mercado":
        # Obtener y convertir los datos en DataFrame
        datos_top_10_calificados_mercado = convertir_a_dataframe(
            obtener_datos(query_top_10_calificados_mercado), ['nombre', 'rating']
        )

        # Crear el gráfico utilizando Plotly Express
        fig = px.bar(
            datos_top_10_calificados_mercado, x='nombre', y='rating',
            title="Top 10 Productos Mejor Calificados en Mercado Libre (Adidas)",
            labels={'nombre': 'Nombre del Producto', 'rating': 'Rating'}
        )
        fig.update_layout(plot_bgcolor="red", paper_bgcolor="black", font={"color": "white"})

        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in datos_top_10_calificados_mercado.columns],
            data=datos_top_10_calificados_mercado.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        )

        return html.Div([
            table,
            dcc.Graph(figure=fig, config={'displayModeBar': False})
        ])

    elif pathname == "/comparativa-precios":
        # convertir los datos en DataFrame
        datos_comparativa = convertir_a_dataframe(obtener_datos(query_comparativa), ['plataforma', 'promedio_precio'])

        # Crear el gráfico utilizando Plotly Express
        fig = px.bar(datos_comparativa, x='plataforma', y='promedio_precio',
                     title="Grafica de barras en precio promedio",
                     labels={'plataforma': 'Plataforma', 'promedio_precio': 'Precio Promedio'})
        fig.update_layout(plot_bgcolor="red", paper_bgcolor="black", font={"color": "white"})

        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in datos_comparativa.columns],
            data=datos_comparativa.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        )

        return html.Div([
            table,
            dcc.Graph(figure=fig,config={'displayModeBar': False})
        ])

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)
