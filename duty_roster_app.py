import streamlit as st
import pandas as pd 
import os
import datetime
import sqlite3

conn=sqlite3.connect("House_members.db")
Members=pd.read_sql("SELECT * FROM Members", conn)
time_diff=datetime.timedelta(days=7)
anino=datetime.date(2021,1,2)
dates=[anino+(i*time_diff) for i in range(20)]

dates=list(map(lambda x:x.strftime(format="%m/%d/%Y"), dates))

roster={name:[] for name in Members.name}

for i in range(len(dates)):
    roster[Members.name[i%len(Members.name)]].append(dates[i]) 

Fin=pd.DataFrame(roster)

st.title("Duty Roster")

st.markdown("<p><strong>Find out who is scrubbing.</strong></p>", unsafe_allow_html=True)
chosen_date=st.date_input("Select Date:")
date_today=datetime.date.today()
next_saturday=date_today+datetime.timedelta((5-date_today.weekday())%7)
next_scrub=chosen_date+datetime.timedelta((5-chosen_date.weekday())%7)
if chosen_date<datetime.date.today():
    st.write("Invalid date! Please choose a date on or after today.")
else:
    st.markdown("<p><strong>Next scrub day from chosen day:</strong> {}</p>".format(next_scrub),True)
    st.markdown("<p><strong>Person in-charge:</strong> {}</p>".format(max(roster.keys(), key=lambda x: roster[x].count(next_scrub.strftime(format="%m/%d/%Y")))), True)


if st.checkbox("Show Roster",value=True):
    st.write(Fin)
    st.markdown("<p><strong>Next Scrub Day From Today</strong></p>", True)
    st.markdown("<p><strong>{}</strong>: {}</p>".format(next_saturday,max(roster.keys(), key=lambda x: roster[x].count(next_saturday.strftime(format="%m/%d/%Y")))),True)
    



