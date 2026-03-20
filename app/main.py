import argparse
from pathlib import Path
from app.parser import parse_properties
from app.exporter import export_to_excel, export_to_csv
from app.scraper import fetch_page


def filter_properties(
    properties: list[dict],
    city: str | None = None,
    max_price: float | None = None
) -> list[dict]:
    filtered = properties

    if city:
        filtered = [
            p for p in filtered
            if p["ubicacion"].lower() == city.lower()
        ]

    if max_price is not None:
        filtered = [
            p for p in filtered
            if p["precio"] is not None and p["precio"] <= max_price
        ]

    return filtered


def sort_properties_by_price(
    properties: list[dict],
    ascending: bool = True
) -> list[dict]:
    return sorted(
        properties,
        key=lambda p: p["precio"] if p["precio"] is not None else float("inf"),
        reverse=not ascending
    )


def deduplicate_properties(properties: list[dict]) -> list[dict]:
    seen_links = set()
    seen_titles = set()
    unique_properties = []

    for prop in properties:
        link = (prop.get("enlace") or "").strip().lower()
        title = (prop.get("titulo") or "").strip().lower()

        if link:
            if link in seen_links:
                continue
            seen_links.add(link)
        else:
            if title in seen_titles:
                continue
            seen_titles.add(title)

        unique_properties.append(prop)

    return unique_properties


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extractor y filtrador de inmuebles/libros desde HTML o URL"
    )

    parser.add_argument(
        "--input",
        nargs="+",
        help="Una o varias rutas de archivos HTML de entrada"
    )

    parser.add_argument(
        "--url",
        type=str,
        help="URL de una página HTML para scrapear"
    )

    parser.add_argument(
        "--city",
        type=str,
        help="Filtrar por ciudad exacta"
    )

    parser.add_argument(
        "--max-price",
        type=float,
        help="Precio máximo, por ejemplo: 30.5"
    )

    parser.add_argument(
        "--desc",
        action="store_true",
        help="Ordenar por precio descendente"
    )

    parser.add_argument(
        "--output-name",
        type=str,
        default="resultado",
        help="Nombre base de los archivos de salida, sin extensión"
    )

    return parser.parse_args()


def load_properties_from_files(file_paths: list[str]) -> list[dict]:
    all_properties = []

    for file_path in file_paths:
        html_file = Path(file_path)

        if not html_file.exists():
            print(f"No se encontró el archivo HTML: {html_file}")
            continue

        html = html_file.read_text(encoding="utf-8")
        properties = parse_properties(html)

        print(f"{html_file}: {len(properties)} elementos extraídos")
        all_properties.extend(properties)

    return all_properties


def load_properties_from_url(url: str) -> list[dict]:
    try:
        html = fetch_page(url)
        properties = parse_properties(html, base_url=url)
        print(f"URL procesada: {url}")
        print(f"Elementos extraídos desde URL: {len(properties)}")
        return properties
    except Exception as e:
        print(f"Error al procesar la URL: {e}")
        return []


def main():
    args = parse_args()

    properties = []

    if args.input:
        properties.extend(load_properties_from_files(args.input))

    if args.url:
        properties.extend(load_properties_from_url(args.url))

    if not args.input and not args.url:
        print("Debes indicar --input o --url")
        return

    if not properties:
        print("No se encontraron elementos en ninguna fuente.")
        return

    total_before_dedup = len(properties)
    unique_properties = deduplicate_properties(properties)
    total_duplicates_removed = total_before_dedup - len(unique_properties)

    filtered_properties = filter_properties(
        unique_properties,
        city=args.city,
        max_price=args.max_price
    )

    if not filtered_properties:
        print("No hay elementos tras aplicar filtros.")
        return

    sorted_properties = sort_properties_by_price(
        filtered_properties,
        ascending=not args.desc
    )

    excel_file = f"output/{args.output_name}.xlsx"
    csv_file = f"output/{args.output_name}.csv"

    export_to_excel(sorted_properties, excel_file)
    export_to_csv(sorted_properties, csv_file)

    print(f"Archivo Excel generado: {excel_file}")
    print(f"Archivo CSV generado: {csv_file}")
    print(f"Elementos totales extraídos: {total_before_dedup}")
    print(f"Duplicados eliminados: {total_duplicates_removed}")
    print(f"Elementos únicos: {len(unique_properties)}")
    print(f"Elementos tras filtrar: {len(filtered_properties)}")
    print(
        "Orden aplicado: "
        + ("precio descendente" if args.desc else "precio ascendente")
    )

    if args.max_price is not None:
        print(f"Filtro precio máximo: {args.max_price}")

    print(f"Nombre base de salida: {args.output_name}")


if __name__ == "__main__":
    main()