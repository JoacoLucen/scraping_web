import sqlite3

# Define los grupos de palabras clave aquí
keyword_groups = {
    "MILEI": ["MILEI", "JAVIER MILEI"],
    "KICILLOF": ["KICILLOF", "AXEL KICILLOF"],
    "LA LIBERTAD AVANZA": ["LA LIBERTAD AVANZA"],
    "FUERZA PATRIA": ["FUERZA PATRIA", "PERONISMO", "LA CAMPORA"]
}

# Word lists
words_tragedy = [
    "muere", "mueren", "murieron", "fallece", "fallecieron",
    "asesinato", "asesinados", "asesinan",
    "suicidio", "se suicidó", "suicidios",
    "siniestro", "tragedia", "catástrofe", "accidente",
    "herido", "heridos", "lesionado",
    "homicidio", "violencia", "crimen",
    "desaparecido", "desaparecidos",
    "salud", "pandemia", "infectados", "epidemia",
    "dolor", "conmoción", "tristeza", "luto",
    "masacre", "tiroteo", "derrumbe", "inundación", "incendio",
    "colapso", "atentado", "explosión", "choque", "devastación",
    "alerta", "emergencia", "rescate", "víctima", "pánico",
    "secuestro", "amenaza", "desastre", "luto", "shock"
]

words_politics = [
    "gobierno", "ministro", "presidente", "elecciones",
    "política", "oposición", "alianza", "campaña",
    "poder", "ley", "debate", "escándalo", "corrupción",
    "partido", "voto", "resultado", "polémica",
    "reforma", "acusación", "crítica", "promesa",
    "estado", "movimiento", "oficialista", "opositor",
    "parlamento", "congreso", "senado", "diputados", "asamblea",
    "referéndum", "dictamen", "mandato", "candidato", "coalición",
    "funcionario", "autoridad", "intendente", "gobernador", "embajador",
    "juramento", "anuncio", "resolución", "tratado", "discurso"
]

words_economy = [
    "inflación", "precios", "dólar", "deuda", "ajuste",
    "impuestos", "crisis", "recesión", "bonos", "tasas",
    "mercados", "pobreza", "ingreso", "salario", "subsidios",
    "producción", "exportaciones", "industrial", "consumo",
    "tarifas", "déficit", "fiscal", "finanzas", "inversión",
    "banco central", "devaluación", "ahorro", "empleo", "desempleo",
    "presupuesto", "créditos", "hipoteca", "billetera", "acciones",
    "bolsa", "ganancias", "pérdidas", "aranceles", "competitividad",
    "desarrollo", "crecimiento", "PIB", "riesgo país", "suba"
]

def clean_duplicate_titles():
    # Connect to the database
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()

    # Delete duplicates, keeping the first occurrence
    cursor.execute("""
        DELETE FROM titles
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM titles
            GROUP BY title
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Clear Data Base: Duplicates removed.")


def get_date_range():
    """Return the oldest and newest dates in the database formatted as day/month/year."""
    with sqlite3.connect("noticias.db") as conn:
        cursor = conn.cursor()
        # Use STRFTIME to format the dates directly in the SQL query
        cursor.execute("SELECT STRFTIME('%d/%m/%Y', MIN(date)), STRFTIME('%d/%m/%Y', MAX(date)) FROM titles")
        result = cursor.fetchone()
    return result

def stats():
    """Generate a report with various statistics from the database."""
    # 1. Clean duplicates
    clean_duplicate_titles()

    # 2. Database connection
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()

    # 3. Fetch all titles and media at once
    cursor.execute("SELECT news_media, title FROM titles")
    rows = cursor.fetchall()
    conn.close()

    # 4. Initialize data structures
    category_counts = {}
    
    # Initialize keyword_counts usando los grupos
    keyword_counts = {group: {} for group in keyword_groups}
    total_titles_per_media = {}
    
    total_politics, total_tragedy, total_economy = 0, 0, 0
    
    # Process data in a single loop
    for media, title in rows:
        title_upper = title.upper() # Standardize for comparison

        # Initialize dictionaries for the media if they don't exist
        if media not in category_counts:
            category_counts[media] = {"politics": 0, "tragedy": 0, "economy": 0}
            total_titles_per_media[media] = 0

        total_titles_per_media[media] += 1

        # Count by category (a title can belong to multiple categories)
        is_politics = any(word.upper() in title_upper for word in words_politics)
        is_tragedy = any(word.upper() in title_upper for word in words_tragedy)
        is_economy = any(word.upper() in title_upper for word in words_economy)

        if is_politics:
            category_counts[media]["politics"] += 1
            total_politics += 1
        if is_tragedy:
            category_counts[media]["tragedy"] += 1
            total_tragedy += 1
        if is_economy:
            category_counts[media]["economy"] += 1
            total_economy += 1

        # Count specific keywords using the groups
        for group, variants in keyword_groups.items():
            if media not in keyword_counts[group]:
                keyword_counts[group][media] = 0
            if any(variant in title_upper for variant in variants):
                keyword_counts[group][media] += 1

    # 5. Get other data
    date_range = get_date_range()
    
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM titles")
    total_titles = cursor.fetchone()[0]
    conn.close()

    # Return the report
    return {
        "date_range": date_range,
        "titles_per_media": list(total_titles_per_media.items()),
        "category_counts_per_media": category_counts,
        "specific_keywords_counts": keyword_counts,
        "totals": {
            "total_titles": total_titles,
            "politics_titles": total_politics,
            "tragedy_titles": total_tragedy,
            "economy_titles": total_economy
        }
    }