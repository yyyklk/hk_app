import streamlit as st
import re
from openai import OpenAI
from config import DEFAULT_SESSION_STATE, PROPERTY_TYPES, CHART_COLORS
import pandas as pd

class UIComponents:
    def initialize_session_state(self):#
        """初始化 session state"""
        for key, value in DEFAULT_SESSION_STATE.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def create_time_selector(self, options, key_prefix, title):#
        """建立時間選擇器"""
        st.header(title, divider='rainbow')
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("起始時間", divider='rainbow')
            st.selectbox("", options=options, key=f"{key_prefix}_st", index=0)
        
        with col2:
            st.subheader("終止時間", divider='rainbow')
            st.selectbox("", options=options, key=f"{key_prefix}_en", index=len(options)-1)
    


    def create_color_picker(self):#
        """建立顏色選擇器"""
        cola, colb = st.columns(2)
        with cola:
            st.session_state.m_color1 = st.color_picker("選擇長條圖顏色", value=st.session_state.m_color1)
        with colb:
            st.session_state.m_color2 = st.color_picker("選擇折線圖顏色", value=st.session_state.m_color2)
    


    def generate_time_range(self, start, end, period_type):#
        """生成時間範圍"""
        if period_type == 'monthly':
            result = []
            y, m = divmod(start, 100)
            while y * 100 + m <= end:
                result.append(y * 100 + m)
                m += 1
                if m > 12:
                    m = 1
                    y += 1
            return result
        else:  # quarterly
            return self.generate_year_quarter_range(start, end)
    
    def generate_year_quarter_range(self, start, end):#
        """生成年季範圍"""
        start_year, start_q = int(start[:4]), int(start[-1])
        end_year, end_q = int(end[:4]), int(end[-1])
        result = []
        
        while (start_year < end_year) or (start_year == end_year and start_q <= end_q):
            result.append(f"{start_year}Q{start_q}")
            start_q += 1
            if start_q > 4:
                start_q = 1
                start_year += 1
        return result
    
    def create_analysis_tabs(self, data, time_range, chart_utils, period_type):#
        """建立分析標籤頁"""
        tab1, tab2, tab3, tab4, tab5 = st.tabs(PROPERTY_TYPES)
        
        time_col = '年月' if period_type == 'monthly' else '年季'
        
        # 住宅標籤頁
        with tab1:
            self._create_property_analysis(
                data, time_range, chart_utils, '住宅', time_col
            )
        
        with tab2:
            self._create_property_analysis(
                data, time_range, chart_utils, '辦公', time_col
            )
        with tab3:
            self._create_property_analysis(
                data, time_range, chart_utils, '零售', time_col
            )
        with tab4:
            self._create_property_analysis(
                data, time_range, chart_utils, '廠辦', time_col
            )
        with tab5:
            self._create_data_view(data, time_range, time_col)
            


    def _create_data_view(self, data, time_range, time_col):
        """檢視/下載資料表"""
        st.subheader(f"{'月' if time_col=='年月' else '季'}資料表下載", divider='rainbow')
        data_type_names = {
            'trade': '交易量資料表',
            'return': '投報率資料表',
            'sold' : '售價指數資料表',
            'rent' : '租金指數資料表', 
            'vac' : '空置率資料表'
        }
        # 欄位配置
        monthly_cols = {
            'trade': ['年','季','月','年月','住宅(一手買賣)','住宅(二手買賣)','住宅','辦公','零售','廠辦'],
            'return': ['年','季','月','年月','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)','辦公(甲級)','辦公(乙級)','零售','廠辦'],
            'sold': ['年','季','月', '年月','住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)'],
            'rent': ['年','季','月' ,'年月','住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)'],
        }
        quarterly_cols = {
            'trade': ['年','季','年季','住宅(一手買賣)','住宅(二手買賣)','住宅','辦公','零售','廠辦'],
            'return': ['年','季','年季','住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)','辦公(甲級)','辦公(乙級)','零售','廠辦'],
            'sold': ['年','季','年季','住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)'],
            'rent': ['年','季','年季','住宅(A)','住宅(B)', '住宅(C)', '住宅(D)', '住宅(E)', '住宅(平均)','辦公(甲級)', '辦公(乙級)', '辦公(丙級)', '辦公(平均)','零售(平均)','廠辦(平均)'],
            'vac' : ['年', '季','年季', '住宅(A)','住宅(B)','住宅(C)','住宅(D)','住宅(E)','住宅(總數)', '辦公(甲級)','辦公(乙級)','辦公(丙級)','辦公(總數)', '零售(總數)', '廠辦(總數)']
        }

        col_map = monthly_cols if time_col == '年月' else quarterly_cols
        display_types = ['trade', 'return', 'sold', 'rent'] if time_col == '年月' else ['trade', 'return', 'sold', 'rent', 'vac']
        cols = st.columns(4) if time_col == '年月' else st.columns(5)

        for i, dt in enumerate(display_types):
            df = data.get(dt, pd.DataFrame())#取資料
            a = '個月' if time_col == '年月' else '個季'
            if not df.empty and time_col in df.columns:#避免無資料
                rng_df = df[df[time_col].isin(time_range)]
                
                cols[i].metric(data_type_names[dt], f"共{len(rng_df)}{a}")
            else:
                cols[i].metric(data_type_names[dt], f"0{a}")   
        for d_type in display_types:
            df = data.get(d_type, pd.DataFrame())#取資料
            with st.expander(data_type_names[d_type], expanded=False):
                if df.empty or time_col not in df.columns:#避免無資料
                    st.info("無資料")
                    continue
                filt_df = df[df[time_col].isin(time_range)].copy()
                # 動態欄位
                wanted = [c for c in col_map[d_type] if c in filt_df.columns] #取設定好的欄位配置，取有在df裡的欄位
                if wanted:
                    filt_df = filt_df[wanted]
                st.dataframe(filt_df, use_container_width=True)

    
    def _create_property_analysis(self, data, time_range, chart_utils, property_type, time_col):
        """建立單一物業類型分析"""
        # 篩選資料
        filtered_data = self._filter_data_by_time(data, time_range, time_col)
        
        # 交易量圖表
        if property_type in filtered_data['trade'].columns:
            st.subheader(f'{property_type}買賣市場', divider='rainbow')
            chart_utils.create_trade_chart(
                time_range,
                filtered_data['trade'][property_type],
                filtered_data['sold'][f'{property_type}(平均)'],
                st.session_state.m_color1,
                st.session_state.m_color2
            )
        
        # 租金圖表
        if f'{property_type}(平均)' in filtered_data['rent'].columns:
            st.subheader(f'{property_type}租賃市場', divider='rainbow')
            chart_utils.create_rent_chart(
                time_range,
                filtered_data['rent'][f'{property_type}(平均)'],
                st.session_state.m_color2
            )
        
        # 投報率圖表
        return_cols = [col for col in filtered_data['return'].columns if property_type in col]
        if return_cols:
            st.subheader(f'{property_type}投報率', divider='rainbow')
            return_data = [filtered_data['return'][col] for col in return_cols]
            chart_utils.create_return_chart(
                time_range,
                return_data,
                CHART_COLORS.get(property_type, ['red'])
            )
        if time_col == '年季':
            # 空置圖表
            v = ['住宅(總數)', '辦公(總數)', '零售(總數)', '廠辦(總數)']
            vac_cols = [col for col in v if property_type in col]
            if vac_cols:
                st.subheader(f'{property_type}空置率', divider='rainbow')
                vac_data = [filtered_data['vac'][col] for col in vac_cols]
                chart_utils.create_vac_chart(
                    time_range,
                    vac_data,
                    CHART_COLORS.get(property_type, ['red'])
                )

    def _filter_data_by_time(self, data, time_range, time_col):#
        """依時間篩選資料"""
        filtered = {}
        for data_type, df in data.items():
            if not df.empty and time_col in df.columns:
                filtered[data_type] = df.set_index(time_col).reindex(time_range).reset_index()
            else:
                filtered[data_type] = df
        return filtered
    
    def create_ai_analysis_section(self, data, analysis_type):
        """建立 AI 分析區塊"""
        t = '月' if analysis_type == 'monthly' else '季'
        st.header(f"香港{t}資料AI摘要", divider='rainbow')
        
        with st.expander('輸入api金鑰', expanded=False):
            api_key = st.text_input('', max_chars=60)
        
        temperature = st.number_input(
            "修改輸出內容多樣性(數字越小越穩定)", 
            min_value=0.0, max_value=1.0, value=0.5, step=0.1
        )
        
        if st.button("進行分析"):
            if api_key:
                result = self._perform_ai_analysis(data, api_key, temperature)
                self._display_ai_result(result)
            else:
                st.error("請輸入 API 金鑰")
    
    def _perform_ai_analysis(self, data, api_key, temperature):
        """執行 AI 分析"""
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
            # 準備資料
            data_json = {
                'trade': data['trade'].to_json(orient='records', lines=True, force_ascii=False),
                'return': data['return'].to_json(orient='records', lines=True, force_ascii=False),
                'sold': data['sold'].to_json(orient='records', lines=True, force_ascii=False),
                'rent': data['rent'].to_json(orient='records', lines=True, force_ascii=False)
            }
            
            system_prompt = """
            你是一位香港房市分析專家，擅長透過數據分析房市。
            使用提供的交易量、物價指數、租金指數、投報率四個資料表格，進行以下要求：
            1. 用繁體中文及台灣用語回答，禁止其他語言。
            2. 回應精簡，邏輯清晰，避免冗長或籠統陳述。
            3. 必須僅引用提供的數據。
            4. 若有空值，請不要分析該時間點的數據，直接忽略。
            5. 聚焦異常趨勢，如急升/降或相關性。
            """
            
            user_prompt = """
            根據表格回答問題，分五段，各段都需照順序分析交易量、售價指數、租金指數、各級物件投報率四種指標：
            第一段：住宅市場分析
            第二段：辦公市場分析
            第三段：零售市場分析
            第四段：廠辦市場分析
            第五段：總結。
            必須在回答中引述提供的數據。
            """
            
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"生成回應時發生錯誤: {str(e)}"
    
    def _display_ai_result(self, result):
        """顯示 AI 分析結果"""
        result_no_punct = re.sub(r'[^\w\u4e00-\u9fff]', '', result)
        char_count = len(result_no_punct)
        st.write(result)
        st.info(f"AI 分析結果字數（不含標點符號）：{char_count} 字")