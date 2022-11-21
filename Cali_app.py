import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
st.set_page_config(layout="wide")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('./Picture/Solar-Battery-Storage-Full.jpg')




col1, col2, col3 = st.columns([1, 5, 20])

with col2:
    st.image("./Picture/lOGO.jpg", width=100)
with col3:
    st.markdown("""
    <style>
    .big-font {
        font-size:70px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Community Level Power System Optimization Platform</p>', unsafe_allow_html=True)
st.text('\n')
st.text('\n')
st.sidebar.header("About")
st.sidebar.text("A smart optimization platform\n"
                "towards building flexibility\n"
                "Reduce Energy Consumption\n"
                "Energy Storage System Management\n"
                "Hierarchy control"
                )
st.sidebar.header("Advanced Tech")
st.sidebar.text("Smart HVAC，\n"
                "AI Learn，\n"
                "Occupancy Behavior，\n"
                "Efficiency Envelope，\n"
                "MPC")
st.sidebar.header("Contact Support")
st.sidebar.text("zjiang19@syr.edu")

st.text('\n')


check = st.checkbox("Start")
if check:
    with st.spinner("Waiting for calculation.."):
        time.sleep(3)
    st.success("Finished!")
    st.balloons()
    pathdr = './Datafile/Cali.csv'
    df = pd.read_csv(pathdr)

    df['total'] = 1 - df['SOC']
    # df['opt'] = df['Opt_price']
    # df['bas'] = df['Base_price']
    # df['PPv'] = df['Ppv']
    # creating a single-element container
    placeholder = st.empty()

    for seconds in range(95):
        dffnew = df[0:seconds]
        dfnew = df[seconds:seconds + 1]


        with placeholder.container():

            kpi1, kpi2, kpi3 = st.columns(3)

            kpi1.metric(
                label="Power Consumption(kW)",
                value=round(dfnew.Opt_load),
                #delta=round(avg_age) - 10,
            )

            kpi2.metric(
                label="PV Generation(kW)",
                value=int(dfnew.Ppv),
                #delta=-10 + count_married,
            )

            kpi3.metric(
                label="Battery Generation(kW)",
                value=int(dfnew.Pbattery),
                #delta=-round(balance / count_married) * 100,
            )


            # create two columns for charts
            fig_col1, fig_col2, fig_col3 = st.columns([1, 3, 3])
            with fig_col1:
                st.markdown("\t SOC")

                fig = px.bar(dfnew, x='Time', y=['SOC', 'total'])
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="SOC%",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )

                st.write(fig)

            with fig_col2:
                st.markdown("\t Power System Optimization")
                fig2 = px.line(dffnew, x="Time", y=['Pbattery','Ppv','Base_load'])
                fig2.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Power（kW）",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )
                st.write(fig2)

            with fig_col3:
                st.markdown("\t Total Load")
                fig3 = px.line(dffnew, x="Time", y=['Base_load', 'Opt_load'])
                fig3.update_layout(
                    xaxis_title="Time",
                    yaxis_title="kW",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )
                st.write(fig3)


            fig_col1, fig_col2= st.columns([2, 2])
            with fig_col1:
                st.markdown("\t Cost")
                fig1 = px.line(dffnew, x="Time", y=['Base_price', 'Opt_price'])
                fig1.update_layout(
                    xaxis_title="Time",
                    yaxis_title="$/Hour",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )
                st.write(fig1)

            with fig_col2:
                st.markdown("\t Power System Optimization")
                fig2 = px.line(dffnew, x="Time", y=['Price'])
                fig2.update_layout(
                    xaxis_title="Time",
                    yaxis_title="TOU($/kWh)",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )
                st.write(fig2)

            time.sleep(0.08)
            col1, col2= st.columns([20, 20])

            with col1:
                st.subheader("Quickest Payback Year(1.5y)")
                st.image("./Picture/Cali.png", width=800)
            with col2:
                st.subheader("10 Years potential benefit(0.3-2.5M $)")
                st.image("./Picture/SmallEarn.png", width=800)

