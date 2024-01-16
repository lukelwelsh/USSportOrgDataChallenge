import pandas as pd

women = pd.read_csv('women.csv')
men = pd.read_csv('men.csv')

w_stds = women.groupby(['Name', 'Apparatus'])['Score'].agg(std_dev = 'std')
w_event_stds = w_stds.groupby('Apparatus')['std_dev'].mean()

m_stds = men.groupby(['Name', 'Apparatus'])['Score'].agg(std_dev = 'std')
m_event_stds = m_stds.groupby('Apparatus')['std_dev'].mean()

class female_gymnast:
    def __init__(self, name):
        indv = women[women['Name'] == name]
        self.summ_table = indv.groupby('Apparatus')['Score'].agg(std_dev='std', mean = 'mean')
        self.summ_table['std_dev'] = self.summ_table['std_dev'].fillna(w_event_stds)
        self.country = indv['Country'].max()

class male_gymnast:
    def __init__(self, name):
        indv = men[men['Name'] == name]
        self.summ_table = indv.groupby('Apparatus')['Score'].agg(std_dev='std', mean = 'mean')
        self.summ_table['std_dev'] = self.summ_table['std_dev'].fillna(m_event_stds)
        self.country = indv['Country'].max()
        
class m_country:
    def __init__(self, country):
        performances = men[men['Country'] == country]
        self.ath_perf = {}
        self.athletes = performances['Name'].unique()
        for athlete in self.athletes:
            self.ath_perf[athlete] = male_gymnast(athlete).summ_table
        
        self.apps = {'FX': [], 'HB': [], 'PB': [], 'PH': [], 'SR': [], 'VT': []}
        for ath in self.ath_perf:  # check if each athlete has competed in at least 3 apparatus, if so, kept if they have a top 2 score for the country, included
            ath_scores = self.ath_perf[ath]
            if len(ath_scores) >= 3:
                for row in ath_scores.itertuples():
                    if len(self.apps[row.Index]) < 2:
                        self.apps[row.Index].append(row.mean)
                    elif row.mean > min(self.apps[row.Index]):
                        self.apps[row.Index][self.apps[row.Index].index(min(self.apps[row.Index]))] = row.mean
        self.aths = set()
        for ath in self.ath_perf: # get just athletes that have competed in at least 3 apparatus AND have a top 2 score for any apparatus for the country
            ath_scores = self.ath_perf[ath]
            for row in ath_scores.itertuples():
                if row.mean in self.apps[row.Index]:
                    self.aths.add(ath)
        self.top_5 = {}
        self.flipped_dict = {}
        for ath in self.aths: # get the 5 athletes with the highest average score across all apparatuses, given that they meet the prior qualifications
            a = self.ath_perf[ath]['mean'].mean()
            self.flipped_dict[a] = ath
            if len(self.top_5) < 5:
                self.top_5[ath] = a
            elif a > min(self.top_5.values()):
                self.top_5.pop(self.flipped_dict[min(self.top_5.values())])
                self.top_5[ath] = a
        for ath in self.top_5:
            self.top_5[ath] = self.ath_perf[ath]
            
class w_country:
    def __init__(self, country):
        performances = women[women['Country'] == country]
        self.ath_perf = {}
        self.athletes = performances['Name'].unique()
        for athlete in self.athletes:
            self.ath_perf[athlete] = female_gymnast(athlete).summ_table
            
        self.apps = {'FX': [], 'UB': [], 'BB': [], 'VT': []}
        for ath in self.ath_perf:
            ath_scores = self.ath_perf[ath]
            if len(ath_scores) >= 2: # check if each athlete has competed in at least 2 apparatus, if so, kept if they have a top 2 score for the country, included
                for row in ath_scores.itertuples():
                    if len(self.apps[row.Index]) < 3:
                        self.apps[row.Index].append(row.mean)
                    elif row.mean > min(self.apps[row.Index]):
                        self.apps[row.Index][self.apps[row.Index].index(min(self.apps[row.Index]))] = row.mean
        self.aths = set()
        for ath in self.ath_perf:
            ath_scores = self.ath_perf[ath]
            for row in ath_scores.itertuples():
                if row.mean in self.apps[row.Index]:
                    self.aths.add(ath)
        self.top_5 = {}
        self.flipped_dict = {}
        for ath in self.aths:
            a = self.ath_perf[ath]['mean'].mean()
            self.flipped_dict[a] = ath
            if len(self.top_5) < 5:
                self.top_5[ath] = a
            elif a > min(self.top_5.values()):
                self.top_5.pop(self.flipped_dict[min(self.top_5.values())])
                self.top_5[ath] = a
        for ath in self.top_5:
            self.top_5[ath] = self.ath_perf[ath]