#%%
# ===========================================
# ==========  套件匯入區（import）  ==========
# ===========================================

import streamlit as st

#######
from config import *
from data_manager import DataManager
from chart_utils import ChartUtils
from ui_components import UIComponents


# ===========================================
# https://nb7d3pazwhxzsybs3zde75.streamlit.app
# ===========================================


#%%
st.set_page_config(

    layout="wide", 
    page_title="香港房市分析"

)
#%%
@st.cache_resource
def initialize_components():
    return DataManager(), ChartUtils(), UIComponents()

#%%
def main():
    data_manager, chart_utils, ui_components = initialize_components()
    
    # 初始化 session state
    ui_components.initialize_session_state()
    
    # 主選單
    st.selectbox(
        "",
        options=ANALYSIS_OPTIONS,
        key="hk_type", 
        index=0
    )
    
    if st.session_state.hk_type == '香港月資料分析':
        monthly_analysis(data_manager, chart_utils, ui_components) ###


    elif st.session_state.hk_type == '香港季資料分析':
        quarterly_analysis(data_manager, chart_utils, ui_components) ######


    else:
        st.write("功能開發中...")


#%%未檢查
def monthly_analysis(data_manager, chart_utils, ui_components):
    st.title("香港月資料分析")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 載入月資料
        monthly_data = data_manager.load_monthly_data()
        
        # 時間選擇
        time_options = data_manager.get_time_options(monthly_data, 'monthly')
        ui_components.create_time_selector(time_options, 'hk_mo_ti', '香港近期房市數據追蹤')
        
        if st.session_state.hk_mo_ti_st <= st.session_state.hk_mo_ti_en:
            time_range = ui_components.generate_time_range(
                st.session_state.hk_mo_ti_st, 
                st.session_state.hk_mo_ti_en, 
                'monthly'
            )
            st.session_state.result_ti = time_range
            
            # 顏色選擇
            ui_components.create_color_picker()
            
            # 建立標籤頁
            ui_components.create_analysis_tabs(monthly_data, time_range, chart_utils, 'monthly')
        else:
            st.error('時間設定錯誤')
    
    with col2:
        ui_components.create_ai_analysis_section(monthly_data, 'monthly')


#%%未檢查
def quarterly_analysis(data_manager, chart_utils, ui_components):
    st.title("香港季資料分析")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 載入季資料
        quarterly_data = data_manager.load_quarterly_data()
        
        # 時間選擇
        time_options = data_manager.get_time_options(quarterly_data, 'quarterly')
        ui_components.create_time_selector(time_options, 'hk_se_ti', '香港近期房市數據追蹤')
        
        if st.session_state.hk_se_ti_st <= st.session_state.hk_se_ti_en:
            time_range = ui_components.generate_year_quarter_range(
                st.session_state.hk_se_ti_st, 
                st.session_state.hk_se_ti_en
            )
            st.session_state.year_quarter_list = time_range
            
            # 顏色選擇
            ui_components.create_color_picker()
            
            # 建立標籤頁
            ui_components.create_analysis_tabs(quarterly_data, time_range, chart_utils, 'quarterly')
        else:
            st.error('時間設定錯誤')
    
    with col2:
        ui_components.create_ai_analysis_section(quarterly_data, 'quarterly')

if __name__ == "__main__":
    main()
#




####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


###########
# %% 交易量
# trade_mon = pd.DataFrame()
# for key,value in trahk_path.items():
#     path = value
#     types = key






        

            

            

        # df['月'] = df['月'].replace(' ', np.nan)
        # df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        # df_clean['季'] =round((df_clean['月']+1)/3)
        # df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        # df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        # # 顯示數據的前幾行
        # if trade_mon.empty:
        #     trade_mon = df_clean
        # else:
        #     trade_mon = pd.merge(trade_mon,df_clean, on=['年', '季', '月'], how='outer')

    # else:
    #     st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")

# trade_mon['住宅'] = trade_mon['住宅(一手買賣)'] + trade_mon['住宅(二手買賣)']
# trade_mon = trade_mon[['年', '季', '月', '住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']]
# trade_mon['年月'] = trade_mon['年']*100 + trade_mon['月']
# trade_mon = trade_mon[['年', '季', '月', '年月', '住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']]
# trade_mon[['年', '季', '月', '年月']] = trade_mon[['年', '季', '月', '年月']].astype(int)
# trade_mon[['住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']] = trade_mon[['住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']].astype(int)
# st.subheader('交易量資料表', divider = 'rainbow')
# st.write(trade_mon)


#交易季資料
# trade_sea = trade_mon.copy()
# trade_sea = trade_sea.groupby(['年', '季']).agg({
#     '住宅': 'sum',
#     '辦公': 'sum',
#     '零售': 'sum',
#     '廠辦': 'sum'
# }).reset_index()

# trade_sea['年季'] = trade_sea['年'].astype(int).astype(str) + 'Q' + trade_sea['季'].astype(int).astype(str)
# trade_sea = trade_sea[['年', '季', '年季', '住宅', '辦公', '零售', '廠辦']]



#%%投報率
# retu_mon = pd.DataFrame()
# for key,value in retuhk_path.items():
#     path = value
#     types = key

#     # 使用pandas讀取Excel文件
#     # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數

#     response = requests.get(path)


