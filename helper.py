import pandas as pd
import numpy as np

# Read the dataset containing football match results
results = pd.read_csv('results.csv')

# Function to generate a basic tally of results without altering the tournament column
def results_tally_og(results):
    # Determine the winning team: if home score > away score, home team wins; vice versa; else it's a draw
    results['winning_team'] = results.apply(
        lambda row: row['home_team'] if row['home_score'] > row['away_score']
        else row['away_team'] if row['away_score'] > row['home_score']
        else np.nan, axis=1
    )

    # Determine the losing team similarly
    results['losing_team'] = results.apply(
        lambda row: row['home_team'] if row['away_score'] > row['home_score']
        else row['away_team'] if row['home_score'] > row['away_score']
        else np.nan, axis=1
    )

    # Replace NaNs with 'Draw' for matches that ended in a draw
    results = results.fillna('Draw')

    # Calculate total goals scored in each match
    results['total_goals'] = results['home_score'].fillna(0) + results['away_score'].fillna(0)

    # Extract the year from the date column
    results['year'] = results['date'].apply(get_year)

    return results

# Function to generate a results tally and classify tournaments into 'Friendly' or 'Non Friendly'
def results_tally(results):

    # Determine the winning team using same logic as above
    results['winning_team'] = results.apply(
        lambda row: row['home_team'] if row['home_score'] > row['away_score']
        else row['away_team'] if row['away_score'] > row['home_score']
        else np.nan, axis=1
    )

    # Determine the losing team
    results['losing_team'] = results.apply(
        lambda row: row['home_team'] if row['away_score'] > row['home_score']
        else row['away_team'] if row['home_score'] > row['away_score']
        else np.nan, axis=1
    )

    # Replace NaNs with 'Draw' to handle draws
    results = results.fillna('Draw')

    # Calculate total goals for each match
    results['total_goals'] = results['home_score'].fillna(0) + results['away_score'].fillna(0)

    # Extract year from the date for time-based analysis
    results['year'] = results['date'].apply(get_year)

    # Classify tournaments as either 'Friendly' or 'Non Friendly'
    results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

    return results

