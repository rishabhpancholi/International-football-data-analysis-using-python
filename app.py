# Import necessary libraries
import streamlit as st
import pandas as pd
import helper
import plotly.express as px

# Set Streamlit layout to wide for better use of screen space
st.set_page_config(layout="wide")

# Load the dataset containing match results
results = pd.read_csv('results.csv')

# Sidebar configuration
st.sidebar.title("International Football Data Analysis from 1872 to mid 2024")

# Add an image to the sidebar
st.sidebar.image('https://juicestorm.com/wp-content/uploads/2017/11/international-soccer-ball1-600x430.jpg')

# Sidebar radio menu for navigation between different analysis pages
user_menu = st.sidebar.radio(
    'Select an option',
    ('Results Tally', 'Goal Tally', 'Overall Analysis', 'Country-Wise Analysis')
)

# Instructional text for users
st.write(
    'Choose an option from the menu to get the data analysis regarding matches, goals scored in the entire history of international football'
)

# Function to create a centered header and a red-colored centered title using HTML styling
def centered_header_and_title(header, title):
    st.markdown(f"<h3 style='text-align: center;'>{header}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:red;'>{title}</h1>", unsafe_allow_html=True)


# If the user selects 'Results Tally' from the sidebar menu
if user_menu == 'Results Tally':
    # Display a header in the sidebar
    st.sidebar.header("Results Tally")

    # Preprocess the results DataFrame using a helper function
    results = helper.results_tally(results)

    # Get lists of available years and countries from the dataset
    years, countries = helper.country_year_list(results)

    # Sidebar filters for user selections
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    selected_venue_type = st.sidebar.selectbox("Select Venue Type", ('Overall', 'Neutral', 'Home', 'Away'))
    selected_match_type = st.sidebar.selectbox("Select Match Type", ('Overall', 'Friendly', 'Non Friendly'))

    # Fetch the results tally based on selected filters
    results_tally = helper.fetch_results_tally(results, selected_year, selected_country, selected_venue_type,
                                               selected_match_type)

    # Set dynamic title based on selected filters
    if selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Overall Results Tally")
    elif selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Match Type")
    elif selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Venue Type")
    elif selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Venue Type and Match Type")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Country")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Country and Match Type")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Country and Venue Type")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Country, Venue Type, and Match Type")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year and Match Type")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year and Venue Type")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year, Venue Type, and Match Type")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year and Country")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year, Country, and Match Type")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year, Country, and Venue Type")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year, Country, Venue Type, and Match Type")

    # Convert float columns to int for cleaner display
    results_tally = results_tally.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    # Display the results table
    st.table(results_tally)

# If the user selects 'Goal Tally' from the sidebar menu
if user_menu == 'Goal Tally':
    # Display a header in the sidebar
    st.sidebar.header("Goals Tally")

    # Preprocess the results DataFrame for goal analysis
    results = helper.goals_tally(results)

    # Get updated list of years and countries
    years, countries = helper.country_year_list(results)

    # Sidebar filters for goal tally analysis
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    selected_venue_type = st.sidebar.selectbox("Select Venue Type", ('Overall', 'Neutral', 'Home', 'Away'))
    selected_match_type = st.sidebar.selectbox("Select Match Type", ('Overall', 'Friendly', 'Non Friendly'))

    # Fetch goal tally based on selected filters
    goals_tally = helper.fetch_goals_tally(results, selected_year, selected_country, selected_venue_type,
                                           selected_match_type)

    # Set dynamic title based on filters
    if selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Overall Goals Tally")
    elif selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Match Type")
    elif selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Venue Type")
    elif selected_year == 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Venue Type and Match Type")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Country")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Country and Match Type")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Country and Venue Type")
    elif selected_year == 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Country, Venue Type, and Match Type")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year and Match Type")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year and Venue Type")
    elif selected_year != 'Overall' and selected_country == 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year, Venue Type, and Match Type")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year and Country")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type == 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year, Country, and Match Type")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type == 'Overall':
        st.title("Filtered by Year, Country, and Venue Type")
    elif selected_year != 'Overall' and selected_country != 'Overall' and selected_venue_type != 'Overall' and selected_match_type != 'Overall':
        st.title("Filtered by Year, Country, Venue Type, and Match Type")

    # Convert float columns to int for cleaner display
    goals_tally = goals_tally.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    # Display the goals tally table
    st.table(goals_tally)


