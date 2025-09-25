import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from config import DATA_SOURCES
import re

class DataManager:
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
                df = self._download_excel(url,sheet_name='Monthly(Domestic) 按月(住宅)',header=6)
                df = df[['年','Unnamed: 5','Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
                df.columns = ['年','月','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']

                
            elif (key =='其他'):
                df = self._download_excel(url,sheet_name='Monthly(Non-domestic) 按月(非住宅)',header=8)
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
                df = self._download_excel(url,sheet_name='Quarterly(Domestic) 按季(住宅)',header=6)
                df = df[['年','月', 'Unnamed: 8','Unnamed: 11', 'Unnamed: 14','Unnamed: 17','Unnamed: 20']]
                df.columns = ['年','月','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)']
            elif (key =='其他'):
                df = self._download_excel(url,sheet_name='Quarterly(Non-domestic) 按季(非住宅)',header=8)
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
            df = self._download_excel(url,sheet_name=0,header=5)
            if (key =='住宅') :
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
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
            df = self._download_excel(url,sheet_name=1,header=5)
            if (key =='住宅') :
                df = df[['年', '月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
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
            df = self._download_excel(url,sheet_name=0,header=5)
            if (key =='住宅') :
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = df[['年','Unnamed: 5', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
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
            df = self._download_excel(url,sheet_name=1,header=5)
            if (key =='住宅') :
                df = df[['年', '月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17','Unnamed: 18', 'Unnamed: 20','Unnamed: 21',
                            'Unnamed: 29']]
                df.columns = ['年','月','住宅(A)','住宅(A)*','住宅(B)','住宅(B)*','住宅(C)','住宅(C)*','住宅(D)','住宅(D)*','住宅(E)','住宅(E)*','住宅(平均)']
                
            if (key =='辦公'):
                df = df[['年','月', 'Unnamed: 8','Unnamed: 9', 'Unnamed: 11','Unnamed: 12',
                            'Unnamed: 14','Unnamed: 15', 'Unnamed: 17']]
                df.columns = ['年','月','辦公(甲級)','辦公(甲級)*','辦公(乙級)','辦公(乙級)*','辦公(丙級)','辦公(丙級)*','辦公(平均)']
                
            if (key == '零售') | (key == '廠辦'):
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