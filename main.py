# Terminology and extra information

#Assists
    #The person who set up the goal scorer/ the person who passes the ball to the person who scored.

#xG
    #Expected goal - This rating is donated to how probable the ball will go in from the opportunity of your shot. If you shoot outside the box you might only have an xG of .10, even if you score from that unlikely position. If you shoot on the line the XG will be closer to 1 and even if you miss it will remain at the figure. It's the likelihood of scoring from a certain position.
#xA ?
    #Expected assists. Similar function to xG. If a player is in a good opportunity to assist and pass the ball but the goal scorer misses, they will get a lower xA. The likelihood of your pass will result in a goal. 1 being that you passed to a person who has a great opportunity, and 0 to a very hard opportunity.
#npg ?
    #This is non penalty goals
#npxg ?
    #This is non penalty expected goals. This is similar to xG but it takes away goals scored from penalties.
#Goal contributions ?
    #The combination of goals and assists




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# importing the first kaggle file, which has 5 csv files (https://www.kaggle.com/shreyanshkhandelwal/goal-dataset-top-5-european-leagues)
df_spain = pd.read_csv("chpaters/LaLiga-goalScorer(20-21).csv")
df_england = pd.read_csv("chpaters/epl-goalScorer(20-21).csv")
df_france = pd.read_csv("chpaters/Ligue_1-goalScorer(20-21).csv")
df_germany = pd.read_csv("chpaters/Bundesliga-goalScorer(20-21).csv")
df_italy = pd.read_csv("chpaters/Serie_A-goalScorer(20-21).csv")

#add country columm to each of the individual tables - this will allow us to see where (country) each player was playing
#we can can them all by their rel;evant country as the files are set up indvidually
df_germany['country'] = 'Germany'
df_england['country'] = 'England'
df_spain['country'] = 'Spain'
df_italy['country'] = 'Italy'
df_france['country'] = 'France'

# The first merge -  need to merge/join all the dataframes into one dataframe that will display everything - since all the headers are the same we can use a simple concartination
merge1 = pd.concat([df_spain, df_france, df_italy, df_germany, df_england], ignore_index = True)

# setting the display to see all columns and rows, unless us specifiy what i want to see
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 2000)
pd.options.display.width = None


# The second merge - adding in the second databaser that includes the 2020 stats.
# I didnt want to use stats from other files becasue they arent updated (https://www.kaggle.com/shushrutsharma/top-5-football-leagues)
stats_2015_2020 = pd.read_csv("chpaters/Fullmetadata.csv")


# dropping the columns that include the 2020 data ast they arent updated
filt = stats_2015_2020['year'] == 2020
stats_2015_2019 = stats_2015_2020.drop(index=stats_2015_2020[filt].index)

#since they were missing the year for the first merge we will create a new column and add in the year for all of them

merge1['year'] = 2020

#update names on merge 1 to match the columns of stats_2015_2019 so it will make the second merge much easier to preform

merge1.rename(columns = {'id': 'player_id', 'team_title': 'team_name'}, inplace = True)

all_players = pd.merge(merge1, stats_2015_2019, on = ['player_id', 'player_name', 'games', 'time', 'goals',
    'xG', 'assists', 'xA', 'shots', 'key_passes', 'yellow_cards', 'red_cards', 'position', 'team_name', 'npg', 'npxG',
                                        'xGChain', 'xGBuildup', 'year'], how = 'outer')



# Assigning the teams column into a list, and using a for loop to remove all duplicates

all_teams = all_players["team_name"].value_counts()
#print(all_teams)


teams = (all_players.loc[:,"team_name"])

teams_list = teams.tolist()

teams_list_clean = []
for i in teams_list:
    if i not in teams_list_clean:
        teams_list_clean.append(i)

# Assigning clubs to to their countries lists

