import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import clear_stats as cs
import pandas as pd
import pdf_create as pc
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
img_root = project_root / "resource" / "img"
pdf_root = project_root / "resource" / "pdf"
img_root.mkdir(parents=True, exist_ok=True)

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Run stats with caching to avoid re-running on every reload
@st.cache_data
def get_stats():
    return cs.stats()

report = get_stats()
# Define a consistent color map for all news media
color_map = {
    'TN': '#6A0DAD',      # Dark Violet
    'C5N': '#9370DB',     # Medium Violet
    'LN': '#B8A4E3',      # Light Violet
    'Clarin': '#8F7FBF'   # Slate Blue (similar to violet)
}

# -----------------
# General Overview (Full width)
# -----------------
st.title("What do the most viewed Argentine news portals talk about?")
st.write(
    """
    The objective of this app is to show how much news portals (most viewed in Argentina) 
    talk about central Argentine topics such as the economy, politics, and insecurity.
    """
)
oldest, newest = report["date_range"]
st.write(f"The data collected is from **{oldest}** to **{newest}**")

# General survey (centered using columns)
st.markdown("---")
st.subheader("General survey")
col_spacer1, col_metrics, col_spacer2 = st.columns([1, 2, 1])

with col_metrics:
    col1, col2, col3, col4 = st.columns(4)
    totals = report["totals"]

    with col1:
        st.metric(label="Total Titles", value=f"{totals['total_titles']}")
    with col2:
        st.metric(label="Politics Titles", value=f"{totals['politics_titles']}")
    with col3:
        st.metric(label="Tragedy Titles", value=f"{totals['tragedy_titles']}")
    with col4:
        st.metric(label="Economy Titles", value=f"{totals['economy_titles']}")

# ---
# Two-column layout for main charts (adjusted for smaller graphs)
# ---
st.markdown("---")
st.subheader("Titles per Media")

col_chart1, col_chart2 = st.columns([0.6, 0.4])

