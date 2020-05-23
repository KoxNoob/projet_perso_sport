# Import
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
import plotly.express as px
import plotly.graph_objects as go

pd.options.mode.chained_assignment = None 
read_and_cache_csv = st.cache(pd.read_csv)

# Je récupère le dataframe sur Github
df = pd.read_csv('https://raw.githubusercontent.com/KoxNoob/Stats-Nba/master/resume_saison%20(1)')

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
  return round(df[mask]['home_team_score'].mean())

# Moyenne de points pour à l'extérieur
def moy_pts_ext_p(df,team):
  mask1 = df['away_team'] == team
  mask2 = df['away_team_score']
  mask = mask1&mask2
  return round(df[mask]['away_team_score'].mean())

# Moyenne de points pour
def moy_pts_p(df,team):
  return round((moy_pts_dom_p(df,team) + moy_pts_ext_p(df,team)) / 2)

# Moyenne de points contre à domicile
def moy_pts_dom_c(df,team):
  mask1 = df['home_team'] == team
  mask2 = df['home_team_score']
  mask = mask1&mask2
  return round(df[mask]['away_team_score'].mean())

# Moyenne de points contre à l'extérieur
def moy_pts_ext_c(df,team):
  mask1 = df['away_team'] == team
  mask2 = df['away_team_score']
  mask = mask1&mask2
  return round(df[mask]['home_team_score'].mean())

# Moyenne de points contre
def moy_pts_c(df,team):
  return round((moy_pts_dom_c(df,team) + moy_pts_ext_c(df,team)) / 2)

# Poucentage de victoires
def pourcent(df,team):
  return round(nb_victory(df,team)/(nb_victory(df,team) + nb_defeat(df,team))*100)

# Conference Est ou Ouest ?
def conf(df,team):
  listW = ['Los Angeles Lakers', 'Los Angeles Clippers', 'Denver Nuggets', 'Utah Jazz',
           'Houston Rockets', 'Oklahoma City Thunder', 'Dallas Mavericks', 'Memphis Grizzlies',
           'Portland Trail Blazers', 'New Orleans Pelicans', 'Sacramento Kings', 'San Antonio Spurs',
           'Phoenix Suns', 'Minnesota Timberwolves', 'Golden State Warriors']
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
link = 'https://raw.githubusercontent.com/KoxNoob/Stats-Nba/master/df_gps'
df_gps = pd.read_csv(link)
df_gps = df_gps.rename(columns={'Longitude': 'longitude', 'Latitude' : 'latitude'})

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


def display_stat(df):
    fig = go.Figure(data=[go.Table(columnorder=[i for i in range(0,len(df)+1)], columnwidth=100,
                                   header=dict(
                                       values=df.columns,
                                       fill_color='#B82E2E',
                                       line=dict(width=2), font=dict(color='white', size=14)),
                                   cells=dict(values=df.T,
                                              fill_color=['#B82E2E', '#3366CC'],
                                              font=dict(color='white', size=[14, 12]),
                                              line=dict(width=2), height=50))])

    fig.update_layout(width=2000, height=500)
    st.plotly_chart(fig, use_container_width=True)


###### Code Streamlit ######

path="https://github.com/KoxNoob/projet_perso_sport/blob/master/nba.jpg?raw=true"

# Page d'accueil
st.markdown("<h1 style='text-align: center; color: #3366CC;'>Statistiques NBA</h1>", unsafe_allow_html=True)
st.sidebar.image(path, use_column_width=True)

# Sidebar
vue = st.sidebar.radio(
     "Menu",
     ('Accueil', 'Classement', 'Confrontation'), 0)

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

        # Mapping
        st.markdown('<p align="center"><img width="200" height="100" src="https://github.com/KoxNoob/Stats-Nba/blob/master/logo/NBA-logo.jpg?raw=true"></p>',unsafe_allow_html=True)
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
        points_w = alt.Chart(df_gps[df_gps['Conf'] == 'West']).mark_circle(size=100).encode(
            longitude='longitude',
            latitude='latitude',
            color=alt.value('#B82E2E'),
            tooltip=['Team']

        )

        points_e = alt.Chart(df_gps[df_gps['Conf'] == 'East']).mark_circle(size=100).encode(
            longitude='longitude',
            latitude='latitude',
            color=alt.value('#3366CC'),
            tooltip=['Team']

        )
        background + points_w + points_e
    
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

        # Mapping
        st.markdown('<p align="center"><img width="200" height="100" src="https://github.com/KoxNoob/Stats-Nba/blob/master/logo/225px-Conf%C3%A9rence_Ouest_de_la_NBA.png?raw=true"></p>',unsafe_allow_html=True)

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
            longitude='longitude',
            latitude='latitude',
            color=alt.value('#B82E2E'),
            tooltip=['Team']

        )
        background + points
