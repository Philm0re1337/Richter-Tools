import streamlit as st
import streamlit.components.v1 as components
import os

# Konfiguration der Seite für maximale Breite
st.set_page_config(
    page_title="Richter Management Tools",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Erweitertes CSS, um Streamlit-Standardabstände (Padding) zu entfernen
st.markdown("""
    <style>
        /* Entfernt Padding vom Haupt-Container */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }
        [data-testid="stSidebar"] .stMarkdown h2 {
            color: #dc2626;
            font-weight: bold;
        }
        /* Hintergrund der Hauptseite */
        .main {
            background-color: #121212;
        }
        /* Versteckt das Streamlit-Header-Menü für einen saubereren Look */
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def load_html(file_name):
    """Lädt die HTML Datei sicher ein."""
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def main():
    # Seitenleiste
    st.sidebar.title("RICHTER TOOLS")
    st.sidebar.markdown("---")
    
    # Navigation
    selection = st.sidebar.radio(
        "Navigation",
        ["Personalkosten", "KER Analyse"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("v1.2.0 (Full-Width Edition)")

    # Content Bereich
    if selection == "Personalkosten":
        html_content = load_html("Personalkosten Richter.html")
        if html_content:
            # Wir betten das HTML in einen Container ein, der die Breite erzwingt
            components.html(
                f"<div style='margin:-8px; padding:0;'>{html_content}</div>", 
                height=1000, 
                scrolling=True
            )
        else:
            st.error("Datei 'Personalkosten Richter.html' nicht im Repository gefunden.")

    elif selection == "KER Analyse":
        html_content = load_html("KER Analyse Tool.html")
        if html_content:
            components.html(
                f"<div style='margin:-8px; padding:0;'>{html_content}</div>", 
                height=1000, 
                scrolling=True
            )
        else:
            st.error("Datei 'KER Analyse Tool.html' nicht im Repository gefunden.")

if __name__ == "__main__":
    main()
