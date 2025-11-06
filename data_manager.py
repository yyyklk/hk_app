import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from config import DATA_SOURCES
import re
import json


class DataManager:
    #%%統一
    def __init__(self):
        self._cache_timeout = 3600  # 1小時快取
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def _download_excel(_self, url, sheet_name=0, header=5):
        """快取下載 Excel 檔案"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return pd.read_excel(BytesIO(response.content), sheet_name=sheet_name, header=header)
            else:
                st.error(f"下載失敗，HTTP狀態碼: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"下載錯誤: {str(e)}")
            return None
    
    def _clean_dataframe(self, df):
        """統一資料清理"""
        if df is None or df.empty:
            return pd.DataFrame()
        
        # 處理年月欄位
        df['年'] = pd.to_numeric(df['年'], errors='coerce')
        month_col = '月' if '月' in df.columns else df.columns[1]
        df['月'] = pd.to_numeric(df[month_col], errors='coerce')
        
        # 篩選有效資料
        df_clean = df[(~df['月'].isnull()) & (df['月'] != '月') & (df['月'] != 'Month')].reset_index(drop=True)
        
        if df_clean.empty:
            return pd.DataFrame()
        
        # 計算季度
        df_clean['季'] = np.round((df_clean['月'] + 1) / 3).astype(int)
        df_clean['年'] = df_clean['年'].ffill()
        
        # 替換特殊字符
        df_clean = df_clean.replace([')', ')@', ')~'], 'Indicates fewer than 20 transactions.')
        df_clean = df_clean.replace('-', np.nan)
        
        return df_clean
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def load_monthly_data(_self):
        """載入月資料"""
        with st.spinner('載入月資料中...'):
            return {
                'trade': _self._process_trade_monthly(),
                'return': _self._process_return_monthly(),
                'sold': _self._process_sold_monthly(),
                'rent': _self._process_rent_monthly()
            }
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def load_quarterly_data(_self):
        """載入季資料"""
        with st.spinner('載入季資料中...'):
            return {
                'trade': _self._process_trade_quarterly(),
                'return': _self._process_return_quarterly(),
                'sold': _self._process_sold_quarterly(),
                'rent': _self._process_rent_quarterly(), 
                'vac': _self._process_vac_quarterly()
            }

########################################################################################################################################################

    @st.cache_data(ttl=3600, show_spinner=False)    
    def load_macro_data(_self):
        """載入總體資料"""
        with st.spinner('載入總體資料中...'):
            return {
                'GDP': _self._process_gdp(),
                '失業率': _self._process_une(),
                '訪港旅遊人數': _self._process_tra()
                ,'利率': _self._process_int()
            }
        

    def _process_gdp(self):
        url1 = "https://www.censtatd.gov.hk/api/post.php"
        """處理GDP資料"""
        result_df = pd.DataFrame()
        
        parameters1 ={
        "cv": {
            "GDP_COMPONENT": []
        },
        "sv": {
            "CON": [
            "YoY_1dp_%_s"
            ]
        },
        "period": {
            "start": "197403"
        },
        "id": "310-30001",
        "lang": "tc"
        }
        gdp_data = {'query': json.dumps(parameters1)}
        gdp_response = requests.post(url1, data=gdp_data, timeout=20)
        if gdp_response.status_code == 200:
            gdp_result = gdp_response.json()  # 解析 JSON
            print("API 回應成功！")
            gdp_data_list = [
                        {
                            "季度": item.get("period", "N/A"),
                            "值": item.get("figure", "N/A"),
                        }
                        for item in gdp_result.get("dataSet", [])
                        if re.match(r"^\d{4}(03|06|09|12)$", item.get("period", ""))
                    ]
            gdp_df = pd.DataFrame(gdp_data_list)    
            gdp_df['季度'] = gdp_df['季度'].astype(int)
            gdp_df = gdp_df.sort_values(by=['季度'], ascending = True).reset_index(drop=True)  
            gdp_df['年'] = gdp_df['季度'] // 100  # 整數除法，提取年份 (202202 // 100 = 2022)
            gdp_df['年'] = gdp_df['年'].astype(int)
            gdp_df['月'] = gdp_df['季度'] % 100   # 模運算，提取月份 (202202 % 100 = 02)
            gdp_df['季'] = np.round((gdp_df['月'] + 1) / 3).astype(int)
            gdp_df['年季'] = gdp_df['年'].astype(int).astype(str) + 'Q' + gdp_df['季'].astype(int).astype(str)
            gdp_df = gdp_df[['年', '季', '年季', '值']]
            gdp_df.columns = ['年', '季', '年季', 'GDP年增率']
            gdp_df['GDP年增率'] = gdp_df['GDP年增率']/100
            result_df = gdp_df[['年', '季', '年季', 'GDP年增率']]

        else:
            print(f"錯誤：{gdp_response.status_code} - {gdp_response.text}")
        return result_df
    

    def _process_une(self):
        url1 = "https://www.censtatd.gov.hk/api/post.php"
        """處理失業率資料"""
        result_df = pd.DataFrame()
        
        parameters2 ={
        "cv": {
            "SEX": [
            "M",
            "F"
            ]
        },
        "sv": {
            "UR": [
            "Rate_1dp_%_n"
            ]
        },
        "period": {
            "start": "198503"
        },
        "id": "210-06101",
        "lang": "tc"
        }
        une_data = {'query': json.dumps(parameters2)}
        une_response = requests.post(url1, data=une_data, timeout=20)
        if une_response.status_code == 200:
            une_result = une_response.json()  # 解析 JSON
            print("失業率 API 回應成功！")
            une_data_list_m = [
                        {
                            "季度": item.get("period", "N/A"),
                            "值": item.get("figure", "N/A"),
                        }
                        for item in une_result.get("dataSet", [])
                        if (item.get("SEX", "") == "M" and item.get("freq", "N/A") == "M3M" and re.match(r"^\d{4}(03|06|09|12)$", item.get("period", "")))
                    ]
            une_df_m = pd.DataFrame(une_data_list_m)
            une_df_m['季度'] = une_df_m['季度'].astype(int)
            une_df_m = une_df_m.sort_values(by=['季度'], ascending = True).reset_index(drop=True)
            
            une_data_list_f = [
                        {
                            "季度": item.get("period", "N/A"),
                            "值": item.get("figure", "N/A"),
                        }
                        for item in une_result.get("dataSet", [])
                        if (item.get("SEX", "") == "F" and item.get("freq", "N/A") == "M3M" and re.match(r"^\d{4}(03|06|09|12)$", item.get("period", "")))
                    ]
            une_df_f = pd.DataFrame(une_data_list_f)
            une_df_f['季度'] = une_df_f['季度'].astype(int)
            une_df_f = une_df_f.sort_values(by=['季度'], ascending = True).reset_index(drop=True)  

            une_data_list = [
                        {
                            "季度": item.get("period", "N/A"),
                            "值": item.get("figure", "N/A"),
                        }
                        for item in une_result.get("dataSet", [])
                        if (item.get("SEX", "") == "" and item.get("freq", "N/A") == "M3M" and re.match(r"^\d{4}(03|06|09|12)$", item.get("period", "")))
                    ]
            une_df = pd.DataFrame(une_data_list)
            une_df['季度'] = une_df['季度'].astype(int)
            une_df = une_df.sort_values(by=['季度'], ascending = True).reset_index(drop=True)
            
            a_df = pd.merge(une_df_m, une_df_f, on=['季度'], how='outer', suffixes=('_男', '_女'))
            une_df = pd.merge(a_df, une_df, on=['季度'], how='outer')
            une_df['年'] = une_df['季度'] // 100  # 整數除法，提取年份 (202202 // 100 = 2022)
            une_df['年'] = une_df['年'].astype(int)
            une_df['月'] = une_df['季度'] % 100   # 模運算，提取月份 (202202 % 100 = 02)
            une_df['季'] = np.round((une_df['月'] + 1) / 3).astype(int)
            une_df['年季'] = une_df['年'].astype(int).astype(str) + 'Q' + une_df['季'].astype(int).astype(str)
            une_df = une_df[['年', '季', '年季', '值_男', '值_女', '值']]
            une_df.columns = ['年', '季', '年季', '失業率（男性）', '失業率（女性）', '失業率（合計）']
            une_df[['失業率（男性）', '失業率（女性）', '失業率（合計）']] = une_df[['失業率（男性）', '失業率（女性）', '失業率（合計）']]/100
            result_df = une_df[['年', '季', '年季', '失業率（男性）', '失業率（女性）', '失業率（合計）']]

        else:
            print(f"錯誤：{une_response.status_code} - {une_response.text}")

        return result_df


    def _process_tra(self):
        url1 = "https://www.censtatd.gov.hk/api/post.php"
        """處理旅遊人數資料"""
        result_df = pd.DataFrame()
        
        parameters3 ={
        "cv": {
            "REGION": [
            "CN"
            ]
        },
        "sv": {
            "VIS_ARR": [
            "Raw_per_n"
            ]
        },
        "period": {
            "start": "200401"
        },
        "id": "650-80001",
        "lang": "tc"
        }
        tra_data = {'query': json.dumps(parameters3)}
        tra_response = requests.post(url1, data=tra_data, timeout=20)
        if tra_response.status_code == 200:
            tra_result = tra_response.json()  # 解析 JSON
            print("旅遊人數 API 回應成功！")
            tra_data_list_c = [
                        {
                            "季度": item.get("period", "N/A"),
                            "值": item.get("figure", "N/A"),
                        }
                        for item in tra_result.get("dataSet", [])
                        if (item.get("REGIONDesc", "") == "中國內地" and re.match(r"^\d{6}$", item.get("period", "")))
                    ]
            tra_df_c = pd.DataFrame(tra_data_list_c)
            tra_df_c['季度'] = tra_df_c['季度'].astype(int)
            tra_df_c = tra_df_c.sort_values(by=['季度'], ascending = True).reset_index(drop=True)
            
            tra_data_list_o = [
                        {
                            "季度": item.get("period", "N/A"),
                            "值": item.get("figure", "N/A"),
                        }
                        for item in tra_result.get("dataSet", [])
                        if (item.get("REGIONDesc", "") == "Total" and re.match(r"^\d{6}$", item.get("period", "")))
                    ]
            tra_df_o = pd.DataFrame(tra_data_list_o)
            tra_df_o['季度'] = tra_df_o['季度'].astype(int)
            tra_df_o = tra_df_o.sort_values(by=['季度'], ascending = True).reset_index(drop=True)  
            
            tra_df = pd.merge(tra_df_c, tra_df_o, on=['季度'], how='outer', suffixes=('_中國', '_總計'))
            tra_df['訪港旅客(不含中國內地)'] = tra_df['值_總計'] - tra_df['值_中國']
            tra_df = tra_df[['季度', '值_中國', '訪港旅客(不含中國內地)', '值_總計']]
            tra_df.columns = ['年月', '訪港旅客(中國內地)', '訪港旅客(不含中國內地)', '訪港旅客(總數)']
            tra_df['年'] = tra_df['年月'] // 100  # 整數除法，提取年份 (202202 // 100 = 2022)
            tra_df['年'] = tra_df['年'].astype(int)
            tra_df['月'] = tra_df['年月'] % 100   # 模運算，提取月份 (202202 % 100 = 02)
            tra_df['季'] = np.round((tra_df['月'] + 1) / 3).astype(int)
            tra_df['年季'] = tra_df['年'].astype(int).astype(str) + 'Q' + tra_df['季'].astype(int).astype(str)
            tra_df = tra_df.groupby(['年', '季', '年季']).agg({
                '訪港旅客(中國內地)':'sum', 
                '訪港旅客(不含中國內地)':'sum', 
                '訪港旅客(總數)': 'sum'
            }).reset_index()
            result_df = tra_df[['年', '季', '年季', '訪港旅客(中國內地)', '訪港旅客(不含中國內地)', '訪港旅客(總數)']]

            

        else:
            print(f"錯誤：{tra_response.status_code} - {tra_response.text}")


        return result_df
    
    def _process_int(self):
        """處理利率資料"""
        result_df = pd.DataFrame()
        
        for _, url in DATA_SOURCES['int'].items():
            df = self._download_excel(url, sheet_name=0, header=14)

            if df is None:
                continue
            

            df = df[['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 4']]
            df.columns = ['年', '月', 'interest_rate']
            df = df.dropna(how='all')
            df['年'] = df['年'].ffill()
            df['月'] = df['月'].str.replace('月', '')
            df['年'] = df['年'].astype(int)
            df['月'] = df['月'].astype(int)
            df = df.reset_index(drop=True)
            df['季'] = ((df['月'] - 1) // 3 + 1).astype(int)
            df = df[['年', '季', '月', 'interest_rate']]

                    # 先依「年」、「季」排序，確保每季的第一個月在最前面
            df_sorted = df.sort_values(['年', '季', '月'])
            
            # 以「年」、「季」分組，取每組的第一筆（即每季的第一個月）
            df_sorted = df_sorted.groupby(['年', '季'], as_index=False).first()
            
            # 只保留需要的欄位
            df_sorted = df_sorted[['年', '季', 'interest_rate']]
            df_sorted['年季'] = df_sorted['年'].astype(int).astype(str) + 'Q' + df_sorted['季'].astype(int).astype(str)
            result_df = df_sorted[['年', '季', '年季', 'interest_rate']]
            result_df.columns = ['年', '季', '年季', '利率']
            result_df['利率'] = result_df['利率']/100
        return result_df









#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################

    def _process_trade_monthly(self):
        """處理月交易量資料"""
        result_df = pd.DataFrame()
        
        for key, url in DATA_SOURCES['trade'].items():
            df = self._download_excel(url, sheet_name=0, header=6)
            if df is None:
                continue
            
            if key == '住宅':
                df = df[['年', 'Unnamed: 5', '數目', '數目.1']]
                df.columns = ['年', '月', '住宅(一手買賣)', '住宅(二手買賣)']
            else:
                df = df[['年', 'Unnamed: 5', '宗數', '宗數.1', '宗數.2']]
                df.columns = ['年', '月', '辦公', '零售', '廠辦']
            
            df_clean = self._clean_dataframe(df)
            if df_clean.empty:
                continue
            
            if result_df.empty:
                result_df = df_clean
            else:
                result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')
        
        if not result_df.empty:
            # 計算住宅總量
            result_df['住宅'] = result_df['住宅(一手買賣)'] + result_df['住宅(二手買賣)']
            result_df['年月'] = (result_df['年'] * 100 + result_df['月']).astype(int)
            
            # 確保數據類型
            numeric_cols = ['住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']
            result_df[numeric_cols] = result_df[numeric_cols].astype(float)
        
        return result_df
    
    def _process_trade_quarterly(self):
        """處理季交易量資料"""
        monthly_data = self._process_trade_monthly()
        if monthly_data.empty:
            return pd.DataFrame()
        
        quarterly_data = monthly_data.groupby(['年', '季']).agg({
            '住宅(一手買賣)':'sum', 
            '住宅(二手買賣)':'sum', 
            '住宅': 'sum',
            '辦公': 'sum',
            '零售': 'sum',
            '廠辦': 'sum'
        }).reset_index()
        
        quarterly_data['年季'] = quarterly_data['年'].astype(int).astype(str) + 'Q' + quarterly_data['季'].astype(int).astype(str)
        return quarterly_data[['年', '季', '年季', '住宅(一手買賣)', '住宅(二手買賣)', '住宅', '辦公', '零售', '廠辦']]
    
    def get_time_options(self, data, period_type):
        """取得時間選項"""
        if period_type == 'monthly':
            if 'trade' in data and not data['trade'].empty:
                all_months = sorted(data['trade']['年月'].dropna().unique())
                return all_months[-14:] if len(all_months) >= 14 else all_months
        else:  # quarterly
            if 'sold' in data and not data['sold'].empty:
                all_quarters = sorted(data['sold']['年季'].dropna().unique())
                return all_quarters[-94:] if len(all_quarters) >= 94 else all_quarters
        
        return []
    


    # 其他資料處理方法...
    def _process_return_monthly(self):
        result_df = pd.DataFrame()
        
        for key, url in DATA_SOURCES['return'].items():
            df = None
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name='Monthly(Domestic) 按月(住宅)',header=5)
                df = df[['年','Unnamed: 5','Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
                df.columns = ['年','月','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']

                
            elif (key =='其他'):
                df = self._download_excel(url,sheet_name='Monthly(Non-domestic) 按月(非住宅)',header=6)
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(乙級)','廠辦','零售']

            if df is not None:
                df_clean = self._clean_dataframe(df)
                if not df_clean.empty:
                    if result_df.empty:
                        result_df = df_clean
                    else:
                        result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')
        result_df.loc[:] = result_df.loc[:].apply(pd.to_numeric, errors='coerce')
        result_df['年月'] = (result_df['年']*100 + result_df['月']).astype(int)
        result_df = result_df[['年', '季', '月', '年月', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
        result_df[['年', '季', '月', '年月']] = result_df[['年', '季', '月', '年月']].astype(int)
        result_df[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']] = result_df[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']].astype(float)
        return result_df
    

    def _process_return_quarterly(self):

        result_df = pd.DataFrame()
        for key, url in DATA_SOURCES['return'].items():
            df = None
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name='Quarterly(Domestic) 按季(住宅)',header=5)
                df = df[['年','月', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
                df.columns = ['年','月','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']
            elif (key =='其他'):
                df = self._download_excel(url,sheet_name='Quarterly(Non-domestic) 按季(非住宅)',header=6)
                df = df[['年','月', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(乙級)','廠辦','零售']


            if df is not None:
                df_clean = self._clean_dataframe(df)
                if not df_clean.empty:
                    if result_df.empty:
                        result_df = df_clean
                    else:
                        result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')
        result_df.loc[:] = result_df.loc[:].apply(pd.to_numeric, errors='coerce')
        result_df['年季'] = result_df['年'].astype(int).astype(str) + 'Q' + result_df['季'].astype(int).astype(str)
        result_df = result_df[['年', '季', '年季', '住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', 
                        '辦公(甲級)','辦公(乙級)', '零售', '廠辦']]
        result_df[['年', '季']] = result_df[['年', '季']].astype(int)
        result_df[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']] = result_df[['住宅(A)', '住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '辦公(甲級)','辦公(乙級)', '零售', '廠辦']].astype(float)
        return result_df

    
    def _process_sold_monthly(self):
        result_df = pd.DataFrame()
        for key, url in DATA_SOURCES['sold'].items():
            df = None
            
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name=0,header=6)
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = self._download_excel(url,sheet_name=0,header=5)
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
                df = self._download_excel(url,sheet_name=0,header=5)
                df = df[['年','Unnamed: 5','Unnamed: 14']]
                df.columns = ['年','月','零售(平均)'] if key =='零售' else ['年','月','廠辦(平均)']

            if df is not None:
                df_clean = self._clean_dataframe(df)
                if not df_clean.empty:
                    if result_df.empty:
                        result_df = df_clean
                    else:
                        result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')

        result_df = result_df.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)                
        result_df.loc[:] = result_df.loc[:].apply(pd.to_numeric, errors='coerce')
        result_df['年月'] = (result_df['年']*100 + result_df['月']).astype(int)
        result_df = result_df[['年', '季','月', '年月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
            '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
            '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
        result_df[['年', '季', '月', '年月']] = result_df[['年', '季', '月', '年月']].astype(int)
        result_df[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
            '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
            '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = result_df[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
            '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
            '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)
        return result_df

    def _process_sold_quarterly(self):
        result_df = pd.DataFrame()
        for key, url in DATA_SOURCES['sold'].items():
            df = None
            
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name=1,header=6)
                df = df[['年', '月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = self._download_excel(url,sheet_name=1,header=5)
                df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
                df = self._download_excel(url,sheet_name=1,header=5)
                df = df[['年','月','Unnamed: 14']]
                df.columns = ['年','月','零售(平均)'] if key =='零售' else ['年','月','廠辦(平均)']

            if df is not None:
                df_clean = self._clean_dataframe(df)
                if not df_clean.empty:
                    if result_df.empty:
                        result_df = df_clean
                    else:
                        result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')

        result_df = result_df.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)     
        result_df.loc[:] = result_df.loc[:].apply(pd.to_numeric, errors='coerce')
        result_df['年季'] = result_df['年'].astype(int).astype(str) + 'Q' + result_df['季'].astype(int).astype(str)
        result_df = result_df[['年', '季', '年季','住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)']]
        result_df[['年', '季']] = result_df[['年', '季']].astype(int)
        result_df[['住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)']] = result_df[['住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)']].astype(float)

        return result_df
    

    def _process_rent_monthly(self):
        result_df = pd.DataFrame()
        for key, url in DATA_SOURCES['rent'].items():
            df = None
            
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name=0,header=6)
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = self._download_excel(url,sheet_name=0,header=5)
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
                df = self._download_excel(url,sheet_name=0,header=5)
                df = df[['年','Unnamed: 5','Unnamed: 9']]
                df.columns = ['年','月','零售(平均)'] if key =='零售' else ['年','月','廠辦(平均)']

            if df is not None:
                df_clean = self._clean_dataframe(df)
                if not df_clean.empty:
                    if result_df.empty:
                        result_df = df_clean
                    else:
                        result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')

        result_df = result_df.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)                
        result_df.loc[:] = result_df.loc[:].apply(pd.to_numeric, errors='coerce')
        result_df['年月'] = (result_df['年']*100 + result_df['月']).astype(int)
        result_df = result_df[['年', '季', '月', '年月', '住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
            '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
                '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']]
        result_df[['年', '季', '月', '年月']] = result_df[['年', '季', '月', '年月']].astype(int)
        result_df[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
            '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
                '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']] = result_df[['住宅(A)', '住宅(A)*', '住宅(B)', '住宅(B)*', '住宅(C)', '住宅(C)*',
            '住宅(D)', '住宅(D)*', '住宅(E)', '住宅(E)*', '住宅(平均)', '辦公(甲級)', '辦公(甲級)*', '辦公(乙級)',
                '辦公(乙級)*', '辦公(丙級)', '辦公(丙級)*', '辦公(平均)', '零售(平均)', '廠辦(平均)']].astype(float)  
        return result_df
    

    def _process_rent_quarterly(self):
        result_df = pd.DataFrame()
        for key, url in DATA_SOURCES['rent'].items():
            df = None
            
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name=1,header=6)
                df = df[['年', '月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = self._download_excel(url,sheet_name=1,header=5)
                df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
                df = self._download_excel(url,sheet_name=1,header=5)
                df = df[['年','月','Unnamed: 9']]
                df.columns = ['年','月','零售(平均)'] if key =='零售' else ['年','月','廠辦(平均)']

            if df is not None:
                df_clean = self._clean_dataframe(df)
                if not df_clean.empty:
                    if result_df.empty:
                        result_df = df_clean
                    else:
                        result_df = pd.merge(result_df, df_clean, on=['年', '季', '月'], how='outer')

        result_df = result_df.sort_values(by=['年','季','月'], ascending=[True,True,True]).reset_index(drop=True)
        result_df.loc[:] = result_df.loc[:].apply(pd.to_numeric, errors='coerce')
        result_df['年季'] = result_df['年'].astype(int).astype(str) + 'Q' + result_df['季'].astype(int).astype(str)
        result_df = result_df[['年', '季', '年季', '住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)']]
        result_df[['年', '季']] = result_df[['年', '季']].astype(int)
        result_df[['住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)']] = result_df[['住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)']].astype(float)
        return result_df
        
    def _process_vac_quarterly(self):
        result_df = pd.DataFrame()
        for key, url in DATA_SOURCES['vac'].items():
            if (key =='住宅') :
                df = self._download_excel(url,sheet_name=r'Vacancy_空置量',header=10)
                df = df[['年\n\nYear', 'Unnamed: 5','Unnamed: 7', 'Unnamed: 9','Unnamed: 11','Unnamed: 13','Unnamed: 15']]
                df.columns = ['年','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)','住宅(總數)']
            
            if (key =='辦公') :
                df = self._download_excel(url,sheet_name= r'Vacancy_空置量', header=7)
                df = df[['年', 'Unnamed: 5','Unnamed: 7', 'Unnamed: 9','Unnamed: 11']]
                df.columns = ['年','辦公(甲級)','辦公(乙級)','辦公(丙級)','辦公(總數)'] 
                
            if (key =='零售') :
                df = self._download_excel(url,sheet_name='Sheet1',header=8)
                df = df[['Year', r'Vacancy as a % of stock']]
                df.columns = ['年','零售(總數)']
                
            if (key =='廠辦'):
                df = self._download_excel(url,sheet_name='Sheet1',header=8)
                df = df[['Year', r'Vacancy as a % of stock']]
                df.columns = ['年','廠辦(總數)']

            df['年'] = pd.to_numeric(df['年'], errors='coerce')
            df_clean = df[(~df['年'].isnull()) & (df['年']!='年') & (df['年']!='Year')].reset_index(drop=True)
    # 清理百分比欄位（除了「年」以外的所有欄位）
            def clean_percentage(text):
                if pd.isna(text):  # 處理空值
                    return np.nan
                text = str(text).strip()  # 轉為字串並移除前後空格
                # 移除 %、逗號和其他非數字字符（保留小數點）
                cleaned_text = re.sub(r'[^\d.]', '', text)
                try:
                    if float(cleaned_text) >= 1:
                        return float(cleaned_text) / 100  # 轉為浮點數並除以 100
                    else:
                        return float(cleaned_text)
                except ValueError:
                    return np.nan  # 若轉換失敗，返回 NaN

            # 對除了「年」以外的欄位應用清理
            for col in df_clean.columns:
                if col != '年':
                    df_clean[col] = df_clean[col].apply(clean_percentage)

            df_clean = df_clean.replace([')', ')@', ')~'], 'Indicates fewer than 20 transactions.')
            df_clean = df_clean.replace('-', np.nan)
            # 顯示數據的前幾行
            if not df_clean.empty:
                if result_df.empty:
                    result_df = df_clean
                else:
                    result_df = pd.merge(result_df, df_clean, on=['年'], how='outer')

        quarters = [1, 2, 3, 4]
        new_rows = []
        # 對每一年複製四次，分別對應四個季度
        for _, row in result_df.iterrows():
            for quarter in quarters:
                new_row = row.copy()
                new_row['季'] = quarter
                new_rows.append(new_row)

        # 轉換為新的資料框
        result_df = pd.DataFrame(new_rows)

        # 調整欄位順序
        result_df = result_df[['年', '季', '住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)','住宅(總數)', '辦公(甲級)','辦公(乙級)','辦公(丙級)','辦公(總數)',
                               '零售(總數)', '廠辦(總數)']]

        # 確保資料型態正確
        result_df['年'] = result_df['年'].astype(int)

        # 按年和季排序（可選）
        result_df = result_df.sort_values(by=['年', '季']).reset_index(drop=True)
        result_df['年季'] = result_df['年'].astype(int).astype(str) + 'Q' + result_df['季'].astype(int).astype(str)

        # 顯示結果
        return result_df