german_teams = ['Bayern Munich', 'Eintracht Frankfurt', 'Borussia Dortmund', 'Hoffenheim', 'Wolfsburg', 'VfB Stuttgart', 'Borussia M.Gladbach', 'Union Berlin', 'Bayer Leverkusen', 'Freiburg', 'Augsburg', 'RasenBallsport Leipzig', 'Hertha Berlin', 'FC Cologne', 'Mainz 05', 'Bayer Leverkusen,Union Berlin', 'Werder Bremen', 'Mainz 05,Wolfsburg', 'Schalke 04', 'Arminia Bielefeld', 'Hoffenheim,Schalke 04', 'Eintracht Frankfurt,Mainz 05', 'Augsburg,Borussia M.Gladbach', 'Arminia Bielefeld,Hertha Berlin', 'Schalke 04,Wolfsburg', 'Bayern Munich,Hoffenheim', 'Paderborn', 'Fortuna Duesseldorf', 'Hannover 96', 'Nuernberg', 'Troyes', 'Hamburger SV', 'Ingolstadt', 'Darmstadt']
spanish_teams = ['Barcelona', 'Villarreal', 'Real Madrid', 'Atletico Madrid', 'Sevilla', 'Real Sociedad', 'Levante', 'Celta Vigo', 'SD Huesca', 'Eibar', 'Alaves', 'Osasuna', 'Valencia', 'Real Betis', 'Granada', 'Cadiz', 'Athletic Club', 'Elche', 'Real Valladolid', 'Getafe', 'Eibar,Sevilla', 'Barcelona,Getafe', 'Real Sociedad,Sevilla', 'Cadiz,Valencia', 'Athletic Club,Real Valladolid', 'Celta Vigo,Real Valladolid', 'Getafe,Villarreal', 'Atletico Madrid,Valencia', 'Alaves,Granada', 'Alaves,Athletic Club', 'Atletico Madrid,Osasuna', 'Espanyol', 'Leganes', 'Mallorca', 'Rayo Vallecano', 'Girona', 'Malaga', 'Deportivo La Coruna', 'Las Palmas', 'Sporting Gijon']
english_teams = ['Tottenham', 'Liverpool', 'Manchester United', 'Leeds', 'Everton', 'Leicester', 'Aston Villa', 'Manchester City', 'Arsenal', 'Newcastle United', 'Southampton', 'Burnley', 'Crystal Palace', 'West Bromwich Albion', 'West Ham', 'Brighton', 'Arsenal,Newcastle United', 'Chelsea', 'Sheffield United', 'Wolverhampton Wanderers', 'Fulham', 'Everton,Southampton', 'Aston Villa,Chelsea', 'Liverpool,Southampton', 'Chelsea,Fulham', 'West Bromwich Albion,West Ham', 'Arsenal,West Bromwich Albion', 'Arsenal,Brighton', 'Bournemouth', 'Norwich', 'Watford', 'Huddersfield', 'Cardiff', 'Swansea', 'Stoke', 'Sunderland', 'Hull', 'Middlesbrough']
french_teams = ['Paris Saint Germain', 'Lyon', 'Monaco', 'Montpellier', 'Strasbourg', 'Lille', 'Reims', 'Lorient', 'Nice', 'Bordeaux', 'Lens', 'Nimes', 'Nantes', 'Rennes', 'Marseille', 'Brest', 'Metz,Strasbourg', 'Saint-Etienne', 'Angers', 'Dijon', 'Lens,Paris Saint Germain', 'Metz', 'Brest,Nimes', 'Monaco,Strasbourg', 'Lyon,Nice', 'Dijon,Rennes', 'Nice,Nimes', 'Brest,Lyon', 'Brest,Paris Saint Germain', 'Toulouse', 'Amiens', 'Caen', 'Guingamp', 'Troyes', 'SC Bastia', 'Nancy', 'GFC Ajaccio']
italian_teams = ['Lecce', 'SPAL 2013', 'Brescia', 'Juventus', 'Inter', 'Atalanta', 'Fiorentina', 'Lazio', 'Crotone', 'Napoli', 'Sassuolo', 'Cagliari', 'AC Milan', 'Roma', 'Torino', 'Sampdoria', 'Genoa', 'Spezia', 'Udinese', 'Fiorentina,Juventus', 'Bologna', 'Benevento', 'Parma Calcio 1913', 'Verona', 'Udinese,Verona', 'Cagliari,Crotone', 'Inter,Parma Calcio 1913', 'Torino,Udinese', 'Fiorentina,Spezia', 'Sampdoria,Torino', 'Cagliari,Inter', 'Genoa,Verona', 'Napoli,Udinese', 'AC Milan,Torino', 'Fiorentina,Verona', 'Cagliari,Fiorentina', 'AC Milan,Parma Calcio 1913', 'Atalanta,Benevento,Sampdoria', 'Cagliari,Spezia', 'Crotone,Parma Calcio 1913', 'AC Milan,Lazio', 'Fiorentina,Napoli', 'Bologna,Cagliari', 'Genoa,Parma Calcio 1913', 'Genoa,Juventus', 'Crotone,Verona', 'Empoli', 'Chievo', 'Frosinone', 'Palermo', 'Pescara', 'Carpi']

