import os
import csv
from django.db import transaction
from articles.models import Article

def run(*args):
    """
    Uso:
      python manage.py runscript populate_articles --script-args "articles/data/articles.csv" "clear"

    CSV headers aceptados:
      - title,content  (ideal)
      - name,content   (también jala: lo convierte a title)
    """

    if not args:
        print('ERROR: Pasa la ruta del CSV. Ej: python manage.py runscript populate_articles --script-args "articles/data/articles.csv"')
        return

    csv_path = args[0]
    do_clear = len(args) > 1 and args[1].lower() == "clear"

    if not os.path.exists(csv_path):
        print(f"ERROR: No existe el archivo: {csv_path}")
        return

    if do_clear:
        deleted, _ = Article.objects.all().delete()
        print(f"OK: Borrados {deleted} registros previos.")

    rows = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("ERROR: CSV sin headers.")
            return

        headers = [h.strip().lower() for h in reader.fieldnames]

        # Title puede venir como 'title' o 'name'
        if "title" in headers:
            title_key = reader.fieldnames[headers.index("title")]
        elif "name" in headers:
            title_key = reader.fieldnames[headers.index("name")]
        else:
            print("ERROR: El CSV debe tener columna 'title' (o 'name').")
            print(f"Headers detectados: {reader.fieldnames}")
            return

        if "content" in headers:
            content_key = reader.fieldnames[headers.index("content")]
        elif "body" in headers:
            content_key = reader.fieldnames[headers.index("body")]
        else:
            print("ERROR: El CSV debe tener columna 'content' (o 'body').")
            print(f"Headers detectados: {reader.fieldnames}")
            return

        for row in reader:
            title = (row.get(title_key) or "").strip()
            content = (row.get(content_key) or "").strip()

            if not title and not content:
                continue

            rows.append(Article(title=title[:200], content=content))

    if not rows:
        print("AVISO: CSV vacío o sin filas válidas.")
        return

    with transaction.atomic():
        Article.objects.bulk_create(rows, batch_size=500)

    print(f"OK: Insertados {len(rows)} artículos.")