import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

homes = pd.read_excel("EstimatedValue.xlsx")

st.write(homes)
address = st.selectbox(label="Home Address", options=homes["ADDRESS"])
query = homes[homes["ADDRESS"] == address]
query["PriceToValue"] = query["PriceToValue"].round(2)
for col in query.columns:
    st.write(f"{col}: {query[col].values[0]}")
# st.write(homes[homes["ADDRESS"] == address].T)