def overall_results_tally(results, venue, country):
        # Extract the year from the date column
        results['year'] = results['date'].apply(get_year)

        # Identify winning team for each match
        results['winning_team'] = results.apply(
          lambda row: row['home_team'] if row['home_score'] > row['away_score']
          else row['away_team'] if row['away_score'] > row['home_score']
          else np.nan, axis=1
       )

        # Identify losing team for each match
        results['losing_team'] = results.apply(
          lambda row: row['home_team'] if row['away_score'] > row['home_score']
          else row['away_team'] if row['home_score'] > row['away_score']
          else np.nan, axis=1
        )

        # Replace NaNs (draws) with 'Draw'
        results = results.fillna('Draw')

        # Categorize tournaments into Friendly or Non Friendly
        results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

        # Create separate DataFrames for wins and losses excluding draws
        win_df = results
        lose_df = results

        win_df = win_df[win_df['winning_team'] != 'Draw']
        lose_df = lose_df[lose_df['losing_team'] != 'Draw']

        # Count number of wins and losses per country
        win_counts = win_df['winning_team'].value_counts().reset_index()
        win_counts.columns = ['country', 'win_count']

        lose_counts = lose_df['losing_team'].value_counts().reset_index()
        lose_counts.columns = ['country', 'lose_count']

        # Create DataFrame for draw counts (from both home and away perspectives)
        draw_df = results
        draw_df = draw_df[draw_df['winning_team'] == 'Draw']

        home_draw_counts = draw_df['home_team'].value_counts().reset_index()
        home_draw_counts.columns = ['country', 'draw_count']
        away_draw_counts = draw_df['away_team'].value_counts().reset_index()
        away_draw_counts.columns = ['country', 'draw_count']

        # Combine home and away draw counts
        total_draw_counts = pd.concat([home_draw_counts, away_draw_counts]).groupby('country').sum().reset_index()

        # Combine win and loss counts
        win_lose_draw_tally = pd.concat([win_counts, lose_counts]).groupby('country').sum().reset_index()

        # Combine total draw counts with win/loss counts
        results_tally = pd.concat([win_lose_draw_tally, total_draw_counts]).groupby('country').sum().reset_index()

        # Sort based on win count
        results_tally = results_tally.sort_values('win_count', ascending=False).reset_index()

        # Remove unnecessary index column
        results_tally = results_tally.drop(['index'], axis=1)

        # Get neutral matches only
        neutral_results = results[results['neutral'] == True]

        # Filter out non-draw matches in neutral games
        neutral_wins_losses = neutral_results[neutral_results['winning_team'] != 'Draw']

        # Count neutral match wins and losses
        neutral_win_df = neutral_wins_losses['winning_team'].value_counts().reset_index()
        neutral_win_df.columns = ['country', 'win_count']
        neutral_lose_df = neutral_wins_losses['losing_team'].value_counts().reset_index()
        neutral_lose_df.columns = ['country', 'lose_count']

        # Combine neutral match win/loss counts
        neutral_results_tally = pd.concat([neutral_win_df, neutral_lose_df]).groupby('country').sum().reset_index()

        # Filter draws in neutral matches
        neutral_draws = neutral_results[neutral_results['winning_team'] == 'Draw']

        # Count home/away team draws in neutral matches
        neutral_results_home_draws = neutral_draws['home_team'].value_counts().reset_index()
        neutral_results_away_draws = neutral_draws['away_team'].value_counts().reset_index()
        neutral_results_home_draws.columns = ['country', 'draw_count']
        neutral_results_away_draws.columns = ['country', 'draw_count']

        # Combine neutral draw counts
        neutral_draws_df = pd.concat([neutral_results_home_draws, neutral_results_away_draws]).groupby(
            'country').sum().reset_index()

        # Finalize neutral results tally
        neutral_results_tally = pd.concat([neutral_results_tally, neutral_draws_df]).groupby(
            'country').sum().reset_index()
        neutral_results_tally = neutral_results_tally.sort_values('win_count', ascending=False).reset_index()

        neutral_results_tally = neutral_results_tally.drop(['index'], axis=1)

        # Get non-neutral (home/away) matches
        non_neutral_results = results[results['neutral'] == False]

        # Identify home and away wins
        non_neutral_home_wins = non_neutral_results[
            non_neutral_results['home_team'] == non_neutral_results['winning_team']]
        non_neutral_away_wins = non_neutral_results[
            non_neutral_results['away_team'] == non_neutral_results['winning_team']]

        # Count home and away wins
        home_wins_df = non_neutral_home_wins['winning_team'].value_counts().reset_index()
        home_wins_df.columns = ['country', 'win_count']
        away_wins_df = non_neutral_away_wins['winning_team'].value_counts().reset_index()
        away_wins_df.columns = ['country', 'win_count']

        # Identify home and away losses
        non_neutral_home_losses = non_neutral_results[
            non_neutral_results['away_team'] == non_neutral_results['winning_team']]
        non_neutral_away_losses = non_neutral_results[
            non_neutral_results['home_team'] == non_neutral_results['winning_team']]

        # Count home and away losses
        home_losses_df = non_neutral_home_losses['losing_team'].value_counts().reset_index()
        home_losses_df.columns = ['country', 'lose_count']
        away_losses_df = non_neutral_away_losses['losing_team'].value_counts().reset_index()
        away_losses_df.columns = ['country', 'lose_count']

        # Identify draws in non-neutral games
        non_neutral_draws = non_neutral_results[non_neutral_results['winning_team'] == 'Draw']

        home_draws_df = non_neutral_draws['home_team'].value_counts().reset_index()
        away_draws_df = non_neutral_draws['away_team'].value_counts().reset_index()
        home_draws_df.columns = ['country', 'draw_count']
        away_draws_df.columns = ['country', 'draw_count']

        # Combine home results
        home_results_tally = pd.concat([home_wins_df, home_losses_df]).groupby('country').sum().reset_index()
        home_results_tally = pd.concat([home_results_tally, home_draws_df]).groupby('country').sum().reset_index()

        # Combine away results
        away_results_tally = pd.concat([away_wins_df, away_losses_df]).groupby('country').sum().reset_index()
        away_results_tally = pd.concat([away_results_tally, away_draws_df]).groupby('country').sum().reset_index()

        # Finalize home and away tallies
        home_results_tally = home_results_tally.sort_values('win_count', ascending=False).reset_index(drop=True)
        home_results_tally = home_results_tally.drop(columns=['index', 'level_0'], errors='ignore')

        away_results_tally = away_results_tally.sort_values('win_count', ascending=False).reset_index(drop=True)
        away_results_tally = away_results_tally.drop(columns=['index', 'level_0'], errors='ignore')

        # Choose the appropriate result based on selected venue
        if venue == 'Overall':
         overall_results_tally = results_tally
        elif venue == 'Neutral':
         overall_results_tally = neutral_results_tally
        elif venue == 'Away':
         overall_results_tally = away_results_tally
        elif venue == 'Home':
         overall_results_tally = home_results_tally

        # Rename columns and calculate total matches
        overall_results_tally.columns = ['country', 'win_count', 'lose_count', 'draw_count']
        overall_results_tally['total_matches_count'] = overall_results_tally['win_count'] + overall_results_tally['lose_count'] + overall_results_tally['draw_count']
        overall_results_tally = overall_results_tally.fillna(0)
        overall_results_tally = overall_results_tally.sort_values('win_count', ascending=False).reset_index()

        # Filter for a specific country if requested
        if country != 'Overall':
            overall_results_tally = overall_results_tally[overall_results_tally['country'] == country]

        # Drop index column before returning
        overall_results_tally.drop(columns=['index'], inplace=True)
        return overall_results_tally



