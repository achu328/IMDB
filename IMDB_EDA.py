import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql as db
import datetime as dt

st.title("IMDB Movies Data Analysis")
# Load data from the SQL database
# Connect to the database
db_cnct = db.connect(

        host = '127.0.0.1',
        port = 3306,
        database="mat1",
        user="mat",
        password='Durairaj@66'
)

curr = db_cnct.cursor()

query="""
select * from movies
"""
curr.execute(query)
data = curr.fetchall() 
columns = [desc[0] for desc in curr.description]
Data = pd.DataFrame(data, columns=columns)

r =st.sidebar.radio("Navigation",["Data Analysis","Data Filteration"]) # Radio button
if r=="Data Analysis":
        option = st.selectbox("Select a Visualization:", ["1. Top 10 Movies by Rating and Voting Counts", "Genre Distribution", "Average Duration by Genre","Averate Voting by Genre","Rating Distribution:","Genre-Based Rating Leaders:","Most Popular Genres by Voting:","Duration Extremes:","Ratings by Genre:","Correlation Analysis:"])
        if option == "1. Top 10 Movies by Rating and Voting Counts":
#Top 10 Movies by Rating and Voting Counts
                query="""
                select * from mat1.movies
                order by Voting desc, Rating desc;
                """
                curr.execute(query)
                data = curr.fetchall() 
                columns = [desc[0] for desc in curr.description]
                Q1 = pd.DataFrame(data, columns=columns)

                st.header("1. Top 10 Movies by Rating and Voting Counts")
                st.write(Q1.head(10))

        elif option == "Genre Distribution":
#Genre Distribution
                st.header("2.Genre Distribution")
                Genre_data = Data["Genre"].value_counts()
                st.bar_chart(Genre_data)

        elif option == "Average Duration by Genre":
#Average Duration by Genre
                st.header("3. Average Duration by Genre")
                Data['Duration'] = Data['Duration'].dt.total_seconds() / 60
                Genre_duration = Data.groupby("Genre")["Duration"].mean()
                st.bar_chart(Genre_duration)

        elif option == "Averate Voting by Genre":
#Averate Voting by Genre
                st.header("4. Average Voting by Genre")
                Genre_voting = Data.groupby("Genre")["Voting"].mean()   
                st.bar_chart(Genre_voting)

        elif option == "Rating Distribution:":
#Rating Distribution: 
                st.header("5. Rating Distribution")
                plt.hist(Data["Rating"], bins=100, color='Green', edgecolor='black')
                st.pyplot()

        elif option == "Genre-Based Rating Leaders:":
#Genre-Based Rating Leaders:
                st.header("6. Genre-Based Rating Leaders")
                Genre_rating = Data.loc[Data.groupby("Genre")["Rating"].idxmax()]
                Genre_rating[["Genre", "Title", "Rating"]]

        elif option == "Most Popular Genres by Voting:":
#Most Popular Genres by Voting: 
                st.header("7. Most Popular Genres by Voting")
                Genre_voting = Data.groupby("Genre")["Voting"].sum().sort_values(ascending=False)
                plt.pie(Genre_voting, labels=Genre_voting,)
                st.pyplot()

        elif option == "Duration Extremes:":
#Duration Extremes:      
                st.header("8. Duration Extremes")
                st.write("Shortest Movie: ", Data.loc[Data["Duration"].idxmin()]["Title"])
                st.write("Longest Movie: ", Data.loc[Data["Duration"].idxmax()]["Title"])
                Shortest_Movie = Data.loc[Data["Duration"].idxmin()]
                Longest_Movie =  Data.loc[Data["Duration"].idxmax()]
                st.table(pd.DataFrame([Shortest_Movie, Longest_Movie]))


        elif option == "Ratings by Genre:":
#Ratings by Genre:
                st.header("9. Ratings by Genre")
                genre_ratings = Data.groupby('Genre')['Rating'].mean().reset_index()
                heatmap_data = genre_ratings.pivot_table(values="Rating", index="Genre")
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".1f", ax=ax)
                ax.set_title("🎭 Average Ratings by Genre")
                ax.set_xlabel("Rating")
                ax.set_ylabel("Genre")
                st.pyplot(fig)


        elif option == "Correlation Analysis:":
# Correlation Analysis: 
                st.header("10. Correlation Analysis :Ratings vs Voting Counts")
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.scatterplot(x=Data['Voting'], y=Data['Rating'], ax=ax, color="blue")
                sns.regplot(x=Data['Voting'], y=Data['Rating'], scatter=False, ax=ax, color="red")
                ax.set_title("📊 Correlation Between Ratings and Voting Counts")
                ax.set_xlabel("Voting")
                ax.set_ylabel("Movie Rating")
                st.pyplot(fig)



elif r=="Data Filteration":

        Data["Duration"] = Data["Duration"].dt.total_seconds() / 60
        st.sidebar.header("Filter Movies")
        selected_genres = st.sidebar.multiselect("Select Genre", options=Data["Genre"].unique(), default=Data["Genre"].unique())
        min_rating, max_rating = st.sidebar.slider("IMDb Rating", min_value=float(Data["Rating"].min()), max_value=float(Data["Rating"].max()), value=(Data["Rating"].min(), Data["Rating"].max()))
        min_votes, max_votes = st.sidebar.slider("Minimum Voting Count", min_value=int(Data["Voting"].min()), max_value=int(Data["Voting"].max()), value=(Data["Voting"].min(), Data["Voting"].max()))
        duration_option = st.sidebar.radio("Select Duration", ["All", "< 2 Hours", "2-3 Hours", "> 3 Hours"])

        Filtered_Data= Data[Data["Genre"].isin(selected_genres)]
        Filtered_Data = Filtered_Data[(Filtered_Data["Rating"] >= min_rating) & (Filtered_Data["Rating"] <= max_rating)]
        Filtered_Data = Filtered_Data[(Filtered_Data["Voting"] >= min_votes) & (Filtered_Data["Voting"] <= max_votes)]

        if duration_option == "< 2 Hours":
                Filtered_Data = Filtered_Data[Data["Duration"] < 120]
        elif duration_option == "2-3 Hours":
                Filtered_Data = Filtered_Data[(Data["Duration"] >= 120) & (Data["Duration"] <= 180)]
        elif duration_option == "> 3 Hours":
                Filtered_Data = Filtered_Data[Data["Duration"] > 180]

        st.header("Filtered Movies")
        st.table(Filtered_Data)





