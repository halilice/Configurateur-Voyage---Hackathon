import pandas as pd
import streamlit as st
import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from datetime import date, timedelta
pd.options.display.float_format = '{:.2f}'.format
pd.options.mode.chained_assignment = None

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://wallpapers.com/images/hd/4k-summer-2880-x-1800-05lvl8tjkkb4v4av.jpg");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

tabs_font_css = """
<style>
div[class*="stDateInput"] label {
  font-size: 110px;
  color: black;
}

div[class*="stRadio"] label {
  font-size: 110px;
  color: black;
}

div[class*="stNumberInput"] label {
  font-size: 110px;
  color: black;
}
</style>
"""

st.write(tabs_font_css, unsafe_allow_html=True)

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('logo.png', width=150)

st.title('Application du Configurateur de Voyage')

st.text("""
        Bienvenue sur le site de l'application configurateur de voyage. Vous 
        pouvez choisir votre prochaine destination de voyage en utilisant 
        notre formulaire qui comprend différents critères comme le budget 
        repas, le budget emplacement, le budget transport, etc. C'est maintenant 
        à votre tour d'essayer notre application. Profitez-en sans attendre... 
    """)

hackat = pd.read_csv('hackathon_model2.csv')
hackat.drop(['Unnamed: 0'], axis=1, inplace=True)

df_return = hackat.copy()

# encoding column Region

dico = {'Europe':1, 'Asie': 2, 'Afrique': 3, 'Océanie': 4, 'Amérique': 5}

hackat['Region'] = hackat["Region"].replace(dico)

preferance = []

preferance.append('selection')

today = date.today()

default_date_tomorrow = today + timedelta(days=1)

date_deb = st.date_input("Début de votre voyage: ", value="default_value_today")
date_fin = st.date_input("Fin de votre voyage: ", default_date_tomorrow)

jour_vac = abs((date_fin - date_deb).days)

nbr_personne = st.number_input("Pour combien de personnes? ", 
                                min_value=1, max_value=None, placeholder="Type a number...")

continent = st.radio("Quel continent voulez-vous voyager?", ['Europe', 'Asie', 'Afrique', 'Océanie', 
                                                             'Amérique', "Peu n'importe"])
if continent == 'Europe':
    preferance.append(1)

elif continent == 'Asie':
    preferance.append(2)
    
elif continent == 'Afrique':
    preferance.append(3)
    
elif continent == 'Océanie':
    preferance.append(4)
    
else:
    preferance.append(5)

nutri = st.number_input("Votre budget de repas: ", 
                                min_value=1, max_value=None, placeholder="Type a number...")
nutri1 = (nutri / nbr_personne / jour_vac) / 3
preferance.append(nutri1)

liste_budget = ['low_budget_repas', 'avg_budget_repas', 'high_budget_repas']
if nutri1 < 20:
    hackat.drop([liste_budget[1], liste_budget[2]], axis=1, inplace=True)
    liste_budget = liste_budget[0]
elif nutri1 > 60:
    hackat.drop([liste_budget[0], liste_budget[1]], axis=1, inplace=True)
    liste_budget = liste_budget[2]
else:
    hackat.drop([liste_budget[0], liste_budget[2]], axis=1, inplace=True)
    liste_budget = liste_budget[1]

trans1 = st.radio("Quel moyen de transport préférez-vous (local ou taxi)?", ['Local Transport', 'Taxi'])

liste_trans = ['local_trans', 'taxi']

if trans1 == 'Local Transport':
    hackat.drop([liste_trans[1]], axis=1, inplace=True)
    trans = st.number_input("Votre budget de transport: ", 
                                min_value=1, max_value=None, placeholder="Type a number...")
    transs = trans / nbr_personne / jour_vac / 5
    preferance.append(transs)
    liste_trans = liste_trans[0]
if trans1 == 'Taxi':
    hackat.drop([liste_trans[0]], axis=1, inplace=True)
    trans = st.number_input("Votre budget de transport: ", 
                                min_value=1, max_value=None, placeholder="Type a number...")
    transs = trans / nbr_personne / jour_vac
    preferance.append(transs)
    liste_trans = liste_trans[1]

heberge = st.number_input("Votre budget de location en total: ", 
                                min_value=1, max_value=None, placeholder="Type a number...")
hebergee = heberge / nbr_personne / jour_vac
preferance.append(hebergee)

#User input shopping
shopping = st.number_input("Votre budget pour le shopping (50-350$ ", 
                                min_value=1, max_value=None, placeholder="Type a number...")
shopping = shopping / nbr_personne
preferance.append(shopping)

# User input loisirs
loisirs = st.number_input("Quel est votre budget pour les activités? ", 
                                min_value=1, max_value=None, placeholder="Type a number...")
loisirs = loisirs / nbr_personne / 3
preferance.append(loisirs)


preferance.append(date_deb.month)

temp = st.radio("Temperature prefere:", ['Froid', 'Chaud', 'Moyen'])

if temp == 'Froid':
    preferance.append(0)
    
elif temp == 'Moyen':
    preferance.append(1)
    
else:
    preferance.append(2)

    
df_model = hackat[['city', 'Region', liste_budget,  liste_trans, 'location',  'shopping',
                     'loisirs', 'Month', 'temperature']]

dico = {'Froid':0,'Moyen':1, 'Chaud':2}

df_model['temperature'] = df_model["temperature"].replace(dico)

df_model.loc[len(df_model), :] = preferance

df_model = df_model[df_model['Month'] == preferance[7]]

df_model.drop('Month', axis=1, inplace=True)
# sorting by first name
df_model.sort_values("city", inplace=True)
# dropping ALL duplicate values
df_model.drop_duplicates(subset="city", keep=False, inplace=True)
    
df_return = df_return[df_return['Month'] == preferance[7]]
df_return.sort_values("city", inplace=True)

# dropping ALL duplicate values
df_return.drop_duplicates(subset="city", keep=False, inplace=True)
df_return.drop(['Month'], axis=1, inplace=True)
df_return[liste_budget] = df_return[liste_budget].apply(lambda x: round(x, 2))
df_return['location'] = df_return['location'].apply(lambda x: round(x, 2))
df_return[liste_trans] = df_return[liste_trans].apply(lambda x: round(x, 2))
  
df_model.index = df_model['city']
X = df_model.select_dtypes("number")
scaler = StandardScaler()
scaler.fit(X)

X_scaled = pd.DataFrame(scaler.transform(X), index=X.index, columns=X.columns)

modelNN = NearestNeighbors()
modelNN.fit(X_scaled)
ville_concerne_scaled = X_scaled.loc['selection'].to_frame().T
ville_concerne = X.loc['selection']
neigh_dist, neigh_ville = modelNN.kneighbors(ville_concerne_scaled, n_neighbors=11)
cli_ressem = neigh_ville[0][1:]

recom = df_return.iloc[cli_ressem]
recom_photo = recom["link_img"].to_string(index=False)

# Loop to return each title
st.write()
for i, row in recom.iterrows():
    recom_photo = row["link_img"]

    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.image(recom_photo, width=300)

    with col2:
        st.write(row["city"])
        st.write("Continent:", str(row["Region"]))
        st.write("Pays:", str(row["country"]))
        st.write("Population:", str(row["Population"]))
        st.write("Budget Repas:", str(row[liste_budget]))
        st.write("Budget Location:", str(row['location']))
        st.write("Budget Transport:", str(row[liste_trans]))

df_return.drop(['link_img'], axis=1, inplace=True)
st.write(df_return.iloc[cli_ressem])


















