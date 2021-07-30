import streamlit as st
import pandas as pd
import numpy as np
import formulas as f
import base64
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image


# Intro
image = Image.open('logo_fcbs.png')
st.image(image, use_column_width=True)
st.title(' FCBS DH Advanced Analytics')
st.subheader(' Team Stats')
st.sidebar.header('Player List')


# TEAM STATS

# woba weights - using D3 weights from 2019
bb_w = 0.78
hbp_w = 0.81
s_w = 0.97
do_w = 1.39
tr_w = 1.69
hr_w = 2.02

 # woba scale
woba_scale = ((bb_w+hbp_w+s_w+do_w+tr_w+hr_w)/6)

# Teams web scraping stats

def load_teams_data(woba_scale):

    '''
    This function scraps data from a web site 
    transform the retrieved table and returns a
    table with updated fields
    '''
    global totals
    # Web scraping stats
    teams_totals_url = 'http://www.fcbs.cat/campionat/2021/b_dh/stats/lgteams.htm'
    totals_df = pd.read_html(teams_totals_url, index_col=0)
    hitting_table = totals_df[1]
    hitting_table_new_header = hitting_table.iloc[0]
    hitting_table = hitting_table[1:]
    hitting_table.columns = hitting_table_new_header
    # Data Transformation
    hitting_table[['sb','sb_att']] = hitting_table['sb-att'].str.split('-',expand=True)
    hitting_table.drop(['sb-att'], axis=1, inplace=True)
    hitting_table[['G','bb', 'hbp', 'h', '2b', '3b', 'hr', 'ab', 'sf', 'r', 'so', 'sb','sb_att', 'sh' ]] = hitting_table[['G', 'bb', 'hbp', 'h', '2b', '3b', 'hr', 'ab', 'sf', 'r', 'so', 'sb','sb_att', 'sh']].astype(int)
    # Singles columns
    hitting_table['1b'] = hitting_table['h'] - (hitting_table['2b'] + hitting_table['3b'] + hitting_table['hr'])
    # Plate appearance column
    hitting_table['pa'] = (hitting_table['ab'] - hitting_table['h']) + hitting_table['h'] + hitting_table['bb'] + hitting_table['hbp'] + hitting_table['sf'] + hitting_table['sh']    
    # Selecting totals row
    totals = hitting_table.loc['Totals':]
    # Build new df 
    teams_stats = hitting_table.copy()
    #teams = ['CB Barcelona', 'Sant Boi', 'Viladecans', 'Gava', 'Totals']
    #teams_stats['Teams'] = teams
    #teams_col = teams_stats['Teams']
    #teams_stats.drop(labels=['Teams'], axis=1, inplace=True)
    #teams_stats.insert(0, 'Teams', teams_col)
    #teams_stats.columns.name=None
    #teams_stats.reset_index(drop=True)
    return teams_stats
teams_stats = load_teams_data(woba_scale)

# FORMULAS FOR ADVANCED ANALYTICS COLUMNS (TEAMS)

# calling and applying woba function to the teams df
f.league_woba(teams_stats)
league_woba = f.league_woba(totals)

# calling league runs function
f.league_runs_pa(teams_stats)
league_runs = f.league_runs_pa(totals)

# applying league woba to team stats
teams_stats["wOBA"] = teams_stats.apply(f.league_woba, axis=1)

# applying wRAA to team stats
f.wraa_col(teams_stats, league_woba, woba_scale)
teams_stats["wRAA"] = teams_stats.apply(f.wraa_col, args=(league_woba, woba_scale), axis=1)

# applying wRC to team stats
f.wrc_col(teams_stats, league_woba, woba_scale, league_runs)
teams_stats["wRC"] = teams_stats.apply(f.wrc_col, args=(league_woba, woba_scale, league_runs), axis=1)

# applying OPS to team stats
f.ops_col(teams_stats)
teams_stats["OPS"] = teams_stats.apply(f.ops_col, axis=1)

