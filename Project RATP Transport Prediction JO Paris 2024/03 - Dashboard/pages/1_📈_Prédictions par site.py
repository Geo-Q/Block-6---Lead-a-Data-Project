import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

### CONFIG
st.set_page_config(
    page_title="Prédictions par site",
    page_icon="📈",
    layout="wide"
  )

### TITLE AND LOGO


st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://upload.wikimedia.org/wikipedia/fr/thumb/6/68/Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg/675px-Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg.png" style="width:300px;height:auto;"></div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center;'>Prédiction de la fréquentation des transports en commun par site</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h5 style='text-align: center;'>Courbes de la fréquentation des transports en commun prévue en fonctionnement normal sans JO et en fonctionnement avec JO pour toutes les stations à proximité d'un site </h5>",
    unsafe_allow_html=True
)

### LOAD AND CACHE DATA

data_jo = pd.read_csv("99-Data_Clean/df_forecast_jo.csv")
data_jo["ds"] = data_jo["ds"].apply(lambda x: pd.to_datetime(x))

data_ssjo = pd.read_csv("99-Data_Clean/df_forecast_ssjo.csv")
data_ssjo["ds"] = data_ssjo["ds"].apply(lambda x: pd.to_datetime(x))


from datetime import datetime, timedelta
with st.form("Prediction traffic par site"):
    stations_RG = ["PORTE DE SAINT-CLOUD", "PORTE D'AUTEUIL"]
    stations_PDP = ["PORTE DE SAINT-CLOUD", "PORTE D'AUTEUIL", "BOULEVARD VICTOR"]
    stations_SDF = ["STADE DE FRANCE-SAINT-DENIS", "LA PLAINE-STADE DE FRANCE", "SAINT-DENIS-PORTE DE PARIS"]
    stations_GP = ["FRANKLIN-D.ROOSEVELT"]
    stations_INV = ["INVALIDES"]
    stations_CCD = ["PALAIS ROYAL-MUSEE DU LOUVRE", "MADELEINE", "OPERA", "AUBER", "MUSEE D'ORSAY"]
    stations_CDM = ["CHAMP DE MARS-TOUR EIFFEL", "LA MOTTE-PICQUET-GRENELLE", "SEGUR"]
    stations_TEF = ["CHAMP DE MARS-TOUR EIFFEL", "PONT DE L'ALMA", "BIR-HAKEIM (GRENELLE)", "ALMA-MARCEAU"]
    stations_SUD = ["PORTE DE VERSAILLES", "BALARD", "PORTE DE VANVES"]
    stations_CHP = ["PORTE DE LA CHAPELLE", "ROSA PARKS"]
    stations_BER = ["BERCY", "GARE DE LYON"]


