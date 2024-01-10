import streamlit as st
import time

st.title('Streamlit 超入門')
# st.write('DataFrame')

# df = pd.DataFrame(
#     np.random.rand(20, 3),
#     columns=['a', 'b', 'c']
# )

# st.line_chart(df)

# st.write('DisplayImage')
# if st.checkbox('Show Image'):
#     img = Image.open('copy_machine.png')
#     st.image(img, caption='copy machine', use_column_width=True)

# st.dataframe(df.style.highlight_max(axis=0), width=200, height=200)

# st.write('セレクトボックス')
# option = st.selectbox(
#     'あなたが好きな数字を選んでください。',
#     list(range(1, 11))
# )
# 'あなたの好きな数字は', option , 'です。'

st.write('プログレスバー')
'Start!'

latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)


left_column, right_column = st.columns(2)
button = left_column.button('右カラムに表示')
if button:
    right_column.write('ここは右カラム')

expander = st.expander('問合せ')
expander.write('回答・・・')

# text = st.text_input('あなたの趣味を教えてください。')
# condition = st.slider(
#     'あなたの調子を教えてください。',
#     0, 100, 50, 10
#     )
# 'あなたの趣味：', text
# 'あなたのコンディション：', condition

# """

# # 章
# ## 節
# ### 項

# ```python
# import streamlit as st
# import numpy as sp
# import pandas as pd
# ```
# """