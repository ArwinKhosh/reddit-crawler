import matplotlib.pyplot as plt  
import pandas as pd  
import seaborn as sns

####

def plot_trends(df):
    #this small function plots the trends seen in the main ticker df

    sns.lineplot(data=df, x=df.index, y=df.columns)

