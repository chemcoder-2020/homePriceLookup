import streamlit as st
import pandas as pd
import pickle
import numpy as np

with open("homePricing.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(layout="wide")

lookup, pretrained = st.tabs(["Lookup", "Pretrained Model"])

with lookup:
    homes = pd.read_excel("EstimatedValue.xlsx")

    homes["URL"] = homes[
        "URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)"
    ]

    homes.drop(
        columns=[
            "FAVORITE",
            "INTERESTED",
            "LATITUDE",
            "LONGITUDE",
            "URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)",
        ],
        inplace=True,
    )
    st.write(homes)
    address = st.selectbox(label="Home Address", options=homes["ADDRESS"])
    query = homes[homes["ADDRESS"] == address]
    query["PriceToValue"] = query["PriceToValue"].round(2)
    for col in query.columns:
        st.write(f"{col}: {query[col].values[0]}")

with pretrained:
    cols = st.columns(len(model.feature_names_in_))
    parameters = pd.DataFrame()
    for i, col in enumerate(cols):
        if model.feature_names_in_[i] == "PROPERTY TYPE":
            parameters[model.feature_names_in_[i]] = [
                col.selectbox(model.feature_names_in_[i], options=np.unique(homes["PROPERTY TYPE"]))
            ]
        parameters[model.feature_names_in_[i]] = [
            col.text_input(model.feature_names_in_[i])
        ]
    parameters.replace("", np.nan, inplace=True)
    parameters["SQUARE FEET"] = parameters["SQUARE FEET"].astype(float)
    
    st.write(parameters)
    if parameters.isna().sum().sum() == 0:
        st.write(f"Estimated Price: ",model.predict(parameters)[0])