# Assigning clubs lists to their respective countries in the columns

all_players.loc[all_players['team_name'].isin(german_teams), 'country'] = 'Germany'
all_players.loc[all_players['team_name'].isin(spanish_teams), 'country'] = 'Spain'
all_players.loc[all_players['team_name'].isin(italian_teams), 'country'] = 'Italy'
all_players.loc[all_players['team_name'].isin(english_teams), 'country'] = 'England'
all_players.loc[all_players['team_name'].isin(french_teams), 'country'] = 'France'

# Assign players to their current teams
all_players['team_name'] = all_players['team_name'].replace({'Eibar,Sevilla':'Sevilla', 'Barcelona,Getafe':'Getafe', 'Real Sociedad,Sevilla':'Sevilla', 'Cadiz,Valencia':'Valencia', 'Athletic Club,Real Valladolid':'Real Valladolid', 'Celta Vigo,Real Valladolid':'Real Valladolid', 'Getafe,Villarreal':'Villarreal', 'Atletico Madrid,Valencia':'Valencia', 'Alaves,Granada':'Granada', 'Alaves,Athletic Club':'Athletic Club', 'Atletico Madrid,Osasuna':'Osasuna',  'Metz,Strasbourg':'Strasbourg', 'Lens,Paris Saint Germain':'Paris Saint Germain', 'Brest,Nimes':'Nimes', 'Moaco,Strasbourg':'Strasbourg', 'Lyon,Nice':'Nice', 'Dijon,Rennes':'Rennes', 'Nice,Nimes':'Nimes', 'Brest,Lyon':'Lyon', 'Brest,Paris Saint Germain':'Paris Saint Germain', 'Fiorentina,Juventus':'Juventus', 'Udinese,Verona':'Verona', 'Cagliari,Crotone':'Crotone', 'Inter,Parma Calcio 1913':'Parma Calcio 1913', 'Torino,Udinese':'Udinese', 'Fiorentina,Spezia':'Spezia', 'Sampdoria,Torino':'Torino', 'Cagliari,Inter':'Inter', 'Genoa,Verona':'Verona', 'Napoli,Udinese':'Udinese', 'AC Milan,Torino':'Torino', 'Fiorentina,Verona':'Verona', 'Cagliari,Fiorentina':'Fiorentina', 'AC Milan,Parma Calcio 1913':'Parma Calcio 1913', 'Atalanta,Benevento,Sampdoria':'Sampdoria', 'Cagliari,Spezia':'Spezia', 'Crotone,Parma Calcio 1913':'Parma Calcio 1913', 'AC Milan,Lazio':'Lazio', 'Fiorentina,Napoli':'Napoli', 'Bologna,Cagliari':'Cagliari', 'Genoa,Parma Calcio 1913':'Parma Calcio 1913', 'Genoa,Juventus':'Juventus', 'Crotone,Verona':'Verona', 'Bayer Leverkusen,Union Berlin':'Union Berlin', 'Mainz 05,Wolfsburg':'Wolfsburg', 'Hoffenheim,Schalke 04':'Schalke 04', 'Eintracht Frankfurt,Mainz 05':'Mainz 05', 'Augsburg,Borussia M.Gladbach':'Borussia M.Gladbach', 'Arminia Bielefeld,Hertha Berlin':'Hertha Berlin', 'Schalke 04,Wolfsburg':'Wolfsburg', 'Bayern Munich,Hoffenheim':'Hoffenheim',  'Arsenal,Newcastle United':'Newcastle United', 'Everton,Southampton':'Southampton', 'Aston Villa,Chelsea':'Chelsea', 'Liverpool,Southampton':'Southampton', 'Chelsea,Fulham':'Fulham', 'West Bromwich Albion,West Ham':'West Ham', 'Arsenal,West Bromwich Albion':'West Bromwich Albion', 'Arsenal,Brighton':'Brighton'})



# Changing the display
pd.set_option('display.max_columns', 40)
pd.set_option('display.max_rows', 20000)

