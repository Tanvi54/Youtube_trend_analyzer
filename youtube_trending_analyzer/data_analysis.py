import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_data(df):
    df['title_length'] = df['title'].apply(len)
    df['likes_to_views'] = (df['likes'] / df['views']).fillna(0)

    # Title length distribution
    plt.figure(figsize=(8,4))
    sns.histplot(df['title_length'], kde=True, color='blue')
    plt.title("Distribution of Video Title Lengths")
    plt.savefig("plots/title_length_dist.png")
    plt.close()

    # Top channels
    top_channels = df['channel'].value_counts().head(10)
    plt.figure(figsize=(8,4))
    sns.barplot(x=top_channels.values, y=top_channels.index, palette="viridis")
    plt.title("Top 10 Channels in Trending")
    plt.savefig("plots/top_channels.png")
    plt.close()

    # Likes vs Views
    plt.figure(figsize=(6,4))
    sns.scatterplot(x='views', y='likes', data=df)
    plt.title("Likes vs Views")
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig("plots/likes_vs_views.png")
    plt.close()

    return df
