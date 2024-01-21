import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf
import streamlit as st

# タイトル
st.title('米国株価可視化アプリ')

# サイドバーに設定
sbar = st.sidebar
sbar.markdown("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")
# 表示日数選択領域
sbar.markdown("""
## 表示日数選択
""")
days = sbar.slider('日数を指定してください。', 1, 50, 20)
# 表示範囲選択領域
sbar.markdown("""
## 株価の範囲指定
""")
range = sbar.slider(
    '範囲を指定してください。',
    0, 1000,(0, 1000)
    )
ymin, ymax = range[0], range[1]

# 事前に全株価を読み取り

# キャッシュに入れることで、毎回取得する必要をなくしている
# 全データをdfとして取得
@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        # ティッカーシンボルを指定
        tkr = yf.Ticker(tickers[company])
        print(tkr)
        # 株価データ取得
        hist = tkr.history(period=f'{days}d')

        # 日付の表示形式を変更
        hist.index = hist.index.strftime('%d %B %Y')

        # 株価情報としてCloseのみを指定
        hist = hist[['Close']]

        # Closeの軸名をappleに変更
        hist.columns = [company]

        # 表の縦横入れ替え
        hist = hist.T

        # 表の縦軸にNameを追加
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df
    
tickers = {
    'apple': 'AAPL',
    'meta': 'META',
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'microsoft': 'MSFT',
    'nvidia': 'NVDA'
}
try:
    # データ取得
    df = get_data(days, tickers)

    # 対象株選択
    st.markdown(f"""
    ### 過去 **{days}日間** の株価
    """)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['amazon', 'meta']
    )
    if not companies:
        st.error('少なくとも1社は選択してください。')
    else:
        # 株価テーブル表示
        st.write('株価(USD)')
        # 対象会社の絞り込み
        data = df.loc[companies]
        table_data = data
        # テーブル表示
        st.table(table_data)

        # グラフ用データ整形
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns= {'value': 'Stock Prices(USD)'}
        )

        # グラフ描写
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x='Date:T',
                y=alt.Y(
                    'Stock Prices(USD):Q',
                    stack=None,
                    scale= alt.Scale(domain=[ymin, ymax])
                ),
                color='Name:N',
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error('予期せぬエラーが発生しました。')