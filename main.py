import streamlit as st
import pandas as pd
from visualization import *
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def readData():
    Video_Games = pd.read_csv('vgsales.csv')
    Video_Games.rename(columns={'Platform':'Plateform'}, inplace=True)
    Video_Games['Year'] = Video_Games['Year'].fillna(0).astype('int')
    return Video_Games



df = readData()


sidebar = st.sidebar

sidebar.title('User Options')


def home():
    st.title("Video Game Sales Prediction")

    st.image('1.jpg')
    

def data():
    
    st.markdown("## Dataset View")
    st.dataframe(df)


    # Genre in various regions

    st.markdown("## Top Genre in Various Regions")
    genregion = st.selectbox("Select Regions", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    data = df.groupby('Genre', as_index=False).sum().sort_values('NA_Sales', ascending=False)
    #st.dataframe(data)
    fig = plotBar(data, 'Genre', genregion)
    st.plotly_chart(fig, use_container_width=True)


    # Top 10 Publishers in various regions

    st.markdown("## Top 10 Publishers in Various Regions")
    pubregion = st.selectbox("Select any Regions", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    data = df.groupby('Publisher', as_index=False).sum().sort_values('NA_Sales', ascending=False).head(10)
    
    fig = plotBar(data,'Publisher', pubregion)
    st.plotly_chart(fig, use_container_width=True)


    #Top 10 publishers in game count

    st.markdown("## Top 10 Publishers in Game Count ")
    gcregion = st.selectbox("Select one Regions", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    data = df.groupby('Publisher', as_index=False).count().sort_values('NA_Sales', ascending=False).head(10)

    fig = plotBar(data,'Publisher', gcregion)
    st.plotly_chart(fig, use_container_width=True)


    # Top 10 Video Games by Sales

    st.markdown('## Top 10 Publish Video Games by Sales')
    top_10_sales = st.selectbox("Select any option", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    data = df.groupby('Publisher', as_index=False).sum().sort_values('NA_Sales', ascending=False).head(10)

    fig = plotBar(data,'Publisher', top_10_sales)
    st.plotly_chart(fig, use_container_width=True)


    # No. of games published per year

    st.markdown('## Number of Games Published Per Year')
    data = df[df['Year'] != 0].groupby('Year', as_index=False).count()
    #st.dataframe(data)
    fig = plotLine(data, 'Year', 'Publisher')
    st.plotly_chart(fig, use_container_width=True)

 
    # Most popular Genre
    st.markdown('## Most Popular Genre Globally')
    data1 = df.groupby('Genre', as_index=False).count()
    fig= px.pie(data1, labels='Genre', values='Rank', names='Genre')

    data3 = df[df['Year']!=0].groupby('Year', as_index=False).sum()
    st.plotly_chart(fig, use_container_width=True)

    
    # Various Sales in years according to their Regions
    
    st.markdown('## Sales in Various Regions')
    data = df[df['Year'] != 0].groupby('Year', as_index=False).count()
    px.line(data, 'Year', 'Name')

    fig = go.Figure()
    fig.add_trace(go.Line(x = data3.Year, y = data3.NA_Sales, name="NA Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.EU_Sales, name="EU Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.JP_Sales, name="JP Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.Other_Sales, name="Other Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.Global_Sales, name="Global Sales"))
    st.plotly_chart(fig, use_container_width=True)

def execute():
    
    #Predict

    st.markdown("## Sales in Various Regions")
    start, end = st.slider("Double Ended Slider",value=[2005,2008], min_value=1980, max_value=2020)
    selRegion = st.selectbox("Select Region", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    year_count = (i for i in range(start,end))
    count_in_range = df.loc[df['Year'].isin(year_count)] 
    ns = sum(count_in_range[selRegion])
    st.header(round(ns))
    
    plt.figure(figsize=(8, 6))
    plt.bar(count_in_range['Year'], count_in_range[selRegion])
    plt.xlabel('Year')
    plt.ylabel(selRegion)
    plt.title(f'{selRegion} Over Time')
    plt.grid(True)
    st.pyplot(plt)

    #top 10 game sales

    st.markdown('## Top 10 Video Games by Sales in Selected Range')
    top_10_games = df.loc[(df['Year'] >= start) & (df['Year'] <= end)].groupby('Name').sum().nlargest(10, 'Global_Sales')
    top_10_games.reset_index(inplace=True)
    fig = px.bar(top_10_games, x='Name', y='Global_Sales', labels={'Name': 'Game Name', 'Global_Sales': 'Global Sales'})
    fig.update_layout(xaxis_title='Game Name', yaxis_title='Global Sales', title='Top 10 Video Games by Sales')
    st.plotly_chart(fig, use_container_width=True)


options = ['Home', 'Data', 'Execute']

selOption = sidebar.selectbox("Select an Option", options)

if selOption == options[0]:
    home()
elif selOption == options[1]:
    data()
elif selOption == options[2]:
    execute()
