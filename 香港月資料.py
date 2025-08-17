#%%
# ===========================================
# ==========  套件匯入區（import）  ==========
# ===========================================
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import openai
import re
import requests
from io import BytesIO
from datetime import datetime

# ===========================================
# https://nb7d3pazwhxzsybs3zde75.streamlit.app
# ===========================================


#%%
st.set_page_config(

    layout="wide"

)
# from mypackage.mymodule import mul_trade, mul_rent, mul_retu
#%%移套件到本地
def mul_trade(xcol, ycolb, ycols, color1, color2):
    fig = go.Figure()##
    fig.add_trace(go.Bar(
        x = xcol,
        y = ycolb,
        name=ycolb.name,
        marker=dict(color=color1, opacity=0.6),  # 指定使用主 Y 軸
        text=ycolb,  # 顯示數值
        textposition='auto',  # 自動顯示在柱狀圖頂部
        texttemplate='%{text:,.0f}',  # 格式化為整數
        textfont = dict(size = 12, color = 'white')
    ))
    fig.update_xaxes(type='category')

    fig.add_trace(go.Scatter(
        x=xcol,
        y=ycols,
        name=ycols.name, 
        mode='lines+markers+text',
        marker=dict(size=6),
        line = dict(color = color2),
        yaxis='y2', 
        text=ycols,  # 顯示數值
        textposition='top center',  # 顯示在線條上方
        texttemplate='%{text:.2f}', 
        textfont=dict(color = color2, size = 12)
    ))

    fig.update_layout(
        xaxis=dict(
            title=dict(
                text="時間(年月)",
                font=dict(color='black', size=20)
            ),
            tickangle=45,
            tickfont=dict(color='black', size = 15),
            showgrid=False, ##不開網格 
        
        
        ),

        yaxis=dict(
            title=dict(
                text=f'{ycolb.name}交易量',
                font=dict(color = color1, size=20)
            ),
            tickfont=dict(color = color1, size = 15),
            tickformat=',.0f',
            showgrid=True,  # 顯示背景橫線
            gridcolor='#e0e0e0'  # 設定淺灰色橫線
            ,range=[0, ycolb.max() * 1.8]
            ),
    #########################繼續TAB
        yaxis2=dict(
            title=dict(
                text=f'{ycols.name}價格指數',
                font=dict(color = color2, size=20)
            ),
            tickfont=dict(color = color2, size = 15),
            overlaying='y',
            side='right',
            showgrid=True,  # 顯示背景橫線
            gridcolor='#e0e0e0'  # 設定淺灰色橫線
            ,range=[ycols.min() * 0.7, ycols.max() * 1.2]
        ),
        # legend=dict(
        #     x=0.5,
        #     xanchor='center',
        #     y=-0.3,##圖例到圖表下方
        #     yanchor='top',
        #     orientation='h',##
        #     font=dict(size=30, color='black'),  # 增大圖例字體
        # ),

        template="plotly_white",
        hovermode='x unified',  # 統一懸停提示框，提升互動性
        autosize=True,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'

    )

    st.plotly_chart(fig)



#%%
# ==========================
# 製作 租屋市場scatter組合圖
# ==========================


def mul_rent(xcol, ycols, color1):
    fig = go.Figure()##
    fig.add_trace(go.Scatter(
        x=xcol,
        y=ycols,
        name=ycols.name, 
        mode='lines+markers+text',
        marker=dict(size=6),
        line = dict(color = color1),
        text=ycols,  # 顯示數值
        textposition='top center',  # 顯示在線條上方
        texttemplate='%{text:.2f}', 
        textfont=dict(color = color1, size = 12)
    ))
    fig.update_xaxes(type='category')

    fig.update_layout(
        xaxis=dict(
            title=dict(
                text="時間(年月)",
                font=dict(color='black', size=20)
            ),
            tickangle=45,
            tickfont=dict(color='black', size = 15),
            showgrid=False, ##不開網格 
        
        
        ),

        yaxis=dict(
            title=dict(
                text=f'{ycols.name}租金指數',
                font=dict(color = color1, size=20)
            ),
            tickfont=dict(color = color1, size = 15),
            tickformat='.0f',
            showgrid=True,  # 顯示背景橫線
            gridcolor='#e0e0e0'  # 設定淺灰色橫線
            ,range=[0, ycols.max() * 1.8]
            ),
    #########################繼續TAB

        # legend=dict(
        #     x=0.5,
        #     xanchor='center',
        #     y=-0.3,##圖例到圖表下方
        #     yanchor='top',
        #     orientation='h',##
        #     font=dict(size=30, color='black'),  # 增大圖例字體
        # ),

        template="plotly_white",
        hovermode='x unified',  # 統一懸停提示框，提升互動性
        autosize=True,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'

    )

    st.plotly_chart(fig)