#         if (types =='住宅') :
#             df = pd.read_excel(data2,sheet_name='Monthly(Domestic) 按月(住宅)',header=6)
#             df = df[['年','Unnamed: 5','Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
#             df.columns = ['年','Unnamed: 5','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']
#             # df['類別'] = '住宅'
            
#         if (types =='其他'):
#             df = pd.read_excel(data2,sheet_name='Monthly(Non-domestic) 按月(非住宅)',header=8)
#             df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17']]
#             df.columns = ['年','Unnamed: 5','辦公(甲級)','辦公(乙級)','廠辦','零售']
#             #df['類別'] = '辦公'
            
        
        
#         df['年'] = pd.to_numeric(df['年'], errors='coerce')
#         df['月'] = pd.to_numeric(df['Unnamed: 5'], errors='coerce')
#         # df['月'] = df['月'].replace(' ', np.nan)
#         df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
#         df_clean['季'] =round((df_clean['月']+1)/3)
#         df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
#         df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
#         # 顯示數據的前幾行
#         if retu_mon.empty:
#             retu_mon = df_clean
#         else:
#             retu_mon = pd.merge(retu_mon,df_clean, on=['年', '季', '月'], how='outer')

#     else:
#         st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")
                 
# retu_mon = retu_mon[['年', '季', '月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
#                 '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
# retu_mon = retu_mon.replace('-', np.nan)

# retu_mon.loc[:] = retu_mon.loc[:].apply(pd.to_numeric, errors='coerce')
# # retu_mon['年月'] = retu_mon['年']*100 + retu_mon['月']
# retu_mon = retu_mon[['年', '季', '月', '年月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
#                 '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
# retu_mon[['年', '季', '月', '年月']] = retu_mon[['年', '季', '月', '年月']].astype(int)
# retu_mon[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']] = retu_mon[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']].astype(float)
# # st.subheader('投報率資料表', divider = 'rainbow')
# # st.write(retu_mon)


# #########################################################################################################季投報率
# retu_sea = pd.DataFrame()
# for key,value in retuhk_path.items():
#     path = value
#     types = key

#     # 使用pandas讀取Excel文件
#     # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數

#     response = requests.get(path)

#     if response.status_code == 200:

#         data2 = BytesIO(response.content)
        
#         if (types =='住宅') :
#             df = pd.read_excel(data2,sheet_name='Quarterly(Domestic) 按季(住宅)',header=6)
#             df = df[['年','月', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
#             df.columns = ['年','月','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']
#             # df['類別'] = '住宅'
            
#         if (types =='其他'):
#             df = pd.read_excel(data2,sheet_name='Quarterly(Non-domestic) 按季(非住宅)',header=8)
#             df = df[['年','月', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17']]
#             df.columns = ['年','月','辦公(甲級)','辦公(乙級)','廠辦','零售']
#             #df['類別'] = '辦公'
            
        
        
#         df['年'] = pd.to_numeric(df['年'], errors='coerce')
#         df['月'] = pd.to_numeric(df['月'], errors='coerce')
#         # df['月'] = df['月'].replace(' ', np.nan)
#         df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
#         df_clean['季'] =round((df_clean['月']+1)/3)
#         df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
#         df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
#         # 顯示數據的前幾行
#         if retu_sea.empty:
#             retu_sea = df_clean
#         else:
#             retu_sea = pd.merge(retu_sea,df_clean, on=['年', '季', '月'], how='outer')

#     else:
#         st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")
                 
# retu_sea = retu_sea[['年', '季', '月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
#                 '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
# # retu_sea = retu_sea.replace('-', np.nan)

# # retu_sea.loc[:] = retu_sea.loc[:].apply(pd.to_numeric, errors='coerce')
# # retu_sea['年季'] = retu_sea['年'].astype(int).astype(str) + 'Q' + retu_sea['季'].astype(int).astype(str)
# retu_sea = retu_sea[['年', '季', '年季', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
#                 '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
# retu_sea[['年', '季']] = retu_sea[['年', '季']].astype(int)
# retu_sea[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']] = retu_sea[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']].astype(float)





#%% 月售價
# sold_mon = pd.DataFrame()
# for key,value in soldhk_path.items():
#     path = value
#     types = key
        
#     # 使用pandas讀取Excel文件
#     # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數

#     response = requests.get(path)

#     if response.status_code == 200:
#         data3 = BytesIO(response.content)

#         df = pd.read_excel(data3,sheet_name=0,header=5)
    
#         if (types =='住宅') :
#             df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
#                         'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
#                         'Unnamed: 29']]
#             df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
            
#         if (types =='辦公'):
#             df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
#                         'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
#             df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
            
#         if (types == '零售') | (types == '廠辦'):
#             df = df[['年','Unnamed: 5','Unnamed: 14']]
#             df.columns = ['年','月','零售(平均)'] if types =='零售' else ['年','月','廠辦(平均)']
        
#         df['年'] = pd.to_numeric(df['年'], errors='coerce')
#         df['月'] = pd.to_numeric(df['月'], errors='coerce')
#         # df['月'] = df['月'].replace(' ', np.nan)
#         df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
#         df_clean['季'] =round((df_clean['月']+1)/3)
#         df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
#         df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
#         df_clean = df_clean.replace(')@','Indicates fewer than 20 transactions.')
#         df_clean = df_clean.replace(')~','Indicates fewer than 20 transactions.')

#         # 顯示數據的前幾行
        