# Bar chart: Titles per media
with col_chart1:
    titles_per_media = report["titles_per_media"]
    medias = [m for m, _ in titles_per_media]
    counts = [c for _, c in titles_per_media]

    fig_bar = px.bar(
        x=medias,
        y=counts,
        title="Number of Titles per Media",
        labels={"x": "News Media", "y": "Titles"},
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_bar.write_image(str(img_root/"titles_per_media.png"))  # Save the figure as an image
    st.plotly_chart(fig_bar, use_container_width=True)

# Pie chart: Category distribution
with col_chart2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Category Distribution")
    
    # 1. Calculate titles not belonging to any of the three categories
    total_titles = totals['total_titles']
    classified_titles = totals['politics_titles'] + totals['tragedy_titles'] + totals['economy_titles']
    other_titles = total_titles - classified_titles

    # 2. Create labels and values lists with the new category
    labels = ["Politics", "Tragedy", "Economy", "Others"]
    values = [
        totals["politics_titles"],
        totals["tragedy_titles"],
        totals["economy_titles"],
        other_titles
    ]

    #Color palette for the pie chart
    pie_colors = ['#6A0DAD', '#9B59B6', '#D7BDE2', "#746CF0"]
    
    # 3. Generate the pie chart with the new data
    fig_pie = px.pie(
        names=labels, 
        values=values, 
        title="Distribution of Titles by Category", 
        hole=0.3,
        color_discrete_sequence= pie_colors
    )
    fig_pie.write_image(str(img_root/"category_distribution.png"))  # Save the figure as an image
    st.plotly_chart(fig_pie, use_container_width=True)

# --------------------------
# Detailed Analysis per Category
# --------------------------

# Convert titles_per_media to a dictionary for easier lookup
total_titles_per_media_dict = dict(report["titles_per_media"])

# Politics Section
st.markdown("---")
col_pol_title, _ = st.columns([1, 10])
with col_pol_title:
    st.subheader("Politics")

# Create two columns for the charts
col_pol_chart1, col_pol_chart2 = st.columns(2)

category_counts = report["category_counts_per_media"]
medias = list(category_counts.keys())

# Calculate percentages
politics_percentages = {}
for media in medias:
    total_titles = total_titles_per_media_dict.get(media, 0)
    if total_titles > 0:
        percentage = (category_counts[media]["politics"] / total_titles) * 100
        politics_percentages[media] = percentage
    else:
        politics_percentages[media] = 0
        
politics_counts = [category_counts[m]["politics"] for m in medias]

# Find the media with the highest percentage
dominant_media_pol = "N/A"
if politics_percentages:
    dominant_media_pol = max(politics_percentages, key=politics_percentages.get)

# Display charts in their respective columns
with col_pol_chart1:
    fig_pol_count = px.bar(
        x=medias,
        y=politics_counts,
        title="Politics Titles per Media (Count)",
        labels={"x": "News Media", "y": "Politics Titles"},
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_pol_count.write_image(str(img_root/"politics_percentage_count.png"))  # Save the figure as an image
    st.plotly_chart(fig_pol_count, use_container_width=True)

with col_pol_chart2:
    fig_pol_percent = px.bar(
        x=medias,
        y=[politics_percentages[m] for m in medias],
        title="Politics Titles per Media (Percentage)",
        labels={"x": "News Media", "y": "Percentage (%)"},
        text_auto=".1f",
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_pol_percent.write_image(str(img_root/"politics_percentage.png"))  # Save the figure as an image
    st.plotly_chart(fig_pol_percent, use_container_width=True)

# Display text below the charts
st.write(
    f"""
    In these charts, you can visualize how much each news outlet talks about politics and evaluate the importance they give to the topic. Based on this data, we can see that the news outlet that talks the most about this topic is **{dominant_media_pol}**.
    """
)

# New Graphs for Milei vs Kicillof and La Libertad Avanza vs Fuerza Patria
st.markdown("---")
st.subheader("Political Figures and Parties")

# Prepare data for new charts
keyword_counts = report["specific_keywords_counts"]
df_milei_kicillof = pd.DataFrame({
    'News Media': medias,
    'Milei': [
        keyword_counts.get('JAVIER MILEI', {}).get(m, 0) +
        keyword_counts.get('MILEI', {}).get(m, 0)
        for m in medias
    ],
    'Kicillof': [
        keyword_counts.get('AXEL KICILLOF', {}).get(m, 0) +
        keyword_counts.get('KICILLOF', {}).get(m, 0)
        for m in medias
    ]
})


df_lla_fp = pd.DataFrame({
    'News Media': medias,
    'La Libertad Avanza': [
        keyword_counts.get('LA LIBERTAD AVANZA', {}).get(m, 0) for m in medias
    ],
    'Fuerza Patria': [
        keyword_counts.get('FUERZA PATRIA', {}).get(m, 0) +
        keyword_counts.get('PERONISMO', {}).get(m, 0) +
        keyword_counts.get('KIRCHNERISMO', {}).get(m, 0) +
        keyword_counts.get('KIRCHNERISTAS', {}).get(m, 0) +
        keyword_counts.get('KIRCHNERISTA', {}).get(m, 0) +
        keyword_counts.get("PERONISTA", {}).get(m, 0) +
        keyword_counts.get("PERONISTAS", {}).get(m, 0)
        for m in medias
    ]
})

# Calculate percentages for the charts
df_milei_kicillof['Total'] = df_milei_kicillof['Milei'] + df_milei_kicillof['Kicillof']
df_milei_kicillof['Milei (%)'] = (df_milei_kicillof['Milei'] / df_milei_kicillof['Total']) * 100
df_milei_kicillof['Kicillof (%)'] = (df_milei_kicillof['Kicillof'] / df_milei_kicillof['Total']) * 100

df_lla_fp['Total'] = df_lla_fp['La Libertad Avanza'] + df_lla_fp['Fuerza Patria']
df_lla_fp['La Libertad Avanza (%)'] = (df_lla_fp['La Libertad Avanza'] / df_lla_fp['Total']) * 100
df_lla_fp['Fuerza Patria (%)'] = (df_lla_fp['Fuerza Patria'] / df_lla_fp['Total']) * 100

# Create two columns for the new charts
col_pol_keywords1, col_pol_keywords2 = st.columns(2)

with col_pol_keywords1:
    fig_milei_kicillof = go.Figure(data=[
        go.Bar(name='Milei', x=df_milei_kicillof['News Media'], y=df_milei_kicillof['Milei (%)'], text=df_milei_kicillof['Milei (%)'].round(1), textposition='auto', marker_color='#6A0DAD'),
        go.Bar(name='Kicillof', x=df_milei_kicillof['News Media'], y=df_milei_kicillof['Kicillof (%)'], text=df_milei_kicillof['Kicillof (%)'].round(1), textposition='auto', marker_color='#FFD700')
    ])
    fig_milei_kicillof.update_layout(barmode='group', title="Milei vs Kicillof by Media (Percentage)")
    fig_milei_kicillof.write_image(str(img_root/"milei_kicillof_percentage.png"))  # Save the figure as an image
    st.plotly_chart(fig_milei_kicillof, use_container_width=True)
    
with col_pol_keywords2:
    fig_lla_fp = go.Figure(data=[
        go.Bar(name='La Libertad Avanza', x=df_lla_fp['News Media'], y=df_lla_fp['La Libertad Avanza (%)'], text=df_lla_fp['La Libertad Avanza (%)'].round(1), textposition='auto', marker_color='#6A0DAD'),
        go.Bar(name='Fuerza Patria', x=df_lla_fp['News Media'], y=df_lla_fp['Fuerza Patria (%)'], text=df_lla_fp['Fuerza Patria (%)'].round(1), textposition='auto', marker_color='#FFD700')
    ])
    fig_lla_fp.update_layout(barmode='group', title="La Libertad Avanza vs Fuerza Patria by Media (Percentage)")
    fig_lla_fp.write_image(str(img_root/"lla_fp_percentage.png"))  # Save the figure as an image
    st.plotly_chart(fig_lla_fp, use_container_width=True)


# Economy Section
st.markdown("---")
col_eco_title, _ = st.columns([1, 10])
with col_eco_title:
    st.subheader("Economy")

# Create two columns for the charts
col_eco_chart1, col_eco_chart2 = st.columns(2)

# Calculate percentages
economy_percentages = {}
for media in medias:
    total_titles = total_titles_per_media_dict.get(media, 0)
    if total_titles > 0:
        percentage = (category_counts[media]["economy"] / total_titles) * 100
        economy_percentages[media] = percentage
    else:
        economy_percentages[media] = 0

economy_counts = [category_counts[m]["economy"] for m in medias]

# Find the media with the highest percentage
dominant_media_eco = "N/A"
if economy_percentages:
    dominant_media_eco = max(economy_percentages, key=economy_percentages.get)

# Display charts in their respective columns
with col_eco_chart1:
    fig_eco_count = px.bar(
        x=medias,
        y=economy_counts,
        title="Economy Titles per Media (Count)",
        labels={"x": "News Media", "y": "Economy Titles"},
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_eco_count.write_image(str(img_root/"economy_percentage_count.png"))  # Save the figure as an image
    st.plotly_chart(fig_eco_count, use_container_width=True)

with col_eco_chart2:
    fig_eco_percent = px.bar(
        x=medias,
        y=[economy_percentages[m] for m in medias],
        title="Economy Titles per Media (Percentage)",
        labels={"x": "News Media", "y": "Percentage (%)"},
        text_auto=".1f",
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_eco_percent.write_image(str(img_root/"economy_percentage.png")) # Save the figure as an image
    st.plotly_chart(fig_eco_percent, use_container_width=True)

# Display text below the charts
st.write(
    f"""
    In these charts, you can visualize how much each news outlet talks about the economy and evaluate the importance they give to the topic. Based on this data, we can see that the news outlet that talks the most about this topic is **{dominant_media_eco}**.
    """
)

# Tragedy Section
st.markdown("---")
col_tra_title, _ = st.columns([1, 10])
with col_tra_title:
    st.subheader("Tragedy")

# Create two columns for the charts
col_tra_chart1, col_tra_chart2 = st.columns(2)

# Calculate percentages
tragedy_percentages = {}
for media in medias:
    total_titles = total_titles_per_media_dict.get(media, 0)
    if total_titles > 0:
        percentage = (category_counts[media]["tragedy"] / total_titles) * 100
        tragedy_percentages[media] = percentage
    else:
        tragedy_percentages[media] = 0

tragedy_counts = [category_counts[m]["tragedy"] for m in medias]

# Find the media with the highest percentage
dominant_media_tra = "N/A"
if tragedy_percentages:
    dominant_media_tra = max(tragedy_percentages, key=tragedy_percentages.get)

# Display charts in their respective columns
with col_tra_chart1:
    fig_tra_count = px.bar(
        x=medias,
        y=tragedy_counts,
        title="Tragedy Titles per Media (Count)",
        labels={"x": "News Media", "y": "Tragedy Titles"},
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_tra_count.write_image(str(img_root/"tragedy_percentage_count.png"))  # Save the figure as an image
    st.plotly_chart(fig_tra_count, use_container_width=True)

with col_tra_chart2:
    fig_tra_percent = px.bar(
        x=medias,
        y=[tragedy_percentages[m] for m in medias],
        title="Tragedy Titles per Media (Percentage)",
        labels={"x": "News Media", "y": "Percentage (%)"},
        text_auto=".1f",
        color=medias, # Use 'medias' as the color variable
        color_discrete_map=color_map # Apply the custom color map
    )
    fig_tra_percent.write_image(str(img_root/"tragedy_percentage.png"))  # Save the figure as an image
    st.plotly_chart(fig_tra_percent, use_container_width=True)

# Display text below the charts
st.write(
    f"""
    In these charts, you can visualize how much each news outlet talks about tragedy and evaluate the importance they give to the topic. Based on this data, we can see that the news outlet that talks the most about this topic is **{dominant_media_tra}**.
    """
)

# PDF Generation Section
pc.create_report_pdf_en(report)
pc.create_report_pdf_es(report)
st.markdown("---")
file_path1 = str(pdf_root/"Scraping-Report-en.pdf")
file_path2 = str(pdf_root/"Scraping-Report-es.pdf")

with open(file_path1, "rb") as f:
    file_bytes1 = f.read()

with open(file_path2, "rb") as f:
    file_bytes2 = f.read()

st.write("By clicking on the button you can download a PDF with the analysis carried out on this page")

st.download_button(
    label="Download PDF Report (English)",
    data=file_bytes1,
    file_name="Scraping-Report-en.pdf",
    mime="application/pdf"
)
st.download_button(
    label="Download PDF Report (Spanish)",
    data=file_bytes2,
    file_name="Scraping-Report-es.pdf",
    mime="application/pdf"
)