#%%
# ==========================
# 製作 報酬率scatter
# ==========================


def mul_retu(xcol, ycols, color1):
    fig = go.Figure()##
    for col, colora in zip(ycols, color1):
        fig.add_trace(go.Scatter(
            x=xcol,
            y=col,
            name=col.name, 
            mode='lines+markers+text',
            marker=dict(size=6, color = colora),
            line = dict(color = colora),
            text=col,  # 顯示數值
            textposition='top center',  # 顯示在線條上方
            texttemplate='%{text:.2f}', 
            textfont=dict(color = colora, size = 12)
        ))

    fig.update_xaxes(type='category')

    fig.update_layout(
        xaxis=dict(
            title=dict(
                text="時間(年月)",
                font=dict(color='black', size=20)
            ),
            tickangle=45,
            tickfont=dict(color='black', size = 15),
            showgrid=False, ##不開網格 
        
        
        ),

        yaxis=dict(
            title=dict(
                text=f'投資報酬率',
                font=dict(color = 'black', size=20)
            ),
            tickfont=dict(color = 'black', size = 15),
            tickformat='.2f',
            showgrid=True,  # 顯示背景橫線
            gridcolor='#e0e0e0'  # 設定淺灰色橫線
            ,range=[0, ycols[0].max() * 1.8]
            ),
    #########################繼續TAB

        legend=dict(
            x=0.5,
            xanchor='center',
            y=-0.5,##圖例到圖表下方
            yanchor='top',
            orientation='h',##
            font=dict(size=15, color='black'),  # 增大圖例字體
        ),

        template="plotly_white",
        hovermode='x unified',  # 統一懸停提示框，提升互動性
        autosize=True,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'

    )

    st.plotly_chart(fig)

# st.set_page_config(layout="wide")

base_dir = r"\\10.11.6.12\r41200\M08242(庭宇)\hk_month"

# try:
#     subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
#     if len(subfolders) != 5:
#         st.warning(f"找到 {len(subfolders)} 個資料夾，預期為 5 個: {subfolders}")
#     else:
#         st.success(f"找到的子資料夾: {subfolders}")
# except Exception as e:
#     st.error(f"無法讀取資料夾: {e}")
#     st.stop()

#%%
# ==========================
# 創造2024/07到2025/05的數列
# ==========================
def generate_month_list():
    
    now = datetime.now()

    start = (now.year-1) * 100 + now.month-2
    end = now.year * 100 + now.month-2
    result = []
    y, m = divmod(start, 100)##得商數餘數
    while y * 100 + m <= end:
        result.append(y * 100 + m)
        m += 1
        if m > 12:
            m = 1
            y += 1
    return result

t_option = generate_month_list()

####################################################################################################################

#%%資料夾中檔案

trahk_path = {
    '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_16.xls',
    '其他': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_17.xls'
}
retuhk_path = {
    '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_15.xls',
    '其他': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_15.xls'
}
soldhk_path = {
    '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_4.xls',
    '辦公': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_9.xls',
    '零售': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_12.xls',
    '廠辦': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_14.xls'
}
renthk_path = {
    '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_3.xls',
    '辦公': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_8.xls',
    '零售': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_12.xls',
    '廠辦': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_14.xls'
}

###########
# %% 交易量
output1 = pd.DataFrame()
for key,value in trahk_path.items():
    path = value
    types = key

    response = requests.get(path)
    if response.status_code == 200:  
        data1 = BytesIO(response.content)

        df = pd.read_excel(data1,sheet_name=0,header=6)
        
        if (types =='住宅') :
            df = df[['年','Unnamed: 5', '數目','數目.1']]
            df.columns = ['年','月','住宅(一手買賣)','住宅(二手買賣)']
            # df['類別'] = '住宅'
            
        if (types =='其他'):
            df = df[['年','Unnamed: 5', '宗數','宗數.1','宗數.2']]
            df.columns = ['年','月','辦公','零售','廠辦']
            #df['類別'] = '辦公'
            
        df['年'] = pd.to_numeric(df['年'], errors='coerce')
        df['月'] = pd.to_numeric(df['月'], errors='coerce')
        # df['月'] = df['月'].replace(' ', np.nan)
        df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        df_clean['季'] =round((df_clean['月']+1)/3)
        df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        # 顯示數據的前幾行
        if output1.empty:
            output1 = df_clean
        else:
            output1 = pd.merge(output1,df_clean, on=['年', '季', '月'], how='outer')

    else:
        st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")