#         if sold_mon.empty:
#             sold_mon = df_clean   
#         else:
#             sold_mon = pd.merge(sold_mon,df_clean, on=['年', '季', '月'], how='outer')


#     else:
#         st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")    

        

# sold_mon = sold_mon[['年', '季','月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#     '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#     '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# sold_mon = sold_mon.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
# sold_mon = sold_mon.replace('-', np.nan)
# sold_mon.loc[:] = sold_mon.loc[:].apply(pd.to_numeric, errors='coerce')
# sold_mon['年月'] = sold_mon['年']*100 + sold_mon['月']
# sold_mon = sold_mon[['年', '季','月', '年月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#     '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#     '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# sold_mon[['年', '季', '月', '年月']] = sold_mon[['年', '季', '月', '年月']].astype(int)
# sold_mon[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#     '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#     '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = sold_mon[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#     '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#     '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)

# st.subheader('售價指數資料表', divider = 'rainbow')
# st.write(sold_mon)




#%% 季售價
# sold_sea = pd.DataFrame()
# for key,value in soldhk_path.items():
#     path = value
#     types = key
        
#     # 使用pandas讀取Excel文件
#     # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數

#     response = requests.get(path)

#     if response.status_code == 200:
#         data3 = BytesIO(response.content)

#         df = pd.read_excel(data3,sheet_name=1,header=5)
    
#         if (types =='住宅') :
#             df = df[['年', '月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
#                         'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
#                         'Unnamed: 29']]
#             df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
            
#         if (types =='辦公'):
#             df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
#                         'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
#             df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
            
#         if (types == '零售') | (types == '廠辦'):
#             df = df[['年','月','Unnamed: 14']]
#             df.columns = ['年','月','零售(平均)'] if types =='零售' else ['年','月','廠辦(平均)']
        
#         df['年'] = pd.to_numeric(df['年'], errors='coerce')
#         df['月'] = pd.to_numeric(df['月'], errors='coerce')
#         # df['月'] = df['月'].replace(' ', np.nan)
#         df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
#         df_clean['季'] =round((df_clean['月']+1)/3)
#         df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
#         df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
#         df_clean = df_clean.replace(')@','Indicates fewer than 20 transactions.')
#         df_clean = df_clean.replace(')~','Indicates fewer than 20 transactions.')

#         # 顯示數據的前幾行
        
#         if sold_sea.empty:
#             sold_sea = df_clean   
#         else:
#             sold_sea = pd.merge(sold_sea,df_clean, on=['年', '季', '月'], how='outer')


#     else:
#         st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")    

        

# sold_sea = sold_sea[['年', '季','月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#     '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#     # '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# sold_sea = sold_sea.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
# sold_sea = sold_sea.replace('-', np.nan)
# sold_sea.loc[:] = sold_sea.loc[:].apply(pd.to_numeric, errors='coerce')
# sold_sea['年季'] = sold_sea['年'].astype(int).astype(str) + 'Q' + sold_sea['季'].astype(int).astype(str)
# sold_sea = sold_sea[['年', '季', '年季', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# sold_sea[['年', '季']] = sold_sea[['年', '季']].astype(int)
# sold_sea[['住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = sold_sea[['住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)





#%% 月租金
# rent_mon = pd.DataFrame()
# for key,value in renthk_path.items():
#     path = value
#     types = key
        
#     # 使用pandas讀取Excel文件
#     # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數
#     response = requests.get(path)

#     if response.status_code == 200:
#         data4 = BytesIO(response.content)

#         df = pd.read_excel(data4,sheet_name=0,header=5)
        
#         if (types =='住宅') :
#             df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
#                         'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
#                         'Unnamed: 29']]
#             df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
            
#         if (types =='辦公'):
#             df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
#                         'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
#             df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
            
#         if (types == '零售') :
#             df = df[['年','Unnamed: 5','Unnamed: 9']]
#             df.columns = ['年','月','零售(平均)']
        
#         if (types == '廠辦'):
#             df = df[['年','Unnamed: 5','Unnamed: 9']]
#             df.columns = ['年','月','廠辦(平均)']

#         df['年'] = pd.to_numeric(df['年'], errors='coerce')
#         df['月'] = pd.to_numeric(df['月'], errors='coerce')
#         # df['月'] = df['月'].replace(' ', np.nan)
#         df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        # df_clean['季'] =round((df_clean['月']+1)/3)
        # df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        # df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        # 顯示數據的前幾行
        # if rent_mon.empty:
        #     rent_mon = df_clean   
        # else:
        #     rent_mon = pd.merge(rent_mon,df_clean, on=['年', '季', '月'], how='outer')
        #     # print("數據已保存為 rvd_data.csv")


    # else:
    #     st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")    


# rent_mon = rent_mon[['年', '季', '月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#        '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#          '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# rent_mon = rent_mon.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
# rent_mon = rent_mon.replace('-', np.nan)
# rent_mon.loc[:] = rent_mon.loc[:].apply(pd.to_numeric, errors='coerce')
# rent_mon['年月'] = rent_mon['年']*100 + rent_mon['月']
# rent_mon = rent_mon[['年', '季', '月', '年月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#        '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#          '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# rent_mon[['年', '季', '月', '年月']] = rent_mon[['年', '季', '月', '年月']].astype(int)
# rent_mon[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#        '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#          '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = rent_mon[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#        '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#          '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)
# st.subheader('租金指數資料表', divider = 'rainbow')
# st.write(rent_mon)