# Dropping column 'Unnamed: 0'
all_players.drop(['Unnamed: 0'], axis = 1)

# Reordering part 1

columnsTitles = ['player_id', 'year', 'player_name', 'position', 'country', 'team_name', 'games', 'time', 'shots', 'goals', 'xG', 'npg', 'npxG', 'key_passes', 'assists', 'xA', 'xGChain',
       'xGBuildup', 'yellow_cards', 'red_cards']

all_players = all_players.reindex(columns = columnsTitles)


# Adding new columns to the new fully merged dataframe
all_players['conversion_rate'] = (all_players['goals'] / all_players['shots']).round(2)
all_players['goals_per_match'] = (all_players['goals'] / all_players['games']).round(2)
all_players['shots_per_match'] = (all_players['shots'] / all_players['games']).round(2)
all_players['assists_per_match'] = (all_players['assists'] / all_players['games']).round(2)
all_players['key_passes_per_match'] = (all_players['key_passes'] / all_players['games']).round(2)
all_players['penalty_goals'] = (all_players['goals'] - all_players['npg']).round(2)
all_players['diff_goals_xg'] = (all_players['goals'] - all_players['xG']).round(2)
all_players['diff_assists_xa'] = (all_players['assists'] - all_players['xA']).round(2)
all_players['key_pass_conversion'] = (all_players['assists'] / all_players['key_passes']).round(2)
all_players['goal_contributions'] = (all_players['assists'] + all_players['goals']).round(2)

# Creating a filter to show players that have contributed to their teams and countries
all_players_filt = all_players[(all_players['games'] > 18) &
                               (all_players['goals'] > 2) &
                               (all_players['assists'] > 1) &
                               (all_players['shots'] > 16)]


# checking to see if there are any issues
print(all_players_filt.shape)
print(all_players_filt.describe())
print(all_players_filt.info())


# Defining functions that will be used to assign values to players

def pct95(column):
    return column.quantile(0.95)
def pct75(column):
    return column.quantile(0.75)
def pct40(column):
    return column.quantile(0.4)
def pct25(column):
    return column.quantile(0.25)


# using if and else statement in for loops to assign values

# create a new column for scorer status
all_players_filt['scorer_status'] = ''

# assign values to players that meet certain conditions (Tier X scorer)

all_players_filt['scorer_status'] = ["Tier 1 scorer" if i >= 18 else
                       "Tier 2 scorer" if i >= 9 else
                       "Tier 3 scorer" if i > 5 else
                       "Tier 4 scorer" for i in all_players_filt.goals]

# create a new column for the playmakers status
all_players_filt['playmaker_status'] = ''

# assign values to players that meet certain conditions (Tier X playmaker)

all_players_filt['playmaker_status'] = ["Tier 1 playmaker" if i >= 10 else
                          "Tier 2 playmaker" if i >= 6 else
                          "Tier 3 playmaker" if i > 3 else
                          "Tier 4 playmaker" for i in all_players_filt.assists]



#reorders the columns for the all_player_filt dtaframe

columnsTitles = ['player_id', 'year', 'player_name', 'scorer_status', 'playmaker_status', 'position',
                 'country', 'team_name', 'games', 'time', 'shots', 'shots_per_match', 'goals', 'conversion_rate',
                 'xG', 'goals_per_match', 'diff_goals_xg', 'goal_contributions',
                 'npg', 'npxG', 'penalty_goals', 'key_passes',
                 'key_passes_per_match', 'key_pass_conversion',
                 'assists', 'xA', 'assists_per_match', 'diff_assists_xa', 'xGChain',
       'xGBuildup', 'yellow_cards', 'red_cards']

all_players_filt = all_players_filt.reindex(columns = columnsTitles)


# Graph 1 - Highest goal scorers (2020)

player_stats_2020 = all_players_filt[all_players_filt['year'] == 2020]
player_stats_2020_sorted = player_stats_2020.sort_values(by = ['scorer_status', 'goals'], ascending = [True, False])
tier_1_scorers_2020 = player_stats_2020_sorted[player_stats_2020_sorted['scorer_status'] == 'Tier 1 scorer']
fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.bar(tier_1_scorers_2020['player_name'], tier_1_scorers_2020['goals'], alpha = .20, color = 'blue')
ax2.plot(tier_1_scorers_2020['player_name'], tier_1_scorers_2020['goals_per_match'], alpha = 1, color = 'red')
ax.set_xticklabels(tier_1_scorers_2020['player_name'], rotation = 90)
ax.set_xlabel('Players')
ax.set_ylabel('Goals scored in (2020)', color='blue')
ax2.set_ylabel('Goals per match (2020)', color = 'red')
ax.set_title('Tier 1 players goals (2020)')
plt.show()
print(player_stats_2020_sorted)



