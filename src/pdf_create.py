from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
img_root = project_root / "resource" / "img"
pdf_root = project_root / "resource" / "pdf"

pdf_root.mkdir(parents=True, exist_ok=True)

def create_report_pdf_en(report_data):
    doc = SimpleDocTemplate(str(pdf_root/"Scraping-Report-en.pdf"), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Main document title
    story.append(Paragraph("News Analysis - Statistical Report", styles['Title']))
    story.append(Spacer(1, 0.2*inch))

    # Text with variables
    total_titles = report_data['totals']['total_titles']
    date_range = report_data['date_range']
    general_text = (
        f"This report presents an analysis of the headlines from Argentina's main news media. "
        f"Scraping was performed on different days and at different times to be as random as possible."
    )
    general_text2 = (
        f"The period covered is from {date_range[0]} to {date_range[1]} and a total of {total_titles} headlines were collected."
    )
    story.append(Paragraph(general_text, styles['Normal']))
    story.append(Paragraph(general_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    # Bar chart: Titles per media outlet
    titles_text = (
        "The following chart shows the number of headlines scraped for each media outlet. "
        "This is to get an idea of the amount of data available for each outlet for politics, economy, and tragedy."
    )
    story.append(Paragraph("A little context before we begin...", styles['Heading2']))
    story.append(Paragraph(titles_text, styles['Normal']))
    story.append(Image((str(img_root/"titles_per_media.png")), width=450, height=300))
    story.append(Spacer(0.5, 0.2*inch))

    # Politics section
    story.append(Paragraph("Political Analysis", styles['Heading2']))
    total_politics = report_data['totals']['politics_titles']
    category_counts_politics = report_data['category_counts_per_media']
    max_politics_titles = -1
    dominant_media_pol_politics = "N/A"
    for media, counts in category_counts_politics.items():
        if counts['politics'] > max_politics_titles:
            max_politics_titles = counts['politics']
            dominant_media_pol_politics = media
    # Initialize variables to find the highest percentage
    max_politics_percentage = -1.0
    dominant_media_pol_perc = "N/A"

    # Convert titles_per_media to a dictionary for easier access
    titles_per_media_dict = dict(report_data['titles_per_media'])

    # Iterate over media outlets and their category counts
    for media, counts in report_data['category_counts_per_media'].items():
        total_titles_for_media = titles_per_media_dict.get(media, 0)

        # Avoid division by zero
        if total_titles_for_media > 0:
            politics_titles = counts['politics']
            # Calculate the percentage of politics headlines for this outlet
            politics_percentage = (politics_titles / total_titles_for_media) * 100

            # Compare and update if it is the highest percentage
            if politics_percentage > max_politics_percentage:
                max_politics_percentage = politics_percentage
                dominant_media_pol_perc = media
    
    # This text is an example; you should adapt it to match your data
    politics_text = (
        f"In the Politics category, approximately {total_politics} headlines were found. "
        f"The following charts show the gross number of headlines each media outlet dedicates to politics, and also "
        f"the percentage that politics represents for each outlet relative to its total number of headlines."
    )
    politics_text2 = (
        f"The media outlet that published the most politics headlines is {dominant_media_pol_politics} with a total of {max_politics_titles} headlines. "
        f"However, if we analyze the percentage that politics represents for each outlet, the one with the biggest focus on politics is {dominant_media_pol_perc} "
        f"with {max_politics_percentage:.2f}% of its headlines dedicated to this category."
    )
    story.append(Paragraph(politics_text, styles['Normal']))
    story.append(Image(str(img_root/"politics_percentage_count.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"politics_percentage.png"), width=400, height=250))
    story.append(Paragraph(politics_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    # Political parties and figures
    lla_vs_fp_text = (
        "The following chart shows the number of headlines that mention the two main "
        "political figures currently in the media, as well as their respective opposing parties.\n"
        "On one side, La Libertad Avanza with Javier Milei, and on the other, Fuerza Patria with Axel Kicillof."
    )
    note = (
        "Note: Many media outlets tend to refer to the Fuerza Patria sector as Peronismo, Kirchnerismo, or simply La Campora, so it was decided to group them all into the same category."
    )
    story.append(Paragraph("La Libertad Avanza vs. Fuerza Patria", styles['Heading2']))
    story.append(Paragraph(lla_vs_fp_text, styles['Normal']))
    story.append(Paragraph(note, styles['Normal']))
    story.append(Image(str(img_root/"lla_fp_percentage.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"milei_kicillof_percentage.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))

    # Economy section
    story.append(Paragraph("Economic Analysis", styles['Heading2']))
    total_economy = report_data['totals']['economy_titles']
    category_counts_economy = report_data['category_counts_per_media']
    max_economy_titles = -1
    dominant_media_pol_economy = "N/A"
    for media, counts in category_counts_economy.items():
        if counts['economy'] > max_economy_titles:
            max_economy_titles = counts['economy']
            dominant_media_pol_economy = media
    # Initialize variables to find the highest percentage
    max_economy_percentage = -1.0
    dominant_media_eco_perc = "N/A"
    # Iterate over media outlets and their category counts
    for media, counts in report_data['category_counts_per_media'].items():
        total_titles_for_media = titles_per_media_dict.get(media, 0)

        # Avoid division by zero
        if total_titles_for_media > 0:
            economy_titles = counts['economy']
            # Calculate the percentage of economy headlines for this outlet
            economy_percentage = (economy_titles / total_titles_for_media) * 100

            # Compare and update if it is the highest percentage
            if economy_percentage > max_economy_percentage:
                max_economy_percentage = economy_percentage
                dominant_media_eco_perc = media
    economy_text = (
        f"In the Economy category, approximately {total_economy} headlines were found. "
        f"The following charts show the gross number of headlines each media outlet dedicates to the economy, and also "
        f"the percentage that the economy represents for each outlet relative to its total number of headlines."
    )
    economy_text2 = (
        f"The media outlet that published the most economy headlines is {dominant_media_pol_economy} with a total of {max_economy_titles} headlines. "
        f"However, if we analyze the percentage that the economy represents for each outlet, the one with the biggest focus on the economy is {dominant_media_eco_perc} "
        f"with {max_economy_percentage:.2f}% of its headlines dedicated to this category."
    )
    story.append(Paragraph(economy_text, styles['Normal']))
    story.append(Image(str(img_root/"economy_percentage_count.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"economy_percentage.png"), width=400, height=250))
    story.append(Paragraph(economy_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    # Tragedy section
    story.append(Paragraph("Tragedy Analysis", styles['Heading2']))
    total_tragedy = report_data['totals']['tragedy_titles']
    category_counts_tragedy = report_data['category_counts_per_media']
    max_tragedy_titles = -1
    dominant_media_pol_tragedy = "N/A"
    for media, counts in category_counts_tragedy.items():
        if counts['tragedy'] > max_tragedy_titles:
            max_tragedy_titles = counts['tragedy']
            dominant_media_pol_tragedy = media
    # Initialize variables to find the highest percentage
    max_tragedy_percentage = -1.0
    dominant_media_tra_perc = "N/A"
    # Iterate over media outlets and their category counts
    for media, counts in report_data['category_counts_per_media'].items():
        total_titles_for_media = titles_per_media_dict.get(media, 0)

        # Avoid division by zero
        if total_titles_for_media > 0:
            tragedy_titles = counts['tragedy']
            # Calculate the percentage of tragedy headlines for this outlet
            tragedy_percentage = (tragedy_titles / total_titles_for_media) * 100

            # Compare and update if it is the highest percentage
            if tragedy_percentage > max_tragedy_percentage:
                max_tragedy_percentage = tragedy_percentage
                dominant_media_tra_perc = media
    tragedy_text = (
        f"In the Tragedy category, approximately {total_tragedy} headlines were found. "
        f"The following charts show the gross number of headlines each media outlet dedicates to tragedies, and also "
        f"the percentage that tragedies represent for each outlet relative to its total number of headlines."
    )
    tragedy_text2 = (
        f"The media outlet that published the most tragedy headlines is {dominant_media_pol_tragedy} with a total of {max_tragedy_titles} headlines. "
        f"However, if we analyze the percentage that tragedies represent for each outlet, the one with the biggest focus on tragedies is {dominant_media_tra_perc} "
        f"with {max_tragedy_percentage:.2f}% of its headlines dedicated to this category."
    )
    story.append(Paragraph(tragedy_text, styles['Normal']))
    story.append(Image(str(img_root/"tragedy_percentage_count.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"tragedy_percentage.png"), width=400, height=250))
    story.append(Paragraph(tragedy_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))
 
    doc.build(story)

def create_report_pdf_es(report_data):
    doc = SimpleDocTemplate(str(pdf_root/"Scraping-Report-es.pdf"), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Título principal del documento
    story.append(Paragraph("Análisis de Noticias - Informe Estadístico", styles['Title']))
    story.append(Spacer(1, 0.2*inch))

    # Texto con variables
    total_titles = report_data['totals']['total_titles']
    date_range = report_data['date_range']
    general_text = (
        f"Este informe presenta un análisis de los titulares de los principales medios de noticias de Argentina. "
        f"Se realizó un 'scraping' en diferentes días y horarios para ser lo más aleatorio posible."
    )
    general_text2 = (
        f"El período cubierto es desde {date_range[0]} hasta {date_range[1]} y se recolectó un total de {total_titles} titulares."
    )
    story.append(Paragraph(general_text, styles['Normal']))
    story.append(Paragraph(general_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    # Gráfico de barras: Títulos por medio de noticias
    titles_text = (
        "El siguiente gráfico muestra el número de titulares extraídos para cada medio de noticias. "
        "Esto es para tener una idea de la cantidad de datos disponibles para cada medio sobre política, economía y tragedia."
    )
    story.append(Paragraph("Un poco de contexto antes de empezar...", styles['Heading2']))
    story.append(Paragraph(titles_text, styles['Normal']))
    story.append(Image((str(img_root/"titles_per_media.png")), width=450, height=300))
    story.append(Spacer(0.5, 0.2*inch))

    # Sección de Política
    story.append(Paragraph("Análisis Político", styles['Heading2']))
    total_politics = report_data['totals']['politics_titles']
    category_counts_politics = report_data['category_counts_per_media']
    max_politics_titles = -1
    dominant_media_pol_politics = "N/A"
    for media, counts in category_counts_politics.items():
        if counts['politics'] > max_politics_titles:
            max_politics_titles = counts['politics']
            dominant_media_pol_politics = media
    # Inicializar variables para encontrar el porcentaje más alto
    max_politics_percentage = -1.0
    dominant_media_pol_perc = "N/A"

    # Convertir titles_per_media a un diccionario para facilitar el acceso
    titles_per_media_dict = dict(report_data['titles_per_media'])

    # Iterar sobre los medios y sus recuentos por categoría
    for media, counts in report_data['category_counts_per_media'].items():
        total_titles_for_media = titles_per_media_dict.get(media, 0)

        # Evitar la división por cero
        if total_titles_for_media > 0:
            politics_titles = counts['politics']
            # Calcular el porcentaje de titulares de política para este medio
            politics_percentage = (politics_titles / total_titles_for_media) * 100

            # Comparar y actualizar si es el porcentaje más alto
            if politics_percentage > max_politics_percentage:
                max_politics_percentage = politics_percentage
                dominant_media_pol_perc = media

    politics_text = (
        f"En la categoría de Política, se encontraron aproximadamente {total_politics} titulares. "
        f"Los siguientes gráficos muestran el número bruto de titulares que cada medio dedica a la política, y también "
        f"el porcentaje que la política representa para cada medio en relación con su número total de titulares."
    )
    politics_text2 = (
        f"El medio que publicó más titulares de política es **{dominant_media_pol_politics}** con un total de **{max_politics_titles}** titulares. "
        f"Sin embargo, si analizamos el porcentaje que la política representa para cada medio, el que tiene el mayor enfoque en política es **{dominant_media_pol_perc}** "
        f"con un **{max_politics_percentage:.2f}%** de sus titulares dedicados a esta categoría."
    )
    story.append(Paragraph(politics_text, styles['Normal']))
    story.append(Image(str(img_root/"politics_percentage_count.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"politics_percentage.png"), width=400, height=250))
    story.append(Paragraph(politics_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    # Partidos y figuras políticas
    lla_vs_fp_text = (
        "El siguiente gráfico muestra el número de titulares que mencionan a las dos principales "
        "figuras políticas actualmente en los medios, así como a sus respectivos partidos opuestos.\n"
        "Por un lado, La Libertad Avanza con Javier Milei, y por el otro, Fuerza Patria con Axel Kicillof."
    )
    note = (
        "Nota: Muchos medios tienden a referirse al sector de Fuerza Patria como Peronismo, Kirchnerismo, o simplemente La Cámpora, por lo que se decidió agruparlos a todos en la misma categoría."
    )
    story.append(Paragraph("La Libertad Avanza vs. Fuerza Patria", styles['Heading2']))
    story.append(Paragraph(lla_vs_fp_text, styles['Normal']))
    story.append(Paragraph(note, styles['Normal']))
    story.append(Image(str(img_root/"lla_fp_percentage.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"milei_kicillof_percentage.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))

    # Sección de Economía
    story.append(Paragraph("Análisis Económico", styles['Heading2']))
    total_economy = report_data['totals']['economy_titles']
    category_counts_economy = report_data['category_counts_per_media']
    max_economy_titles = -1
    dominant_media_pol_economy = "N/A"
    for media, counts in category_counts_economy.items():
        if counts['economy'] > max_economy_titles:
            max_economy_titles = counts['economy']
            dominant_media_pol_economy = media
    # Inicializar variables para encontrar el porcentaje más alto
    max_economy_percentage = -1.0
    dominant_media_eco_perc = "N/A"
    # Iterar sobre los medios y sus recuentos por categoría
    for media, counts in report_data['category_counts_per_media'].items():
        total_titles_for_media = titles_per_media_dict.get(media, 0)

        # Evitar la división por cero
        if total_titles_for_media > 0:
            economy_titles = counts['economy']
            # Calcular el porcentaje de titulares de economía para este medio
            economy_percentage = (economy_titles / total_titles_for_media) * 100

            # Comparar y actualizar si es el porcentaje más alto
            if economy_percentage > max_economy_percentage:
                max_economy_percentage = economy_percentage
                dominant_media_eco_perc = media
    economy_text = (
        f"En la categoría de Economía, se encontraron aproximadamente **{total_economy}** titulares. "
        f"Los siguientes gráficos muestran el número bruto de titulares que cada medio dedica a la economía, y también "
        f"el porcentaje que la economía representa para cada medio en relación con su número total de titulares."
    )
    economy_text2 = (
        f"El medio que publicó más titulares de economía es **{dominant_media_pol_economy}** con un total de **{max_economy_titles}** titulares. "
        f"Sin embargo, si analizamos el porcentaje que la economía representa para cada medio, el que tiene el mayor enfoque en la economía es **{dominant_media_eco_perc}** "
        f"con un **{max_economy_percentage:.2f}%** de sus titulares dedicados a esta categoría."
    )
    story.append(Paragraph(economy_text, styles['Normal']))
    story.append(Image(str(img_root/"economy_percentage_count.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"economy_percentage.png"), width=400, height=250))
    story.append(Paragraph(economy_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    # Sección de Tragedia
    story.append(Paragraph("Análisis de Tragedia", styles['Heading2']))
    total_tragedy = report_data['totals']['tragedy_titles']
    category_counts_tragedy = report_data['category_counts_per_media']
    max_tragedy_titles = -1
    dominant_media_pol_tragedy = "N/A"
    for media, counts in category_counts_tragedy.items():
        if counts['tragedy'] > max_tragedy_titles:
            max_tragedy_titles = counts['tragedy']
            dominant_media_pol_tragedy = media
    # Inicializar variables para encontrar el porcentaje más alto
    max_tragedy_percentage = -1.0
    dominant_media_tra_perc = "N/A"
    # Iterar sobre los medios y sus recuentos por categoría
    for media, counts in report_data['category_counts_per_media'].items():
        total_titles_for_media = titles_per_media_dict.get(media, 0)

        # Evitar la división por cero
        if total_titles_for_media > 0:
            tragedy_titles = counts['tragedy']
            # Calcular el porcentaje de titulares de tragedia para este medio
            tragedy_percentage = (tragedy_titles / total_titles_for_media) * 100

            # Comparar y actualizar si es el porcentaje más alto
            if tragedy_percentage > max_tragedy_percentage:
                max_tragedy_percentage = tragedy_percentage
                dominant_media_tra_perc = media
    tragedy_text = (
        f"En la categoría de Tragedia, se encontraron aproximadamente **{total_tragedy}** titulares. "
        f"Los siguientes gráficos muestran el número bruto de titulares que cada medio dedica a las tragedias, y también "
        f"el porcentaje que las tragedias representan para cada medio en relación con su número total de titulares."
    )
    tragedy_text2 = (
        f"El medio que publicó más titulares de tragedia es **{dominant_media_pol_tragedy}** con un total de **{max_tragedy_titles}** titulares. "
        f"Sin embargo, si analizamos el porcentaje que las tragedias representan para cada medio, el que tiene el mayor enfoque en las tragedias es **{dominant_media_tra_perc}** "
        f"con un **{max_tragedy_percentage:.2f}%** de sus titulares dedicados a esta categoría."
    )
    story.append(Paragraph(tragedy_text, styles['Normal']))
    story.append(Image(str(img_root/"tragedy_percentage_count.png"), width=400, height=250))
    story.append(Spacer(0.5, 0.2*inch))
    story.append(Image(str(img_root/"tragedy_percentage.png"), width=400, height=250))
    story.append(Paragraph(tragedy_text2, styles['Normal']))
    story.append(Spacer(0.5, 0.2*inch))

    doc.build(story)