import pandas as pd
import obj
import numpy as np

apps = ['FX', 'PH', 'SR', 'VT', 'PB', 'HB']

# From apparatus final scores, distribute medals to appropriate countries
def update_medal_counts_apparatus(row, app_medal_dict):
    medalists = row.nlargest(3).index.str.split(' ')
    for medalist, medal in zip(medalists, ['gold', 'silver', 'bronze']):
        if app_medal_dict[medalist[-1]][medal]:
            app_medal_dict[medalist[-1]][medal] += 1
        else:
            app_medal_dict[medalist[-1]][medal] = 1
    return app_medal_dict

# From individual All Around final scores, distribute medals to appropriate countries
def update_medal_counts_indv_AA(row, AA_medal_dict):
    medalists = row.nlargest(3).index.str.split(' ')
    for medalist, medal in zip(medalists, ['gold', 'silver', 'bronze']):
        if AA_medal_dict[medalist[-1]][medal]:
            AA_medal_dict[medalist[-1]][medal] += 1
        else:
            AA_medal_dict[medalist[-1]][medal] = 1
    return AA_medal_dict

# From team All Around final scores, distribute medals to appropriate countries
def update_medal_counts_team_AA(row, Team_AA_medal_dict):
    medalists = row.nlargest(3).index
    for medalist, medal in zip(medalists, ['gold', 'silver', 'bronze']):
        if Team_AA_medal_dict[medalist][medal]:
            Team_AA_medal_dict[medalist][medal] += 1
        else:
            Team_AA_medal_dict[medalist][medal] = 1
    return Team_AA_medal_dict

# from qualifying round, simulate to final scores
def indv_App_medal_sim(sims, app_medal_dict, n = 100):
    apps = ['FX', 'PH', 'SR', 'VT', 'PB', 'HB']
    for apparatus in apps:
        app_df = sims.filter(regex = f'{apparatus}$', axis = 1)
        app_df['eigth'] = np.sort(app_df.values, axis=1)[:, -8]
        for col in app_df.columns[:-1]:
            app_df[col] = app_df[col] >= app_df['eigth']
        for row in app_df.drop('eigth', axis = 1).itertuples(index = False):
            top_8 = [col for col, value in zip(app_df.columns, row) if value == True]
            final_scores = {}
            for athlete in top_8:
                ath = obj.male_gymnast(athlete.split('-')[0])
                distribution = ath.summ_table.loc[apparatus]
                final_scores[athlete.split('-')[0] + ' ' + ath.country] = np.random.normal(distribution['mean'], distribution['std_dev'], n)
            final_sims = pd.DataFrame(final_scores)
            for row in final_sims.iterrows():
                update_medal_counts_apparatus(row[1], app_medal_dict)

# from qualifying round, simulate to final scores
def indv_AA_medal_sim(sims, AA_medal_dict, n = 100):
    names = sims.columns.str.split('-').str[0]

    # Group by person and sum scores across apparatuses
    total_scores = sims.groupby(names, axis=1).sum()
    total_scores['24'] = np.sort(total_scores.values, axis=1)[:, -24]
    for col in total_scores.columns[:-1]:
        total_scores[col] = total_scores[col] >= total_scores['24']

    for row in total_scores.drop('24', axis = 1).itertuples(index = False):
        finalists = [col for col, value in zip(total_scores.columns, row) if value == True]
        final_scores = {}
        for athlete in finalists:
            athlete_obj = obj.male_gymnast(athlete)
            for app in athlete_obj.summ_table.itertuples():
                final_scores[athlete + ' ' + athlete_obj.country + '-' + app.Index] = np.random.normal(app.mean, app.std_dev, n)
        final_sims = pd.DataFrame(final_scores)
        final_names = final_sims.columns.str.split('-').str[0]
        final_AA_scores = final_sims.groupby(final_names, axis=1).sum()
        for row in final_AA_scores.iterrows():
            update_medal_counts_indv_AA(row[1], AA_medal_dict)

# from qualifying round, simulate to final scores
def team_AA_medal_sim(row, Team_AA_medal_dict, n = 100):
    country_app_totals = {}
    country_app_quals = {}
    country_apps = row.index.str.split('-').str[1]
    for c_app in country_apps:
        country_cols = row.filter(like = c_app)
        top_3 = country_cols.nlargest(3)
        country_app_totals[c_app] = top_3.sum()
        country_app_quals[c_app] = list(top_3.index.str.split('-').str[0])
    
    country_tots = pd.DataFrame(country_app_totals, index = range(len(country_apps)))
    cols = country_tots.columns.str.split('_').str[0]
    team_scores = country_tots.groupby(cols, axis = 1).sum()
    team_scores['eight'] = np.sort(team_scores.values, axis=1)[:, -8]
    for col in team_scores.columns[:-1]:
        team_scores[col] = team_scores[col] >= team_scores['eight']
    teams = team_scores[1:2].apply(lambda row: [col for col, value in zip(team_scores.columns, row) if value == True], axis = 1)
    final_athletes = {}
    for app in apps:
        final_athletes[app] = {}
    for team in teams.loc[1]:
        for app in apps:
            final_athletes[app][team] = country_app_quals[f"{team}_{app}"]
    
    country_app_final = pd.DataFrame()
    for app in final_athletes:
        for country in final_athletes[app]:
            performances = {}
            for athlete in final_athletes[app][country]:
                ath_app_sum = obj.male_gymnast(athlete).summ_table.loc[app]
                performances[athlete] = np.random.normal(ath_app_sum['mean'], ath_app_sum['std_dev'], n)
            country_app_final[country + '_' + app] = (pd.DataFrame(performances).sum(axis = 1))
            
    countries = country_app_final.columns.str.split('_').str[0]
    final_scores = country_app_final.groupby(countries, axis = 1).sum()
    for row in final_scores.iterrows():
        update_medal_counts_team_AA(row[1], Team_AA_medal_dict)
    
# start apparatus, indv. AA, and team AA sims
def qual_to_medals(sims):
    competing_teams = sims.columns.str.split('-').str[-1].str.split('_').str[0].unique()

    app_medal_dict = {}
    AA_medal_dict = {}
    Team_AA_medal_dict = {}

    Team_AA_medal_dict = {}
    for country in competing_teams:
        app_medal_dict[country] = {'gold': 0, 'silver': 0, 'bronze': 0}
    for country in competing_teams:
        AA_medal_dict[country] = {'gold': 0, 'silver': 0, 'bronze': 0}
    for country in competing_teams:
        Team_AA_medal_dict[country] = {'gold': 0, 'silver': 0, 'bronze': 0}

    indv_App_medal_sim(sims, app_medal_dict)
    indv_AA_medal_sim(sims, AA_medal_dict)
    for row in sims.iterrows():
        team_AA_medal_sim(row[1], Team_AA_medal_dict)
    return {'Apparatus': app_medal_dict, 'Indv. AA': AA_medal_dict, 'Team AA': Team_AA_medal_dict}