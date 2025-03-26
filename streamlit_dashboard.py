import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# Medium-width layout (slightly narrower than full)
st.set_page_config(layout="centered")

# Load dataset
main_data_path = "ea_sports_fc_player_ratings.csv"
df = pd.read_csv(main_data_path)

# Quantitative features
quantitative_features = [
    'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical', 'Acceleration', 'Agility',
    'Jumping', 'Stamina', 'Strength', 'Aggression', 'Balance', 'Ball Control', 'Composure',
    'Crossing', 'Curve', 'Defensive Awareness', 'Finishing', 'Free Kick Accuracy', 'GK Diving',
    'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy', 'Interceptions',
    'Long Passing', 'Long Shots', 'Penalties', 'Positioning', 'Reactions', 'Short Passing',
    'Shot Power', 'Sliding Tackle', 'Sprint Speed', 'Standing Tackle', 'Vision', 'Volleys'
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
# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a Page", ["Home", "Africa", "Men vs Women", "Ages"])

if page == "Home":
    st.title("Reflecting Stereotypes in Football Using EA FC 25 Data")
    st.write("""
    ### Introduction
    This dashboard explores how player attributes in EA FC 25 may reflect or reinforce stereotypes based on ethnicity, gender, and age.

    ---
    ### Dashboard Overview
    1. **Africa - Regional Physical Abilities**
    2. **Men vs Women - Gendered Attributes**
    3. **Ages - Age-Based Performance**
    """)


# -------------Africa-----------
elif page == "Africa":
    st.title("Regional Physical Abilities")

    df['region'] = df['Nation'].apply(
        lambda x: 'North Africa' if x in ['Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Mauritania', 'Sudan']
        else ('Rest of Africa' if x in ['Nigeria', 'Senegal', 'Ghana', 'Cameroon'] else 'Rest of World'))

    all_options = quantitative_features[:]
    selected_features = st.multiselect("Select Feature:", ['All'] + all_options,
                                       default=['Pace', 'Stamina', 'Strength', 'Aggression'])

    if 'All' in selected_features and len(selected_features) > 1:
        st.error(
            "You cannot select 'All' and other features at the same time. Please choose either 'All' or specific features.")
        st.stop()

    if 'All' in selected_features:
        selected_features = all_options

    if not selected_features:
        st.warning("Please select at least 1 feature.")
        st.stop()

    region_means = df.groupby('region')[selected_features].mean().reset_index()

    region_colors = {
        'North Africa': '#0705e7',
        'Rest of Africa': '#ff6600',
        'Rest of World': '#4CBB17'
    }

    fig = go.Figure()
    for region in region_means['region']:
        values = region_means[region_means['region'] == region][selected_features].values.flatten()
        fig.add_trace(go.Bar(
            x=selected_features,
            y=values,
            name=region,
            text=np.round(values, 1),
            textposition='outside',
            textfont=dict(color='black'),
            marker_color=region_colors.get(region, '#7f7f7f'),
            hovertemplate=(
                    '<span style="color:black !important;"><b>Continent Category:</b></span> ' + region + '<br>' +
                    '<span style="color:black !important;"><b>Feature:</b></span> %{x}<br>' +
                    '<span style="color:black !important;"><b>Average Rating:</b></span> %{y}<extra></extra>'
            )
        ))

    fig.update_layout(
        barmode='group',
        yaxis_title=dict(
            text="<b>Average Rating</b>",
            font=dict(size=16, color="black")
        ),
        xaxis_title=dict(
            text="<b>Feature</b>",
            font=dict(size=16, color="black")
        ),
        font=dict(size=14),
        yaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=14, color='black')),
        legend=dict(
            title=dict(
                text="<b>Continent Category:</b>",
                font=dict(size=12, color="black")
            ),
            orientation="h",
            title_side="left",
            yanchor="bottom",
            y=1.00,
            xanchor="center",
            x=0.5
        ),
        title=dict(text="Average Feature by Region", y=1.00, x=0, xanchor='left', yanchor='top')
    )
    st.plotly_chart(fig)

    st.markdown("""
    ### Explanation:
    This graph shows the average values of selected physical features for players from different regions — specifically, North Africa, other parts of Africa, and the rest of the world. It allows comparison of how physical attributes such as pace, stamina, strength, and aggression differ across geographic groups.
    
    **Insights:** Players from central and southern parts of Africa tend to have slightly higher average ratings in strength and aggression, while players from North Africa show higher values in pace. These patterns may reflect trends in data collection, scouting, or representation within football databases. Players from central and southern parts of Africa tend to have slightly higher average ratings in strength and aggression, while players from North Africa show higher values in pace. These patterns may reflect trends in data collection, scouting, or representation within football databases.
    """)

    st.markdown("""
    ### How to use
    Use the feature selector to compare physical characteristics across regions. North and Sub-Saharan Africa show different strengths. Try comparing fewer attributes for clarity.
    """)