def overall_goals_tally(results, venue, country):
        # Extract year from the date column
        results['year'] = results['date'].apply(get_year)

        # Fill missing results with 'Draw'
        results = results.fillna('Draw')

        # Mark tournament type as either Friendly or Non Friendly
        results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

        # Filter out matches played at non-neutral venues
        non_neutral_results_df = results[results['neutral'] == False]

        # Total home goals scored by each country (non-neutral matches)
        home_goals_df = non_neutral_results_df.groupby('home_team')['home_score'].sum().reset_index().sort_values(
            'home_score', ascending=False)
        home_goals_df.rename(columns={'home_team': 'country', 'home_score': 'home_goals_scored'}, inplace=True)

        # Total goals conceded at home by each country (non-neutral matches)
        home_goals_conceded_df = non_neutral_results_df.groupby('home_team')[
            'away_score'].sum().reset_index().sort_values('away_score', ascending=False)
        home_goals_conceded_df.rename(columns={'home_team': 'country', 'away_score': 'home_goals_conceded'},
                                      inplace=True)

        # Total away goals scored by each country (non-neutral matches)
        away_goals_df = non_neutral_results_df.groupby('away_team')['away_score'].sum().reset_index().sort_values(
            'away_score', ascending=False)
        away_goals_df.rename(columns={'away_team': 'country', 'away_score': 'away_goals_scored'}, inplace=True)

        # Total goals conceded in away games (non-neutral matches)
        away_goals_conceded_df = non_neutral_results_df.groupby('away_team')[
            'home_score'].sum().reset_index().sort_values('home_score', ascending=False)
        away_goals_conceded_df.rename(columns={'away_team': 'country', 'home_score': 'away_goals_conceded'},
                                      inplace=True)

        # Filter matches played on neutral venues
        neutral_results_df = results[results['neutral'] == True]

        # Goals scored as 'home team' on neutral grounds
        neutral_home_goals_df = neutral_results_df.groupby('home_team')['home_score'].sum().reset_index().sort_values(
            'home_score', ascending=False)
        neutral_home_goals_df.rename(columns={'home_team': 'country', 'home_score': 'neutral_home_goals_scored'},
                                     inplace=True)

        # Goals conceded as 'home team' on neutral grounds
        neutral_home_goals_conceded_df = neutral_results_df.groupby('home_team')[
            'away_score'].sum().reset_index().sort_values('away_score', ascending=False)
        neutral_home_goals_conceded_df.rename(
            columns={'home_team': 'country', 'away_score': 'neutral_home_goals_conceded'}, inplace=True)

        # Goals scored as 'away team' on neutral grounds
        neutral_away_goals_df = neutral_results_df.groupby('away_team')['away_score'].sum().reset_index().sort_values(
            'away_score', ascending=False)
        neutral_away_goals_df.rename(columns={'away_team': 'country', 'away_score': 'neutral_away_goals_scored'},
                                     inplace=True)

        # Goals conceded as 'away team' on neutral grounds
        neutral_away_goals_conceded_df = neutral_results_df.groupby('away_team')[
            'home_score'].sum().reset_index().sort_values('home_score', ascending=False)
        neutral_away_goals_conceded_df.rename(
            columns={'away_team': 'country', 'home_score': 'neutral_away_goals_conceded'}, inplace=True)

        # Combine neutral home and away goal data to get total neutral goals scored
        neutral_total_goals_df = pd.concat([neutral_home_goals_df, neutral_away_goals_df]).groupby(
            'country').sum().reset_index()
        neutral_total_goals_df['neutral_goals_scored'] = neutral_total_goals_df['neutral_home_goals_scored'] + \
                                                         neutral_total_goals_df['neutral_away_goals_scored']
        neutral_total_goals_df.drop(columns=['neutral_home_goals_scored', 'neutral_away_goals_scored'], inplace=True)

        # Combine neutral home and away goals conceded to get total neutral goals conceded
        neutral_total_goals_conceded_df = pd.concat(
            [neutral_home_goals_conceded_df, neutral_away_goals_conceded_df]).groupby('country').sum().reset_index()
        neutral_total_goals_conceded_df['neutral_goals_conceded'] = neutral_total_goals_conceded_df[
                                                                        'neutral_home_goals_conceded'] + \
                                                                    neutral_total_goals_conceded_df[
                                                                        'neutral_away_goals_conceded']
        neutral_total_goals_conceded_df.drop(columns=['neutral_home_goals_conceded', 'neutral_away_goals_conceded'],
                                             inplace=True)

        # Combine home and away goal data to get total goals scored
        total_goals_df = pd.concat([home_goals_df, away_goals_df]).groupby('country').sum().reset_index()
        total_goals_df['total_goals_scored'] = total_goals_df['home_goals_scored'] + total_goals_df['away_goals_scored']

        # Combine home and away goals conceded to get total goals conceded
        total_goals_conceded_df = pd.concat([home_goals_conceded_df, away_goals_conceded_df]).groupby(
            'country').sum().reset_index()
        total_goals_conceded_df['total_goals_conceded'] = total_goals_conceded_df['home_goals_conceded'] + \
                                                          total_goals_conceded_df['away_goals_conceded']

        # Add neutral goals to total goals scored
        total_goals_df = pd.concat([total_goals_df, neutral_total_goals_df]).groupby('country').sum().reset_index()
        total_goals_df['total_goals_scored'] += total_goals_df['neutral_goals_scored']
        total_goals_df.drop(columns=['home_goals_scored', 'away_goals_scored', 'neutral_goals_scored'], inplace=True)

        # Add neutral goals to total goals conceded
        total_goals_conceded_df = pd.concat([total_goals_conceded_df, neutral_total_goals_conceded_df]).groupby(
            'country').sum().reset_index()
        total_goals_conceded_df['total_goals_conceded'] += total_goals_conceded_df['neutral_goals_conceded']
        total_goals_conceded_df.drop(columns=['home_goals_conceded', 'away_goals_conceded', 'neutral_goals_conceded'],
                                     inplace=True)

        # Merge total goals scored and conceded into a single DataFrame
        total_df = pd.merge(total_goals_df, total_goals_conceded_df, on='country')

        # Select venue-specific DataFrame to return
        if venue == 'Overall':
            overall_goals_tally = total_df
        elif venue == 'Neutral':
            overall_goals_tally = neutral_total_goals_df
        elif venue == 'Away':
            overall_goals_tally = away_goals_df
        elif venue == 'Home':
            overall_goals_tally = home_goals_df

        # Replace NaN values with 0 and sort by goals scored
        overall_goals_tally = overall_goals_tally.fillna(0)
        overall_goals_tally = overall_goals_tally.sort_values('total_goals_scored', ascending=False).reset_index()

        # Filter for specific country if given
        if country != 'Overall':
            overall_goals_tally = overall_goals_tally[overall_goals_tally['country'] == country]

        # Remove the extra index column
        overall_goals_tally.drop(columns=['index'], inplace=True)

        # Return the final DataFrame
        return overall_goals_tally

