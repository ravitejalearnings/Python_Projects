import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
import numpy as np
import random
import altair
import time
import datetime


# title
st.title("My streamlit learnings")
st.divider()

# header
st.header("this is a header function")
st.divider()

#subheader
st.subheader("this is a subheader function")
st.divider()

#markdown
st.markdown("this is a markdown text")
st.markdown("""
    # h1 tag
    ## h2 tag
    ### h3 tag
    """)
st.markdown("bold: this is not bold")
st.markdown(""" **bold**: this is bold """)
st.markdown("""_italic_: this is italic""")
st.divider()

#write
st.write("this is a text function")
st.write("_italic_: this is italic")
st.write("**bold**: this is bold")
st.write("# Ravi","learning","_**streamlit**_")
st.write("## Ravi","learning","_**streamlit**_")
st.divider()

# data
a = [1,2,3,4,5,6] # list
n = np.array(a) # convert to array
nd = n.reshape([3,2]) # convert to nd arracy
st.write(nd) # view data like df



# def function_part2():
dict = {"col_name":[1,2,3,4,5,6,7,8,9,10,11,12]}
st.write(dict)
st.dataframe(dict)
st.divider()

st.write("data visualization")
data = pd.DataFrame(np.random.randn(100,3),
                    columns=['a','b','c'])
st.write(data)

st.header("line chart")
st.line_chart(data)
st.divider()

st.header("bar chart")
st.bar_chart(data)
st.divider()

st.header("area chart")
st.area_chart(data)
st.divider()

st.header("display charts in column format")
linechart,bar_chart,area_chart = st.columns(3)
with linechart:
    st.subheader("line chart")
    st.line_chart(data)
with bar_chart:
    st.subheader("bar chart")
    st.bar_chart(data)
with area_chart:
    st.subheader("area chart")
    st.area_chart(data)
st.divider()

st.header("flowchart like visual")
st.graphviz_chart("""
digraph {
    rankdir=LR
    watch -> like
    like -> subscribe;
    subscribe-> hit_bell_icon
}
""")
st.divider()

st.header("Insert Images")
st.image(r"C:\Users\aravit01\Downloads\Used-Car-Prices.jpg", width=500)
st.divider()

st.header("Insert Video")
st.video("https://www.youtube.com/watch?v=O2Cw82YR5Bo&t=792s")
st.divider()

st.header("Insert Auido")
st.divider()

st.header("Widgets")
st.subheader("Buttons")
st.subheader("number_input")
#
# def function_part3():
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("enter number")
with col2:
    b = st.number_input("enter number ")
result = a + b
if st.button("click to view results"):
    st.write(result)
st.divider()

st.subheader("text_input")
text = st.text_input("enter text")
if st.button("click to view text input"):
    st.write(text)
st.divider()

st.subheader("date_input")
date = st.date_input("enter date")
if st.button("click to view selected date"):
    st.write(date)
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("start date")
with col2:
    end_date = st.date_input("end date")
if st.button("click to view diff days"):
    diff_days = end_date - start_date
    st.write(diff_days)
st.divider()

st.subheader("time_input")
time = st.time_input("enter time")
st.write(time)
st.divider()

st.subheader("add checkbox")
if st.checkbox("I agree to T&C"):
    st.button("Thankyou & Continue ➡️")
else:
    st.button("View T&C ⤴️")
st.divider()

st.subheader("Radio button")
radio_selection = st.radio("Select list elements", ['element1','element2','element3'])
if st.button('view radio selection'):
    st.write(radio_selection)
st.divider()

st.subheader("select box")
selected_element = st.selectbox("Select list elements", ['element1','element2','element3'])
if st.button('view selected element'):
    st.write(selected_element)
st.divider()

st.subheader("Multi select")
multi_select_element = st.multiselect("Select list elements", ['element1','element2','element3'])
if st.button('view multi-selected element'):
    st.write(multi_select_element)
st.divider()

st.subheader("slider")
age_slider = st.slider("age_slider", min_value=18, max_value=65, step=1)
st.write(age_slider)
st.divider()

col1, col2,col3 = st.columns(3)
with col1:
    start_date = st.date_input("start_date")
with col2:
    end_date = st.date_input("end_date")
date_slider = st.slider("date range", min_value=start_date, max_value=end_date)
st.write(date_slider)
st.divider()

st.subheader("upload file")
image = st.file_uploader("upload a file")
if image is None:
    st.write("No image is uploaded")
else:
    st.image(image, use_column_width=True)
st.divider()

st.sidebar.title("side bar")
st.sidebar.header("page navigation")
radio_functionality = st.sidebar.radio("radio feature",["part1","part2","part3"])
if radio_functionality == "part1":
    "page 1 report"
elif radio_functionality == "part2":
    "page 2 report"
elif radio_functionality == "part3":
    "page 3 report"
st.sidebar.divider()

select_functionality = st.sidebar.selectbox("select box feature",["part1","part2","part3"])
if select_functionality == "part1":
    "page 1 report"
elif select_functionality == "part2":
    "page 2 report"
elif select_functionality == "part3":
    "page 3 report"
st.sidebar.divider()
st.divider()

st.header("display different msgs")
st.error("show error msg")
st.success("show sucess msg")
st.info("show information")
st.exception(RuntimeError("this is runtime error"))
st.warning("show warning")
st.divider()

st.header("display progress bar")
progress = st.progress(0)
for i in range(100):
    # time.sleep(0.1)
    progress.progress(i+1)
st.divider()

st.header("layouts")
row1 = st.columns(2)
row2 = st.columns(3)
row3 = st.columns([3,1])
row4 = st.columns(3)

col1, col2 = st.columns(2)
with row1[0]:
    col1_input = st.text_input("first_name")
with row1[1]:
    col2_input = st.text_input("last_name")
with row2[0]:
    col1_input = st.text_input("gender")
with row2[1]:
    col2_input = st.number_input("age",  min_value=18, max_value=100,step=1)
with row2[2]:
    col2_input = st.number_input("salary", min_value=10000.00, max_value=5000000.00, step=1000.00)
with row3[0]:
    col1_input = st.text_input("custom feild")
with row4[0]:
    col1_input = st.text_input("username")
with row4[1]:
    col2_input = st.text_input("password", type="password")
with row4[2]:
    col3_input = st.text_input("re-enter password", type="password")

status = st.checkbox("Click to agree terms & conditions")
if status:
    st.button("Submit")
else:
    st.button("agree terms & conditions")