# ---------Men vs Women----------
elif page == "Men vs Women":
    st.title("Gender-Based Attributes Analysis")

    # Step 1: Gender filter
    gender_filter = st.selectbox("Filter by Gender:", ["All", "Men", "Women"], index=0)

    # Step 2: Prepare DataFrames
    df_men = df[df['Gender'] == "Men's Football"].copy()
    df_women = df[df['Gender'] == "Women's Football"].copy()
    df_men['League_Nation'] = df_men['Team'].apply(map_league_men)
    df_women['League_Nation'] = df_women['Team'].apply(map_league_women)
    df_combined = pd.concat([df_men, df_women], ignore_index=True)

    # Step 3: Get league options based on gender
    if gender_filter == "Men":
        league_options = ['All'] + sorted(df_men['League_Nation'].unique().tolist())
        filtered_df = df_men.copy()
    elif gender_filter == "Women":
        league_options = ['All'] + sorted(df_women['League_Nation'].unique().tolist())
        filtered_df = df_women.copy()
    else:
        league_options = ['All'] + sorted(df_combined['League_Nation'].unique().tolist())
        filtered_df = df_combined.copy()

    # Step 4: Use session_state to preserve selected leagues
    if 'selected_leagues' not in st.session_state:
        st.session_state.selected_leagues = ['Germany']  # default league on first load

    # Clean the saved selection in case it no longer exists in new options
    valid_leagues = [l for l in st.session_state.selected_leagues if l in league_options]
    if not valid_leagues:
        valid_leagues = ['All']  # fallback default

    # Step 5: Leagues multiselect
    selected_leagues = st.multiselect("Select Leagues:", league_options, default=valid_leagues)
    st.session_state.selected_leagues = selected_leagues

    # Step 6: Prevent "All" with others
    if 'All' in selected_leagues and len(selected_leagues) > 1:
        st.error(
            "You cannot select 'All' and other leagues at the same time. Please choose either 'All' or specific leagues.")
        st.stop()

    # Step 7: Filter by league
    if 'All' not in selected_leagues:
        filtered_df = filtered_df[filtered_df['League_Nation'].isin(selected_leagues)]

    gk_only_features = ['GK Diving', 'GK Reflexes', 'GK Handling', 'GK Kicking', 'GK Positioning']
    quantitative_features_non_gk = [feat for feat in quantitative_features if feat not in gk_only_features]

    x_axis = st.selectbox("Select X-axis Attribute:", quantitative_features_non_gk, index=quantitative_features_non_gk.index('Aggression'))
    y_axis = st.selectbox("Select Y-axis Attribute:", quantitative_features_non_gk, index=quantitative_features_non_gk.index('Composure'))

    hover_cols = ['Gender', 'Name', 'Team']
    filtered_df['customdata'] = filtered_df[hover_cols].values.tolist()

    hovertemplate = (
        f'<span style="color:black !important;"><b>{x_axis}:</b></span> %{{x}}<br>' +
        f'<span style="color:black !important;"><b>{y_axis}:</b></span> %{{y}}<br>'
    )
    for i, col in enumerate(hover_cols):
        hovertemplate += f'<span style="color:black !important;"><b>{col}:</b></span> %{{customdata[{i}]}}<br>'
    hovertemplate += '<extra></extra>'

    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color='Gender',
        hover_data=hover_cols,
        color_discrete_map={"Men's Football": "#3200ff", "Women's Football": "#fa00ff"}
    )

    fig.update_traces(hovertemplate=hovertemplate)

    for gender in filtered_df['Gender'].unique():
        data = filtered_df[filtered_df['Gender'] == gender]
        x = data[x_axis].values.reshape(-1, 1)
        y = data[y_axis].values
        model = LinearRegression().fit(x, y)
        x_range = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
        y_pred = model.predict(x_range)

        line_color = "#3200ff" if gender == "Men's Football" else "#fa00ff"

        fig.add_trace(go.Scatter(
            x=x_range.flatten(),
            y=y_pred,
            mode='lines',
            name=f"{gender} Trendline",
            line=dict(width=2, color=line_color),
            hovertemplate=(
                    f'<span style="color:black !important;"><b>{x_axis}:</b></span> %{{x}}<br>' +
                    f'<span style="color:black !important;"><b>{y_axis}:</b></span> %{{y}}<br>' +
                    f'<span style="color:black !important;"><b>Gender:</b></span> {gender}<extra></extra>'
            )
        ))

    fig.update_layout(
        xaxis_title=dict(
            text=f"<b>{x_axis}</b>",
            font=dict(size=16, color="black")
        ),
        yaxis_title=dict(
            text=f"<b>{y_axis}</b>",
            font=dict(size=16, color="black")
        ),
        font=dict(size=14),
        yaxis=dict(range=[0, 100], showgrid=False),
        xaxis=dict(showgrid=False),
        legend=dict(
            title=dict(
                text="<b>Gender:</b>",
                font=dict(size=12, color="black")
            ),
            orientation="h",
            title_side="left",
            yanchor="bottom",
            y=1.00,
            xanchor="center",
            x=0.5,
            font=dict(size=11.5)
        ),
        title=dict(text=f"{x_axis} vs {y_axis} by Gender", y=1.00, x=0, xanchor='left', yanchor='top')
    )
    st.plotly_chart(fig)

    st.markdown("""
    ### Explanation:
    This scatter plot compares any two attributes by gender and league. Trendlines highlight overall patterns in male and female footballers.

    **Insights:** You might notice that certain attributes (like aggression or composure) trend differently by gender.
    """)

    st.markdown("""
    ### How to use
    Explore differences in player attributes across genders and leagues. Use the trendlines to identify overall tendencies.
    """)