#%% 季租金
# rent_sea = pd.DataFrame()
# for key,value in renthk_path.items():
#     path = value
#     types = key
        
    # 使用pandas讀取Excel文件
    # 注意：如果Excel文件有多個工作表，你可能需要指定sheet_name參數
    # response = requests.get(path)

    # if response.status_code == 200:
    #     data4 = BytesIO(response.content)

    #     df = pd.read_excel(data4,sheet_name=1,header=5)
        
        # if (types =='住宅') :
        #     df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
        #                 'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
        #                 'Unnamed: 29']]
        #     df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
            
        # if (types =='辦公'):
        #     df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
        #                 'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
        #     df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
            
        # if (types == '零售') :
        #     df = df[['年','月','Unnamed: 9']]
        #     df.columns = ['年','月','零售(平均)']
        
        # if (types == '廠辦'):
        #     df = df[['年','月','Unnamed: 9']]
        #     df.columns = ['年','月','廠辦(平均)']

        # df['年'] = pd.to_numeric(df['年'], errors='coerce')
        # df['月'] = pd.to_numeric(df['月'], errors='coerce')
        # # df['月'] = df['月'].replace(' ', np.nan)
        # df_clean = df[(~df['月'].isnull()) & (df['月']!='月') & (df['月']!='Month')].reset_index(drop=True)

        
        # df_clean['季'] =round((df_clean['月']+1)/3)
        # df_clean.loc[:,'年'] = df_clean.loc[:,'年'].ffill()
        
        # df_clean = df_clean.replace(')','Indicates fewer than 20 transactions.')
        # df_clean = df_clean.replace(')@','Indicates fewer than 20 transactions.')
        # df_clean = df_clean.replace(')~','Indicates fewer than 20 transactions.')

        # 顯示數據的前幾行
        
    #     if rent_sea.empty:
    #         rent_sea = df_clean   
    #     else:
    #         rent_sea = pd.merge(rent_sea,df_clean, on=['年', '季', '月'], how='outer')
    #         # print("數據已保存為 rvd_data.csv")


    # else:
    #     st.error(f"下載{path}時失敗，HTTP狀態碼: {response.status_code}")    


# rent_sea = rent_sea[['年', '季', '月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
#        '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
#          '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# rent_sea = rent_sea.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
# rent_sea = rent_sea.replace('-', np.nan)
# rent_sea.loc[:] = rent_sea.loc[:].apply(pd.to_numeric, errors='coerce')
# rent_sea['年季'] = rent_sea['年'].astype(int).astype(str) + 'Q' + rent_sea['季'].astype(int).astype(str)
# rent_sea = rent_sea[['年', '季', '年季', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
# rent_sea[['年', '季']] = rent_sea[['年', '季']].astype(int)
# rent_sea[['住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = rent_sea[['住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)




# #%%
# # ====================================================
# # 從四個 output DataFrame 中取得最新14個月
# # ====================================================
# def generate_month_list():
#     # 收集所有 DataFrame 中的年月資料
#     all_months = set()
    
#     # 從四個 output DataFrame 中收集年月資料
#     for df in [trade_mon, retu_mon, sold_mon, rent_mon]:
#         if not df.empty and '年月' in df.columns:
#             all_months.update(df['年月'].dropna().astype(int))
    
#     # 排序並取最新的14個月
#     sorted_months = sorted(list(all_months))
#     result = sorted_months[-14:] if len(sorted_months) >= 14 else sorted_months
    
#     return result

# t_option = generate_month_list()

# # ====================================================
# # ====================================================

# #%%
# # ====================================================
# # 從四個 output DataFrame 中取得季
# # ====================================================
# def generate_season_list():
#     # 收集所有 DataFrame 中的年月資料
#     all_seasons = set()
    
#     for df in [trade_sea, retu_sea, sold_sea, rent_sea]:
#         if not df.empty and '年季' in df.columns:
#             all_seasons.update(df['年季'].dropna())

#     # 排序並取最新的14個季
#     sorted_seasons = sorted(list(all_seasons))
#     result = sorted_seasons[-95:]

    
#     return result

# season_option = generate_season_list()

# ====================================================
# ====================================================
#%%
# st.selectbox(
# "",
#     options=('香港月資料分析', '香港季資料分析', '香港總體經濟指標'),
#     key="hk_type", 
#     index = 0
# )
# if st.session_state.hk_type == '香港月資料分析':
#     #%%
#     st.title("香港月資料分析")
#     col11, col12 = st.columns([3, 2])
#     with col11:
#         st.header("香港近期房市數據追蹤", divider= 'rainbow')  ##選時間
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("起始時間", divider = 'rainbow')

#             st.selectbox(
#             "",
#                 options=t_option,
#                 key="hk_mo_ti_st", 
#                 index=1
#         )
            
#         with col2:
#             st.subheader("終止時間", divider = 'rainbow')