# Function to calculate total goals and process the results dataframe
def goals_tally(results):
    # Fill missing values in 'results' dataframe with 'Draw' for missing game outcomes
    results = results.fillna('Draw')
    
    # Calculate total goals by summing the home and away scores
    results['total_goals'] = results['home_score'].fillna(0) + results['away_score'].fillna(0)
    
    # Extract the year from the 'date' column and assign it to a new 'year' column
    results['year'] = results['date'].apply(get_year)
    
    # Assign 'Friendly' or 'Non Friendly' based on the tournament type
    results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

    return results


# Function to fetch the goals tally based on given filters
def fetch_goals_tally(results, year, country, venue, type):
    # If all parameters are 'Overall', return the entire dataset
    if (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results
    # Filter by year, keep the country, venue, and type as 'Overall'
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]
    # Filter by country, keep the year, venue, and type as 'Overall'
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]
    # Filter by venue, keep the year, country, and type as 'Overall'
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results
    # Filter by tournament type, keep the year, country, and venue as 'Overall'
    elif (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]
    # Filter by year and country, keep the venue and type as 'Overall'
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]
    # Filter by year, country, and venue, keep the type as 'Overall'
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]
    # Filter by tournament type and venue, keep the year and country as 'Overall'
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]
    # Filter by year and tournament type, keep the country and venue as 'Overall'
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]
    # Filter by year and tournament type, keep the country and venue as 'Overall'
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]
    # Filter by country and tournament type, keep the year and venue as 'Overall'
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]
    # Filter by country, venue, and tournament type, keep the year as 'Overall'
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]
    # Filter by year and tournament type, keep the country and venue as 'Overall'
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]
    # Filter by year, country, and venue, keep the tournament type as 'Overall'
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]
    # Filter by year, country, venue, and tournament type
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]
    # Filter by year, country, venue, and tournament type
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]

    # Apply overall goals tally function to the filtered results
    final_df = overall_goals_tally(temp_df, venue, country)

    return final_df


