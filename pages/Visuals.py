# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import csv
import altair as alt
import plotly.express as px



# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Major Tourist Attractions in the U.S. 🗺")
tab1, tab2=st.tabs(["Major Tourist Attractions Information", "Popularity of Tourist Attractions"])

# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

with tab1:
    infile = open("united-states-landmarks.json")
    myData = json.load(infile)

#dynamic, simple
    st.header("Session State Scatter Plot")
    st.write("Shows each tourist attraction and it's Location")

    if "myData" not in st.session_state:
        st.session_state["myData"] = pd.read_json("united-states-landmarks.json")
    myData=st.session_state["myData"]

    options=st.multiselect(
        "Select City, State",
        myData["Location"].unique(),
        default=myData["Location"].unique()
    )

    if options:
        filteredData=myData[myData["Location"].isin(options)]
        st.scatter_chart(
            data=filteredData,
            x="Location",
            y="Tourist attraction"
        )

    st.divider()

#static, advanced
    st.header("Plotly Bar Chart")
    st.write("Shows each tourist attraction and the amount of visitors in millions")


    myData=pd.read_json("united-states-landmarks.json")
    fig=px.bar(myData, x='Tourist attraction', y='Visitors (millions)')
    st.plotly_chart(fig)





# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

with tab2:
#Dymnamic, basic
    st.header("Session State Bar Chart")
    st.write("Shows each persons rating for the chosen tourist attraction")

    infile2=open("data.csv")
    myData2=list(csv.reader(infile))

    if "myData2" not in st.session_state:
        st.session_state["myData2"]=pd.read_csv("data.csv")
    myData2=st.session_state["myData2"]

    options=st.selectbox(
        "Select a Tourist Attraction:",
        myData2["Category"].unique()
    )

    filteredData=myData2[myData2["Category"].isin([options])]

    if options:
        filteredData=myData2[myData2["Category"]==options]
        filteredData["Number"]=range(1, len(filteredData)+1)
        st.bar_chart(
            data=filteredData,
            x="Name",
            y="Value"
        )

    st.divider()

#Static, advanced
    st.header("Altair Scatter Plot")
    st.write("Shows each tourist attraction and the ratings it has received")
    df=pd.DataFrame(myData2)
    chart = alt.Chart(df).mark_circle().encode(
        x=alt.X("Category:N", title="Tourist Attraction"),
        y=alt.Y("Value:Q", title="Rating"),
        color="Category:N",
        size="Value:Q",
        tooltip=["Category", "Value"]
    ).properties(
        width=600,
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)






