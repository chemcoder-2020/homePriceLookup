import streamlit as st
import pandas as pd
import pickle
import numpy as np
from st_aggrid import AgGrid


st.set_page_config(layout="wide")

lookup, pretrained = st.tabs(["Lookup", "Pretrained Model"])

with lookup:
    homes = pd.read_excel("EstimatedValue.xlsx")
    print(homes.columns)
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
    
    address = st.selectbox(label="Home Address", options=homes["ADDRESS"])
    query = homes[homes["ADDRESS"] == address]
    query["PriceToValue"] = query["PriceToValue"].round(2)
    query = pd.Series(query.T[query.T.columns[0]])
    query.name = query.ADDRESS
    st.write(query)
    # for col in query.columns:
    #     st.write(f"{col}: {query[col].values[0]}")
    # st.write(homes)
    AgGrid(homes)
    

with pretrained:
    mname = st.selectbox("Model", options=["homePricing","homePricing_votingmodel","homePricing_nn3layer","homePricing_gradboost_20230220"], index=2)
    with open(f"{mname}.pkl", "rb") as f:
        model = pickle.load(f)
    cols = st.columns(len(model.feature_names_in_))
    parameters = pd.DataFrame()
    for i, col in enumerate(cols):
        if model.feature_names_in_[i] == "PROPERTY TYPE":
            parameters[model.feature_names_in_[i]] = [
                col.selectbox(model.feature_names_in_[i], options=np.unique(homes["PROPERTY TYPE"]))
            ]
        else:
            parameters[model.feature_names_in_[i]] = [
                col.text_input(model.feature_names_in_[i])
            ]
    parameters.replace("", np.nan, inplace=True)
    parameters.astype({"SQUARE FEET":float, "BEDS":float, "BATHS":float})
    
    st.write(parameters)
    if parameters.isna().sum().sum() == 0:
        st.write(f"Estimated Price: ",int(model.predict(parameters)[0]))