# Classement Conférence Est
    if option == 'Conférence Est':
        if stats == ['Générales']:
          st.dataframe(df_stat_6)
        if stats == ['Victoires/Défaites domicile/extérieur']:
          st.dataframe(df_stat_3)
        if stats == ['Moyennes de points Pour/Contre détaillées']:
          st.dataframe(df_stat_9)
        if sorted(stats) == ['Générales', 'Victoires/Défaites domicile/extérieur']:
          st.dataframe(df_east.iloc[:,:11])
        if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées']:
          df_stat_12 = pd.merge(left = df_stat_6, right = df_stat_9, on=['Team', 'Conf'], how = 'inner')
          df_stat_12.index = df_stat_12.index + 1
          st.dataframe(df_stat_12)
        if sorted(stats) == ['Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
          df_stat_15 = pd.merge(left = df_stat_3, right = df_stat_9, on=['Team', 'Conf'], how = 'inner')
          df_stat_15.index = df_stat_15.index + 1
          st.dataframe(df_stat_15)
        if sorted(stats) == ['Générales','Moyennes de points Pour/Contre détaillées','Victoires/Défaites domicile/extérieur']:
          st.dataframe(df_east)

        # Mapping
        st.markdown('<p align="center"><img width="200" height="100" src="https://github.com/KoxNoob/Stats-Nba/blob/master/logo/225px-Conf%C3%A9rence_Est_de_la_NBA.png?raw=true"></p>',unsafe_allow_html=True)
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
            longitude='longitude',
            latitude='latitude',
            color=alt.value('#3366CC'),
            tooltip=['Team']
        )
        background + points

