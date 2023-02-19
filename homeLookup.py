import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

homes = pd.read_excel("EstimatedValue.xlsx")
homes.rename({"URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)": "URL"}, inplace=True)
homes.drop(columns=["FAVORITE","INTERESTED","LATITUDE","LONGITUDE"], inplace=True)
st.write(homes)
address = st.selectbox(label="Home Address", options=homes["ADDRESS"])
query = homes[homes["ADDRESS"] == address]
query["PriceToValue"] = query["PriceToValue"].round(2)
for col in query.columns:
    st.write(f"{col}: {query[col].values[0]}")
# st.write(homes[homes["ADDRESS"] == address].T)
