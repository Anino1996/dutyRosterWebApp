import streamlit as st
import pandas as pd 
import os
import datetime
import sqlite3

#############################################################
# This program reads member infomation from a db and finds  #
# the next in line to scrub based on the next saturday      #
#############################################################

# Connect to the house members database
conn=sqlite3.connect("House_members.db")


# Read the house_members data into a pandas dataframe
Members=pd.read_sql("SELECT * FROM Members", conn)

# Set a standard time difference between scrub days (Weekly)
time_diff=datetime.timedelta(days=7)

# Set an arbitrary start date from which scrub days are displayed
anino=datetime.date(2021,1,2)

# Generate 20 weeks' worth of dates starting from start date
dates=[anino+(i*time_diff) for i in range(20)]
dates=list(map(lambda x:x.strftime(format="%m/%d/%Y"), dates))


# Define dictionary to contain member names and their corresponding dates
roster={name:[] for name in Members.name}

for i in range(len(dates)):
    roster[Members.name[i%len(Members.name)]].append(dates[i]) 

# Create a dataframe containing all members and their corresponding scrub dates
# Column name -> Member name
# Values -> Scrub date
Fin=pd.DataFrame(roster)

#######################################################################
#							Streamlit implementation				  #
#######################################################################	

st.title("Duty Roster for 933 Oaklawn Avenue")

st.markdown("<p><strong>Find out who is scrubbing.</strong></p>", unsafe_allow_html=True)

# Date input to take date selection based on which next scrubber is determined
chosen_date=st.date_input("Select Date:")

# Calculate  date for next Saturday from chosen day
next_scrub=chosen_date+datetime.timedelta((5-chosen_date.weekday())%7)

# Find next scrub date from present day
date_today=datetime.date.today()
next_saturday=date_today+datetime.timedelta((5-date_today.weekday())%7)


# Ensure that the chosen date isn't in the past
if chosen_date<datetime.date.today():
    st.write("Invalid date! Please choose a date on or after today.")

# If not, display next person in charge of scrubbing
else:
    st.markdown("<p><strong>Next scrub day from chosen day:</strong> {}</p>".format(next_scrub),True)
    st.markdown("<p><strong>Person in-charge:</strong> {}</p>".format(max(roster.keys(), key=lambda x: roster[x].count(next_scrub.strftime(format="%m/%d/%Y")))), True)


# Optional display of full duty roster table
if st.checkbox("Show Roster",value=True):
    st.write(Fin)
    st.markdown("<p><strong>Next Scrub Day From Today</strong></p>", True)
    st.markdown("<p><strong>{}</strong>: {}</p>".format(next_saturday,max(roster.keys(), key=lambda x: roster[x].count(next_saturday.strftime(format="%m/%d/%Y")))),True)
    