#             st.selectbox(
#             "",
#                 options=t_option,
#                 key="hk_mo_ti_en", 
#                 index = len(t_option)-1
#         )


    # if st.session_state.hk_mo_ti_st <= st.session_state.hk_mo_ti_en:
    #     hk_m_get_ti = [st.session_state.hk_mo_ti_st, st.session_state.hk_mo_ti_en]
    #     st.session_state.result_ti = []
    #     y, m = divmod(hk_m_get_ti[0], 100)##得商數餘數
    #     while y * 100 + m <= hk_m_get_ti[1]:
    #         st.session_state.result_ti.append(y * 100 + m)
    #         m += 1
    #         if m > 12:
    #             m = 1
    #             y += 1
    #     st.success(f'你已選擇：{hk_m_get_ti[0]}到{hk_m_get_ti[1]}')
            # st.write(st.session_state.result_ti)



            #%%選顏色
            # cola, colb = st.columns(2)
            # if 'm_color1' not in st.session_state:
            #     st.session_state.m_color1 = '#5C4141'
            # if 'm_color2' not in st.session_state:
            #     st.session_state.m_color2 = '#1F77B4'


            # with cola:
            #     st.session_state.m_color1 = st.color_picker("選擇長條圖顏色", value=st.session_state.m_color1)
            # with colb:
            #     st.session_state.m_color2 = st.color_picker("選擇折線圖顏色", value=st.session_state.m_color2)


            # tab1, tab2, tab3, tab4, tab5 = st.tabs(['住宅', '辦公', '零售', '廠辦', '檢視與下載資料表'])



#             with tab1:
#                 # col1, col2, col3 = st.columns(3)

#                 # with col1:
#                     x = st.session_state.result_ti
#                     yb_1_1 = trade_mon[trade_mon['年月'].isin(st.session_state.result_ti)]['住宅']
#                     ys_1_1 = sold_mon[sold_mon['年月'].isin(st.session_state.result_ti)]['住宅(平均)']
#                     co1_1_1 = st.session_state.m_color1
#                     co2_1_1 = st.session_state.m_color2
#                     st.subheader('住宅買賣市場', divider='rainbow')
#                     mul_trade(x, yb_1_1, ys_1_1, co1_1_1, co2_1_1)
#                 # with col2:
#                     ys_1_2 = rent_mon[rent_mon['年月'].isin(st.session_state.result_ti)]['住宅(平均)']
#                     st.subheader('住宅租賃市場', divider='rainbow')
#                     mul_rent(x, ys_1_2, co2_1_1)
#                 # with col3:
#                     ys_1_3 = [retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['住宅(A)'],
#                             retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['住宅(B)'],
#                             retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['住宅(C)'],
#                             retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['住宅(D)'],
#                             retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['住宅(E)']
#                     ] 

#                     col1_3 = ['red', 'green', 'blue', 'orange', 'purple']
#                     st.subheader('住宅投報率', divider='rainbow')
#                     mul_retu(x, ys_1_3, col1_3)   


            
#             with tab2:
#                 # col1, col2, col3 = st.columns(3)
#                 # with col1:
#                     x = st.session_state.result_ti
#                     yb_2_1 = trade_mon[trade_mon['年月'].isin(st.session_state.result_ti)]['辦公']
#                     ys_2_1 = sold_mon[sold_mon['年月'].isin(st.session_state.result_ti)]['辦公(平均)']
#                     st.subheader('辦公買賣市場', divider='rainbow')
#                     mul_trade(x, yb_2_1, ys_2_1, co1_1_1, co2_1_1)
#                 # with col2:
#                     ys_2_2 = rent_mon[rent_mon['年月'].isin(st.session_state.result_ti)]['辦公(平均)']
#                     st.subheader('辦公租賃市場', divider='rainbow')
#                     mul_rent(x, ys_2_2, co2_1_1)
#                 # with col3:
#                     ys_2_3 = [retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['辦公(甲級)'],
#                             retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['辦公(乙級)']
#                     ]
#                     col2_3 = ['red', 'green'] 
#                     st.subheader('辦公投報率', divider='rainbow')
#                     mul_retu(x, ys_2_3, col2_3)     

#             with tab3:
#                 # col1, col2, col3 = st.columns(3)
#                 # with col1:
#                     x = st.session_state.result_ti
#                     yb_3_1 = trade_mon[trade_mon['年月'].isin(st.session_state.result_ti)]['零售']
#                     ys_3_1 = sold_mon[sold_mon['年月'].isin(st.session_state.result_ti)]['零售(平均)']

#                     st.subheader('零售買賣市場', divider='rainbow')
#                     mul_trade(x, yb_3_1, ys_3_1, co1_1_1, co2_1_1)    
#                 # with col2:
#                     ys_3_2 = rent_mon[rent_mon['年月'].isin(st.session_state.result_ti)]['零售(平均)']        
#                     st.subheader('零售租賃市場', divider='rainbow')
#                     mul_rent(x, ys_3_2, co2_1_1)
#                 # with col3:
#                     ys_3_3 = [retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['零售']
#                     ]
#                     col3_3 = ['red'] 
#                     st.subheader('零售投報率', divider='rainbow')
#                     mul_retu(x, ys_3_3, col3_3)          

#             with tab4:
#                 # col1, col2, col3 = st.columns(3)

#                 # with col1:
#                     x = st.session_state.result_ti
#                     yb_4_1 = trade_mon[trade_mon['年月'].isin(st.session_state.result_ti)]['廠辦']
#                     ys_4_1 = sold_mon[sold_mon['年月'].isin(st.session_state.result_ti)]['廠辦(平均)']
#                     st.subheader('廠辦買賣市場', divider='rainbow')
#                     mul_trade(x, yb_4_1, ys_4_1, co1_1_1, co2_1_1)