# ---------Ages----------
elif page == "Ages":
    st.title("Age-Based Performance")
    df['Birthdate'] = pd.to_datetime(df['Birthdate'], errors='coerce')
    df['Age'] = 2024 - df['Birthdate'].dt.year

    age_range = st.slider("Select Age Range:", 17, 43, (17, 43))
    df_age = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

    filtered_features = [f for f in quantitative_features if 'GK ' not in f]

    selected_features = st.multiselect("Select features:", ['All'] + filtered_features,
                                       default=['Pace', 'Stamina', 'Reactions', 'Strength'])

    if 'All' in selected_features and len(selected_features) > 1:
        st.error(
            "You cannot select 'All' and other features at the same time. Please choose either 'All' or specific features.")
        st.stop()

    if 'All' in selected_features:
        selected_features = filtered_features

    if not selected_features:
        st.warning("Please select at least one feature.")
        st.stop()

    age_means = df_age.groupby('Age')[selected_features].mean().reset_index()

    import itertools

    custom_palette = [
        "#0705e7",  # blue
        "#ff6600",  # valencia orange
        "#4CBB17",  # green
        "#ff5850",  # red
        "#9467bd",  # purple
        "#8c564b",  # brown
        "#e377c2",  # pink
        "#7f7f7f",  # gray
        "#bcbd22",  # lime
        "#17becf",  # cyan
        "#393b79",  # dark blue
        "#637939",  # olive green
        "#8c6d31",  # ochre
        "#843c39",  # brick red
        "#7b4173",  # plum
        "#17a398",  # teal
        "#ff6347",  # tomato red
        "#00ced1",  # dark turquoise
        "#6a5acd",  # slate blue
        "#32cd32",  # lime green
        "#ff69b4",  # hot pink
        "#ffa500",  # pure orange
        "#4682b4",  # steel blue
        "#9acd32",  # yellow green
        "#dc143c",  # crimson
        "#00fa9a",  # medium spring green
        "#ff1493",  # deep pink
        "#a52a2a",  # brown
        "#5f9ea0",  # cadet blue
        "#9932cc",  # dark orchid
    ]

    color_discrete_map = dict(zip(selected_features, itertools.cycle(custom_palette)))

    fig = px.line(age_means, x='Age', y=selected_features, color_discrete_map=color_discrete_map)
    for i, feature in enumerate(selected_features):
        fig.data[i].hovertemplate = (
                '<span style="color:black !important;"><b>Feature:</b></span> ' + feature + '<br>' +
                '<span style="color:black !important;"><b>Age:</b></span> %{x}<br>' +
                '<span style="color:black !important;"><b>Average Rating:</b></span> %{y}<extra></extra>'
        )

    fig.update_layout(
        xaxis_title=dict(
            text="<b>Age</b>",
            font=dict(size=16, color="black")
        ),
        yaxis_title=dict(
            text="<b>Average Rating</b>",
            font=dict(size=16, color="black")
        ),
        font=dict(
            size=16,
            color="black"
        ),
        yaxis=dict(range=[0, 100], showgrid=False),
        xaxis=dict(showgrid=False),
        legend=dict(
            title=dict(
                text="<b>Feature:</b>",
                font=dict(size=12, color="black")
            ),
            orientation="h",
            title_side="left",
            yanchor="bottom",
            y=1.00,
            xanchor="center",
            x=0.5
        ),
        title=dict(text="Changes in Abilities Over Age", y=1.00, x=0, xanchor='left', yanchor='top')
    )
    st.plotly_chart(fig)

    st.markdown("""
    ### Explanation:
    This line chart illustrates how different player abilities evolve with age. It focuses on non-goalkeepers and tracks selected attributes over a user-defined age range.

    **Insights:** Physical abilities such as pace and stamina tend to decline as age increases, while features like reactions may remain stable or improve.
    """)

    st.markdown("""
    ### How to use
    Examine how physical and mental features evolve with player age. Filter the range to identify age peaks for different abilities.
    """)

