import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
import datetime

# URL de la página web
url = "https://elpais.com/noticias/ecologia/"

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la etiqueta <title>
    title_tag = soup.find('title')

    # Obtener el contenido del título
    title = title_tag.text.strip() if title_tag else "Título no encontrado"

    # Encontrar la etiqueta <p> con la clase "c_d" para la descripción
    descripcion_tag = soup.find("p", class_="c_d")
    # Verificar si la etiqueta <p> fue encontrada
    descripcion = descripcion_tag.text.strip() if descripcion_tag else "Descripción no encontrada"
    print("Descripción:", descripcion)

    # Encontrar la etiqueta <img> con la clase "c_m_e _re a_m-h" para la imagen
    img_tag = soup.find("img", class_="c_m_e _re a_m-h")
    # Verificar si la etiqueta <img> fue encontrada
    imagen_url = img_tag.get("src") if img_tag else None
    print("URL de la imagen:", imagen_url)

    # Fecha y hora de la noticia
    fecha_hora = datetime.datetime.now()

    # Creamos un DataFrame de Pandas
    df = pd.DataFrame({
        "titulo": [title],
        "descripcion": [descripcion],
        "imagen_url": [imagen_url],
        "fecha": [fecha_hora]
    })

    # Imprimimos el DataFrame
    print(df)

    # Establecemos la conexión con la base de datos MySQL
    mydb = mysql.connector.connect(
        host="jorge246.mysql.database.azure.com",
        user="administrador",
        password="Math2468013579",
        database="noticie",
        port="3306"
    )

    # Insertamos los datos en la tabla noticie
    cursor = mydb.cursor()
    sql = "INSERT INTO noticie (titulo, descripcion, linkimagen, fecha) VALUES (%s, %s, %s, %s)"
    valores = (title, descripcion, imagen_url, fecha_hora)
    cursor.execute(sql, valores)
    mydb.commit()
    cursor.close()

    # Al imprimir este mensaje es sinónimo de la finalización de la consulta.
    print("Noticia almacenada correctamente en nuestra base de datos")

else:
    print("Error al acceder a la página. Código de estado:", response.status_code)