if vue == 'Confrontation':
    st.markdown('### Dans cette section, vous allez pouvoir choisir 2 équipes pour avoir un petit résumé de leurs statistiques \
    respectives, et dans leur face-à-face.')

    confTeamA = st.sidebar.selectbox("Choisissez la conférence de l'équipe à domicile", ('Conférence Ouest', 'Conférence Est'), 0)
    if confTeamA == 'Conférence Ouest':
        teamA = st.sidebar.selectbox("Choisissez l\'équipe à domicile", df_final[df_final['Conf'] == "West"]['Team'].unique())
    else:
        teamA = st.sidebar.selectbox("Choisissez l\'équipe à domicile", df_final[df_final['Conf'] == "East"]['Team'].unique())

    confTeamB = st.sidebar.selectbox("Choisissez la conférence de l'équipe à l'extérieur", ('Conférence Ouest', 'Conférence Est'), 1)
    if confTeamB == 'Conférence Ouest':
        teamB = st.sidebar.selectbox("Choisissez l\'équipe à l'extérieur", df_final[df_final['Conf'] == "West"]['Team'].unique())
    else:
        teamB = st.sidebar.selectbox("Choisissez l\'équipe à l'extérieur", df_final[df_final['Conf'] == "East"]['Team'].unique())

    localisation = st.sidebar.checkbox("Localiser les Team")

    # Comparaison des moyennes de points
    def display_moy_pts_dom(team):
        st.write("Moyenne de points marqués à domicile : " + str(moy_pts_dom_p(df, team)))
        st.write("Moyenne de points encaissés à domicile : " + str(moy_pts_dom_c(df, team)))

    def display_moy_pts_ext(team):
        st.write("Moyenne de points marqués à l'extérieur : " + str(moy_pts_ext_p(df, team)))
        st.write("Moyenne de points encaissés à l'extérieur : " + str(moy_pts_ext_c(df, team)))

    def vict_team1(team):
        mask1 = df_final['Team'] == team
        V_team = df_final.loc[mask1]['%V'].sum()
        st.write("Pourcentage total de victoires  : " + str(V_team) + "%")

    def display_stat(team):
        st.markdown("<h2 style='text-align: center; color: gray; size = 0'>" + str(team), unsafe_allow_html=True)
        st.markdown('<p align="center"><img width="150" height="150" src=' + df_gps[df_gps['Team'] == team]['Logo'].any() + "</p>", unsafe_allow_html=True)
        vict_team1(team)
        if team == teamA:
            display_moy_pts_dom(team)
        else:
            display_moy_pts_ext(team)

    def mapping(team1, team2):
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
        mask1 = df_gps[df_gps['Team'] == team1]
        mask2 = df_gps[df_gps['Team'] == team2]
        mask3 = pd.concat([mask1, mask2])
        points = alt.Chart(mask3).mark_circle(size=500).encode(
            longitude='longitude',
            latitude='latitude',
            color=alt.value('#3366CC'),
            tooltip=['Team']
        )
        background + points


    def team1VD(team1, team2):
        mask1 = df["home_team"] == team1
        mask2 = df["away_team"] == team2
        mask3 = df["home_team_score"] > df["away_team_score"]
        mask = mask1 & mask2 & mask3
        return len(df[mask])


    def team1VE(team1, team2):
        mask1 = df["home_team"] == team2
        mask2 = df["away_team"] == team1
        mask3 = df["away_team_score"] > df["home_team_score"]
        mask = mask1 & mask2 & mask3
        return len(df[mask])


    def team2VD(team1, team2):
        mask1 = df["home_team"] == team2
        mask2 = df["away_team"] == team1
        mask3 = df["home_team_score"] > df["away_team_score"]
        mask = mask1 & mask2 & mask3
        return len(df[mask])


    def team2VE(team1, team2):
        mask1 = df["home_team"] == team1
        mask2 = df["away_team"] == team2
        mask3 = df["away_team_score"] > df["home_team_score"]
        mask = mask1 & mask2 & mask3
        return len(df[mask])


    def resultat_confrontation(team1, team2):
        v_team1 = team1VD(team1, team2) + team1VE(team1, team2)
        v_team2 = team2VD(team1, team2) + team2VE(team1, team2)
        if v_team1 > v_team2:
            st.write("Les " + team1 + " dominent les confrontations contre les " + team2 + ", " + str(v_team1) + " victoire(s) à " + str(v_team2) + " .")
        elif v_team1 < v_team2:
            st.write("Les " + team2 + " dominent les confrontations contre les " + team1 + ", " + str(v_team2) + " victoire(s) à " + str(v_team1) + " .")
        else:
            st.write(" Les 2 équipes sont à égalité dans leurs confrontations " + str(v_team1) + " - " + str(v_team2) + " .")


    def historique_confrontation(team1, team2):
        mask1 = df['home_team'] == team1
        mask2 = df['away_team'] == team2
        mask3 = df['home_team'] == team2
        mask4 = df['away_team'] == team1
        maskA = mask1 & mask2
        maskB = mask3 & mask4
        df_hist = pd.concat([df[maskA], df[maskB]])
        df_hist = df_hist.drop(columns=['start_time'])
        df_hist = df_hist.rename(
            columns={'away_team': 'Team_Ext', 'away_team_score': 'Score_Ext', 'home_team': 'Team_Dom',
                     'home_team_score': 'Score_Dom'})
        df_hist = df_hist.reset_index(drop=True)
        df_hist = df_hist.drop('Unnamed: 0', axis =1)
        return df_hist

    def display_historique(df):
        fig = go.Figure(data=[go.Table(columnorder=[1,2,3,4,5], columnwidth=[15, 30, 15, 30, 15],
                                       header=dict(values=['Match','Team Extérieur', 'Score Ext', 'Team Domicile', 'Score Dom'],
                                                   fill_color='#B82E2E',
                                                   line=dict(width=2), font=dict(color='white', size=14)),
                                       cells=dict(values=[[i for i in range(1, len(df)+1)], df.Team_Ext, df.Score_Ext, df.Team_Dom, df.Score_Dom],
                                                  fill_color=['#B82E2E', '#3366CC'], font=dict(color='white', size=[14, 12]),
                                                  line=dict(width=2), height=50))])

        fig.update_layout(width=1200, height=500)
        st.plotly_chart(fig, use_container_width=True)

    def versus(team1, team2):
        st.markdown('<h2 style=\'text-align: center; color: grey; size = 0\'> FACE A FACE', unsafe_allow_html=True)
        resultat_confrontation(team1, team2)
        display_historique(historique_confrontation(team1, team2))


    display_stat(teamA)
    display_stat(teamB)
    if localisation :
        mapping(teamA, teamB)
    versus(teamA, teamB)
