import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'  # Great Unicode font
import plotly.express as px
from youtube_api import get_trending_videos

st.set_page_config(page_title="YouTube Trending Analyzer", layout="wide")

st.title("📊 YouTube Trending Video Analyzer")
st.markdown("Explore what makes videos trend: **views, likes, categories, channels & more**")

# Load or fetch data
if st.button("🔄 Fetch Latest Trending Data"):
    df = get_trending_videos()
else:
    df = pd.read_csv("trending_data.csv")

if df.empty:
    st.warning("No data available. Please click 'Fetch Latest Trending Data'.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect("Select Categories", options=df['category'].unique(), default=df['category'].unique())
channel_filter = st.sidebar.text_input("Search Channel Name")

filtered_df = df[df['category'].isin(category_filter)]
if channel_filter:
    filtered_df = filtered_df[filtered_df['channel'].str.contains(channel_filter, case=False)]

st.write(f"### Showing {len(filtered_df)} videos")
st.dataframe(filtered_df[['title','channel','category','views','likes','comments','publish_time']])

# Plotly charts
st.subheader("Top 10 Channels by Trending Videos")
top_channels = filtered_df['channel'].value_counts().head(10)
fig1 = px.bar(top_channels, x=top_channels.values, y=top_channels.index, orientation='h',
              labels={'x': 'Number of Videos', 'y': 'Channel'}, color=top_channels.values,
              color_continuous_scale='viridis')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Views vs Likes (Interactive)")
fig2 = px.scatter(filtered_df, x='views', y='likes', color='category', size='comments',
                  hover_data=['title', 'channel'], log_x=True, log_y=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Distribution of Video Title Lengths")
filtered_df['title_length'] = filtered_df['title'].apply(len)
fig3 = px.histogram(filtered_df, x='title_length', nbins=30, marginal='box', color_discrete_sequence=['#1DB954'])
st.plotly_chart(fig3, use_container_width=True)
