import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1, 5, 20])

with col2:
    st.image("lOGO.jpg", width=100)
with col3:
    st.markdown("""
    <style>
    .big-font {
        font-size:70px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">工业园智能用电管理系统</p>', unsafe_allow_html=True)
st.text('\n')
st.text('\n')
st.sidebar.header("关于")
st.sidebar.text("本项目位于苏州高新技术产业园区\n"
                "为积极响应国家“碳达峰碳中和”双碳战略\n"
                "全面实现能源结构转型升级、产业规划与优化、生态增汇治理\n"
                "本公司以智能优化算法为核心，利于机器学习为企业提供“双碳”服务、开展园区智慧用电绿色供应链建设，致力于节能降碳技术的推广应用"
                )
st.sidebar.header("核心技术")
st.sidebar.text("HVAC智能温控调节系统，\n"
                "国际先进AI⼈⼯智能算法，\n"
                "⼈员流动分析，\n"
                "建筑外壁温度调节 ，\n"
                "AI无监督控制")
st.sidebar.header("联系方式")
st.sidebar.text("+86123456789")
# col1, col2, col3, col4 = st.columns([20, 20, 20, 20])
#
# with col1:
#     st.image("Big.png", width=800)
# with col2:
#     st.image("BigEarn.png", width=800)
# with col3:
#     st.image("Small.png", width=800)
# with col4:
#     st.image("SmallEarn.png", width=800)
st.text('\n')


df = pd.DataFrame({
    'first column': ["中小型（180-720千瓦时）","大型（1080-1800千瓦时）"]
    })
option = st.selectbox(
    '请选择您的电池、太阳能组规格',
     df['first column'])

if option == "中小型（180-720千瓦时）":
    st.subheader('请输入您的电池、太阳能板容量')
    st.text('\n')



    PVsize = st.slider("太阳能板容量(kW)", min_value=60, max_value=300, step=20)
    Batsize = st.slider("电池容量(kWh)", min_value=180, max_value=720, step=45)
    check = st.checkbox("确认")
    if check:
        with st.spinner("Waiting.."):
            time.sleep(3)
        st.success("Finished!")
        st.balloons()
        CSVdr = "Batsize_{}_PVsize_{}.csv".format(int(Batsize/0.9),int(PVsize))
        pathdr = 'D:\\Project\\China_Battery\\New_Battery\\SizingOPT\\'
        dfname =pathdr+CSVdr
        df = pd.read_csv(dfname)
        df['total'] = 1 - df['SOC_opt']
        df['opt'] = (df['PBaseline']+df['PBattery']+df['PPv'])*df['price']
        df['bas'] = (df['PBaseline']) * df['price']
        df['PPv'] = df['PPv']*(-1)
        # creating a single-element container
        placeholder = st.empty()

        for seconds in range(95):
            dffnew = df[0:seconds]
            dfnew = df[seconds:seconds + 1]


            with placeholder.container():

                kpi1, kpi2, kpi3 = st.columns(3)

                kpi1.metric(
                    label="实时用电量(kW)",
                    value=round(dfnew.PBaseline),
                    #delta=round(avg_age) - 10,
                )

                kpi2.metric(
                    label="太阳能发电量(kW)",
                    value=int(dfnew.PPv),
                    #delta=-10 + count_married,
                )

                kpi3.metric(
                    label="电池放电量(kW)",
                    value=int(dfnew.PBattery),
                    #delta=-round(balance / count_married) * 100,
                )


                # create two columns for charts
                fig_col1, fig_col2, fig_col3 = st.columns([1, 3, 3])
                with fig_col1:
                    st.markdown("\t 电池电量")

                    fig = px.bar(dfnew, x='Time', y=['SOC_opt', 'total'])
                    fig.update_layout(
                        xaxis_title="时间",
                        yaxis_title="电量%",
                        font=dict(
                            size=16,
                            color="RebeccaPurple"
                        )
                    )

                    st.write(fig)

                with fig_col2:
                    st.markdown("\t 智能用电优化控制")
                    fig2 = px.line(dffnew, x="Time", y=['PBattery','PPv','PBaseline'])
                    fig2.update_layout(
                        xaxis_title="时间",
                        yaxis_title="功率（千瓦）",
                        font=dict(
                            size=16,
                            color="RebeccaPurple"
                        )
                    )
                    st.write(fig2)

                with fig_col3:
                    st.markdown("\t 用电成本")
                    fig3 = px.line(dffnew, x="Time", y=['bas', 'opt'])
                    fig3.update_layout(
                        xaxis_title="时间",
                        yaxis_title="元/小时",
                        font=dict(
                            size=16,
                            color="RebeccaPurple"
                        )
                    )
                    st.write(fig3)

                st.markdown("\t 实时电价")
                fig = px.line(dffnew, x="Time", y=['price'],width=1750, height=300,color_discrete_sequence=["#026873"])
                fig.update_layout(
                    xaxis_title="时间",
                    yaxis_title="元/千瓦时",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )
                st.write(fig)

                time.sleep(0.1)
                col1, col2= st.columns([20, 20])

                with col1:
                    st.subheader("投资回收期(不含政府补贴)(4.8-7.1年)")
                    st.image("Small.png", width=800)
                with col2:
                    st.subheader("十年预期收益(不含政府补贴)(87-312万元)")
                    st.image("SmallEarn.png", width=800)

                col1, col2= st.columns([20, 20])

                with col1:
                    st.subheader("投资回收期(含政府补贴)(3.19-4.42年)")
                    st.image("Small_with.png", width=800)
                with col2:
                    st.subheader("十年预期收益(含政府补贴)(142-570万元)")
                    st.image("SmallEarn_with.png", width=800)


else:
    st.subheader('请输入您的电池、太阳能板容量')
    st.text('\n')



    PVsize = st.slider("太阳能板容量(kW)", min_value=200, max_value=600, step=50)
    Batsize = st.slider("电池容量(kWh)", min_value=1080, max_value=1800, step=90)
    check = st.checkbox("确认")
    if check:
        with st.spinner("Waiting.."):
            time.sleep(3)
        st.success("Finished!")
        st.balloons()
        CSVdr = "Batsize_{}_PVsize_{}.csv".format(int(Batsize/0.9),int(PVsize))
        pathdr = 'D:\\Project\\China_Battery\\New_Battery\\SizingOPT_big\\'
        dfname =pathdr+CSVdr
        df = pd.read_csv(dfname)
        df['total'] = 1 - df['SOC_opt']
        df['opt'] = (df['PBaseline']+df['PBattery']+df['PPv'])*df['price']
        df['bas'] = (df['PBaseline']) * df['price']
        df['PPv'] = df['PPv']*(-1)
        # creating a single-element container
        placeholder = st.empty()

        for seconds in range(95):
            dffnew = df[0:seconds]
            #df = df[1:]
            dfnew = df[seconds:seconds+1]


            with placeholder.container():

                kpi1, kpi2, kpi3 = st.columns(3)

                kpi1.metric(
                    label="实时用电量(kW)",
                    value=round(dfnew.PBaseline),
                    #delta=round(avg_age) - 10,
                )

                kpi2.metric(
                    label="太阳能发电量(kW)",
                    value=int(dfnew.PPv),
                    #delta=-10 + count_married,
                )

                kpi3.metric(
                    label="电池放电量(kW)",
                    value=int(dfnew.PBattery),
                    #delta=-round(balance / count_married) * 100,
                )


                # create two columns for charts
                fig_col1, fig_col2, fig_col3 = st.columns([1, 3, 3])
                with fig_col1:
                    st.markdown("\t 电池电量")

                    fig = px.bar(dfnew, x='Time', y=['SOC_opt', 'total'])
                    fig.update_layout(
                        xaxis_title="时间",
                        yaxis_title="电量%",
                        font=dict(
                            size=16,
                            color="RebeccaPurple"
                        )
                    )
                    st.write(fig)

                with fig_col2:
                    st.markdown("\t 智能用电优化控制")
                    fig2 = px.line(dffnew, x="Time", y=['PBattery','PPv','PBaseline'])
                    fig2.update_layout(
                        xaxis_title="时间",
                        yaxis_title="功率（千瓦）",
                        font=dict(
                            size=16,
                            color="RebeccaPurple"
                        )
                    )
                    st.write(fig2)

                with fig_col3:
                    st.markdown("\t 用电成本")
                    fig3 = px.line(dffnew, x="Time", y=['bas', 'opt'])
                    fig3.update_layout(
                        xaxis_title="时间",
                        yaxis_title="元/小时",
                        font=dict(
                            size=16,
                            color="RebeccaPurple"
                        )
                    )
                    st.write(fig3)


                st.markdown("\t 实时电价")
                fig = px.line(dffnew, x="Time", y=['price'],width=1750, height=300,color_discrete_sequence=["#026873"])
                fig.update_layout(
                    xaxis_title="时间",
                    yaxis_title="元/千瓦时",
                    font=dict(
                        size=16,
                        color="RebeccaPurple"
                    )
                )
                st.write(fig)

                time.sleep(0.1)

                col1, col2= st.columns([20, 20])

                with col1:
                    st.subheader("投资回收期(不含政府补贴)(6.1-8.9年)")
                    st.image("Big.png", width=800)
                with col2:
                    st.subheader("十年预期收益(不含政府补贴)(239-570万元)")
                    st.image("BigEarn.png", width=800)

                col1, col2= st.columns([20, 20])

                with col1:
                    st.subheader("投资回收期(含政府补贴)(3.6-5.1年)")
                    st.image("Big_with.png", width=800)
                with col2:
                    st.subheader("十年预期收益(含政府补贴)(470-1098万元)")
                    st.image("BigEarn_with.png", width=800)