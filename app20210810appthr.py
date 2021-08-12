import streamlit as st
import pandas as pd
from bokeh.models import DataTable, TableColumn, NumberFormatter, DateFormatter
from bokeh.models import ColumnDataSource
from PIL import Image
from bokeh.models import HoverTool
from bokeh.plotting import figure
import warnings
warnings.filterwarnings('ignore')
import datetime


@st.cache
def loadDf_sweet_potato():
    data = pd.read_csv('1.sweet_poratoes.csv', parse_dates=["DATE"], index_col="DATE")
    return data

@st.cache
def load_Bokeh_sweet_potato():
    data = pd.read_csv('보케_고구마.csv', encoding='utf-8')
    return data

@st.cache
def loadDf_apple():
    data = pd.read_csv('2.apple.csv', parse_dates=["DATE"], index_col="DATE")
    return data

@st.cache(allow_output_mutation=True)
def load_Bokeh_apple():
    data = pd.read_csv('보케_사과.csv', encoding='utf-8')
    return data

def accept_user_data():
    user_input=st.text_input('날짜를 입력하세요. (입력형태: YYYY-MM-DD, 기간: ~2021-06-29)')
    return user_input

def main():
    # 인트로
    st.title("**[당근막켓] 농산물 가격 예측 서비스**")
    st.subheader(
        """
        전국 도매시장 거래가격을 예측 & 비교 합니다. (1KG 당 가격)
        """
    )
    st.markdown(
        """
            - 🗂️ 농산물 품목 선택 후, 가격 데이터를 확인합니다.
            - ⚙️ 딥러닝을 이용한 예측모델의 정확도를 측정합니다.
            - 📉 가격 예측 그래프로 실제가격과 예측가격을 비교합니다.
            - 🩺 딥러닝을 기반으로 내일의 농산물 가격을 예측합니다.
            - 🔎 전국 7개 도매시장의 농산물 거래가격 차이를 비교합니다.
            -----
            """
    )


    # 데이터 & 서비스 선택
    choose_data = st.sidebar.selectbox('농산품 선택', ['고구마', '사과', '감자', '당근', '배', '상추', '호박'])
