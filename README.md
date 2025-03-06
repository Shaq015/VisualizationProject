# EA FC 25 Visualization Project - Reflecting Stereotypes in Football

This project analyzes player attributes from the EA FC 25 game to explore whether they reflect or reinforce stereotypes related to ethnicity, gender, and age. 

## Project Goals
The dashboard aims to answer:
- Do African players receive higher ratings in physical attributes, reinforcing stereotypes about athleticism?
- Are male players rated more aggressive and female players more composed, reflecting gender-based perceptions?
- How do player abilities change with age, and do older players systematically lose physical capabilities?

## Dashboard Structure
The dashboard consists of 3 main sections:
1. **Africa - Regional Physical Abilities:** Compare physical abilities (e.g., Pace, Strength, Stamina) across players from North Africa, Rest of Africa, and Rest of the World.
2. **Men vs Women - Gendered Attributes:** Analyze differences between male and female players across key attributes (e.g., Composure, Aggression) and allow comparisons within major leagues.
3. **Ages - Age-Based Performance:** Track changes in physical abilities (e.g., Pace, Reactions) across different player ages.

## Data Files
- `ea_sports_fc_player_ratings.csv`: Contains all player ratings and metadata.
- `Table no goalkeepers with age.csv`: Processed dataset used in the age analysis.

## Technologies Used
- Python
- Python Libraries: Streamlit, Plotly, Seaborn, Matplotlib, Pandas, Scikit-learn, Numpy

## Running the Dashboard
### Local (for development)
Run:
```bash
streamlit run streamlit_dashboard.py