# Function to extract the year from a given date
def get_year(date):
        my_str=date[:4]  # Extract the first 4 characters (the year) from the date string
        res=int(my_str)  # Convert the extracted year string to an integer
        return res  # Return the year as an integer

# Function to get the list of years and countries
def country_year_list(results):
        results['year'] = results['date'].apply(get_year)  # Add a new 'year' column to the DataFrame by extracting the year from the 'date' column
        years = results['year'].unique().tolist()  # Get the unique years in the dataset
        years.sort()  # Sort the years in ascending order
        years.insert(0, 'Overall')  # Add 'Overall' to the start of the year list
        
        overall_results_tally =  results_tally(results)  # Get the overall results tally
        countries = overall_results_tally['country'].unique().tolist()  # Get the unique countries from the overall results tally
        countries.sort()  # Sort the countries alphabetically
        countries.insert(0, 'Overall')  # Add 'Overall' to the start of the countries list

        return years, countries  # Return the years and countries lists

# Function to fetch results based on year, country, venue, and tournament type
def fetch_results_tally(results, year, country, venue, type):
    # Multiple conditional checks to filter the results based on different combinations of year, country, venue, and tournament type
    if (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results  # Return all results if all filters are 'Overall'
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]  # Filter results based on the specified year
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]  # Filter results for the specified country
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results  # No filtering applied for this case
    elif (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]  # Filter results based on the specified tournament type
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]  # Filter results for the specified country and year
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]  # Filter results for the specified country
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]  # Filter results for the specified tournament type
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]  # Filter results based on the specified year
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]  # Filter results based on year and tournament type
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]  # Filter results for the specified country and tournament type
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]  # Filter results for the specified country and tournament type
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]  # Filter results based on year and tournament type
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]  # Filter results for the specified country and year
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]  # Filter results for the specified country, year, and tournament type
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]  # Filter results for the specified country, year, and tournament type

    final_df = overall_results_tally(temp_df,venue,country)  # Generate the final tally based on the filtered results

    return final_df  # Return the final results

# Function to calculate the number of matches per year over time
def football_matches_over_time(results):
    matches_per_year_over_time = results['year'].value_counts().reset_index()  # Count the number of matches per year
    matches_per_year_over_time.rename(columns={'year': 'Year', 'count': 'Number of Matches'}, inplace=True)  # Rename the columns for clarity

    matches_per_year_over_time = matches_per_year_over_time.sort_values('Year')  # Sort the results by year
    return matches_per_year_over_time  # Return the matches per year data

# Function to calculate the total goals scored per year over time
def football_goals_over_time(results):
    goals_per_year_over_time = results.groupby('year')['total_goals'].sum().reset_index()  # Sum the total goals per year
    goals_per_year_over_time.rename(columns={'year': 'Year', 'total_goals': 'Number of Goals'}, inplace=True)  # Rename the columns for clarity

    return goals_per_year_over_time  # Return the goals per year data

