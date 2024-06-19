import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
import numpy as np
from sklearn.linear_model import LinearRegression 

lr = LinearRegression()

data = pd.read_csv("Salary_Data.csv")
x = np.array(data["YearsExperience"]).reshape(-1,1)

lr.fit(x,np.array(data["Salary"]))

st.title("Salary Prediction")

st.image("https://blog.schoolforai.com/content/images/size/w2000/2021/12/Salary-pred.png", width= 800)
nav = st.sidebar.radio("Navigation",["Home","Prediction","Contribute"])

if nav == "Home":
    
    st.write("Home")

    if st.checkbox("show table"):
        st.table(data)
    
    graph = st.selectbox("What kind of graph ?", ["Non-interactive","interactive"])

    val = st.slider("Filter data using years",0,20)
    data = data.loc[data["YearsExperience"]>= val]
    if graph == "Non-interactive":
        plt.figure(figsize= (10,5))
        plt.scatter(data["YearsExperience"],data["Salary"])
        plt.ylim(0)
        plt.xlabel("year of experince")
        plt.ylabel("salary")
        plt.tight_layout()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    if graph == "interactive":
        layout = go.Layout(
            xaxis = dict(range=[0,16]),
            yaxis = dict(range =[0,210000])
        )
        fig = go.Figure(data=go.Scatter(x=data["YearsExperience"], y=data["Salary"], mode='markers'),layout = layout)
        st.plotly_chart(fig)
        


if nav == "Prediction":
    st.header("Know your salary")
    val = st.number_input("Enter you experince",0.00,20.00, step= 0.25)
    val = np.array(val).reshape(1,-1)
    pred = lr.predict(val)[0]

    if st.button("Predict"):
        st.success(f"your predicted salary is {round(pred)}")

if nav == "Contribute":
    st.header("Contribute to our dataset")
    ex = st.number_input("Enter your experince",0.0,20.0)
    sal = st.number_input("Enter your salary",0,1000000,step=1000)

    if st.button("Submit"):
        to_add = {
            "YearsExperince":[ex], 
            "salary": [sal]
        }

        to_add = pd.DataFrame(to_add)
        to_add.to_csv("Salary_Data.csv",mode = "a", header = False, index = False )
        st.success("Submitted")
