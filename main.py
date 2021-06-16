import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded" )

@st.cache
def load_data():
    sql = "SELECT * FROM aws_mysql_tables.iphone_data"
    project_id = "teak-hearth-316213"
    df = pd.read_gbq(sql, project_id=project_id)
    return df

df = load_data()

"""
# スマートフォン相場検索
過去にフリマで取引されたスマートフォンのデータベースから  
機種や容量・状態毎の価格分布や時系列推移を確認できるサイトです。
"""

# Side Bar
st.sidebar.title("条件")
maker = st.sidebar.selectbox(
    "シリーズ",
    ["Apple"],
)

brand = st.sidebar.radio(
    "機種",
    ["ALL"] + list(df["brand"].unique())
)

# main
# 直近n日の取引件数ランキング

n_days = 30

def get_date_n_days_before(n):
    date_of_n_days_before = (datetime.datetime.now() - datetime.timedelta(days=n_days)).strftime("%Y-%m-%d")
    return date_of_n_days_before

sales_counts_top10 = df[df["sales_date"] >= get_date_n_days_before(30)] \
                    .groupby(["brand"]) \
                    .count()["sales_date"] \
                    .sort_values(ascending=False)[:10]

def plot_top10_brands(df):
    fig, ax = plt.subplots()
    sales_counts_top10 = df[df["sales_date"] >= get_date_n_days_before(30)] \
                    .groupby(["brand"]) \
                    .count()["sales_date"] \
                    .sort_values(ascending=False)[:10]
    
    sns.barplot(sales_counts_top10.index, sales_counts_top10.values, ax=ax)
    ax.xaxis.set_tick_params(rotation=60)
    ax.set_xlabel(None)
    ax.set_ylabel("Counts")
    return fig


col1, col2 = st.beta_columns(2)

col1.subheader(f"直近{n_days}日間の取引件数（上位10機種）")
col1.pyplot(plot_top10_brands(df))

col2.subheader("トレンド")
col2.pyplot(plot_top10_brands(df))