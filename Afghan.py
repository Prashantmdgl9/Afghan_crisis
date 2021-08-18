import pandas as pd
import turicreate as tc
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from turicreate import SFrame

alt.renderers.enable('mimetype')
alt.renderers.enable('altair_viewer')

df_l = pd.read_csv("data_gtd_2.csv", encoding='ISO-8859-1')

sf = tc.SFrame.read_csv('data_gtd_af_2.csv')
sf.shape
sf.column_names

columns = ['iyear', 'imonth', 'country_txt', 'region_txt', 'provstate', 'city', 'success', 'attacktype1_txt', 'targtype1_txt', 'targsubtype1_txt', 'corp1', 'target1', 'natlty1_txt', 'gname', 'motive',
            'weapdetail', 'nkill', 'nwound', 'summary' ]

sf_a = sf[columns]
sf_a.head(3)

sf_tmp = sf_a.groupby('iyear', tc.aggregate.COUNT())
sf_tmp.sort('iyear', ascending = True)
tc.visualization.set_target(target='browser')

source = sf_tmp.to_dataframe()



alt.Chart(source).mark_bar(color='#808080').encode(
    x=alt.X("iyear:O", axis=alt.Axis(title='Years')),
    y=alt.Y('Count:Q', axis=alt.Axis(title='Number of attacks'))
).properties(height=400, width = 600, title='Terror attacks in Afghanistan since 1970')


sf_tmp = sf_a.groupby('attacktype1_txt', tc.aggregate.COUNT())
sf_tmp

source = sf_tmp.to_dataframe()

alt.Chart(source).mark_bar(color='#003153').encode(
    y=alt.Y("attacktype1_txt:O", sort = '-x', axis=alt.Axis(title='Attack type')),
    x=alt.X('Count:Q', axis=alt.Axis(title='Number of attacks'))
).properties(height=400, width = 600, title='Types of attacks in Afghanistan by extremists')

sf_tmp = sf_a.groupby('targtype1_txt', tc.aggregate.COUNT())
sf_tmp

source = sf_tmp.to_dataframe()

alt.Chart(source).mark_bar(color='#ffa500').encode(
    y=alt.Y("targtype1_txt:O", sort = '-x', axis=alt.Axis(title='Victims')),
    x=alt.X('Count:Q', axis=alt.Axis(title='Number of attacks'))
).properties(height=400, width = 600, title='Preferred targets')

sf_tmp = sf_a.groupby('iyear', tc.aggregate.SUM('nkill'), tc.aggregate.COUNT())
sf_tmp


source = sf_tmp.to_dataframe()

alt.Chart(source).mark_line(color='#ff0000').encode(
    x=alt.X("iyear:O", axis=alt.Axis(title='Years')),
    y=alt.Y('Sum of nkill:Q', axis=alt.Axis(title='Number of deaths'))
).properties(height=400, width = 600, title='Number of people killed in the attacks')

sf_tmp = sf_a.groupby('gname', tc.aggregate.SUM('nkill')).sort('Sum of nkill', ascending = False)
sf_tmp
source = sf_tmp.to_dataframe()


alt.Chart(source[0:25]).mark_bar(color='#808080').encode(
    x=alt.X("gname:O", sort = '-y', axis=alt.Axis(title='Terrorist organisation')),
    y=alt.Y('Sum of nkill:Q', axis=alt.Axis(title='Deaths caused by the group')),
    color=alt.condition(
        alt.datum.gname == "Taliban",  #
        alt.value('red'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(height=400, width = 600, title='Most notorious groups')

sf_tmp = sf_a.groupby('iyear', tc.aggregate.FREQ_COUNT('gname'))
sf_tmp = sf_tmp.unpack()
source = sf_tmp.to_dataframe()
cols = ['iyear', 'Taliban']
source =  source[cols]
source

alt.Chart(source).mark_line().encode(
    x=alt.X("iyear:O", axis=alt.Axis(title='Years')),
    y=alt.Y('Taliban', axis=alt.Axis(title='Number of attacks'))
).properties(height=400, width = 600, title="Taliban's activity over the years")

sf_a.groupby('motive', tc.aggregate.COUNT())
