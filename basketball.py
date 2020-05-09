# Import
import pandas as pd
import streamlit as st
import numpy as np
import time
import altair as alt
from vega_datasets import data
pd.options.mode.chained_assignment = None 

# Je récupère le dataframe sur Github
df = pd.read_csv('https://raw.githubusercontent.com/KoxNoob/projet_perso_sport/master/resume_saison')

########## Définition des fonctions ##########
@st.cache
# Nombre de victoires total 
def nb_victory(df,team):
  return nb_ext_victory(df,team) + nb_dom_victory(df,team)

# Nombre de défaites total 
def nb_defeat(df,team):
  return nb_ext_defeat(df,team) + nb_dom_defeat(df,team)

# Nombre de victoires à domicile
def nb_dom_victory(df,team):
  mask1 = df["home_team"]== team
  mask2 = df["home_team_score"]>df["away_team_score"]
  mask = mask1&mask2
  return len(df[mask])

# Nombre de victoires à l'extérieur
def nb_ext_victory(df,team):
  mask1 = df["away_team"]== team
  mask2 = df["away_team_score"]>df["home_team_score"]
  mask = mask1&mask2
  return len(df[mask])

# Nombre de défaites à domicile
def nb_dom_defeat(df,team):
  mask1 = df["home_team"]== team
  mask2 = df["home_team_score"]<df["away_team_score"]
  mask = mask1&mask2
  return len(df[mask])

# Nombre de défaites à l'extérieur
def nb_ext_defeat(df,team):
  mask1 = df["away_team"]== team
  mask2 = df["away_team_score"]<df["home_team_score"]
  mask = mask1&mask2
  return len(df[mask])

# Moyenne de points pour à domicile
def moy_pts_dom_p(df,team):
  mask1 = df['home_team'] == team
  mask2 = df['home_team_score']
  mask = mask1&mask2
  return round(df[mask]['home_team_score'].mean(),1)

# Moyenne de points pour à l'extérieur
def moy_pts_ext_p(df,team):
  mask1 = df['away_team'] == team
  mask2 = df['away_team_score']
  mask = mask1&mask2
  return round(df[mask]['away_team_score'].mean(),1)

# Moyenne de points pour
def moy_pts_p(df,team):
  return round((moy_pts_dom_p(df,team) + moy_pts_ext_p(df,team)) / 2, 1)

# Moyenne de points contre à domicile
def moy_pts_dom_c(df,team):
  mask1 = df['home_team'] == team
  mask2 = df['home_team_score']
  mask = mask1&mask2
  return round(df[mask]['away_team_score'].mean(),1)

# Moyenne de points contre à l'extérieur
def moy_pts_ext_c(df,team):
  mask1 = df['away_team'] == team
  mask2 = df['away_team_score']
  mask = mask1&mask2
  return round(df[mask]['home_team_score'].mean(),1)

# Moyenne de points contre
def moy_pts_c(df,team):
  return round((moy_pts_dom_c(df,team) + moy_pts_ext_c(df,team)) / 2, 1)

# Poucentage de victoires
def pourcent(df,team):
  return round(nb_victory(df,team)/(nb_victory(df,team) + nb_defeat(df,team))*100,1)

# Conference Est ou Ouest ?
def conf(df,team):
  listW = ['LOS ANGELES LAKERS', 'LOS ANGELES CLIPPERS', 'DENVER NUGGETS', 'UTAH JAZZ',
           'HOUSTON ROCKETS', 'OKLAHOMA CITY THUNDER', 'DALLAS MAVERICKS', 'MEMPHIS GRIZZLIES',
           'PORTLAND TRAIL BLAZERS', 'NEW ORLEANS PELICANS', 'SACRAMENTO KINGS', 'SAN ANTONIO SPURS',
           'PHOENIX SUNS', 'MINNESOTA TIMBERWOLVES', 'GOLDEN STATE WARRIORS']
  if team in listW:
    return 'West'
  else:
    return 'East'


########## Création du DF avec les données ##########

# Création d'un dataframe vide
df_final=pd.DataFrame()

# Remplissage du dataframe final
for team in list(df["away_team"].unique()):
  mask1=df["away_team"]==team
  mask2=df["home_team"]==team
  mask=mask1|mask2
  df2=df[mask]
  df1=pd.DataFrame({"Team":[team], 'Conf' : conf(df2, team) ,'%V' : pourcent(df2,team),'W' : nb_victory(df2,team), 'L' : nb_defeat(df2,team), "W_dom":nb_dom_victory(df2,team), 
                    "L_dom":nb_dom_defeat(df2,team), "W_ext":nb_ext_victory(df2,team), "L_ext":nb_ext_defeat(df2,team), 'Moy_Pts_Pour' : moy_pts_p(df2, team)
                    , 'Moy_Pts_Contre' : moy_pts_c(df2, team), 'Moy_Pts_Dom_Pour': moy_pts_dom_p(df2,team), 'Moy_Pts_Dom_Contre': moy_pts_dom_c(df2,team),
                     'Moy_Pts_Ext_Pour' : moy_pts_ext_p(df2,team),'Moy_Pts_Ext_Contre' : moy_pts_ext_c(df2,team)})
  df_final=df_final.append(df1)

