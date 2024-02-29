import streamlit as st
st.set_page_config(
    page_title="transports en commun et JO PARIS2024🏅",
    page_icon="🚆",
)

st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://upload.wikimedia.org/wikipedia/fr/thumb/6/68/Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg/675px-Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg.png" style="width:300px;height:auto;"></div>',
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center;'>Prédiction de la demande des transports en commun pendant les Jeux Olympiques PARIS2024 🏅</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    Ce Dashboard présente les prédictions de la demande des transports en commun sur le réseau ferré parisien à proximité des sites de compétition prévus pour les JO PARIS2024.

    **👈 Choisissez un type d'analyse du menu** pour découvrir les différentes fonctionnalités 🚀.

    ### Que contient ce dashboard ? 
    - 📈 Des prédictions par site sur une plage de dates.
    - 📅 Des prédictions par jour, par site et sur toutes les stations de métro à proximité.
    - 🌡️ Le taux de saturation du métro sur la période de juillet et août 2024.
    - 🥇 Les compétitions prévus par jour.

    ### Source des données ?
    Les données ont été collecctées à partir du portail OpenData de Ile-de-France-Mobilité https://data.iledefrance-mobilites.fr/

"""
    )

st.markdown("---")

### EXPANDER

st.markdown("""
    ### Une petite vidéo de présentation des JO Paris 2024 ci-dessous :
""")

with st.expander("⏯️ Les Jeux Olympiques et Paralympiques de Paris 2024"):
    st.video("https://www.youtube.com/watch?v=tfBX9dDEhy8")

st.markdown("---")
