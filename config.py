# 資料來源設定
DATA_SOURCES = {
    'trade': {
        '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_16.xls',
        '其他': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_17.xls'
    },
    'return': {
        '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_15.xls',
        '其他': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_15.xls'
    },
    'sold': {
        '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_4.xls',
        '辦公': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_9.xls',
        '零售': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_12.xls',
        '廠辦': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_14.xls'
    },
    'rent': {
        '住宅': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_3.xls',
        '辦公': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_8.xls',
        '零售': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_12.xls',
        '廠辦': r'https://www.rvd.gov.hk/doc/en/statistics/his_data_14.xls'
    }, 
    'vac': {
        '住宅' : r'https://www.rvd.gov.hk/doc/en/statistics/private_domestic.xls', 
        '辦公' : r'https://www.rvd.gov.hk/doc/en/statistics/private_office.xls', 
        '零售' : r'https://www.rvd.gov.hk/doc/en/statistics/private_commercial.xls', 
        '廠辦' : r'https://www.rvd.gov.hk/doc/en/statistics/private_flatted_factories.xls'
    }
}

# 分析選項
ANALYSIS_OPTIONS = ('香港月資料分析', '香港季資料分析', '香港總體經濟指標')

# 預設 session state
DEFAULT_SESSION_STATE = {
    'm_color1': '#5C4141',
    'm_color2': '#1F77B4'
}

PROPERTY_TYPES = ['住宅', '辦公', '零售', '廠辦', '檢視與下載資料表']


# 圖表顏色設定
CHART_COLORS = {
    '住宅': ['red', 'green', 'blue', 'orange', 'purple'],
    '辦公': ['red', 'green'],
    '零售': ['red'],
    '廠辦': ['red']
}