#                 # with col2:
#                     ys_4_2 = rent_mon[rent_mon['年月'].isin(st.session_state.result_ti)]['廠辦(平均)']
#                     st.subheader('廠辦租賃市場', divider='rainbow')
#                     mul_rent(x, ys_4_2, co2_1_1)

#                 # with col3:
#                     ys_4_3 = [retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)]['廠辦']
#                     ]
#                     col4_3 = ['red']
#                     st.subheader('廠辦投報率', divider='rainbow') 
#                     mul_retu(x, ys_4_3, col4_3)          

#             with tab5:
#                 trade_mon = trade_mon[trade_mon['年月'].isin(st.session_state.result_ti)][['年', '季', '月', '年月', '住宅', '辦公', '零售', '廠辦']]
#                 with st.expander('交易量資料表', expanded=False):
#                     st.dataframe(trade_mon)

#                 retu_mon = retu_mon[retu_mon['年月'].isin(st.session_state.result_ti)][['年', '季', '月', '年月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
#                 with st.expander('投報率資料表', expanded=False):
#                     st.dataframe(retu_mon)

#                 sold_mon = sold_mon[sold_mon['年月'].isin(st.session_state.result_ti)][['年', '季','月', '年月', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
#                 with st.expander('價格指數資料表', expanded=False):
#                     st.dataframe(sold_mon)
                    
#                 rent_mon = rent_mon[rent_mon['年月'].isin(st.session_state.result_ti)][['年', '季', '月', '年月', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
#                 with st.expander('租金指數資料表', expanded=False):
#                     st.dataframe(rent_mon)
#                 # st.dataframe(pd.DataFrame(trade_mon.dtypes, columns=['資料型態']))
#                 # st.dataframe(pd.DataFrame(retu_mon.dtypes, columns=['資料型態']))
#                 # st.dataframe(pd.DataFrame(sold_mon.dtypes, columns=['資料型態']))
#                 # st.dataframe(pd.DataFrame(rent_mon.dtypes, columns=['資料型態']))


#         else:
#             st.error('時間問題')



#     with col12:
#         st.header("香港月資料AI摘要", divider= 'rainbow')


#         with st.expander('輸入api金鑰', expanded=False):
#             key = st.text_input('', max_chars= 60)

#         def GAI_hk_month_copy(a, b, c, d):
#             client = OpenAI(
#                 api_key=key,
#                 base_url="https://api.groq.com/openai/v1"
#             )
            
#             model = "meta-llama/llama-4-scout-17b-16e-instruct"
#             system_prompt = f"""
#             你是一位香港房市分析專家，擅長透過數據分析房市。
#             使用提供的交易量{a}、物價指數{c}、租金指數{d}、投報率{b}四個資料表格，進行以下要求：
#             1. 用繁體中文及台灣用語回答，禁止其他語言。
#             2. 回應精簡，邏輯清晰，避免冗長或籠統陳述。
#             3. 必須僅引用提供的數據。
#             4. 若有空值，請不要分析該時間點的數據，直接忽略。
#             5. 聚焦異常趨勢，如急升/降或相關性。
#             其中投報率retu.json表格中住宅A類面積最小，住宅E類面積最大；甲級辦公室比乙級辦公室高級。
#             """ 

#             final_prompt = f"""
#             根據表格回答問題，分五段，各段都需照順序分析交易量、售價指數、租金指數、各級物件投報率四種指標：
#             第一段：住宅市場分析
#             第二段：辦公市場分析
#             第三段：零售市場分析
#             第四段：廠辦市場分析
#             第五段：總結。
#             必須在回答中引述提供的數據。
#             """

#             try:
#                 response = client.chat.completions.create(
#                     model=model,
#                     messages=[
#                         {"role": "system", "content": system_prompt},
#                         {"role": "user", "content": final_prompt},
#                     ],
#                     temperature=m_tem
#                 )
                
#                 answer = response.choices[0].message.content
#                 return answer
                
#             except Exception as e:
#                 error_msg = f"生成回應時發生錯誤: {str(e)}"
#                 return error_msg
            
#         m_tem = st.number_input("修改輸出內容多樣性(數字越小越穩定)", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key = 'hk_mon_ai_tem')


#         if st.button("進行分析", key = 'hk_mon_ai_b1'):
#             result = GAI_hk_month_copy(trade_mon.to_json(orient='records', lines=True, force_ascii=False), retu_mon.to_json(orient='records', lines=True, force_ascii=False), sold_mon.to_json(orient='records', lines=True, force_ascii=False), rent_mon.to_json(orient='records', lines=True, force_ascii=False))
#             result_no_punct = re.sub(r'[^\w\u4e00-\u9fff]', '', result)  # 移除標點符號（含中英文）
#             char_count = len(result_no_punct)
#             st.write(result)
#             st.info(f"AI 分析結果字數（不含標點符號）：{char_count} 字")


# # elif st.session_state.hk_type == '香港季資料分析':
# #     #%%
# #     st.title("香港季資料分析")
# #     col11, col12 = st.columns([3, 2])
# #     with col11:
# #         st.header("香港近期房市數據追蹤", divider= 'rainbow')  ##選時間
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             st.subheader("起始時間", divider = 'rainbow')

# #             st.selectbox(
# #             "",
# #                 options=season_option,
# #                 key="hk_se_ti_st", 
# #                 index=0
# #         )
            
# #         with col2:
# #             st.subheader("終止時間", divider = 'rainbow')

