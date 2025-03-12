import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Load Data
df = pd.read_csv("ea_sports_fc_player_ratings.csv")

# Define quantitative attributes
quantitative_features = [
    'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical',
    'Acceleration', 'Agility', 'Jumping', 'Stamina', 'Strength', 'Aggression',
    'Balance', 'Ball Control', 'Composure', 'Crossing', 'Curve',
    'Defensive Awareness', 'Finishing', 'Free Kick Accuracy', 'GK Diving', 'GK Handling',
    'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy',
    'Interceptions', 'Long Passing', 'Long Shots', 'Penalties', 'Positioning',
    'Reactions', 'Short Passing', 'Shot Power', 'Sliding Tackle', 'Sprint Speed',
    'Standing Tackle', 'Vision', 'Volleys'
]

# ---- League Mapping Functions ----
def map_league_men(team):
    english_men_teams = ['Arsenal', 'Aston Villa', 'Manchester City', 'Manchester Utd', 'Chelsea', 'Liverpool',
                         'AFC Bournemouth', 'Spurs', 'Newcastle Utd', 'West Ham', 'Everton', 'Crystal Palace',
                         'Brighton', 'Wolves', 'Fulham', "Nott'm Forest", 'Brentford', 'Leicester City', 'Southampton', 'Ipswich']
    spanish_men_teams = ['FC Barcelona', 'Real Madrid', 'Atlético de Madrid', 'Athletic Club', 'Girona FC', 'Villarreal CF',
                         'Real Sociedad', 'Real Betis', 'Sevilla FC', 'RCD Mallorca', 'Valencia CF', 'Rayo Vallecano',
                         'RC Celta', 'CA Osasuna', 'UD Las Palmas', 'D. Alavés', 'Getafe CF', 'CD Leganes', 'RCD Espanyol',
                         'R. Valladolid CF']
    german_men_teams = ['FC Bayern München', 'Leverkusen', 'Borussia Dortmund', 'RB Leipzig', 'Frankfurt', 'TSG Hoffenhein',
                        'SC Freiburg', "M'gladbach", 'VfL Wolfsburg', 'VfB Stuttgart', 'Union Berlin', 'SV Werder Bremen',
                        'FC Augsburg', '1. FSV Mainz 05', 'VfL Bochum 1848', 'Heidenheim', 'FC St. Pauli', 'Holstein Kiel']
    french_men_teams = ['Paris SG', 'OM', 'OL', 'AS Monaco', 'LOSC Lille', 'OGC Nice', 'RC Lens', 'Stade Brestois 29',
                        'Stade Rennais FC', 'Montpellier', 'Stade de Reims', 'Toulouse FC', 'FC Nantes', 'Strasbourg',
                        'Havre AC', 'AJ Auxerre', 'AS Saint-Étienne', 'Angers SCO']
    usa_men_teams = ['Inter Miami CF', 'LAFC', 'LA Galaxy', 'FC Cincinnati', 'Columbus Crew', 'Philadelphia',
                     'Sounders FC', 'Charlotte FC', 'Whitecaps FC', 'Houston Dynamo', 'St. Louis CITY SC', 'New England',
                     'Atlanta United', 'Orlando City', 'SJ Earthquakes', 'Portland Timbers', 'Real Salt Lake', 'FC Dallas',
                     'Nashville SC', 'Austin FC', 'D.C. United', 'Sporting KC', 'Red Bulls', 'Toronto FC', 'Minnesota United',
                     'New York City FC', 'Chicago Fire FC', 'CF Montréal', 'Colorado Rapids']

    if team in english_men_teams:
        return 'England'
    elif team in spanish_men_teams:
        return 'Spain'
    elif team in german_men_teams:
        return 'Germany'
    elif team in french_men_teams:
        return 'France'
    elif team in usa_men_teams:
        return 'USA'
    else:
        return 'Rest of the World'

def map_league_women(team):
    english_women_teams = ['Arsenal', 'Aston Villa', 'Brighton', 'Chelsea', 'Crystal Palace', 'Everton', 'Leicester City',
                           'Liverpool', 'Manchester City', 'Manchester Utd', 'Spurs', 'West Ham']
    spanish_women_teams = ['FC Barcelona', 'Real Madrid CF', 'Atlético de Madrid', 'Athletic Club', 'Granada CF',
                           'Levante Badalona', 'Levante UD', 'Madrid CFF', 'RC Deportivo', 'RCD Espanyol', 'Real Betis',
                           'Real Sociedad', 'SD Eibar', 'Sevilla FC', 'UD Tenerife', 'Valencia CF']
    german_women_teams = ['1. FC Köln', 'Carl Zeiss Jena', 'FC Bayern München', 'Frankfurt', 'Leverkusen', 'RB Leipzig',
                          'SC Freiburg', 'SGS Essen', 'SV Werder Bremen', 'TSG Hoffenheim', 'Turbine Potsdam', 'VfL Wolfsburg']
    french_women_teams = ['OL', 'Paris SG', 'AS Saint Étienne', 'Dijon FCO', 'En Avant Guingamp', 'FC Fleury 91', 'FC Nantes',
                          'Havre AC', 'Montpellier', 'Paris FC', 'Stade de Reims', 'Strasbourg']
    usa_women_teams = ['Angel City FC', 'Bay FC', 'Chicago Red Stars', 'KC Current', 'Houston Dash', 'NC Courage', 'NJ/NY Gotham',
                       'Orlando Pride', 'Portland Thorns', 'Rac. Louisville', 'San Diego Wave', 'Seattle Reign', 'Utah Royals FC',
                       'Washington Spirit']

    if team in english_women_teams:
        return 'England'
    elif team in spanish_women_teams:
        return 'Spain'
    elif team in german_women_teams:
        return 'Germany'
    elif team in french_women_teams:
        return 'France'
    elif team in usa_women_teams:
        return 'USA'
    else:
        return 'Rest of the World'

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Africa", "Men vs Women", "Ages"])

