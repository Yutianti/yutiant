import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba# 用于中文分词
from collections import Counter# 用于计数
import matplotlib.pyplot as plt# 用于绘图
from pyecharts.charts import Bar, Pie, Line,Scatter,Radar# 用于绘制各类图表
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts import options as opts# 用于设置图表属性
def main():
    st.title('Welcome to streamlit!')
    url = st.text_input('Enter url：')
    st.sidebar.title("请选择图表类型")
    selected_option =  st.sidebar.radio('请选择一种图表类型：', ('饼状图', '条形图', '折线图', '柱状图','词云','散点图','雷达图','面积图'))
    if  url:
        res = requests.get(url)
        encoding = res.encoding if 'charset' in res.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding=encoding)
        text = soup.text#获取网页内容
        words = [word for word in jieba.cut(text) if len(word) >= 2 and '\u4e00' <= word <= '\u9fff']#中文分词
        word_counts = Counter(words)#计算每个词语出现次数
        #根据用户选择呈现不同的图表
        if selected_option== '饼状图':
            c = (
                Pie()
                .add("", word_counts.most_common(20))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))# 设置标签格式
                .render("pie_chart.html")#渲染为Html文件
               )
        #在页面上显示html文件
            st.components.v1.html(open('pie_chart.html', 'r', encoding='utf-8').read(), height=800)
        elif selected_option == '条形图':
            c = (
                Bar()
                .add_xaxis([x[0] for x in word_counts.most_common(20)])
                .add_yaxis("词频", [x[1] for x in word_counts.most_common(20)], category_gap="50%")  # 设置间距为50%
                .reversal_axis()  # 将 x 轴和 y 轴交换位置
                .set_global_opts(title_opts=opts.TitleOpts(title="条形图"))
                .render("bar_chart.html")
               )
            st.components.v1.html(open('bar_chart.html', 'r', encoding='utf-8').read(),width=1000, height=800)
        elif selected_option == '折线图':
        # 获取词频排名前20的词作为雷达图的指标项
            x_axis = [x[0] for x in word_counts.most_common(20)]
        # 获取词频排名前20的词的频数作为雷达图的数据
            y_axis = [x[1] for x in word_counts.most_common(20)]
            c = (
                Line()
                .add_xaxis(x_axis)#添加x轴数据
                .add_yaxis("", y_axis, is_smooth=True)# 添加 y 轴数据，并将线条进行平滑处理
                .set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
                .render("line_chart.html")
                 )
            st.components.v1.html(open('line_chart.html', 'r', encoding='utf-8').read(),width=2000, height=800)
        elif selected_option == '柱状图':
            x_axis = [x[0] for x in word_counts.most_common(20)]
            y_axis = [x[1] for x in word_counts.most_common(20)]
            c = (
                Bar()
                .add_xaxis(x_axis)#添加x轴坐标
                .add_yaxis("", y_axis)#添加y轴坐标
                .set_global_opts(title_opts=opts.TitleOpts(title="柱状图"))
                 )
            c.render("bar_chart.html")
            st.components.v1.html(open('bar_chart.html', 'r', encoding='utf-8').read(),width=2000,height=800)
        elif selected_option=="词云":
            wordcloud = WordCloud()
            wordcloud.add("", word_counts.most_common(20), word_size_range=[20, 100])
            wordcloud.render("wordcloud.html")
            st.components.v1.html(open('wordcloud.html', 'r', encoding='utf-8').read(), height=800)
        elif selected_option == '散点图':
            x_axis = [x[0] for x in word_counts.most_common(20)]
            y_axis = [x[1] for x in word_counts.most_common(20)]
            c = (
                Scatter()
                .add_xaxis(x_axis)
                .add_yaxis("", y_axis)
                .set_series_opts(label_opts=opts.LabelOpts(""))
                .render("scatter_chart.html")
                 )
            st.components.v1.html(open('scatter_chart.html', 'r', encoding='utf-8').read(), height=800)
        elif selected_option == '雷达图':
            x_axis = [x[0] for x in word_counts.most_common(20)]
            y_axis = [x[1] for x in word_counts.most_common(20)]
            radar = (
                Radar()
                .add_schema(
                    schema=[
             # 设置雷达图的指标项，这里假设最大值为30
                    opts.RadarIndicatorItem(name=x, max_=30) for x in x_axis
                    ]

                )
                .add(series_name="", data=[y_axis])
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .render("radar_chart.html")
            )
            # 显示图表
            st.components.v1.html(open('radar_chart.html', 'r', encoding='utf-8').read(), height=800)
        elif selected_option == '面积图':
            x_axis = [x[0] for x in word_counts.most_common(20)]
            y_axis = [x[1] for x in word_counts.most_common(20)]
            # 绘制面积图
            line_chart = (
                Line()
                .add_xaxis(x_axis)
                .add_yaxis("", y_axis, areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            )

            # 渲染面积图并保存为 HTML 文件
            line_chart.render("area_chart.html")

            # 在 Streamlit 中展示面积图
            st.components.v1.html(open('area_chart.html', 'r', encoding='utf-8').read(), height=800)
if __name__ == '__main__':
     main()



 