# #             st.selectbox(
# #             "",
# #                 options=season_option,
# #                 key="hk_se_ti_en", 
# #                 index = len(season_option)-1
# #         )


#         # if st.session_state.hk_se_ti_st <= st.session_state.hk_se_ti_en:
#         #     def generate_year_quarter_range(start, end):
#         #         # start, end 格式都像 "2020Q1"
#         #         start_year, start_q = int(start[:4]), int(start[-1])
#         #         end_year, end_q = int(end[:4]), int(end[-1])
#         #         result = []
#         #         while (start_year < end_year) or (start_year == end_year and start_q <= end_q):
#         #             result.append(f"{start_year}Q{start_q}")
#         #             start_q += 1
#         #             if start_q > 4:
#         #                 start_q = 1
#         #                 start_year += 1
#         #         return result
#         #     st.session_state.year_quarter_list = generate_year_quarter_range(st.session_state.hk_se_ti_st, st.session_state.hk_se_ti_en)
#             # st.write(st.session_state.result_ti)



#             #%%選顏色
#             cola, colb = st.columns(2)
#             if 'm_color1' not in st.session_state:
#                 st.session_state.m_color1 = '#5C4141'
#             if 'm_color2' not in st.session_state:
#                 st.session_state.m_color2 = '#1F77B4'


#             with cola:
#                 st.session_state.m_color1 = st.color_picker("選擇長條圖顏色", value=st.session_state.m_color1)
#             with colb:
#                 st.session_state.m_color2 = st.color_picker("選擇折線圖顏色", value=st.session_state.m_color2)


#             tab1, tab2, tab3, tab4, tab5 = st.tabs(['住宅', '辦公', '零售', '廠辦', '檢視與下載資料表'])



#             with tab1:
#                 # col1, col2, col3 = st.columns(3)

#                 # with col1:
#                     x = st.session_state.year_quarter_list
#                     yb_1_1 = trade_sea[trade_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅']
#                     ys_1_1 = sold_sea[sold_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(平均)']
#                     co1_1_1 = st.session_state.m_color1
#                     co2_1_1 = st.session_state.m_color2
#                     st.subheader('住宅買賣市場', divider='rainbow')
#                     mul_trade(x, yb_1_1, ys_1_1, co1_1_1, co2_1_1)
#                 # with col2:
#                     ys_1_2 = rent_sea[rent_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(平均)']
#                     st.subheader('住宅租賃市場', divider='rainbow')
#                     mul_rent(x, ys_1_2, co2_1_1)
#                 # with col3:
#                     ys_1_3 = [retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(A)'],
#                             retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(B)'],
#                             retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(C)'],
#                             retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(D)'],
#                             retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['住宅(E)']
#                     ] 

#                     col1_3 = ['red', 'green', 'blue', 'orange', 'purple']
#                     st.subheader('住宅投報率', divider='rainbow')
#                     mul_retu(x, ys_1_3, col1_3)   


            
#             with tab2:
#                 # col1, col2, col3 = st.columns(3)
#                 # with col1:
#                     x = st.session_state.year_quarter_list
#                     yb_2_1 = trade_sea[trade_sea['年季'].isin(st.session_state.year_quarter_list)]['辦公']
#                     ys_2_1 = sold_sea[sold_sea['年季'].isin(st.session_state.year_quarter_list)]['辦公(平均)']
#                     st.subheader('辦公買賣市場', divider='rainbow')
#                     mul_trade(x, yb_2_1, ys_2_1, co1_1_1, co2_1_1)
#                 # with col2:
#                     ys_2_2 = rent_sea[rent_sea['年季'].isin(st.session_state.year_quarter_list)]['辦公(平均)']
#                     st.subheader('辦公租賃市場', divider='rainbow')
#                     mul_rent(x, ys_2_2, co2_1_1)
#                 # with col3:
#                     ys_2_3 = [retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['辦公(甲級)'],
#                             retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['辦公(乙級)']
#                     ]
#                     col2_3 = ['red', 'green'] 
#                     st.subheader('辦公投報率', divider='rainbow')
#                     mul_retu(x, ys_2_3, col2_3)     

#             with tab3:
#                 # col1, col2, col3 = st.columns(3)
#                 # with col1:
#                     x = st.session_state.year_quarter_list
#                     yb_3_1 = trade_sea[trade_sea['年季'].isin(st.session_state.year_quarter_list)]['零售']
#                     ys_3_1 = sold_sea[sold_sea['年季'].isin(st.session_state.year_quarter_list)]['零售(平均)']

#                     st.subheader('零售買賣市場', divider='rainbow')
#                     mul_trade(x, yb_3_1, ys_3_1, co1_1_1, co2_1_1)    
#                 # with col2:
#                     ys_3_2 = rent_sea[rent_sea['年季'].isin(st.session_state.year_quarter_list)]['零售(平均)']        
#                     st.subheader('零售租賃市場', divider='rainbow')
#                     mul_rent(x, ys_3_2, co2_1_1)
#                 # with col3:
#                     ys_3_3 = [retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['零售']
#                     ]
#                     col3_3 = ['red'] 
#                     st.subheader('零售投報率', divider='rainbow')
#                     mul_retu(x, ys_3_3, col3_3)          

#             with tab4:
#                 # col1, col2, col3 = st.columns(3)