#    choose_service = st.sidebar.selectbox('서비스 선택', ['가격 예측', '가격 비교'])

    # 고구마
    if(choose_data=='고구마'):
        product_nm='고구마'
        data=loadDf_sweet_potato()
        data_bokeh = load_Bokeh_sweet_potato()

    elif(choose_data=='사과'):
        product_nm= '사과'
        data=loadDf_apple()
        data_bokeh = load_Bokeh_apple()

    if (choose_data!='사과') and (choose_data!='고구마'):
        st.subheader('서비스를 준비 중 입니다.')

    else:
        # 가격정보 데이터
        #    st.info('1. %s 가격 정보'%product_nm)
        st.subheader('1. %s 가격 정보' % product_nm)
        data2 = data.loc['2021-06-07':'2021-06-11']
        data2 = data2.astype(int)
        data2['날짜'] = data2.index
        data2['날짜'] = data2['날짜'].astype(str).str.slice(start=0, stop=10)
        data2 = data2.sort_values(by=['날짜'], axis=0)
        data2.reset_index(drop=True, inplace=True)
        data2.columns = ['가락도매', '평균가', '최저가', '최고가', '표준편차', '국제유가', '물가지수', '날짜']
        data2 = data2[['날짜', '가락도매', '평균가', '최저가', '최고가', '표준편차', '국제유가', '물가지수']]
        st.write(data2)

        # lstm 분석 결과
        #    st.info('2. 딥러닝 예측모델 정확도')
        st.subheader('2. 예측모델의 정확도')
        st.write('▶ 본 예측모델은 지난 20년 동안의 %s 가격에 대해 86.27%% 의 설명력을 가집니다.' % product_nm)

        # 예측시각화
        if (choose_data == '고구마'):
            df_temp = pd.read_csv('고구마_예측가격플롯.csv', encoding='utf-8')
            df_temp['DATE'] = pd.to_datetime(df_temp['DATE'])
            df_temp = df_temp.sort_values(by=['DATE'], axis=0)
            #    st.info('3. %s 가격 예측 그래프' % product_nm)
            st.subheader('3. %s 가격 예측 그래프' % product_nm)

            p = figure(height=300, x_axis_type='datetime')
            p.line(df_temp['DATE'], df_temp['Gyunglak_PRCE'], legend_label='실제가격', color='#99d594')
            p.line(df_temp['DATE'], df_temp['예측가격'], legend_label='예측가격', line_width=3, color='#3288bd')
            p.legend.location = 'top_left'
            p.legend.click_policy = 'hide'

            p.add_tools(HoverTool(
                tooltips=[('가격', '@y{0,0}' + '원'), ],
                formatters={'x': 'datetime', }
            ))

        if (choose_data == '사과'):
            df_temp = pd.read_csv('사과_예측가격플롯.csv', encoding='utf-8')
            df_temp['DATE'] = pd.to_datetime(df_temp['DATE'])
            df_temp = df_temp.sort_values(by=['DATE'], axis=0)
            #    st.info('3. %s 가격 예측 그래프' % product_nm)
            st.subheader('3. %s 가격 예측 그래프' % product_nm)

            p = figure(height=300, x_axis_type='datetime')
            p.line(df_temp['DATE'], df_temp['Gyunglak_PRCE'], legend_label='실제가격', color='#99d594')
            p.line(df_temp['DATE'], df_temp['예측가격'], legend_label='예측가격', line_width=2, color='#3288bd')
            p.legend.location = 'top_left'
            p.legend.click_policy = 'hide'

            p.add_tools(HoverTool(
                tooltips=[('가격', '@y{0,0}' + '원'), ],
                formatters={'x': 'datetime', }
            ))

        st.bokeh_chart(p, use_container_width=True)

        # 가격예측
        #    st.info('4. %s의 가격 예측'%product_nm)
        st.subheader('4. %s의 가격 예측' % product_nm)
        try:
            if (st.checkbox("실제가격과 예측가격을 비교할 날짜 선택")):
                user_input = accept_user_data()
                if (choose_data == '고구마'):
                    if len(user_input) == 10:
                        st.text("※ 현재 서비스는, 입력날짜와 관계없이 동일한 예측결과를 보여드리는 점 양해부탁드립니다.")
                        st.text("%s일 %s 실제가격: 4,284 원" % (user_input, product_nm))
                        st.text("%s일 %s 예측가격: 4,633.123 원" % (user_input, product_nm))
                        st.text("*정확도: 91.850%")

                    elif len(user_input) == 0:
                        st.text("")
                    else:
                        st.text("입력형태를 확인해주세요")

                if (choose_data=='사과'):
                    if len(user_input) == 10:
                        st.text("※ 현재 서비스는, 입력날짜와 관계없이 동일한 예측결과를 보여드리는 점 양해부탁드립니다.")
                        st.text("%s일 %s 실제가격: 3,512.38 원" % (user_input, product_nm))
                        st.text("%s일 %s 예측가격: 3,616.75 원" % (user_input, product_nm))
                        st.text("*정확도: 97.028%")


                    elif len(user_input) == 0:
                        st.text("")
                    else:
                        st.text("입력형태를 확인해주세요")

            if (st.checkbox("내일 (2021-06-30) 가격 예측하기")):
                if (choose_data == '고구마'):
                    st.text('내일 %s의 가격은 "3,965.88 원"으로 예상됩니다.' % (product_nm))
                if (choose_data=='사과'):
                    st.text('내일 %s의 가격은 "4,060.93 원"으로 예상됩니다.' % (product_nm))
        except:
            pass


        #도매시장별 가격비교 Bokeh 시각화
        st.subheader('5. 2021년 상반기 도매시장 가격변화(원/1KG)')
        cols = ['서울가락도매', '서울강서도매', '부산엄궁도매', '대구북부도매', '인천구월도매', '광주각화도매', '대전오정도매']
        colors = ['#3288bd', '#99d594', '#e6f598', '#fee08b', '#fc8d59', '#d53e4f', '#808080']
        if product_nm=='고구마':
            data_bokeh=data_bokeh.loc[:150]
        if product_nm=='사과': data_bokeh=data_bokeh.loc[:152]
        data_bokeh['AUC_YMD'] = pd.to_datetime(data_bokeh['AUC_YMD'])
        data_bokeh = data_bokeh[['AUC_YMD', '서울가락도매', '서울강서도매', '부산엄궁도매', '대구북부도매',
                     '인천구월도매', '광주각화도매', '대전오정도매']]
        data_bokeh2 = data_bokeh.copy()
        data_bokeh['Std'] = data_bokeh2.std(axis=1)
        data_bokeh['Std'] = round(data_bokeh['Std'], 0)
        data_bokeh['Max'] = data_bokeh2.max(axis=1)
        data_bokeh['Min'] = data_bokeh2.min(axis=1)
        data_bokeh['diff'] = data_bokeh['Max'] - data_bokeh['Min']

        #### (1) 플롯
        p2 = figure(title='%s'%product_nm,plot_width=1000, plot_height=350, x_axis_type="datetime")
        for col, color in zip(cols, colors):
            p2.line(data_bokeh['AUC_YMD'], data_bokeh[col], line_width=2, alpha=0.8, legend_label=col, color=color)
            p2.square(data_bokeh['AUC_YMD'], data_bokeh[col], line_width=2, alpha=0.8, size=3, legend_label=col, color=color)

        p2.legend.location = "top_left"
        p2.legend.click_policy = 'hide'
        # p2.legend.title = '지역'

        p2.add_tools(HoverTool(
            tooltips=[('가격', '@y{0,0}' + '원'), ],
            formatters={'x': 'datetime', }
        ))
        st.bokeh_chart(p2, use_container_width=True)

        #### (2) 가격표준편차
        st.subheader('6. 도매시장 일일 가격 표준편차')
        st.write('▶ 전국 7개 도매시장별 일일 가격 표준편차')
        data_bokeh['left'] = data_bokeh.AUC_YMD - datetime.timedelta(days=0.5)
        data_bokeh['right'] = data_bokeh.AUC_YMD + datetime.timedelta(days=0.5)

        plot = figure(title='%s'%product_nm,x_axis_type="datetime", height=200, width=1000)
        # plot.quad(top=data['Max'], bottom=data['Min'], left=data['left'], right=data['right'], color=Blues4[2],legend_label="차이")
        # plot.vbar(x=data['AUC_YMD'], top=data['diff'], width=10)
        plot.line(data_bokeh['AUC_YMD'], data_bokeh['Std'], line_width=2, alpha=0.8)  # legend_label='일일 표준편차'

        plot.add_tools(HoverTool(
            tooltips=[('일일표준편차', '@y{0}'), ],
            formatters={'x': 'datetime', }
        ))
        st.bokeh_chart(plot, use_container_width=True)



        #### (3) 데이터테이블