# graph 2 - Best players in each category over the years

player_df_unfilt = all_players_filt.groupby('player_name')[['games', 'assists', 'goals', 'shots', 'key_passes']].sum().reset_index()
player_df = player_df_unfilt[player_df_unfilt['games'] >= 105]
player_df['key_passes_per_match'] = player_df['key_passes'] / player_df['games']
player_df['shots_per_match'] = player_df['shots'] / player_df['games']
total_assists_goals = player_df.groupby('player_name')[['games', 'goals', 'assists', 'shots', 'key_passes', 'shots_per_match', 'key_passes_per_match']].sum().reset_index()
# print(total_assists_goals.describe())
ax=sns.scatterplot(data=total_assists_goals, x="goals", y="assists", hue = 'shots_per_match', size = 'key_passes_per_match')
idx=total_assists_goals["goals"]>100
idx=idx | (total_assists_goals["assists"]>50)
for i,row in total_assists_goals.loc[idx].iterrows():
  ax.text(row["goals"], row["assists"],row["player_name"])
  # print(row)
plt.axvline(100, c=(.5,.5,.5), ls='--')
plt.axhline(40, c=(.5,.5,.5), ls='--')
ax.set_title('Best goals scorers and playmakers (2015-2020)')
ax.set_ylabel('Assists (2015-2020)')
ax.set_xlabel('Goals (2015-2020)')
plt.show()
print(total_assists_goals)



# Graph 3

# Goal contributions per country from season 2015 - 2020

country_df_unsorted = all_players.groupby(['country', 'year'])[['goals', 'assists', 'goal_contributions']].sum().reset_index()
country_df = country_df_unsorted.sort_values(by = 'year', ascending = False)
sns.set(rc={'figure.figsize':(11.7,8.27)})
r = sns.lineplot(data = country_df, x="year", y="goal_contributions", hue = "country", style = "country", linewidth = 3)
r.set_title('Goal contributions for each country (2015-2020)')
r.set_xlabel('years (2015-2020)')
r.set_ylabel('Goal contributions (2015-2020)')
plt.show()


# Graph 4 - Heatmap of the main stats

correlation_df = all_players_filt.groupby('player_name')[['goals', 'assists', 'xG', 'xA', 'shots', 'key_passes', 'npg', 'penalty_goals']].sum().reset_index()
dataplot = sns.heatmap(correlation_df.corr(), cmap ='Blues', annot = True, annot_kws = {'fontsize': 14, 'fontweight':'bold'}, linewidth = 1)
ax.set_title('Correlation between the player stats')
plt.show()


# Graph 5 - Best clubs over the years

teams_df_unfilt = all_players_filt.groupby('team_name')['goals', 'assists', 'shots', 'xG', 'xA'].sum().reset_index()
teams_df_unfilt['xG_per_match'] = (teams_df_unfilt['xG'] / 210).round(2)
teams_df_unfilt['xA_per_match'] = (teams_df_unfilt['xA'] / 210).round(2)
teams_df_unfilt['shots_per_match'] = (teams_df_unfilt['shots'] / 210).round(2)
teams_df = teams_df_unfilt[teams_df_unfilt['goals'] >= 100]
print(teams_df.head(100))
sns.set(rc={'figure.figsize': (11.7, 8.27)})
plt.style.use('seaborn')
ax = sns.scatterplot(data=teams_df, hue = 'shots_per_match', x="xG_per_match", y="xA_per_match", size = 'shots_per_match')
idx=teams_df["xG_per_match"]>1.3
idx=idx | (teams_df["xA_per_match"]>0.75)
for i,row in teams_df.loc[idx].iterrows():
  ax.text(row["xG_per_match"], row["xA_per_match"],row["team_name"])
ax.set_title('Best clubs (2015-2020)')
ax.set_ylabel('xA per match (2015-2020)')
ax.set_xlabel('xG per match (2015-2020)')


  # print(row)

plt.show()




