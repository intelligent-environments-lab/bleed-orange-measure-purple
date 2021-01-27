import streamlit as st
import src.data.purpleair_data_retriever as pdr
import plotly.express as px

st.title("Bleed Orange Measure Purple")

gt=st.button('Update')
if gt:
    gat=pdr.live_data()
    st.write(gat)
    px.set_mapbox_access_token('pk.eyJ1IjoiY2xpbjI2NSIsImEiOiJja2NuaXpkZjMwMnEyMnJxcGQ4YTM2aTY5In0.4mHf-EjuvLGnivDWEr4uKA')
    fig = px.scatter_mapbox(gat, lat="Lat", lon="Lon", hover_name="sensor", hover_data=["PM2.5_ATM_ug/m3", "Lat","Lon"],
                        color="PM2.5_ATM_ug/m3", text="PM2.5_ATM_ug/m3", zoom=13.5, height=400, size=[6]*(gat.count()[0]),
                        color_continuous_scale=px.colors.diverging.RdYlBu[::-1])
    fig.update_layout(showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
expander = st.beta_expander("Not in Use")
with expander:
    start = st.date_input('Start date:')
    end = st.date_input('End date:')
    channel = st.selectbox('Channel:',['primaryA','primaryB'])
    status = st.button('Download',key='purple')
