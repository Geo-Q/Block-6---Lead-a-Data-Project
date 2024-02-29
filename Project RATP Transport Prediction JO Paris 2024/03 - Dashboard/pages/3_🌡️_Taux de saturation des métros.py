import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
### TITLE AND LOGO


st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://upload.wikimedia.org/wikipedia/fr/thumb/6/68/Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg/675px-Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg.png" style="width:300px;height:auto;"></div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center;'>Taux de saturation des transports en commun par site</h1>",
    unsafe_allow_html=True
)

### LOAD AND CACHE DATA

data=pd.read_csv('99-Data_Clean/df_forecast_jo.csv')

### LOAD AND CACHE DATA

geo_data = pd.read_csv("99-Data_Clean/geoloc_jo24.csv")
data_jo = pd.read_csv("99-Data_Clean/df_forecast_jo.csv")
event=pd.read_csv("99-Data_Clean/event_jo.csv")
event["ds"] = event["ds"].apply(lambda x: pd.to_datetime(x))
data_jo["ds"] = data_jo["ds"].apply(lambda x: pd.to_datetime(x))
data_jo = data_jo.merge(geo_data[["lieu","type","capacite"]], left_on='station', right_on='lieu')
data_jo = data_jo.drop(axis=1, columns='lieu')
compet=pd.read_csv("99-Data_Clean/compet_par_site.csv")
compet["ds"] = compet["ds"].apply(lambda x: pd.to_datetime(x))
token = 'pk.xxxxxxxxxxxxxxx'  # Replace with your actual Mapbox Access Token


from datetime import datetime, timedelta
with st.form("Carte flux par site"):
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

    sites_competitions=["ROLAND-GARROS", "PARC DES PRINCES", "STADE DE FRANCE", "GRAND PALAIS", "ARENA INVALIDES", "STADE DE LA CONCORDE", "ARENA CHAMPS DE MARS", "STADE TOUR EIFFEL", "ARENA PARIS SUD", "ARENA LA CHAPELLE", "ARENA BERCY"]
    site = st.selectbox("Quel site voulez-vous visualiser :", sites_competitions)
    
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

    def events(site):
        if site == "ROLAND-GARROS":
            return "EVENT_RG"
        elif site == "PARC DES PRINCES":
            return "EVENT_PDP"
        elif site == "STADE DE FRANCE":
            return "EVENT_SDF"
        elif site == "GRAND PALAIS":
            return "EVENT_GP"
        elif site == "ARENA INVALIDES":
            return "EVENT_INV"
        elif site == "STADE DE LA CONCORDE":
            return "EVENT_CCD"
        elif site == "ARENA CHAMPS DE MARS":
            return "EVENT_CDM"
        elif site == "STADE TOUR EIFFEL":
            return "EVENT_TEF"
        elif site == "ARENA PARIS SUD":
            return "EVENT_SUD"
        elif site == "ARENA LA CHAPELLE":
            return "EVENT_CHP"
        elif site == "ARENA BERCY":
            return "EVENT_BER"
        else:
            return 0


    data_jo = data_jo.loc[viz_mask(site)]


    start_date = datetime(2024, 7, 1)
    end_date = start_date + timedelta(days=61)

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
                
        event = event[['ds', events(site)]]
        event["ds"] = event["ds"].apply(lambda x: pd.to_datetime(x))
        event['ds'] = event['ds'].apply(lambda x: str(x))
        event.iloc[:,1] = event.iloc[:,1].apply(lambda x: 10 if x == 1 else 5)
        
        data_jo = data_jo.reset_index().drop(axis=1, columns='index')
        data_jo['ds'] = data_jo['ds'].apply(lambda x: pd.to_datetime(x))
        data_jo = data_jo.loc[data_jo['ds'] >= start_date]
        data_jo = data_jo.loc[data_jo['ds'] <= end_date]
        data_jo = data_jo.reset_index().drop(axis=1, columns='index')
        data_jo['ds'] = data_jo['ds'].apply(lambda x: str(x))
        data_jo['satur'] = data_jo['yhat'] / data_jo['capacite'] * 100
        data_jo['satur_color_bin'] = data_jo['satur'].apply(lambda x: 0 if (x < 100) else 1)
        site_data=compet.loc[compet['site'] == site]

        data_jo = data_jo.merge(event, on='ds')
        
        
        fig1 = px.scatter_mapbox(data_jo, lat="lat", lon="lng", mapbox_style="carto-positron", height= 650,  zoom=12, animation_frame = 'ds', hover_name="station", 
                        size=data_jo.iloc[:,-1], color="satur", color_continuous_scale="Bluered", range_color=[0,data_jo['satur'].max()],
                        title=f"Taux de saturation pour les stations du site {site}")


        fig2 = go.Figure(go.Scattermapbox(
            lat=site_data["lat"],
            lon=site_data["lng"],
            hoverinfo="text",
            text=site_data["site"], 
            mode="markers+text",
            marker=go.scattermapbox.Marker(
                size=12,
                color='gray',  
                symbol='square',
          
            ),
        name='site',
        textposition="bottom center",showlegend=False, 
        ))

        for trace in fig2.data:
            fig1.add_trace(trace)

        fig1.update_layout(
            mapbox=dict(accesstoken=token, 
            style='light',
            zoom=13
            ),
        title=f"Taux de saturation pour les stations du site {site}",

        )

        st.plotly_chart(fig1, use_container_width=True)


        max=data_jo['satur'].max()
        figbar=px.bar(data_jo, x="station", y="satur", animation_frame="ds", color="satur_color_bin",color_continuous_scale="Bluered", title=f"Taux de saturation pour les stations du site {site}")
        figbar.update(layout_yaxis_range = [0,max])
        st.plotly_chart(figbar, use_container_width=True)