if user_menu == 'Overall Analysis':
    results = helper.results_tally_og(results)

    # General stats
    total_matches_played = results.shape[0]
    total_host_cities = results['city'].nunique()
    total_host_countries = results['country'].nunique()

    # Goals related
    total_goals_scored = results['total_goals'].sum()
    no_of_matches_with_zero_goals = results['total_goals'].value_counts().get(0, 0)
    most_goals_in_a_match = results['total_goals'].max()

    # Clean sheets and draws
    no_of_matches_with_clean_sheets = results[(results['away_score'] == 0) | (results['home_score'] == 0)].shape[0]
    no_of_clean_sheets = no_of_matches_with_clean_sheets + no_of_matches_with_zero_goals
    total_matches_draw = results[results['winning_team'] == 'Draw'].shape[0]

    # Venue and type of matches
    total_matches_on_neutral_grounds = results[results['neutral'] == True].shape[0]
    total_friendly_matches = results[results['tournament'] == 'Friendly'].shape[0]

    # Tournament matches count
    total_world_cup_matches = results[results['tournament'] == 'FIFA World Cup'].shape[0]
    total_euro_matches = results[results['tournament'] == 'UEFA Euro'].shape[0]
    total_copa_america_matches = results[results['tournament'] == 'Copa América'].shape[0]

    # Tournament editions
    total_world_cup_editions = results[results['tournament'] == 'FIFA World Cup']['year'].nunique()
    total_euro_editions = results[results['tournament'] == 'UEFA Euro']['year'].nunique()
    total_copa_america_editions = results[results['tournament'] == 'Copa América']['year'].nunique()

    # Goals by tournament
    total_goals_in_world_cups = results[results['tournament'] == 'FIFA World Cup']['total_goals'].sum()
    total_goals_in_euros = results[results['tournament'] == 'UEFA Euro']['total_goals'].sum()
    total_goals_in_copa_americas = results[results['tournament'] == 'Copa América']['total_goals'].sum()

    st.title("Overall Data From 1872 to Mid 2024")

    # Section 1: General Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        centered_header_and_title("Total Football Matches Played", total_matches_played)
    with col2:
        centered_header_and_title("Total Number Of Host Cities", total_host_cities)
    with col3:
        centered_header_and_title("Total Number Of Host Countries", total_host_countries)

    st.header("", divider="red")

    # Section 2: Goals
    col1, col2, col3 = st.columns(3)
    with col1:
        centered_header_and_title("Total Goals Scored", total_goals_scored)
    with col2:
        centered_header_and_title("Matches With Zero Goals", no_of_matches_with_zero_goals)
    with col3:
        centered_header_and_title("Most Goals In A Match", most_goals_in_a_match)

    st.header("", divider="red")

    # Section 3: Clean Sheets & Draws
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        centered_header_and_title("Total Clean Sheets", no_of_clean_sheets)
    with col2:
        centered_header_and_title("Matches Ended In A Draw", total_matches_draw)
    with col3:
        centered_header_and_title("Matches On Neutral Grounds", total_matches_on_neutral_grounds)
    with col4:
        centered_header_and_title("Friendly Matches", total_friendly_matches)

    st.header("", divider="red")

    # Section 4: Tournament Match Counts
    col1, col2, col3 = st.columns(3)
    with col1:
        centered_header_and_title("FIFA World Cup Matches", total_world_cup_matches)
    with col2:
        centered_header_and_title("UEFA Euro Matches", total_euro_matches)
    with col3:
        centered_header_and_title("Copa América Matches", total_copa_america_matches)

    st.header("", divider="red")

    # Section 5: Tournament Editions
    col1, col2, col3 = st.columns(3)
    with col1:
        centered_header_and_title("FIFA World Cup Editions", total_world_cup_editions)
    with col2:
        centered_header_and_title("UEFA Euro Editions", total_euro_editions)
    with col3:
        centered_header_and_title("Copa América Editions", total_copa_america_editions)

    st.header("", divider="red")

    # Section 6: Goals by Tournament
    col1, col2, col3 = st.columns(3)
    with col1:
        centered_header_and_title("Goals In FIFA World Cups", total_goals_in_world_cups)
    with col2:
        centered_header_and_title("Goals In UEFA Euros", total_goals_in_euros)
    with col3:
        centered_header_and_title("Goals In Copa Américas", total_goals_in_copa_americas)

    st.header("", divider="red")

    # Calculate match statistics per year