#                 # with col1:
#                     x = st.session_state.year_quarter_list
#                     yb_4_1 = trade_sea[trade_sea['年季'].isin(st.session_state.year_quarter_list)]['廠辦']
#                     ys_4_1 = sold_sea[sold_sea['年季'].isin(st.session_state.year_quarter_list)]['廠辦(平均)']
#                     st.subheader('廠辦買賣市場', divider='rainbow')
#                     mul_trade(x, yb_4_1, ys_4_1, co1_1_1, co2_1_1)

#                 # with col2:
#                     ys_4_2 = rent_sea[rent_sea['年季'].isin(st.session_state.year_quarter_list)]['廠辦(平均)']
#                     st.subheader('廠辦租賃市場', divider='rainbow')
#                     mul_rent(x, ys_4_2, co2_1_1)

#                 # with col3:
#                     ys_4_3 = [retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)]['廠辦']
#                     ]
#                     col4_3 = ['red']
#                     st.subheader('廠辦投報率', divider='rainbow') 
#                     mul_retu(x, ys_4_3, col4_3)          

#             with tab5:
#                 trade_sea = trade_sea[trade_sea['年季'].isin(st.session_state.year_quarter_list)][['年', '季', '年季', '住宅', '辦公', '零售', '廠辦']]
#                 with st.expander('交易量資料表', expanded=False):
#                     st.dataframe(trade_sea)

#                 retu_sea = retu_sea[retu_sea['年季'].isin(st.session_state.year_quarter_list)][['年', '季', '年季', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
#                 with st.expander('投報率資料表', expanded=False):
#                     st.dataframe(retu_sea)

#                 sold_sea = sold_sea[sold_sea['年季'].isin(st.session_state.year_quarter_list)][['年', '季', '年季', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
#                 with st.expander('價格指數資料表', expanded=False):
#                     st.dataframe(sold_sea)
#                 rent_sea = rent_sea[rent_sea['年季'].isin(st.session_state.year_quarter_list)][['年', '季', '年季', '住宅(平均)', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
#                 with st.expander('租金指數資料表', expanded=False):
#                     st.dataframe(rent_sea)
#                 # st.dataframe(pd.DataFrame(trade_sea.dtypes, columns=['資料型態']))
#                 # st.dataframe(pd.DataFrame(retu_sea.dtypes, columns=['資料型態']))
#                 # st.dataframe(pd.DataFrame(sold_sea.dtypes, columns=['資料型態']))
#                 # st.dataframe(pd.DataFrame(rent_sea.dtypes, columns=['資料型態']))


#         else:
#             st.error('時間問題')



#     with col12:
#         st.header("香港季資料AI摘要", divider= 'rainbow')



#         with st.expander('輸入api金鑰', expanded=False):
#             key = st.text_input('', max_chars= 60)

#         def GAI_hk_seath_copy(a, b, c, d):
#             client = OpenAI(
#                 api_key=key,
#                 base_url="https://api.groq.com/openai/v1"
#             )
            
#             model = "meta-llama/llama-4-scout-17b-16e-instruct" # 模型設定
#             system_prompt = f"""
#             你是一位香港房市分析專家，擅長透過數據分析房市。
#             使用提供的交易量{a}、物價指數{c}、租金指數{d}、投報率{b}四個季資料表格，進行以下要求：
#             1. 用繁體中文及台灣用語回答，禁止其他語言。
#             2. 回應精簡，邏輯清晰，避免冗長或籠統陳述。
#             3. 必須僅引用提供的數據。
#             4. 若有空值，請不要分析該時間點的數據，直接忽略。
#             5. 聚焦異常趨勢，如急升/降或相關性。
#             其中投報率retu.json表格中住宅A類面積最小，住宅E類面積最大；甲級辦公室比乙級辦公室高級。
#             """ 

#             final_prompt = f"""
#             根據表格回答問題，分五段，各段都需照順序分析交易量、售價指數、租金指數、各級物件投報率四種指標：
#             第一段：住宅市場分析
#             第二段：辦公市場分析
#             第三段：零售市場分析
#             第四段：廠辦市場分析
#             第五段：總結。
#             必須在回答中引述提供的數據。
#             """

#             try:
#                 response = client.chat.completions.create(
#                     model=model,
#                     messages=[
#                         {"role": "system", "content": system_prompt},
#                         {"role": "user", "content": final_prompt},
#                     ],
#                     temperature=m_tem
#                 )
                
#                 answer = response.choices[0].message.content
#                 return answer
                
#             except Exception as e:
#                 error_msg = f"生成回應時發生錯誤: {str(e)}"
#                 return error_msg
            
#         m_tem = st.number_input("修改輸出內容多樣性(數字越小越穩定)", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key = 'hk_sea_ai_tem')


#         if st.button("進行分析", key = 'hk_sea_ai_b1'):
#             result = GAI_hk_seath_copy(trade_sea.to_json(orient='records', lines=True, force_ascii=False), retu_sea.to_json(orient='records', lines=True, force_ascii=False), sold_sea.to_json(orient='records', lines=True, force_ascii=False), rent_sea.to_json(orient='records', lines=True, force_ascii=False))
#             result_no_punct = re.sub(r'[^\w\u4e00-\u9fff]', '', result)  # 移除標點符號（含中英文）
#             char_count = len(result_no_punct)
#             st.write(result)
#             st.info(f"AI 分析結果字數（不含標點符號）：{char_count} 字")
# else:
#     123