# ---- HOME PAGE ----
if page == "Home":
    st.title("Reflecting Stereotypes in Football Using EA FC 25 Data")
    st.write("""
    ### Introduction
    This dashboard explores **how player attributes in EA FC 25 reflect or reinforce stereotypes** based on ethnicity, gender, and age. Beyond being a football video game, EA FC 25 serves as a **cultural lens**, shaping perceptions about players from different backgrounds.

    ---
    ### 📊 Dashboard Overview

    **1. Africa - Regional Physical Abilities**  
    Compares speed, stamina, strength, and aggression across:
    - North Africa
    - Rest of Africa
    - Rest of the World

    **2. Men vs Women - Gendered Attributes**  
    Analyzes differences across selected attributes (like composure, aggression, etc.) for men and women players in selected leagues.

    **3. Ages - Age-Based Performance**  
    Tracks how selected physical attributes change across ages.

    🔄 **Customize Your Analysis:**  
    Users can select different attributes to explore patterns beyond the defaults.
    """)

# ---- AFRICA TAB ----
if page == "Africa":
    st.title("Africa - Regional Physical Abilities")

    # Define Regions
    north_african_countries = ['Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Mauritania', 'Sudan']
    rest_of_africa_countries = ['Angola', 'Benin', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde Islands',
                                'Central African Republic', 'Chad', 'Congo DR', "Côte d'Ivoire", 'Equatorial Guinea',
                                'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea Bissau', 'Kenya', 'Liberia',
                                'Madagascar', 'Malawi', 'Mali', 'Mozambique', 'Namibia', 'Nigeria', 'Rwanda',
                                'Senegal', 'Sierra Leone', 'Somalia', 'Tanzania', 'Togo', 'Uganda', 'Zambia', 'Zimbabwe']

    df['region'] = df['Nation'].apply(lambda x: 'North Africa' if x in north_african_countries else
                                      ('Rest of Africa' if x in rest_of_africa_countries else 'Rest of World'))

    # Trait Selection
    selected_features = st.multiselect("Select 1 to 5 Traits:", quantitative_features,
                                       default=['Pace', 'Stamina', 'Strength', 'Aggression'], max_selections=5)

    if len(selected_features) < 1:
        st.warning("Please select at least 1 feature.")
        st.stop()

    region_means = df.groupby('region')[selected_features].mean().reset_index()

    # Reshape data to long format for Plotly
    df_melted = region_means.melt(id_vars=['region'], var_name="Attribute", value_name="Average Value")

    # Create the grouped bar chart by Attribute
    fig = px.bar(df_melted, x="Attribute", y="Average Value", color="region",
                 barmode="group", title="Comparison of Physical Features by Region")

    st.plotly_chart(fig)


# ---- MEN VS WOMEN TAB ----
if page == "Men vs Women":
    st.title("Men vs Women - Gendered Attributes")

    df_men = df[df['Gender'] == "Men's Football"]
    df_women = df[df['Gender'] == "Women's Football"]

    df_men['League_Nation'] = df_men['Team'].apply(map_league_men)
    df_women['League_Nation'] = df_women['Team'].apply(map_league_women)

    df_combined = pd.concat([df_men, df_women], ignore_index=True)

    # Default leagues: England, France, Germany, Spain, USA
    selected_leagues = st.multiselect("Select Leagues:", df_combined["League_Nation"].unique(),
                                      default=['England', 'France', 'Germany', 'Spain', 'USA'])

    if not selected_leagues:
        st.warning("Please select at least one league.")
        st.stop()

    # Default X & Y attributes
    x_attr = st.selectbox("Select X-axis Attribute:", quantitative_features, index=quantitative_features.index('Aggression'))
    y_attr = st.selectbox("Select Y-axis Attribute:", quantitative_features, index=quantitative_features.index('Composure'))

    df_filtered = df_combined[df_combined['League_Nation'].isin(selected_leagues)]

    fig = px.scatter(df_filtered, x=x_attr, y=y_attr, color="Gender",
                     color_discrete_map={"Men's Football": "blue", "Women's Football": "orange"},
                     title="Comparison of Player Attributes by Gender",
                     trendline="ols", opacity=0.7, hover_data=["Name"])

    st.plotly_chart(fig)

# ---- AGES TAB ----
if page == "Ages":
    st.title("Ages - Age-Based Performance")

    df['Birthdate'] = pd.to_datetime(df['Birthdate'], errors='coerce')
    reference_date = datetime(2024, 10, 1)
    df['Age'] = df['Birthdate'].apply(lambda x: reference_date.year - x.year -
                                      ((reference_date.month, reference_date.day) < (x.month, x.day)) if pd.notnull(x) else None)

    df = df[df['Position'] != 'GK']

    age_range = st.slider("Select Age Range:", 17, 43, (17, 43), step=1)

    if age_range[0] == age_range[1]:
        st.warning("Minimum and Maximum age should be different.")
        st.stop()

    selected_features = st.multiselect("Select 1 to 5 Traits:", quantitative_features,
                                       default=['Pace', 'Stamina', 'Reactions', 'Strength'], max_selections=5)

    if len(selected_features) < 1:
        st.warning("Please select at least 1 feature.")
        st.stop()

    df_filtered = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

    fig = px.line(df_filtered.groupby("Age")[selected_features].mean().reset_index(),
                  x="Age", y=selected_features, title="Trends in Player Attributes by Age")

    st.plotly_chart(fig)