output1['住宅'] = output1['住宅(一手買賣)'] + output1['住宅(二手買賣)']
output1 = output1[['年', '季', '月', '住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']]
output1['年月'] = output1['年']*100 + output1['月']
output1 = output1[['年', '季', '月', '年月', '住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']]
output1[['年', '季', '月', '年月']] = output1[['年', '季', '月', '年月']].astype(int)
output1[['住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']] = output1[['住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']].astype(int)
# st.subheader('交易量資料表', divider = 'rainbow')
# st.write(output1)





#%%投報率
output2 = pd.DataFrame()
for key,value in retuhk_path.items():
    path = value
    types = key

    # 使用pandas讀取Excel文件
    # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數

    response = requests.get(path)

    if response.status_code == 200:

        data2 = BytesIO(response.content)
        
        if (types =='住宅') :
            df = pd.read_excel(data2,sheet_name='Monthly(Domestic) 按月(住宅)',header=6)
            df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
            df.columns = ['年','Unnamed: 5','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']
            # df['類別'] = '住宅'
            
        if (types =='其他'):
            df = pd.read_excel(path,sheet_name='Monthly(Non-domestic) 按月(非住宅)',header=8)
            df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17']]
            df.columns = ['年','Unnamed: 5','辦公(甲級)','辦公(乙級)','廠辦','零售']
            #df['類別'] = '辦公'
            
        
        
        df['年'] = pd.to_numeric(df['年'], errors='coerce')
        df['月'] = pd.to_numeric(df['Unnamed: 5'], errors='coerce')
        # df['月'] = df['月'].replace(' ', np.nan)
        df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        df_clean['季'] =round((df_clean['月']+1)/3)
        df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        # 顯示數據的前幾行
        if output2.empty:
            output2 = df_clean
        else:
            output2 = pd.merge(output2,df_clean, on=['年', '季', '月'], how='outer')

    else:
        st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")
                 