#mettre a jour les stations en fonction des sites rajoutés
    sites_competitions=["ROLAND-GARROS", "PARC DES PRINCES", "STADE DE FRANCE", "GRAND PALAIS", "ARENA INVALIDES", "STADE DE LA CONCORDE", "ARENA CHAMPS DE MARS", "STADE TOUR EIFFEL", "ARENA PARIS SUD", "ARENA LA CHAPELLE", "ARENA BERCY"]
    site = st.selectbox("Quel site voulez-vous analyser :", sites_competitions)
    
    mask_rg = (data_jo['station'] == 'PORTE DE SAINT-CLOUD') | (data_jo['station'] == "PORTE D'AUTEUIL")
    mask_pdp = (data_jo['station'] == 'PORTE DE SAINT-CLOUD') | (data_jo['station'] == "PORTE D'AUTEUIL") | (data_jo['station'] == "BOULEVARD VICTOR")
    mask_sdf = (data_jo['station'] == 'STADE DE FRANCE-SAINT-DENIS') | (data_jo['station'] == "LA PLAINE-STADE DE FRANCE") | (data_jo['station'] == "SAINT-DENIS-PORTE DE PARIS")
    mask_gp = (data_jo['station'] == "FRANKLIN-D.ROOSEVELT")
    mask_inv = (data_jo['station'] == "INVALIDES")
    mask_ccd = (data_jo['station'] == "PALAIS ROYAL-MUSEE DU LOUVRE") | (data_jo['station'] == "MADELEINE") | (data_jo['station'] == "OPERA") | (data_jo['station'] == "AUBER") | (data_jo['station'] == "MUSEE D'ORSAY")
    mask_cdm = (data_jo['station'] == "CHAMP DE MARS-TOUR EIFFEL") | (data_jo['station'] == "LA MOTTE-PICQUET-GRENELLE") | (data_jo['station'] == "SEGUR")
    mask_tef = (data_jo['station'] == "CHAMP DE MARS-TOUR EIFFEL") | (data_jo['station'] == "PONT DE L'ALMA") | (data_jo['station'] == "BIR-HAKEIM (GRENELLE)") | (data_jo['station'] == "ALMA-MARCEAU")
    mask_sud = (data_jo['station'] == "PORTE DE VERSAILLES") | (data_jo['station'] == "BALARD") | (data_jo['station'] == "PORTE DE VANVES")
    mask_chp = (data_jo['station'] == "PORTE DE LA CHAPELLE") | (data_jo['station'] == "ROSA PARKS")
    mask_ber = (data_jo['station'] == "BERCY") | (data_jo['station'] == "GARE DE LYON")

    def viz_mask(site):
        if site == "ROLAND-GARROS":
            return mask_rg
        elif site == "PARC DES PRINCES":
            return mask_pdp
        elif site == "STADE DE FRANCE":
            return mask_sdf
        elif site == "GRAND PALAIS":
            return mask_gp
        elif site == "ARENA INVALIDES":
            return mask_inv
        elif site == "STADE DE LA CONCORDE":
            return mask_ccd
        elif site == "ARENA CHAMPS DE MARS":
            return mask_cdm
        elif site == "STADE TOUR EIFFEL":
            return mask_tef
        elif site == "ARENA PARIS SUD":
            return mask_sud
        elif site == "ARENA LA CHAPELLE":
            return mask_chp
        elif site == "ARENA BERCY":
            return mask_ber
        else:
            return 0

    mask_ssrg = (data_ssjo['station'] == 'PORTE DE SAINT-CLOUD') | (data_ssjo['station'] == "PORTE D'AUTEUIL")
    mask_sspdp = (data_ssjo['station'] == 'PORTE DE SAINT-CLOUD') | (data_ssjo['station'] == "PORTE D'AUTEUIL") | (data_ssjo['station'] == "BOULEVARD VICTOR")
    mask_sssdf = (data_ssjo['station'] == 'STADE DE FRANCE-SAINT-DENIS') | (data_ssjo['station'] == "LA PLAINE-STADE DE FRANCE") | (data_ssjo['station'] == "SAINT-DENIS-PORTE DE PARIS")
    mask_ssgp = (data_ssjo['station'] == "FRANKLIN-D.ROOSEVELT")
    mask_ssinv = (data_ssjo['station'] == "INVALIDES")
    mask_ssccd = (data_ssjo['station'] == "PALAIS ROYAL-MUSEE DU LOUVRE") | (data_ssjo['station'] == "MADELEINE") | (data_ssjo['station'] == "OPERA") | (data_ssjo['station'] == "AUBER") | (data_ssjo['station'] == "MUSEE D'ORSAY")
    mask_sscdm = (data_ssjo['station'] == "CHAMP DE MARS-TOUR EIFFEL") | (data_ssjo['station'] == "LA MOTTE-PICQUET-GRENELLE") | (data_ssjo['station'] == "SEGUR")
    mask_sstef = (data_ssjo['station'] == "CHAMP DE MARS-TOUR EIFFEL") | (data_ssjo['station'] == "PONT DE L'ALMA") | (data_ssjo['station'] == "BIR-HAKEIM (GRENELLE)") | (data_ssjo['station'] == "ALMA-MARCEAU")
    mask_sssud = (data_ssjo['station'] == "PORTE DE VERSAILLES") | (data_ssjo['station'] == "BALARD") | (data_ssjo['station'] == "PORTE DE VANVES")
    mask_sschp = (data_ssjo['station'] == "PORTE DE LA CHAPELLE") | (data_ssjo['station'] == "ROSA PARKS")
    mask_ssber = (data_ssjo['station'] == "BERCY") | (data_ssjo['station'] == "GARE DE LYON")

    def viz_ssmask(site):
        if site == "ROLAND-GARROS":
            return mask_ssrg
        elif site == "PARC DES PRINCES":
            return mask_sspdp
        elif site == "STADE DE FRANCE":
            return mask_sssdf
        elif site == "GRAND PALAIS":
            return mask_ssgp
        elif site == "ARENA INVALIDES":
            return mask_ssinv
        elif site == "STADE DE LA CONCORDE":
            return mask_ssccd
        elif site == "ARENA CHAMPS DE MARS":
            return mask_sscdm
        elif site == "STADE TOUR EIFFEL":
            return mask_sstef
        elif site == "ARENA PARIS SUD":
            return mask_sssud
        elif site == "ARENA LA CHAPELLE":
            return mask_sschp
        elif site == "ARENA BERCY":
            return mask_ssber
        else:
            return 0

    def viz_stations(site):
        if site == "ROLAND-GARROS":
            return stations_RG
        elif site == "PARC DES PRINCES":
            return stations_PDP
        elif site == "STADE DE FRANCE":
            return stations_SDF
        elif site == "GRAND PALAIS":
            return stations_GP
        elif site == "ARENA INVALIDES":
            return stations_INV
        elif site == "STADE DE LA CONCORDE":
            return stations_CCD
        elif site == "ARENA CHAMPS DE MARS":
            return stations_CDM
        elif site == "STADE TOUR EIFFEL":
            return stations_TEF
        elif site == "ARENA PARIS SUD":
            return stations_SUD
        elif site == "ARENA LA CHAPELLE":
            return stations_CHP
        elif site == "ARENA BERCY":
            return stations_BER
        else:
            return 0


    data_jo = data_jo.loc[viz_mask(site)]
    data_ssjo = data_ssjo.loc[viz_ssmask(site)]

    start_date = datetime(2024, 7, 1)
    end_date = start_date + timedelta(days=61)
    stations=viz_stations(site)
    selected_date = st.slider(
        "Sélectionnez une plage de dates :",
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        step=timedelta(days=1),
    )
    submit = st.form_submit_button("valider")

    if submit:

        start_date = selected_date[0]
        start_date = pd.to_datetime(start_date)
        end_date = selected_date[1]
        end_date = pd.to_datetime(end_date)

        
        for station in stations :

            st.write("🚆 ", station)
        
            maskjo = (data_jo["ds"] > start_date) & (data_jo["ds"] < end_date) & (data_jo["station"] == station)
            maskssjo = (data_ssjo["ds"] > start_date) & (data_ssjo["ds"] < end_date) & (data_ssjo["station"] == station)

            filtered_data_jo= data_jo[maskjo].sort_values(by="ds") 
            filtered_data_ssjo=data_ssjo[maskssjo].sort_values(by="ds")

            filtered_data_jo['yhat'] = filtered_data_jo['yhat'].apply(np.floor).astype(int)
            filtered_data_ssjo['yhat'] = filtered_data_ssjo['yhat'].apply(np.floor).astype(int)
            filtered_data_jo['event']="avec JO"

            import plotly.graph_objects as go

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_data_jo["ds"], y=filtered_data_jo["yhat"], fill=None,mode='markers+lines',name="Fonctionnement pendant JO"))
            fig.add_trace(go.Scatter(x=filtered_data_ssjo["ds"], y=filtered_data_ssjo["yhat"],fill='tonexty',mode='markers+lines',name="Fonctionnement Normal")) # fill to trace0 y
            
            fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))

            st.plotly_chart(fig, use_container_width=True)