#       st.subheader('7. %s의 일일표준편차' % product_nm)
        st.write('▶ 2021-06-29 일 %s 가격정보'%product_nm)
        if (product_nm=='고구마'):
            st.text("  - 가격 일일표준편차: 723")
            st.text("  - 최대가격차이: 약 1,953 원")
            st.text("  - 최저가: 3,319 원")
            st.text("  - 최고가: 5,250 원")

        if (product_nm=='사과'):
            st.text("  - 가격 일일표준편차: 1095")
            st.text("  - 최대가격차이: 약 3,008 원")
            st.text("  - 최저가: 2,749 원")
            st.text("  - 최고가: 5,757 원")


        data_rev = data_bokeh[::-1]
        source = ColumnDataSource(data_rev)

        columns = [
            TableColumn(field="AUC_YMD", title="날짜", formatter=DateFormatter(format='%Y-%m-%d')),
            TableColumn(field='Std', title='가격 일일표준편차'),
            TableColumn(field='diff', title='시장별 최대 가격차이', formatter=NumberFormatter(format='\0,0')),
            TableColumn(field='Min', title='최저가 (원)', formatter=NumberFormatter(format='\0,0')),
            TableColumn(field='Max', title='최고가 (원)', formatter=NumberFormatter(format='\0,0')),
        ]

        data_table = DataTable(source=source, columns=columns, height=200, width=700)
        st.bokeh_chart(data_table, use_container_width=True)

        if product_nm=='고구마':
            try:
                if (st.checkbox("서울가락도매시장 일일 가격차이 확인하기")):
                    image = Image.open('가락시장-법인별-가격비교-고구마.png')
                    st.image(image, caption='같은 도매시장에서 거래되는 상품이라도 법인에 따라 가격차이를 보입니다.')
            except:
                pass


        if product_nm=='사과':
            try:
                if (st.checkbox("서울가락도매시장 일일 가격차이 확인하기")):
                    image = Image.open('가락시장-법인별-가격비교-사과.png')
                    st.image(image, caption='같은 도매시장에서 거래되는 상품이라도 법인에 따라 가격차이를 보입니다.')
            except:
                pass


if __name__ == "__main__":
    main()