output2 = output2[['年', '季', '月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
                '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
output2 = output2.replace('-', np.nan)

output2.loc[:] = output2.loc[:].apply(pd.to_numeric, errors='coerce')
output2['年月'] = output2['年']*100 + output2['月']
output2 = output2[['年', '季', '月', '年月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
                '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
output2[['年', '季', '月', '年月']] = output2[['年', '季', '月', '年月']].astype(int)
output2[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']] = output2[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']].astype(float)
# st.subheader('投報率資料表', divider = 'rainbow')
# st.write(output2)



#%% 售價
output3 = pd.DataFrame()
for key,value in soldhk_path.items():
    path = value
    types = key
        
    # 使用pandas讀取Excel文件
    # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數

    response = requests.get(path)

    if response.status_code == 200:
        data3 = BytesIO(response.content)

        df = pd.read_excel(data3,sheet_name=0,header=5)
    
        if (types =='住宅') :
            df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                        'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                        'Unnamed: 29']]
            df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
            
        if (types =='辦公'):
            df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                        'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
            df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
            
        if (types == '零售') | (types == '廠辦'):
            df = df[['年','Unnamed: 5','Unnamed: 14']]
            df.columns = ['年','月','零售(平均)'] if types =='零售' else ['年','月','廠辦(平均)']
        
        df['年'] = pd.to_numeric(df['年'], errors='coerce')
        df['月'] = pd.to_numeric(df['月'], errors='coerce')
        # df['月'] = df['月'].replace(' ', np.nan)
        df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        df_clean['季'] =round((df_clean['月']+1)/3)
        df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        df_clean = df_clean.replace(')@','Indicates fewer than 20 transactions.')
        df_clean = df_clean.replace(')~','Indicates fewer than 20 transactions.')

        # 顯示數據的前幾行
        
        if output3.empty:
            output3 = df_clean   
        else:
            output3 = pd.merge(output3,df_clean, on=['年', '季', '月'], how='outer')


    else:
        st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")    

        

output3 = output3[['年', '季','月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
    '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
    '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
output3 = output3.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
output3 = output3.replace('-', np.nan)
output3.loc[:] = output3.loc[:].apply(pd.to_numeric, errors='coerce')
output3['年月'] = output3['年']*100 + output3['月']
output3 = output3[['年', '季','月', '年月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
    '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
    '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
output3[['年', '季', '月', '年月']] = output3[['年', '季', '月', '年月']].astype(int)
output3[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
    '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
    '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = output3[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
    '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
    '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)

# st.subheader('售價指數資料表', divider = 'rainbow')
# st.write(output3)



#%% 租金
output4 = pd.DataFrame()
for key,value in renthk_path.items():
    path = value
    types = key
        
    # 使用pandas讀取Excel文件
    # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數
    response = requests.get(path)

    if response.status_code == 200:
        data4 = BytesIO(response.content)

        df = pd.read_excel(data4,sheet_name=0,header=5)
        
        if (types =='住宅') :
            df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                        'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                        'Unnamed: 29']]
            df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
            
        if (types =='辦公'):
            df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                        'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
            df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
            
        if (types == '零售') :
            df = df[['年','Unnamed: 5','Unnamed: 9']]
            df.columns = ['年','月','零售(平均)']
        
        if (types == '廠辦'):
            df = df[['年','Unnamed: 5','Unnamed: 9']]
            df.columns = ['年','月','廠辦(平均)']

        df['年'] = pd.to_numeric(df['年'], errors='coerce')
        df['月'] = pd.to_numeric(df['月'], errors='coerce')
        # df['月'] = df['月'].replace(' ', np.nan)
        df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        df_clean['季'] =round((df_clean['月']+1)/3)
        df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        # 顯示數據的前幾行
        if output4.empty:
            output4 = df_clean   
        else:
            output4 = pd.merge(output4,df_clean, on=['年', '季', '月'], how='outer')
            # print("數據已保存為 rvd_data.csv")


    else:
        st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")    


output4 = output4[['年', '季', '月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
       '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
         '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
output4 = output4.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
output4 = output4.replace('-', np.nan)
output4.loc[:] = output4.loc[:].apply(pd.to_numeric, errors='coerce')
output4['年月'] = output4['年']*100 + output4['月']
output4 = output4[['年', '季', '月', '年月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
       '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
         '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]

output4[['年', '季', '月', '年月']] = output4[['年', '季', '月', '年月']].astype(int)
output4[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
       '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
         '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = output4[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
       '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
         '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)
# st.subheader('租金指數資料表', divider = 'rainbow')
# st.write(output4)






#%%
st.title("香港月資料分析")
col11, col12 = st.columns([3, 2])
with col11:
    st.header("香港近期房市數據追蹤", divider= 'rainbow')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("起始時間", divider = 'rainbow')

        st.selectbox(
        "",
            options=t_option,
            key="hk_mo_ti_st", 
            index=0
    )
        
    with col2:
        st.subheader("終止時間", divider = 'rainbow')

        st.selectbox(
        "",
            options=t_option,
            key="hk_mo_ti_en", 
            index = len(t_option)-1
    )


    if st.session_state.hk_mo_ti_st <= st.session_state.hk_mo_ti_en:
        hk_m_get_ti = [st.session_state.hk_mo_ti_st, st.session_state.hk_mo_ti_en]
        st.session_state.result_ti = []
        y, m = divmod(hk_m_get_ti[0], 100)##得商數餘數
        while y * 100 + m <= hk_m_get_ti[1]:
            st.session_state.result_ti.append(y * 100 + m)
            m += 1
            if m > 12:
                m = 1
                y += 1
        st.success(f'你已選擇：{hk_m_get_ti[0]}到{hk_m_get_ti[1]}')
        # st.write(st.session_state.result_ti)

        #%%
        cola, colb = st.columns(2)
        if 'm_color1' not in st.session_state:
            st.session_state.m_color1 = '#5C4141'
        if 'm_color2' not in st.session_state:
            st.session_state.m_color2 = '#1F77B4'


        with cola:
            st.session_state.m_color1 = st.color_picker("選擇長條圖顏色", value=st.session_state.m_color1)
        with colb:
            st.session_state.m_color2 = st.color_picker("選擇折線圖顏色", value=st.session_state.m_color2)


        tab1, tab2, tab3, tab4, tab5 = st.tabs(['住宅', '辦公', '零售', '廠辦', '檢視與下載資料表'])



        with tab1:
            # col1, col2, col3 = st.columns(3)

            # with col1:
                x = st.session_state.result_ti
                yb_1_1 = output1[output1['年月'].isin(st.session_state.result_ti)]['住宅']
                ys_1_1 = output3[output3['年月'].isin(st.session_state.result_ti)]['住宅(平均)']
                co1_1_1 = st.session_state.m_color1
                co2_1_1 = st.session_state.m_color2
                st.subheader('住宅買賣市場', divider='rainbow')
                mul_trade(x, yb_1_1, ys_1_1, co1_1_1, co2_1_1)
            # with col2:
                ys_1_2 = output4[output4['年月'].isin(st.session_state.result_ti)]['住宅(平均)']
                st.subheader('住宅租賃市場', divider='rainbow')
                mul_rent(x, ys_1_2, co2_1_1)
            # with col3:
                ys_1_3 = [output2[output2['年月'].isin(st.session_state.result_ti)]['住宅(A)'],
                        output2[output2['年月'].isin(st.session_state.result_ti)]['住宅(B)'],
                        output2[output2['年月'].isin(st.session_state.result_ti)]['住宅(C)'],
                        output2[output2['年月'].isin(st.session_state.result_ti)]['住宅(D)'],
                        output2[output2['年月'].isin(st.session_state.result_ti)]['住宅(E)']
                ] 

                col1_3 = ['red', 'green', 'blue', 'orange', 'purple']
                st.subheader('住宅投報率', divider='rainbow')
                mul_retu(x, ys_1_3, col1_3)   


        
        with tab2:
            # col1, col2, col3 = st.columns(3)
            # with col1:
                x = st.session_state.result_ti
                yb_2_1 = output1[output1['年月'].isin(st.session_state.result_ti)]['辦公']
                ys_2_1 = output3[output3['年月'].isin(st.session_state.result_ti)]['辦公(平均)']
                st.subheader('辦公買賣市場', divider='rainbow')
                mul_trade(x, yb_2_1, ys_2_1, co1_1_1, co2_1_1)
            # with col2:
                ys_2_2 = output4[output4['年月'].isin(st.session_state.result_ti)]['辦公(平均)']
                st.subheader('辦公租賃市場', divider='rainbow')
                mul_rent(x, ys_2_2, co2_1_1)
            # with col3:
                ys_2_3 = [output2[output2['年月'].isin(st.session_state.result_ti)]['辦公(甲級)'],
                        output2[output2['年月'].isin(st.session_state.result_ti)]['辦公(乙級)']
                ]
                col2_3 = ['red', 'green'] 
                st.subheader('辦公投報率', divider='rainbow')
                mul_retu(x, ys_2_3, col2_3)     

        with tab3:
            # col1, col2, col3 = st.columns(3)
            # with col1:
                x = st.session_state.result_ti
                yb_3_1 = output1[output1['年月'].isin(st.session_state.result_ti)]['零售']
                ys_3_1 = output3[output3['年月'].isin(st.session_state.result_ti)]['零售(平均)']

                st.subheader('零售買賣市場', divider='rainbow')
                mul_trade(x, yb_3_1, ys_3_1, co1_1_1, co2_1_1)    
            # with col2:
                ys_3_2 = output4[output4['年月'].isin(st.session_state.result_ti)]['零售(平均)']        
                st.subheader('零售租賃市場', divider='rainbow')
                mul_rent(x, ys_3_2, co2_1_1)
            # with col3:
                ys_3_3 = [output2[output2['年月'].isin(st.session_state.result_ti)]['零售']
                ]
                col3_3 = ['red'] 
                st.subheader('零售投報率', divider='rainbow')
                mul_retu(x, ys_3_3, col3_3)          

        with tab4:
            # col1, col2, col3 = st.columns(3)

            # with col1:
                x = st.session_state.result_ti
                yb_4_1 = output1[output1['年月'].isin(st.session_state.result_ti)]['廠辦']
                ys_4_1 = output3[output3['年月'].isin(st.session_state.result_ti)]['廠辦(平均)']
                st.subheader('廠辦買賣市場', divider='rainbow')
                mul_trade(x, yb_4_1, ys_4_1, co1_1_1, co2_1_1)

            # with col2:
                ys_4_2 = output4[output4['年月'].isin(st.session_state.result_ti)]['廠辦(平均)']
                st.subheader('廠辦租賃市場', divider='rainbow')
                mul_rent(x, ys_4_2, co2_1_1)

            # with col3:
                ys_4_3 = [output2[output2['年月'].isin(st.session_state.result_ti)]['廠辦']
                ]
                col4_3 = ['red']
                st.subheader('廠辦投報率', divider='rainbow') 
                mul_retu(x, ys_4_3, col4_3)          

        with tab5:
            output1 = output1[output1['年月'].isin(st.session_state.result_ti)][['年', '季', '月', '年月', '住宅', '辦公', '零售', '廠辦']]
            with st.expander('交易量資料表', expanded=False):
                st.dataframe(output1)

            output2 = output2[output2['年月'].isin(st.session_state.result_ti)][['年', '季', '月', '年月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
            with st.expander('投報率資料表', expanded=False):
                st.dataframe(output2)

            output3 = output3[output3['年月'].isin(st.session_state.result_ti)][['年', '季','月', '年月', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
            with st.expander('價格指數資料表', expanded=False):
                st.dataframe(output3)
                
            output4 = output4[output4['年月'].isin(st.session_state.result_ti)][['年', '季', '月', '年月', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
            with st.expander('租金指數資料表', expanded=False):
                st.dataframe(output4)
            # st.dataframe(pd.DataFrame(output1.dtypes, columns=['資料型態']))
            # st.dataframe(pd.DataFrame(output2.dtypes, columns=['資料型態']))
            # st.dataframe(pd.DataFrame(output3.dtypes, columns=['資料型態']))
            # st.dataframe(pd.DataFrame(output4.dtypes, columns=['資料型態']))


    else:
        st.error('時間問題')



with col12:
    st.header("香港月資料AI摘要", divider= 'rainbow')


    openai.api_base = "https://api.groq.com/openai/v1"
    with st.expander('輸入api金鑰', expanded=False):
        key = st.text_input('', max_chars= 60)
    openai.api_key = key  # 請替換為您的 Groq API 金鑰
    def GAI_hk_month_copy(a, b, c, d):
        model = "meta-llama/llama-4-scout-17b-16e-instruct" # 模型設定
        system_prompt = f"""
        你是一位香港房市分析專家，擅長透過數據分析房市。
        使用提供的交易量{a}、物價指數{c}、租金指數{d}、投報率{b}四個資料表格，進行以下要求：
        1. 用繁體中文及台灣用語回答，禁止其他語言。
        2. 回應精簡，邏輯清晰，避免冗長或籠統陳述。
        3. 必須僅引用提供的數據。
        4. 若有空值，請不要分析該時間點的數據，直接忽略。
        5. 聚焦異常趨勢，如急升/降或相關性。
        其中投報率retu.json表格中住宅A類面積最小，住宅E類面積最大；甲級辦公室比乙級辦公室高級。
        """ 

        final_prompt = f"""
        根據表格回答問題，分五段，各段都需照順序分析交易量、售價指數、租金指數、各級物件投報率四種指標：
        第一段：住宅市場分析
        第二段：辦公市場分析
        第三段：零售市場分析
        第四段：廠辦市場分析
        第五段：總結。
        必須在回答中引述提供的數據。
        """

        try:
            # 固定格式
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},#預設
                    {"role": "user", "content": final_prompt},#使用者
                ]
                , temperature=m_tem  # 控制生成內容的隨機性，較低值更穩定
            )

            # 回答固定格式
            answer = response.choices[0].message.content
            return answer
            
        except Exception as e:
            error_msg = f"生成回應時發生錯誤: {str(e)}"
            # print(error_msg)
            return error_msg
        
    m_tem = st.number_input("修改輸出內容多樣性(數字越小越穩定)", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key = 'hk_mon_ai_tem')


    if st.button("進行分析", key = 'hk_mon_ai_b1'):
        result = GAI_hk_month_copy(output1.to_json(orient='records', lines=True, force_ascii=False), output2.to_json(orient='records', lines=True, force_ascii=False), output3.to_json(orient='records', lines=True, force_ascii=False), output4.to_json(orient='records', lines=True, force_ascii=False))
        result_no_punct = re.sub(r'[^\w\u4e00-\u9fff]', '', result)  # 移除標點符號（含中英文）
        char_count = len(result_no_punct)
        st.write(result)
        st.info(f"AI 分析結果字數（不含標點符號）：{char_count} 字")
