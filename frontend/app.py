import streamlit as st

st.set_page_config(page_title="Production ENR", page_icon="⚡", layout="wide")

st.title("Production d'Énergie Renouvelable")
st.markdown("""
Bienvenue dans le tableau de bord **ENR**.
Utilisez le menu latéral pour visualiser ou prédire la production :
- **Hydro**
- **Solaire**
- **Éolien**
""")

st.markdown(
    "[Documentation API](https://gaetancsimplon.github.io/production_enr/)",
    unsafe_allow_html=True
)
