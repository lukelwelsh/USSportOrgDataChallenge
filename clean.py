import pandas as pd
pd.options.mode.chained_assignment = None # block error messages

df_22_23 = pd.read_csv('data_2022_2023.csv')
df_22_23['FirstName'] = df_22_23['FirstName'].str.replace('\xa0', '', regex=True) # some weird space characters hidden within
df_22_23['Name'] = df_22_23['FirstName'] + ' ' + df_22_23['LastName'] # creating Name column
df_22_23['Apparatus'] = df_22_23['Apparatus'].str.replace('1', '').str.replace('2', '').str.replace('hb', 'HB') # Some of the apparatuses were inconsistent
df_22_23 = df_22_23.dropna(subset=['Name']) # a couple entries had a blank name

multi_gender_names = list(df_22_23.groupby('Name').filter(lambda x: len(x['Gender'].unique()) > 1)['Name'].unique()) # some names appear as both male and female
multi_gender_names.remove('Victor MARTINEZ') # Appears that there are two Victor MARTINEZ, one male from Belgium, the other female from Venezuela
# test code used to find this # df_22_23[df_22_23['Name'] == 'Victor MARTINEZ'].head()
df_22_23.loc[df_22_23['Name'].isin(multi_gender_names), 'Gender'] = 'w'
    # All other issues are from the VT AAqual at the BIRMINGHAM 2022 Commonwealth Games
    # test code used to find this # df_22_23[(df_22_23['Competition'] == "BIRMINGHAM 2022 Commonwealth Games") & (df_22_23['Round'] == 'AAqual') & (df_22_23['Name'].isin(multi_gender_names))]

men = df_22_23[df_22_23['Gender'] == 'm']
women = df_22_23[df_22_23['Gender'] == 'w']

# many names inconsistent between competitions
men['FirstName'] =  (men['FirstName']
                          .str.replace('Ga-ram', 'Garam')
                          .str.replace('Yo-seop', 'Yoseop')
                          .str.replace('Jin-seong', 'Jinseong')
                          .str.replace('-', ' ')
                          .str.replace('Yu-Jan', 'Yu Jan')
                          .str.replace('VInzenz', 'Vinzenz')
                          .str.replace('Dimitrijs', 'Dmitrijs')
                          .str.replace('Jann', 'Jan')
                          .str.replace('Léo', 'Leo')
                    )
men['FirstName'] = men['FirstName'].str.split().str.get(0)
men['LastName'] = men['LastName'].str.split().str.get(0)
men['LastName'] =  (men['LastName']
                          .str.replace('Ñ', 'N')
                          .str.replace('Ö', 'O')
                          .str.replace('Ê', 'E')
                          .str.replace('Ü', 'UE')
                          .str.replace('HOCK', 'HOECK')
                          .str.replace('Ã', 'A')
                          .str.replace('É', 'E')
                          .str.replace('Ó', 'O')
                          .str.replace('ELMARAGHY', 'MARAGHY')
                          .str.replace('PÄVÄNEN', 'PÄIVÄNEN')
                          .str.replace('KARENEJENKO', 'KARNEJENKO')
                          .str.replace('HOERR', 'HORR')
                          .replace('FU', 'FUALLEN')
                          .str.replace('FU-ALLEN', 'FUALLEN')
                          .str.replace('MODOIANU-ZSEDER', 'MODOIANU')
                          .str.replace('DORDEVIC', 'DJORDJEVIC')
                          .replace('IDESJO', 'IDESJOE')
                          .str.replace('VANSTROEM', 'VANSTROM')
                          .str.replace('WANSTROM', 'VANSTROM')
                          .str.replace('GUENDOGDU', 'GUNDOGDU')
                    )
