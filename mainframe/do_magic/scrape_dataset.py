import pandas

def scrub_players():
    df = pandas.read_csv('../../csv_files/Players.csv')
    # replace nAN with 0
    df = df.fillna(0)
    for i in range(len(df)) : 
        df.at[i, "height"] =  convert_from_cm(df.at[i, "height"])
        df.at[i, 'weight'] = convertKilo(df.at[i, "weight"])
    #nitpicking
    df = df.rename(columns={'collage': 'college'})
    # 1 indicates columns, 0 : rows | for deleting column of row numbers
    df = df.drop('Unnamed: 0', 1)
    print(df)


def scrub_players_data():
    df = pandas.read_csv('../../csv_files/player_data.csv')
    df = df.fillna(0)
    for i in range(len(df)) : 
        df.at[i, "height"] =  str(df.at[i, "height"]).replace('-','.') 
    df = df.rename(columns={'name': 'Player'})
    # rearrange columns
    df = df[['Player','height','weight', 'college', 'birth_date', 'year_start', 'year_end', 'position']]
    print(df)


def scrub_season_stats():
    df = pandas.read_csv('../../csv_files/Seasons_Stats.csv')
    df = df.fillna(0)
    # df = df.drop('Unnamed: 0', 1)
    df = df.rename(columns={'Tm': 'team'})
    df = df.rename(columns={'G': 'games'})
    df = df.rename(columns={'MP': 'avgminsprgame'})
    df = df.rename(columns={'GS': 'gamestartd'})
    acryonms = acronym_finder()
    j = 0
    for i in range(len(df.team)):
        k = df.at[i, 'team']
        if k in acryonms:
            df.at[i, 'team'] = acryonms.get(k)
            j+=1
    df.to_csv('../../csv_files/updatedTeams.csv')
    print(df)


def convert_from_cm(metric_height):
    return round((metric_height * .393701) / 12, 1)

def convertKilo(val):
    return int(val * 2.20462)




def acronym_finder():
    df = pandas.read_html('https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations',skiprows=1)
#   df = df.rename(columns={'Abbreviation/Acronym': 'Acronym'})
    key_value_acryonms = {}
    for i in range(len(df[0])):
        key_value_acryonms[df[0].iloc[i][0]] = df[0].iloc[i][1] 
    return key_value_acryonms


# scrub_players()
# scrub_players_data()
scrub_season_stats()
# acronym_finder()