df_final = df_final.reset_index(drop=True)
df_final = df_final.sort_values(by= '%V', ascending = False)
df_final = df_final.reset_index(drop=True)
df_final.index = df_final.index + 1
link = 'https://raw.githubusercontent.com/KoxNoob/projet_perso_sport/master/gps.csv'
df_gps = pd.read_csv(link)

###### Préparation des df secondaires pour les classements ######

df_west = df_final[df_final['Conf'] == 'West']
df_west = df_west.reset_index(drop=True)
df_west.index = df_west.index + 1

df_east = df_final[df_final['Conf'] == 'East']
df_east = df_east.reset_index(drop=True)
df_east.index = df_east.index + 1

mask1 = df_final.iloc[:,:5]
mask2 = df_final.iloc[:,9:11]
df_stat_4 = pd.merge(left = mask1, right = mask2, left_index = True, right_index = True, how = 'inner')


mask3 = df_final.iloc[:,:2]
mask4 = df_final.iloc[:,5:9]
df_stat_1 = pd.merge(left = mask3, right = mask4, left_index = True, right_index = True, how = 'inner')


mask5 = df_final.iloc[:,:2]
mask6 = df_final.iloc[:,11:]
df_stat_7 = pd.merge(left = mask5, right = mask6, left_index = True, right_index = True, how = 'inner')


mask7 = df_west.iloc[:,:5]
mask8 = df_west.iloc[:,9:11]
df_stat_5 = pd.merge(left = mask7, right = mask8, left_index = True, right_index = True, how = 'inner')


mask9 = df_west.iloc[:,:2]
mask10 = df_west.iloc[:,5:9]
df_stat_2 = pd.merge(left = mask9, right = mask10, left_index = True, right_index = True, how = 'inner')


mask11 = df_west.iloc[:,:2]
mask12 = df_west.iloc[:,11:]
df_stat_8 = pd.merge(left = mask11, right = mask12, left_index = True, right_index = True, how = 'inner')


mask13 = df_east.iloc[:,:5]
mask14 = df_east.iloc[:,9:11]
df_stat_6 = pd.merge(left = mask13, right = mask14, left_index = True, right_index = True, how = 'inner')


mask15 = df_east.iloc[:,:2]
mask16 = df_east.iloc[:,5:9]
df_stat_3 = pd.merge(left = mask15, right = mask16, left_index = True, right_index = True, how = 'inner')


mask17 = df_east.iloc[:,:2]
mask18 = df_east.iloc[:,11:]
df_stat_9 = pd.merge(left = mask17, right = mask18, left_index = True, right_index = True, how = 'inner')


###### Code Streamlit ######

path="https://github.com/KoxNoob/projet_perso_sport/blob/master/nba.jpg?raw=true"

# Page d'accueil
st.markdown("<h1 style='text-align: center; color: blue;'>Statistiques NBA</h1>", unsafe_allow_html=True)
st.sidebar.image(path, use_column_width=True)

# Sidebar
vue = st.sidebar.radio(
     "Menu",
     ('Accueil', 'Classement'), 0)

# Page d'accueil
if vue == 'Accueil':
  st.markdown("<h3 style='text-align: center; color: grey; size = 0'>Fan de la NBA bien le bonjour. Voici une petit app faite par un fan pendant son temps libre. Enjoy it !</h3>", unsafe_allow_html=True)
  st.image('https://media.giphy.com/media/3o6fJbxSSH6poHZQha/giphy-downsized.gif',use_column_width=True)
# Page classement
if vue == 'Classement':
  
# Possibilité de choisir quel classement voir
  option = st.selectbox('Quel classement voulez-vous ?',
                ('Général', 'Conférence Ouest', 'Conférence Est'))

# Possibilité de choisir les statistiques à afficher
  stats = st.multiselect('Quelles statistiques voulez-vous voir ?', 
                ('Générales', 'Victoires/Défaites domicile/extérieur','Moyennes de points Pour/Contre détaillées' ))
  
