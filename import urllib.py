#%%
import requests
import json
import re
import pandas as pd
import numpy as np

#%%
from data_manager import DataManager
#%%統一
url1 = "https://www.censtatd.gov.hk/api/post.php"

# {
#     "header": {
#         "status": {
#             "name": "Fail",
#             "code": 1,
#             "description": "Validation error",
#             "message": [
#                 "Query is not defined"
#             ],
#             "apiHelp": "https://www.censtatd.gov.hk//web_table.html?id=&api_popup=1"
#         },
#         "count": {
#             "noOfRecords": 0,
#             "started": "2025-09-26T01:54:32+00:00",
#             "finished": "2025-09-26T01:54:32+00:00",
#             "durationSeconds": 0.000025
#         }
#     }
# }

url2 = 'https://www.hkma.gov.hk/media/eng/doc/market-data-and-statistics/monthly-statistical-bulletin/T070301.xls'
# %%
#gdp
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
#失業
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
#訪港旅遊
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

#%%
gdp_data = {'query': json.dumps(parameters1)}
gdp_response = requests.post(url1, data=gdp_data, timeout=20)
#%%
une_data = {'query': json.dumps(parameters2)}
une_response = requests.post(url1, data=une_data, timeout=20)
#%%
tra_data = {'query': json.dumps(parameters3)}
tra_response = requests.post(url1, data=tra_data, timeout=20)
# %%
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

else:
    print(f"錯誤：{gdp_response.status_code} - {gdp_response.text}")
    
# %%
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

    

else:
    print(f"錯誤：{une_response.status_code} - {une_response.text}")
    
# %%
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
    tra_df = tra_df[['年', '季', '年季', '訪港旅客(中國內地)', '訪港旅客(不含中國內地)', '訪港旅客(總數)']]

    

else:
    print(f"錯誤：{tra_response.status_code} - {tra_response.text}")
# %%
print(gdp_df)
#%%
print(une_df)
#%%
print(tra_df)
# %%
