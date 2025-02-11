import streamlit as st
import pandas as pd
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
new_df = pd.read_csv(config["NEW_DATA"])
new_df["Ticket-Issue"] = new_df["Ticket ID"] + "_" + new_df["Issue"]
print(new_df)