# applying ISO to team stats
f.iso_col(teams_stats)
teams_stats["ISO"] = teams_stats.apply(f.iso_col, axis=1)

# applying BABIP to team stats
f.babip_col(teams_stats)
teams_stats["BABIP"] = teams_stats.apply(f.babip_col, axis=1)

# applying SO% to team stats
f.k_percentage(teams_stats)
teams_stats["SO%"] = teams_stats.apply(f.k_percentage, axis=1)

# applying BB% to team stats
f.bb_percentage(teams_stats)
teams_stats["BB%"] = teams_stats.apply(f.bb_percentage, axis=1)

# Displaying Teams DF
st.dataframe(teams_stats.style.format({'wOBA':'{:.3f}', 'wRAA':'{:.0f}', 'wRC':'{:.0f}', 'OPS':'{:.3f}', 'ISO':'{:.3f}', 'BABIP':'{:.3f}', 'SO%':'{:.2f}', 'BB%':'{:.2f}'}))


# Players Web scraping stats
@st.cache(allow_output_mutation=True)
def load_player_data():
    #global dh_individual_hitting
    # hitting stats
    individuals_url = 'http://www.fcbs.cat/campionat/2021/b_dh/stats/lgplyrs.htm'

    hitting_individual_df = pd.read_html(individuals_url)

    # droping rows with all nan
    dh_individual_hitting = hitting_individual_df[1].dropna(thresh=19)
    dh_individual_hitting.drop(64, inplace=True)

    # updating the headers
    new_header = dh_individual_hitting.iloc[0]
    dh_individual_hitting = dh_individual_hitting[1:]
    dh_individual_hitting.columns = new_header

    # splitting player column in two to have player name and team in two different columns
    dh_individual_hitting[['Jugador','Equip']] = dh_individual_hitting['Player'].str.split(',',expand=True)
    dh_individual_hitting[['gp','gs']] = dh_individual_hitting['gp-gs'].str.split('-',expand=True)
    dh_individual_hitting[['sb','sb_att']] = dh_individual_hitting['sb-att'].str.split('-',expand=True)

    # converting dtypes
    dh_individual_hitting[['gp','rbi', 'tb', 'gdp', 'sh', 'bb', 'hbp', 'h', '2b', '3b', 'hr', 'ab', 'sf', 'r', 'so' ]] = dh_individual_hitting[['gp', 'rbi', 'tb', 'gdp', 'sh', 'bb', 'hbp', 'h', '2b', '3b', 'hr', 'ab', 'sf', 'r', 'so' ]].astype(int)

    # singles columns
    dh_individual_hitting['1b'] = dh_individual_hitting['h'] - (dh_individual_hitting['2b'] + dh_individual_hitting['3b'] + dh_individual_hitting['hr'])

    # plate appearance column
    dh_individual_hitting['pa'] = (dh_individual_hitting['ab'] - dh_individual_hitting['h']) + dh_individual_hitting['h'] + dh_individual_hitting['bb'] + dh_individual_hitting['hbp'] + dh_individual_hitting['sf'] + dh_individual_hitting['sh']

    # re-arrenging columns
    dh_individual_hitting = dh_individual_hitting[['Jugador', 'Equip', 'avg', 'gp', 'gs', 'ab', 'pa', 'r', 'h', '1b', '2b', '3b', 'hr', 'rbi', 'tb', 'slg%', 'bb', 'hbp', 'so', 'gdp', 'ob%', 'sf', 'sh', 'sb', 'sb_att']]
    return dh_individual_hitting
dh_individual_hitting = load_player_data()


# FORMULAS FOR ADVANCED ANALYTICS COLUMNS (PLAYERS)

# wOBA
# calling and applying woba function to individual players
f.individual_woba(dh_individual_hitting)
dh_individual_hitting["wOBA"] = dh_individual_hitting.apply(f.individual_woba, axis=1)

# wRAA
f.wraa_col(dh_individual_hitting, league_woba, woba_scale)
dh_individual_hitting["wRAA"] = dh_individual_hitting.apply(f.wraa_col, args=(league_woba, woba_scale), axis=1)

