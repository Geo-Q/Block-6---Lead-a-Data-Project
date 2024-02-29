import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go


### TITLE AND LOGO


st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://upload.wikimedia.org/wikipedia/fr/thumb/6/68/Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg/675px-Logo_JO_d%27%C3%A9t%C3%A9_-_Paris_2024.svg.png" style="width:300px;height:auto;"></div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center;'>Prédiction de la fréquentation des transports en commun par jour</h1>",
    unsafe_allow_html=True
)


### LOAD DATA GEO

#changer geo par geo
geo1=pd.read_csv('99-Data_Clean/geoloc_jo24.csv')
geo2=pd.read_csv("99-Data_Clean/sites_jo.csv")
geo2[['lat', 'lng']] = geo2['geo_point'].str.split(',', expand=True)
geo2['lat'] = pd.to_numeric(geo2['lat'])
geo2['lng'] = pd.to_numeric(geo2['lng'])

geo=geo1.merge(geo2[["lieu","activité"]], on="lieu",how="outer")
st.markdown(
    "<h5 style='text-align: left;'>Carte globale des sites de compétitions et des stations de métro à proximité </h5>",
    unsafe_allow_html=True
)

mapbox_access_token = 'pk.xxxxxxxxxxxxxxx'  # Replace with your actual Mapbox Access Token
site_data = geo.loc[geo["type"]=="site"]
station_data = geo.loc[geo["type"]=="station"]
fig1 = go.Figure(go.Scattermapbox(
    lat=site_data["lat"],
    lon=site_data["lng"],
    hoverinfo="text",
    text=site_data["lieu"],
    mode="markers+text",
    marker=go.scattermapbox.Marker(
        size=10,
        sizemin=0,
        color='lightskyblue',  
        symbol='square',
        allowoverlap=True  
    ),
    name="Sites de compétition",
    textposition='bottom center',
))

# Création de la deuxième carte Scatter Mapbox pour les stations
fig2 = go.Figure(go.Scattermapbox(
    lat=station_data["lat"],
    lon=station_data["lng"],
    hoverinfo="text",
    text=station_data["lieu"],
    mode="markers",
    marker=go.scattermapbox.Marker(
        size=10,
        color='lightsalmon',  
        symbol='circle',
        allowoverlap=True  
    ),
    name="Stations de métro"
))

# Superposition des deux cartes Scatter Mapbox
for trace in fig2.data:
    fig1.add_trace(trace)

# Mise à jour de la mise en page
fig1.update_layout(
    mapbox=dict(accesstoken=mapbox_access_token, 
        style='light',
        zoom=10,
        center=dict(lat=geo['lat'].mean()+0.01, lon=geo['lng'].mean())
    ),
    margin=dict(l=25, r=25, t=25, b=25),
)

fig1.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))


st.plotly_chart(fig1, use_container_width=True)

### LOAD DATA PRED
st.markdown(
    "<h5 style='text-align: left;'>Cartes de la fréquentation des transports en commun par site et par jour </h5>",
    unsafe_allow_html=True
)
#event_data=pd.read_csv("99-Data_Clean/event_jo.csv")
geo_data = pd.read_csv("99-Data_Clean/geoloc_jo24.csv")

data_jo = pd.read_csv("99-Data_Clean/df_forecast_jo.csv",sep=',')
data_jo["ds"] = data_jo["ds"].apply(lambda x: pd.to_datetime(x))
data_jo['lat'] = pd.to_numeric(data_jo['lat'])
data_jo['lng'] = pd.to_numeric(data_jo['lng'])
data_jo['yhat'] = pd.to_numeric(data_jo['yhat'])


data_ssjo = pd.read_csv("99-Data_Clean/df_forecast_ssjo.csv",sep=',')
data_ssjo["ds"] = data_ssjo["ds"].apply(lambda x: pd.to_datetime(x))
data_ssjo['lat'] = pd.to_numeric(data_ssjo['lat'])
data_ssjo['lng'] = pd.to_numeric(data_ssjo['lng'])
data_ssjo['yhat'] = pd.to_numeric(data_ssjo['yhat'])

