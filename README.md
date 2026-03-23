Real Estate / Web Data Scraper CLI
Herramienta en Python para extraer datos estructurados desde archivos HTML o URLs reales, limpiarlos, eliminar duplicados, filtrarlos, ordenarlos y exportarlos a Excel y CSV.

Características
Extracción de datos desde uno o varios archivos HTML
Extracción desde una URL real
Limpieza y normalización de campos numéricos
Eliminación de duplicados por enlace o título
Filtros por ciudad y precio máximo
Ordenación por precio ascendente o descendente
Exportación a Excel (.xlsx) y CSV (.csv)
Uso desde línea de comandos (CLI)
Tecnologías usadas
Python
BeautifulSoup
Requests
Pandas
OpenPyXL
Estructura del proyecto
scraper-inmuebles/
│
├── app/
│   ├── main.py
│   ├── scraper.py
│   ├── parser.py
│   └── exporter.py
│
├── output/
├── sample_properties.html
├── sample_properties_2.html
├── requirements.txt
└── README.md


Instalación

Clona el repositorio y crea un entorno virtual:

    git clone <TU_REPO_URL>
    cd scraper-inmuebles
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Uso
1. Procesar un archivo HTML local
python3 -m app.main --input sample_properties.html 

2. Procesar varios archivos HTML
python3 -m app.main --input sample_properties.html sample_properties_2.html

3. Filtrar por ciudad
python3 -m app.main --input sample_properties.html sample_properties_2.html --city Málaga

4. Filtrar por precio máximo
python3 -m app.main --input sample_properties.html sample_properties_2.html --max-price 200000

5. Ordenar por precio descendente
python3 -m app.main --input sample_properties.html sample_properties_2.html --desc

6. Elegir nombre de salida
python3 -m app.main --input sample_properties.html sample_properties_2.html --output-name malaga_filtrado

Esto generará:

output/malaga_filtrado.xlsx

output/malaga_filtrado.csv

7. Procesar una URL real

               python3 -m app.main --url https://books.toscrape.com/ --output-name books_demo

Salida

La herramienta genera dos archivos:

- Excel (.xlsx)

- CSV (.csv)

Ejemplo de columnas exportadas:

- titulo

- precio_texto

-precio

- ubicacion

- metros_texto

- metros

- disponibilidad

- enlace

Funcionalidades implementadas

- Parsing de HTML estructurado

- Adaptación a una web real de prueba

- Soporte para múltiples fuentes

- Deduplicación de registros

- Filtros configurables

- Ordenación

- Exportación profesional

- Casos de uso

- Este proyecto puede adaptarse fácilmente para:

- scraping inmobiliario

- extracción de productos ecommerce

- comparadores de precios

- directorios de empresas

- lead generation

- automatización de informes

Mejoras futuras

- Soporte para paginación

- Exportación a JSON

- Soporte para múltiples selectores por web

- Interfaz web simple

- Programación automática de ejecuciones

Autor

Proyecto desarrollado por Juan Carrasco como parte de un portfolio orientado a automatización, scraping y trabajos freelance en Python.