results_og = helper.results_tally_og(results)
no_of_matches_over_time = helper.football_matches_over_time(results_og)

# Bar chart for number of matches per year
fig = px.bar(no_of_matches_over_time, x='Year', y='Number of Matches')
st.title("Number Of Matches Per Year From 1872 To Mid 2024")
st.plotly_chart(fig)

# Find year with most matches and the count of matches
most_matches_in_an_year = no_of_matches_over_time['Number of Matches'].max()
year_with_most_matches = \
no_of_matches_over_time[no_of_matches_over_time['Number of Matches'] == most_matches_in_an_year]['Year'][0]

# Display statistics in two columns
col1, col2 = st.columns(2)
with col1:
    centered_header_and_title("Year With Most Matches", year_with_most_matches)
with col2:
    centered_header_and_title("Most Matches in an Year", most_matches_in_an_year)

st.header("", divider="red")

# Calculate goal statistics per year
results_og = helper.results_tally_og(results)
no_of_goals_over_time = helper.football_goals_over_time(results_og)

# Bar chart for number of goals per year
fig = px.bar(no_of_goals_over_time, x='Year', y='Number of Goals')
st.title("Number Of Goals Per Year From 1872 To Mid 2024")
st.plotly_chart(fig)

# Find year with most goals and the count
most_goals_in_an_year = no_of_goals_over_time['Number of Goals'].max()
year_with_most_goals = \
no_of_goals_over_time[no_of_goals_over_time['Number of Goals'] == most_goals_in_an_year].reset_index()['Year'][0]

# Display statistics in two columns
col1, col2 = st.columns(2)
with col1:
    centered_header_and_title("Year With Most Goals", year_with_most_goals)
with col2:
    centered_header_and_title("Most Goals in an Year", most_goals_in_an_year)

st.header("", divider="red")

