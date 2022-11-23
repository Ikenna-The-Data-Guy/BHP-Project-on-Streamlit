import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def is_float(x):
    try:
        float(x)
    except:
        return False
    return True


def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0])+float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None


def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out


def remove_BHK_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        BHK_stats = {}
        for BHK, BHK_df in location_df.groupby('BHK'):
            BHK_stats[BHK] = {
                'mean': np.mean(BHK_df.price_per_sqft),
                'std': np.std(BHK_df.price_per_sqft),
                'count': BHK_df.shape[0]
            }
        for BHK, BHK_df in location_df.groupby('BHK'):
            stats = BHK_stats.get(BHK-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, BHK_df[BHK_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')



@st.cache
def load_data():
    df1 = pd.read_csv(r"C:\Users\USER\Downloads\datasets_20710_26737_Bengaluru_House_Data.csv")
    df2 = df1.drop(['area_type','availability','society','balcony'],axis='columns')
    df3 = df2.dropna()
    df3['BHK'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))
    df4 = df3.copy()
    df4['total_sqft'] = df4['total_sqft'].apply(convert_sqft_to_num)
    df5 = df4.copy()
    df5['price_per_sqft'] = df5['price']*100000/df5['total_sqft']
    location_stats = df5.groupby('location')['location'].agg('count').sort_values(ascending=False)
    location_stats_less_than_10 = location_stats[location_stats<=10]
    df5.location = df5.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
    df6 = df5[~(df5.total_sqft/df5.BHK<300)]
    df7 = remove_pps_outliers(df6)
    df8 = remove_BHK_outliers(df7)
    df9 = df8[df8.bath<df8.BHK+2]
    df10 = df9.drop(['size','price_per_sqft'],axis='columns')


    return df10
    

    
df10 = load_data()


def show_explore_page_bhp():
    st.title("Explore Bengalore Home Prices")



    st.write(
        """
        ### Bengalore Home Price Data 2021
        """
    )

    data = df10["location"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  #Equal aspects ratio ensures that pie is drawn as a circle.


    st.write("""#### Data from Different Locations""")

    st.pyplot(fig1)

    st.write("""#### Mean Price Based on Location""")

    data = df10.groupby(["location"])['price'].mean().sort_values(ascending=True)
    st.bar_chart(data)


    st.write("""#### Mean Price Based on Property Size""")

    data = df10.groupby(["total_sqft"])['price'].mean().sort_values(ascending=True)
    st.line_chart(data)

    