# Function to calculate the total goals scored by a team in each year
def yearwise_goal_tally(results,country):
    # Filter matches where the given country is the home team
    temp_df = results[(results['home_team'] == country)]
    # Count the number of home goals for each year
    temp_df = temp_df.groupby('year').count()['home_score'].reset_index()

    # Filter matches where the given country is the away team
    temp_df_ = results[(results['away_team'] == country)]
    # Count the number of away goals for each year
    temp_df_ = temp_df_.groupby('year').count()['away_score'].reset_index()

    # Combine both home and away goals by year
    total_df = pd.concat([temp_df, temp_df_]).groupby('year').sum().reset_index()

    # Calculate the total goals scored in each year
    total_df['total_goals'] = total_df['home_score'] + total_df['away_score']
    # Convert all columns with float type to integers
    total_df = total_df.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    return total_df

# Function to calculate the overall goals scored in each year
def overall_yearwise_goal_tally(results):
    # Group by year and count the total goals
    temp_df = results
    temp_df = temp_df.groupby('year').count()['total_goals'].reset_index()
    # Convert all columns with float type to integers
    temp_df = temp_df.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    return temp_df

# Function to calculate the total goals conceded by a team in each year
def yearwise_concede_tally(results,country):
    # Filter matches where the given country is the home team
    temp_df_conceded_home = results[(results['home_team'] == country)]
    # Sum the goals conceded by the home team in each year
    temp_df_conceded_home = temp_df_conceded_home.groupby('year').sum()['away_score'].reset_index()

    # Filter matches where the given country is the away team
    temp_df_conceded_away = results[(results['away_team'] == country)]
    # Sum the goals conceded by the away team in each year
    temp_df_conceded_away = temp_df_conceded_away.groupby('year').sum()['home_score'].reset_index()

    # Combine both home and away conceded goals by year
    total_df_conceded = pd.concat([temp_df_conceded_home, temp_df_conceded_away]).groupby('year').sum().reset_index()

    # Calculate the total goals conceded in each year
    total_df_conceded['total_goals_conceded'] = total_df_conceded['away_score'] + total_df_conceded['home_score']
    # Convert all columns with float type to integers
    total_df_conceded = total_df_conceded.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    return total_df_conceded

# Function to calculate the total goals scored by a team against each opponent
def goals_scored_opp(results,country):
    # Calculate goals scored at home by the team against each away team
    home_goals_opp_wise = results[(results['home_team'] == country)].groupby('away_team')['home_score'].sum().reset_index().sort_values('home_score', ascending=False)
    # Calculate goals scored away by the team against each home team
    away_goals_opp_wise = results[(results['away_team'] == country)].groupby('home_team')['away_score'].sum().reset_index().sort_values('away_score', ascending=False)
    
    # Rename columns for consistency in merging
    away_goals_opp_wise = away_goals_opp_wise.rename(columns={'home_team': 'country', 'away_score': 'goals_scored'})
    home_goals_opp_wise = home_goals_opp_wise.rename(columns={'away_team': 'country', 'home_score': 'goals_scored'})
    
    # Combine both home and away goals and group by opponent
    total_goals_opp_wise = pd.concat([away_goals_opp_wise, home_goals_opp_wise]).groupby('country').sum().reset_index().sort_values('goals_scored', ascending=False)
    
    return total_goals_opp_wise

# Function to calculate the total goals conceded by a team against each opponent
def goals_conceded_opp(results,country):
    # Calculate goals conceded at home by the team to each away team
    home_goals_conceded_opp_wise = results[(results['home_team'] == country)].groupby('away_team')['away_score'].sum().reset_index().sort_values('away_score', ascending=False)
    # Calculate goals conceded away by the team to each home team
    away_goals_conceded_opp_wise = results[(results['away_team'] == country)].groupby('home_team')['home_score'].sum().reset_index().sort_values('home_score', ascending=False)
    
    # Rename columns for consistency in merging
    away_goals_conceded_opp_wise = away_goals_conceded_opp_wise.rename(columns={'home_team': 'country', 'home_score': 'goals_conceded'})
    home_goals_conceded_opp_wise = home_goals_conceded_opp_wise.rename(columns={'away_team': 'country', 'away_score': 'goals_conceded'})
    
    # Combine both home and away conceded goals and group by opponent
    total_goals_conceded_opp_wise = pd.concat([away_goals_conceded_opp_wise, home_goals_conceded_opp_wise]).groupby('country').sum().reset_index().sort_values('goals_conceded', ascending=False)
    
    return total_goals_conceded_opp_wise