# Country-wise analysis section
if user_menu == 'Country-Wise Analysis':
    # Prepare goals data and get year-country dropdown values
    results = helper.goals_tally(results)
    years, countries = helper.country_year_list(results)

    # Dropdown for selecting country
    selected_country = st.sidebar.selectbox("Select Country", countries)

    if selected_country == 'Overall':
        # Line chart for overall goals scored over the years
        overall_df = helper.overall_yearwise_goal_tally(results)
        overall_df = overall_df.rename(columns={'year': 'Year', 'total_goals': 'Number Of Goals'})
        fig = px.line(overall_df, x='Year', y='Number Of Goals')
        st.title("Overall Goals Scored Chart From 1872 To Mid 2024")
        st.plotly_chart(fig)
        st.header("", divider="red")

        # (Optional) Plot for goals conceded (commented out)
        # overall_df_ = helper.overall_yearwise_goal_tally(results)
        # overall_df_ = overall_df_.rename(columns={'year': 'Year', 'total_goals_conceded': 'Number Of Goals Conceded'})
        # fig_ = px.line(overall_df_, x='Year', y='Number Of Goals Conceded')
        # st.title("Overall Goals Conceded Chart From 1872 To Mid 2024")
        # st.plotly_chart(fig_)
    
    else:
        # Line chart for selected country's goals scored per year
        country_df = helper.yearwise_goal_tally(results, selected_country)
        country_df = country_df.rename(columns={'year': 'Year', 'total_goals': 'Number Of Goals'})
        fig = px.line(country_df, x='Year', y='Number Of Goals')
        st.title(f"Country-Wise Goals Scored Chart From 1872 To Mid 2024 for {selected_country}")
        st.plotly_chart(fig)

        # Display year and count with most goals scored
        most_goals_in_an_year = country_df['Number Of Goals'].max()
        year_with_most_goals = \
            country_df[country_df['Number Of Goals'] == most_goals_in_an_year].reset_index()['Year'][0]
        col1, col2 = st.columns(2)
        with col1:
            centered_header_and_title("Year With Most Goals", year_with_most_goals)
        with col2:
            centered_header_and_title("Most Goals in an Year", most_goals_in_an_year)
        st.header("", divider="red")

        # Line chart for goals conceded per year for selected country
        country_df_ = helper.yearwise_concede_tally(results, selected_country)
        country_df_ = country_df_.rename(columns={'year': 'Year', 'total_goals_conceded': 'Number Of Goals Conceded'})
        fig_ = px.line(country_df_, x='Year', y='Number Of Goals Conceded')
        st.title(f"Country-Wise Goals Conceded Chart From 1872 To Mid 2024 for {selected_country}")
        st.plotly_chart(fig_)

        # Display year and count with most goals conceded
        most_goals_in_an_year_ = country_df_['Number Of Goals Conceded'].max()
        year_with_most_goals_ = \
            country_df_[country_df_['Number Of Goals Conceded'] == most_goals_in_an_year_].reset_index()['Year'][0]
        col1, col2 = st.columns(2)
        with col1:
            centered_header_and_title("Year With Most Goals Conceded", year_with_most_goals_)
        with col2:
            centered_header_and_title("Most Goals Conceded in an Year", most_goals_in_an_year_)
        st.header("", divider="red")

        # Display top 5 countries this team has scored the most against
        top_five_goals_opp = helper.goals_scored_opp(results, selected_country)
        top_five_goals_conceded_opp = helper.goals_conceded_opp(results, selected_country)
        st.title(f"Top 5 Countries {selected_country} has scored against")
        for name in top_five_goals_opp['country'][0:5]:
            no_of_goals = top_five_goals_opp[top_five_goals_opp['country']==name]['goals_scored'].iloc[0]
            st.markdown(f"<h1 style='color:red;'>{name}</h1> <h3>{no_of_goals} goals</h3>", unsafe_allow_html=True)

        st.header("", divider="red")

        # Bar chart for top 5 scoring opponents
        top_five_goals_opp.rename(columns={'country':'Country','goals_scored':'Number Of Goals Scored'}, inplace=True)
        fig_ = px.bar(top_five_goals_opp, x='Country', y='Number Of Goals Scored')
        st.title(f"Country-Wise Goals Scored Bar Chart From 1872 To Mid 2024 for {selected_country}")
        st.plotly_chart(fig_)

        st.header("", divider="red")

        # Display top 5 countries this team has conceded the most against
        st.title(f"Top 5 Countries {selected_country} has conceded against")
        for name in top_five_goals_conceded_opp['country'][0:5]:
            no_of_goals = top_five_goals_conceded_opp[top_five_goals_conceded_opp['country']==name]['goals_conceded'].iloc[0]
            st.markdown(f"<h1 style='color:red;'>{name}</h1> <h3>{no_of_goals} goals</h3>", unsafe_allow_html=True)

        st.header("", divider="red")

        # Bar chart for top 5 conceding opponents
        top_five_goals_conceded_opp.rename(columns={'country': 'Country', 'goals_conceded': 'Number Of Goals Conceded'}, inplace=True)
        fig_ = px.bar(top_five_goals_conceded_opp, x='Country', y='Number Of Goals Conceded')
        st.title(f"Country-Wise Goals Conceded Bar Chart From 1872 To Mid 2024 for {selected_country}")
        st.plotly_chart(fig_)