#Classement Général
  if option == 'Général':
    if stats == ['Générales']:
      st.write(df_stat_4)
    if stats == ['Victoires/Défaites domicile/extérieur']:
      st.write(df_stat_1)
    if stats == ['Moyennes de points Pour/Contre détaillées']:
      st.write(df_stat_7)
    if sorted(stats) == ['Générales', 'Victoires/Défaites domicile/extérieur']:
      st.write(df_final.iloc[:,:11])
    if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées']:
      df_stat_10 = pd.merge(left = df_stat_4, right = df_stat_7, on=['Team', 'Conf'], how = 'inner')
      df_stat_10.index = df_stat_10.index + 1
      st.write(df_stat_10)
    if sorted(stats) == ['Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
      df_stat_13 = pd.merge(left = df_stat_1, right = df_stat_7, on=['Team', 'Conf'], how = 'inner')
      df_stat_13.index = df_stat_13.index + 1
      st.write(df_stat_13)
    if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
      st.write(df_final)
    # Test Mapping
    st.markdown("<h3 style='text-align: center; color: blue; size = 0'>Localisation des Team</h3>", unsafe_allow_html=True)
    states = alt.topo_feature(data.us_10m.url, feature='states')

    # US states background
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=700,
        height=400
    ).project('albersUsa')

    # airport positions on background
    points = alt.Chart(df_gps).mark_circle(size=100).encode(
        longitude='Longitude',
        latitude='Latitude',
        color=alt.value('blue'),
        tooltip=['Team']
        
    )
    background + points
# Classement Conférence Ouest
  if option == 'Conférence Ouest':
    if stats == ['Générales']:
      st.write(df_stat_5)
    if stats == ['Victoires/Défaites domicile/extérieur']:
      st.write(df_stat_2)
    if stats == ['Moyennes de points Pour/Contre détaillées']:
      st.write(df_stat_8)
    if sorted(stats) == ['Générales', 'Victoires/Défaites domicile/extérieur']:
      st.write(df_west.iloc[:,:11])
    if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées']:
      df_stat_11 = pd.merge(left = df_stat_5, right = df_stat_8, on=['Team', 'Conf'], how = 'inner')
      df_stat_11.index = df_stat_11.index + 1
      st.write(df_stat_11)
    if sorted(stats) == ['Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
      df_stat_14 = pd.merge(left = df_stat_2, right = df_stat_8, on=['Team', 'Conf'], how = 'inner')
      df_stat_14.index = df_stat_14.index + 1
      st.write(df_stat_14)
    if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
      st.write(df_west)
    # Test Mapping
    st.markdown("<h3 style='text-align: center; color: blue; size = 0'>Localisation des Team de la Conférence Ouest</h3>", unsafe_allow_html=True)
    states = alt.topo_feature(data.us_10m.url, feature='states')

    # US states background
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=700,
        height=400
    ).project('albersUsa')

    # airport positions on background
    points = alt.Chart(df_gps[df_gps['Conf'] == 'West']).mark_circle(size=100).encode(
        longitude='Longitude',
        latitude='Latitude',
        color=alt.value('blue'),
        tooltip=['Team']
        
    )
    background + points
# Classement Conférence Est
  if option == 'Conférence Est':
    if stats == ['Générales']:
      st.write(df_stat_6)
    if stats == ['Victoires/Défaites domicile/extérieur']:
      st.write(df_stat_3)
    if stats == ['Moyennes de points Pour/Contre détaillées']:
      st.write(df_stat_9)
    if sorted(stats) == ['Générales', 'Victoires/Défaites domicile/extérieur']:
      st.write(df_east.iloc[:,:11])
    if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées']:
      df_stat_12 = pd.merge(left = df_stat_6, right = df_stat_9, on=['Team', 'Conf'], how = 'inner')
      df_stat_12.index = df_stat_12.index + 1
      st.write(df_stat_12)
    if sorted(stats) == ['Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
      df_stat_15 = pd.merge(left = df_stat_3, right = df_stat_9, on=['Team', 'Conf'], how = 'inner')
      df_stat_15.index = df_stat_15.index + 1
      st.write(df_stat_15)
    if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
      st.write(df_east)
    # Test Mapping
    st.markdown("<h3 style='text-align: center; color: blue; size = 0'>Localisation des Team de la Conférence Est</h3>", unsafe_allow_html=True)
    states = alt.topo_feature(data.us_10m.url, feature='states')

    # US states background
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=700,
        height=400
    ).project('albersUsa')

    # airport positions on background
    points = alt.Chart(df_gps[df_gps['Conf'] == 'East']).mark_circle(size=100).encode(
        longitude='Longitude',
        latitude='Latitude',
        color=alt.value('blue'),
        tooltip=['Team']
    )
    background + points