# wRC
f.wrc_col(dh_individual_hitting, league_woba, woba_scale, league_runs)
dh_individual_hitting["wRC"] = dh_individual_hitting.apply(f.wrc_col, args=(league_woba, woba_scale, league_runs), axis=1)

# OPS
f.ops_col(dh_individual_hitting)
dh_individual_hitting["OPS"] = dh_individual_hitting.apply(f.ops_col, axis=1)

# ISO
f.iso_col(dh_individual_hitting)
dh_individual_hitting["ISO"] = dh_individual_hitting.apply(f.iso_col, axis=1)

# BABIP
f.babip_col(dh_individual_hitting)
dh_individual_hitting["BABIP"] = dh_individual_hitting.apply(f.babip_col, axis=1)

# SO%
f.k_percentage(dh_individual_hitting)
dh_individual_hitting["SO%"] = dh_individual_hitting.apply(f.k_percentage, axis=1)

# BB%
dh_individual_hitting["BB%"] = dh_individual_hitting.apply(f.bb_percentage, axis=1)


# Streamlit App Features

# Sidebar - Team selection
#sorted_unique_team = sorted(dh_individual_hitting.Equip.unique())
#selected_team = st.sidebar.multiselect('Select Team', sorted_unique_team)

# Sidebar - Player selection 
sorted_unique_player = sorted(dh_individual_hitting.Jugador.unique())
selected_player = st.sidebar.multiselect('Select the player/s that you want to compare', sorted_unique_player)

# Filtering data
df_selected_player = dh_individual_hitting[(dh_individual_hitting.Jugador.isin(selected_player))]

# df_selected_team = dh_individual_hitting[(dh_individual_hitting.Equip.isin(selected_team))]


st.header('Display Stats of Selected Player(s)')
st.write('Data Dimension: ' + str(df_selected_player.shape[0]) + ' rows and ' + str(df_selected_player.shape[1]) + ' columns.')
st.dataframe(df_selected_player.style.format({'wOBA':'{:.3f}', 'wRAA':'{:.0f}', 'wRC':'{:.0f}', 'OPS':'{:.3f}', 'ISO':'{:.3f}', 'BABIP':'{:.3f}', 'SO%':'{:.2f}', 'BB%':'{:.2f}'}))

# Charts

st.subheader('Correlation between wOBA and OPS')
fig1 = plt.figure()
sns.scatterplot(data=df_selected_player, x='wOBA', y='OPS', hue='Jugador')
st.pyplot(fig1)


# Additional Info

st.markdown('___')
about = st.beta_expander('About/Additional Info')
with about:
        ''' 
        **wOBA** - Is a version of on-base percentage that accounts for how a player reached base 
        -- instead of simply considering whether a player reached base. The value for each method of reaching 
        base is determined by how much that event is worth in relation to projected runs scored. Unlike on-base 
        percentage and OPS (OBP + SLG), wOBA assigns value to each method of reaching base, in terms of its impact on scoring runs.

        **wRAA** - Measures the number of offensive runs a player contributes to their team compared to the average player.
        A wRAA of zero is league-average, so a positive wRAA value denotes above-average performance and a negative wRAA denotes below-average performance.

        **wRC** - Quantifies a player’s total offensive value and measure it by runs. Is a cumulative statistic that credits a player for total production rather than on 
        an at bat by at bat basis. 

        **OPS** - Adds on-base percentage and slugging percentage to get one number that unites the two. It's meant to combine how well a hitter can reach base, with how 
        well he can hit for average and for power.

        **ISO** - Is a measure of a hitter’s raw power and tells you how often a player hits for extra bases. Is a quick tool for determining the degree 
        to which a given hitter provides extra base hits as opposed to singles.

        **BABIP** - Measures how often a ball in play goes for a hit.

        **SO%** - Represents the frequency with which a batter strikes out.

        **BB%** - Represents the frequency with which a batter gets on base via a walk. 

        '''