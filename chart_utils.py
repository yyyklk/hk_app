import plotly.graph_objects as go
import streamlit as st

class ChartUtils:
    @staticmethod
    def create_trade_chart(x_data, y_trade, y_price, color1, color2):
        x_data = [str(x) for x in x_data]
        """建立交易量圖表"""
        fig = go.Figure()
        
        # 長條圖
        fig.add_trace(go.Bar(
            x=x_data, 
            y=y_trade, 
            name=y_trade.name,
            marker=dict(color=color1, opacity=0.6),
            text=y_trade, 
            textposition='auto',
            texttemplate='%{text:,.0f}',
            textfont=dict(size=12, color='white')
        ))
        
        # 折線圖
        fig.add_trace(go.Scatter(
            x=x_data, 
            y=y_price, 
            name=y_price.name,
            mode='lines+markers+text', 
            marker=dict(size=6),
            yaxis='y2',
            line=dict(color=color2),
            text=y_price, 
            textposition='top center',
            texttemplate='%{text:.2f}',
            textfont=dict(color=color2, size=12)
        ))
        
        fig.update_layout(
            xaxis=dict(
                title=dict(
                    text="時間",
                    font=dict(color='black', size=20)
                ),
                tickangle=45,
                tickfont=dict(color='black', size = 15),
                showgrid=False, ##不開網格 
            
            
            ),
            yaxis=dict(
                title=dict(
                    text=f'{y_trade.name}交易量',
                    font=dict(color = color1, size=20)
                ),
                tickfont=dict(color = color1, size = 15),
                tickformat=',.0f',
                showgrid=True,  # 顯示背景橫線
                gridcolor='#e0e0e0'  # 設定淺灰色橫線
                ,range=[0, y_trade.max() * 1.8]
                ),
            yaxis2=dict(
                title=dict(
                    text=f'{y_price.name}價格指數',
                    font=dict(color = color2, size=20)
                ),
                tickfont=dict(color = color2, size = 15),
                overlaying='y',
                side='right',
                showgrid=True,  # 顯示背景橫線
                gridcolor='#e0e0e0'  # 設定淺灰色橫線
                ,range=[y_price.min() * 0.7, y_price.max() * 1.2]
            ),
            template="plotly_white",
            hovermode='x unified',  # 統一懸停提示框，提升互動性
            autosize=True,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_rent_chart(x_data, y_data, color):
        x_data = [str(x) for x in x_data]
        """建立租金圖表"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_data, 
            y=y_data, 
            name=y_data.name,
            mode='lines+markers+text',
            marker=dict(size=6),
            line=dict(color=color),
            text=y_data, 
            textposition='top center',
            texttemplate='%{text:.2f}',
            textfont=dict(color=color, size=12)
        ))
        
        fig.update_layout(
            xaxis=dict(
                title=dict(
                    text="時間",
                    font=dict(color='black', size=20)
                ),
                tickangle=45,
                tickfont=dict(color='black', size = 15),
                showgrid=False, ##不開網格 
            
            
            ),

            yaxis=dict(
                title=dict(
                    text=f'{y_data.name}租金指數',
                    font=dict(color = color, size=20)
                ),
                tickfont=dict(color = color, size = 15),
                tickformat='.0f',
                showgrid=True,  # 顯示背景橫線
                gridcolor='#e0e0e0'  # 設定淺灰色橫線
                ,range=[0, y_data.max() * 1.8]
                ),
            template="plotly_white",
            hovermode='x unified',  # 統一懸停提示框，提升互動性
            autosize=True,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'

        )
        
        st.plotly_chart(fig, use_container_width=True)
    

    @staticmethod
    def create_return_chart(x_data, y_data_list, colors):
        x_data = [str(x) for x in x_data]
        """建立投報率圖表"""
        fig = go.Figure()
        
        for y_data, color in zip(y_data_list, colors):
            fig.add_trace(go.Scatter(
                x=x_data, 
                y=y_data, 
                name=y_data.name,
                mode='lines+markers+text',
                marker=dict(size=6, color = color),
                line=dict(color=color),
                text=y_data, 
                textposition='top center',
                texttemplate='%{text:.2f}',
                textfont=dict(color=color, size=12)
            ))
        
        fig.update_layout(
            xaxis=dict(
                title=dict(
                    text="時間",
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
                ,range=[0, y_data_list[0].max() * 1.8]
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
        
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def create_vac_chart(x_data, y_data_list, colors):
        x_data = [str(x) for x in x_data]
        """建立投報率圖表"""
        fig = go.Figure()
        
        for y_data, color in zip(y_data_list, colors):
            fig.add_trace(go.Scatter(
                x=x_data, 
                y=y_data, 
                name=y_data.name,
                mode='lines+markers+text',
                marker=dict(size=6, color = color),
                line=dict(color=color),
                text=y_data, 
                textposition='top center',
                texttemplate='%{text:.2f}',
                textfont=dict(color=color, size=12)
            ))
        
        fig.update_layout(
            xaxis=dict(
                title=dict(
                    text="時間",
                    font=dict(color='black', size=20)
                ),
                tickangle=45,
                tickfont=dict(color='black', size = 15),
                showgrid=False, ##不開網格 
            
            
            ),

            yaxis=dict(
                title=dict(
                    text=f'空置率',
                    font=dict(color = 'black', size=20)
                ),
                tickfont=dict(color = 'black', size = 15),
                tickformat='.2f',
                showgrid=True,  # 顯示背景橫線
                gridcolor='#e0e0e0'  # 設定淺灰色橫線
                ,range=[0, y_data_list[0].max() * 1.8]
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
        
        st.plotly_chart(fig, use_container_width=True)