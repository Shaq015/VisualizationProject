import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# Load dataset
data_path = "ea_sports_fc_player_ratings.csv"
df = pd.read_csv(data_path)

# Define quantitative features (complete list)
quantitative_features = [
    'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical', 'Acceleration', 'Agility',
    'Jumping', 'Stamina', 'Strength', 'Aggression', 'Balance', 'Ball Control', 'Composure',
    'Crossing', 'Curve', 'Defensive Awareness', 'Finishing', 'Free Kick Accuracy', 'GK Diving',
    'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy', 'Interceptions',
    'Long Passing', 'Long Shots', 'Penalties', 'Positioning', 'Reactions', 'Short Passing',
    'Shot Power', 'Sliding Tackle', 'Sprint Speed', 'Standing Tackle', 'Vision', 'Volleys'
]

# Set up League_Nation mapping
def assign_league_nation(team):
    leagues = {
        "England": ['Arsenal', 'Aston Villa', 'Manchester City', 'Chelsea', 'Liverpool', 'Spurs'],
        "Spain": ['FC Barcelona', 'Real Madrid', 'Atlético de Madrid', 'Sevilla FC'],
        "Germany": ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig'],
        "France": ['Paris SG', 'Marseille', 'Lyon', 'Monaco'],
        "USA": ['Inter Miami CF', 'LA Galaxy', 'New York City FC']
    }
    for league, teams in leagues.items():
        if team in teams:
            return league
    return "Rest of the World"

df['League_Nation'] = df['Team'].apply(assign_league_nation)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Home", "Africa", "Men vs Women", "Ages"])

# Home Page
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
    Analyzes differences across selected attributes (like composure, aggression, etc.) for players in selected leagues.

    **3. Ages - Age-Based Performance**  
    Tracks how selected physical attributes change across ages.
    """)

# Africa Tab
elif page == "Africa":
    st.title("Regional Physical Abilities")

    # Select traits (limit 1 to 5)
    selected_features = st.multiselect("Select 1 to 5 Physical Traits:", quantitative_features,
                                       default=['Pace', 'Stamina', 'Strength', 'Aggression'],
                                       max_selections=5)

    if len(selected_features) < 1:
        st.warning("Please select at least 1 feature.")
        st.stop()

    # Set up regions
    df['region'] = df['Nation'].apply(lambda x: 'North Africa' if x in ['Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Mauritania', 'Sudan']
                                      else ('Rest of Africa' if x in ['Nigeria', 'Senegal', 'Ghana', 'Cameroon'] else 'Rest of World'))

    # Average calculation
    region_means = df.groupby('region')[selected_features].mean().reset_index()

    # Bar chart (traits on X, avg values as bars, split by region)
    fig = go.Figure()
    for region in region_means['region']:
        values = region_means[region_means['region'] == region][selected_features].values.flatten()
        fig.add_trace(go.Bar(x=selected_features, y=values, name=region))

    fig.update_layout(barmode='group', title="Average Physical Traits by Region", yaxis=dict(range=[50, 100]))
    st.plotly_chart(fig)

# Men vs Women Tab
elif page == "Men vs Women":
    st.title("Gender-Based Attributes Analysis")

    gender_filter = st.selectbox("Filter by Gender:", ["Both", "Men", "Women"], index=0)
    selected_leagues = st.multiselect("Select Leagues:", df['League_Nation'].unique(), default=df['League_Nation'].unique())

    x_axis = st.selectbox("Select Attribute for X-axis:", quantitative_features, index=quantitative_features.index('Aggression'))
    y_axis = st.selectbox("Select Attribute for Y-axis:", quantitative_features, index=quantitative_features.index('Composure'))

    df_filtered = df[df['League_Nation'].isin(selected_leagues)]
    if gender_filter == "Men":
        df_filtered = df_filtered[df_filtered['Gender'] == "Men's Football"]
    elif gender_filter == "Women":
        df_filtered = df_filtered[df_filtered['Gender'] == "Women's Football"]

    color_map = {"Men's Football": "blue", "Women's Football": "orange"}

    # Scatter Plot
    fig = px.scatter(df_filtered, x=x_axis, y=y_axis, color='Gender', hover_data=['Name', 'Gender'],
                     title=f"{x_axis} vs {y_axis} by Gender & League", color_discrete_map=color_map)

    # Add trendlines (to appear on top)
    for gender in df_filtered['Gender'].unique():
        gender_data = df_filtered[df_filtered['Gender'] == gender]
        x = gender_data[x_axis].values.reshape(-1, 1)
        y = gender_data[y_axis].values
        model = LinearRegression().fit(x, y)
        x_range = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
        y_pred = model.predict(x_range)

        fig.add_trace(go.Scatter(x=x_range.flatten(), y=y_pred, mode='lines',
                                 name=f"{gender} Trendline",
                                 line=dict(color="navy" if gender == "Men's Football" else "#FF6666"),
                                 opacity=1))

    st.plotly_chart(fig)

# Ages Tab
elif page == "Ages":
    st.title("Age-Based Performance")

    min_age, max_age = 17, 43
    age_range = st.slider("Select Age Range (Min & Max should differ):", min_age, max_age, (min_age, max_age))

    if age_range[0] == age_range[1]:
        st.warning("Minimum and Maximum age should be different.")
        st.stop()

    selected_features = st.multiselect("Select 1 to 5 Traits:", quantitative_features,
                                       default=['Pace', 'Stamina', 'Reactions', 'Strength'],
                                       max_selections=5)

    if len(selected_features) < 1:
        st.warning("Please select at least 1 feature.")
        st.stop()

    df['Birthdate'] = pd.to_datetime(df['Birthdate'], errors='coerce')
    df['Age'] = 2024 - df['Birthdate'].dt.year
    df_filtered = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) & (df['Position'] != 'GK')]

    # Grouped mean
    age_means = df_filtered.groupby('Age')[selected_features].mean().reset_index()

    fig = px.line(age_means, x='Age', y=selected_features, title="Changes in Abilities Over Age")
    st.plotly_chart(fig)