compet=pd.read_csv("99-Data_Clean/compet_par_site.csv")
compet["ds"] = compet["ds"].apply(lambda x: pd.to_datetime(x,dayfirst=True))

### Select a day to analyse 
with st.form("Demande de transport par jour"):
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

    data_jo = data_jo.loc[viz_mask(site)]
    data_ssjo = data_ssjo.loc[viz_ssmask(site)]

    maskcompet=(compet['site']==site)
    competsite=compet.loc[maskcompet]

    day = st.date_input("Quel jour voulez-vous analyser :",format="YYYY-MM-DD")

    maskjo_day=(data_jo['ds']==str(day))
    data_jo_day=data_jo.loc[maskjo_day]

    maskssjo_day=(data_ssjo['ds']==str(day))
    data_ssjo_day=data_ssjo.loc[maskssjo_day]

    maskcompetday=(competsite["ds"]==str(day))
    competjour=competsite.loc[maskcompetday].reset_index()

    submit = st.form_submit_button("valider")

    if submit:
        competitions=competjour.at[0,'competition']
        st.write(f'<span style="color:darkslategray">1- Les compétitions prévues ce jour à {site}</span>', f'<span style="color:darkslategray"> : {competitions}</span>', unsafe_allow_html=True)
        st.divider()

        st.write(f'<span style="color:darkslategray">2- Baromètre global du : {str(day)}</span>', f'<span style="color:darkslategray"> pour le site : {site}</span>', unsafe_allow_html=True)
        
        diff=int(((data_jo_day['yhat'].sum()-data_ssjo_day['yhat'].sum())/data_ssjo_day['yhat'].sum())*100)
        value=int(data_jo_day['yhat'].sum())

        st.metric(label="Traffic global, toutes stations confondues", value=value, delta="{:.2f}%".format(diff),delta_color="inverse")
        
        st.divider()


        st.write(f'<span style="color:darkslategray">3- Carte du trafic normal vs trafic JO du {str(day)}</span>', f'<span style="color:darkslategray"> , site {site}</span>', unsafe_allow_html=True)

        mapbox_access_token = 'pk.xxxxxxxxxxxxxxx'  # Replace with your actual Mapbox Access Token

        figjo=px.scatter_mapbox(data_jo_day, lat="lat", lon="lng",mapbox_style="carto-positron", height= 650,  zoom=13,
                    hover_name="station", size="yhat",size_max=30)
        figjo.update_traces(textposition='top center')
        figssjo = px.scatter_mapbox(data_ssjo_day, lat="lat", lon="lng",mapbox_style="carto-positron", height= 650,  zoom=13,
                    hover_name="station",size='yhat')
        figssjo.update_traces(textposition='top center')                 
        figjo.update_traces(marker=dict(color='#FF0000',size=data_jo_day['yhat']))
        figssjo.update_traces(marker=dict(color='blue',size=data_ssjo_day['yhat']))
        fig = figjo.add_trace(figssjo.data[0])

        fig.update_layout(
            mapbox=dict(accesstoken=mapbox_access_token, 
            style='light',
            zoom=13
            ),
        title=f'Fréquentation des stations de métro associées au site {site}',

        )

        site_data = geo_data.loc[geo_data["lieu"]==site]


        # Création de la première carte Scatter Mapbox pour les sites de compétition
        fig1 = go.Figure(go.Scattermapbox(
            lat=site_data["lat"],
            lon=site_data["lng"],
            hoverinfo="text",
            text=site_data["lieu"],
            mode="markers+text",
            marker=go.scattermapbox.Marker(
                size=12,
                color='gray',  
                symbol='square',  
            ),
        name='site',
        textposition="bottom center"
        ))

        for trace in fig1.data:
            fig.add_trace(trace)

        st.plotly_chart(fig, use_container_width=True)