men['Name'] = men['FirstName'] + ' ' + men['LastName']
men['Name'] = (men['Name']
                    .str.replace('Matthew CORMIER', 'Matt CORMIER')
                    .str.replace('Samual DICK', 'Sam DICK')
                    .str.replace('Samuel DICK', 'Sam DICK')
                    .str.replace('Rakah HARITHI', 'Rakan AL HARITH')
                    .str.replace('Rakan HARITHI', 'Rakan AL HARITH')
                    .str.replace('Rakan ALHARITH', 'Rakan AL HARITH')
                    .str.replace('Mohamed KHALIL', 'Mohamad KHALIL')
                    .str.replace('Hansa KUMARASINGHEGE', 'Hansha KUMARASINGHEGE')
                    .str.replace('Dmitriy PATANIN','Dmitry PATANIN')
                    .str.replace('Frederick RICHARD', 'Fred RICHARD')
                    .str.replace('Sam ZAKUTNEY', 'Samuel ZAKUTNEY')
                    .str.replace('Mc ATEER', 'Ewan MCATEER')
                    .replace('Ewan MC', 'Ewan MCATEER')
                    .str.replace('Mc CLENAGHAN', 'Rhys MCCLENAGHAN')
                    .replace('Rhys MC', 'Rhys MCCLENAGHAN')
                    .replace('Edoardo DE', 'Edoardo DEROSA')
                    .str.replace('Edoardo ROSA', 'Edoardo DEROSA')
                    .replace('Justine DE', 'Justine DELEON')
                    .str.replace('Justine LEON', 'Justine DELEON')
                    .replace('Martijn DE', 'Martijn DEVEER')
                    .str.replace('Martijn VEER', 'Martijn DEVEER')
                    .replace('Loran DE', 'Loran DEMUNCK')
                    .replace('Loran MUNCK', 'Loran DEMUNCK')
                    .replace('Luka VAN', 'Luka VANDENKEYBUS')
                    .replace('Luka KEYBUS', 'Luka VANDENKEYBUS')
                   )

women['FirstName'] = women['FirstName'].str.split().str.get(0)
women['FirstName'] = (women['FirstName']
                       .str.replace('Valentin', 'Valentina')
                       .str.replace('Valentinaa', 'Valentina')
                       .str.replace('Elsabeth', 'Ellie')
                       .str.replace('Léa', 'Lea')
                       .str.replace('Shanté', 'Shante')
                       .str.replace('Noémie', 'Noemie')
                       .str.replace('Sasiwimion', 'Sasiwimon')
                      )
women['LastName'] = women['LastName'].str.split().str.get(0)
women['LastName'] = (women['LastName']
                     .str.replace('MÖRZ', 'MOERZ')
                     .str.replace('SCHÖNMAIER', 'SCHOENMAIER')
                     .str.replace('Ö', 'O')
                     .str.replace('É', 'E')
                     .str.replace('MÄKELÄ', 'MAEKELAE')
                     .replace('EVAN', 'EVANS')
                     .str.replace('Ä', 'AE')
                     .str.replace('RENGGANIS', 'REGGANIS')
                     .str.replace('YEROBOSSYNKYZY', 'YERBOSSYNKYZY')
                     .str.replace('Ø', 'OE')
                     .str.replace('ROLSTON-LARKING', 'ROLSTON')
                     .str.replace('Ü', 'U')
                     .str.replace('KROELL', 'KROLL')
                    )

women['Name'] = women['FirstName'] + ' ' + women['LastName']

women['Name'] = (women['Name']
                  .str.replace('Hua TING', 'Hua-Tien TING')
                  .str.replace('Yi LIAO', 'Yi-Chun LIAO')
                  .str.replace('Yi LIN', 'Yi-Chen LIN')
                  .str.replace('Pin LAI', 'Pin-Ju LAI')
                  .replace('Aberdeen O', "Aberdeen O'DRISCOL")
                 )

country_conversion = {'NIR': 'IRL', 'WAL': 'GBR', 'GE1': 'GER', 'SCO': 'GBR', 'ENG': 'GBR', 'SIN': 'SGP', 'GE2': 'GER', 'IOM': 'GBR', 'EAI': 'CCS'} # addressing ineligible country codes
men['Olympic_Nation'] = men['Country'].apply(lambda country: country_conversion.get(country, country))
women['Olympic_Nation'] = women['Country'].apply(lambda country: country_conversion.get(country, country))

w_country_spec = {"Sydney BARROS": "PUR", "Teja BELAK": "SLO", "Halle HILTON": "IRL", "Madeleine MARSHALL": "NZL"} # specifying athletes who competed under multiple eligible countries
m_country_spec = {"Dominick CUNNINGHAM": "IRL", "Matthew MCCLYMONT": "JAM"}
men['Olympic_Nation'] = men.apply(lambda row: m_country_spec.get(row['Name'], row['Olympic_Nation']), axis=1)
women['Olympic_Nation'] = women.apply(lambda row: w_country_spec.get(row['Name'], row['Olympic_Nation']), axis=1)

women.to_csv('women.csv', index = False) # writing cleaned data to be used in next steps
men.to_csv('men.csv', index = False)