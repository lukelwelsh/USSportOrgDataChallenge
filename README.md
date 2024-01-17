# U.S. Sport Organization
Data Challenge with the U.S. Sport Organization

This project provides insights towards which five USA gymnasts should be chosen to represent the country for the 2024 Olympic games in artistic gymnastics. Through the use of Monte Carlo simulation, many different possible lineups are assessed against the prospective field of competitors in order to simulate the format of the Olympic competition.

## Description of Workings of Different Files:

data_2022_2023.csv: All data with which to base analysis on

clean.py: Starting with data_2022_2023.csv, cleans data to remove any inconsistencies. Outputs 2 files: men.csv and women.csv, each the same format as data_2022_2023.csv, but with added Name column and fixes to inconsistent data

obj.py: contains classes which are used to organize various athletes and countries. Imported and used in men/women_compile.ipynb and men/women_sim.ipynb

men/women_compile.ipynb: Starting with respective men.csv and women.csv from clean.py, incorporates qualifying rules to ultimately output m/w_sims.csv, which contains 100 qualifying simulation scores for each apparatus that each of the 91 non-USA athletes are estimated to compete in. 

men/women_sim.ipynb: First determines eligible USA athletes with which to consider for a potential team. Then, using m/w_sims.csv for each possible combination of these eligible athletes, simulates 10,000 complete Olympic competitions and calculates medals earned for each lineup combination. Outputs men/women_medals.csv, which contains a row for each possible combination of USA athletes, along with the amount of medals they would win in each category over 10,000 simulations.

men/women_sim.py: Functions used in men/women_sim.ipynb in order to output simulated medal results for the USA, starting with the qualifying rounds. 

medal_summary.ipynb: Starting with men/women_medals from men/women_sim.ipynb, creates a table with the top lineup of athletes according to 5 logical criteria for success in the form of medal counts.
