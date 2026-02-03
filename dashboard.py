import streamlit as st
import pandas as pd

st.title("Teiko Exam Dashboard")

df = pd.read_csv("cell-count.csv")

sample = st.selectbox("Choose a subject", df["subject"].unique())

filtered = df[df["subject"] == sample]

st.table(filtered)
