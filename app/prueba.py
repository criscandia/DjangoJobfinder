import feedparser
from bs4 import BeautifulSoup
import re
from dateutil import parser as date_parser
from datetime import datetime


def parse_rss(rss_feed_url):
    parsed_entries = []

    parser_feed = feedparser.parse(rss_feed_url)

    for entry in parser_feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        description = entry.get("description", "")
        pub_date = (
            date_parser.parse(entry.get("published", ""))
            if entry.get("published")
            else None
        )

        # Limpiar la descripción HTML usando BeautifulSoup
        soup = BeautifulSoup(description, "html.parser")

        # Eliminar las etiquetas específicas como <img>, <a>, <script>, <style>, etc.
        for tag in soup(
            ["img", "a", "script", "style", "br", "li", "ul", "strong", "div", "p"]
        ):
            tag.decompose()

        # Obtener solo el texto limpio eliminando etiquetas restantes y espacios innecesarios
        description_text = soup.get_text(separator=" ").strip()
        description_text = re.sub(r"\s+", " ", description_text)

        # Depuración: imprimir el texto limpio
        print(f"Descripción limpia para el título '{title}':\n{description_text}\n")

        # Simular la creación de un objeto Job (en un entorno real, este sería un modelo Django)
        job = {
            "title": title,
            "company": "Example Company",
            "location": "",
            "description": description_text,
            "pub_date": pub_date,
            "link": link,
        }

        parsed_entries.append(job)

    return parsed_entries


# URL del feed RSS de prueba
rss_feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

# Llamar a la función de prueba
parsed_entries = parse_rss(rss_feed_url)
