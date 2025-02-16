import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
from io import BytesIO
import base64
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors

# Функция аутентификации
def authenticate(username, password):
    return username == "admin" and password == "admin"

# Функция перевода
def translate(text, language):
    translations = {
        "Russian": {
            "Authorization": "Авторизация",
            "Select Period": "Выбор периода",
            "Select Operator": "Выбор оператора",
            "Evaluate Operator": "Оценка оператора",
            "Evaluate Center": "Оценка центра",
            "Export Report": "Экспорт отчета",
            "Language": "Язык",
            "Start Date": "Начальная дата",
            "End Date": "Конечная дата",
            "Score": "Оценка",
            "Errors": "Ошибки",
            "Recommendations": "Рекомендации",
            "Settings": "Настройки",
            "Generate Report": "Сгенерировать отчет",
            "Report generated as": "Отчет сгенерирован как",
            "Username": "Имя пользователя",
            "Password": "Пароль",
            "Login": "Войти",
            "Invalid username or password": "Неверное имя пользователя или пароль",
            "Logged in successfully!": "Вход выполнен успешно!",
            "Start date cannot be later than end date": "Начальная дата не может быть позже конечной даты",
            "Selected period cannot exceed one year": "Выбранный период не может превышать один год",
            "Data loaded for period": "Данные загружены за период",
            "Evaluation for": "Оценка для",
            "Center Evaluation": "Оценка центра",
            "Generate report for": "Сгенерировать отчет для",
            "Operator": "Оператора",
            "Center": "Центра"
        },
        "English": {
            # English translations are the same as the keys
        },
        "Chinese": {
            "Authorization": "授权",
            "Select Period": "选择时期",
            "Select Operator": "选择操作员",
            "Evaluate Operator": "评估操作员",
            "Evaluate Center": "评估中心",
            "Export Report": "导出报告",
            "Language": "语言",
            "Start Date": "开始日期",
            "End Date": "结束日期",
            "Score": "分数",
            "Errors": "错误",
            "Recommendations": "建议",
            "Settings": "设置",
            "Generate Report": "生成报告",
            "Report generated as": "报告生成为",
            "Username": "用户名",
            "Password": "密码",
            "Login": "登录",
            "Invalid username or password": "用户名或密码无效",
            "Logged in successfully!": "登录成功！",
            "Start date cannot be later than end date": "开始日期不能晚于结束日期",
            "Selected period cannot exceed one year": "所选时期不能超过一年",
            "Data loaded for period": "已加载时期的数据",
            "Evaluation for": "评估",
            "Center Evaluation": "中心评估",
            "Generate report for": "生成报告",
            "Operator": "操作员",
            "Center": "中心"
        }
    }
    return translations.get(language, {}).get(text, text)

def get_data(start_date, end_date):
    # Создаем тестовые данные
    dates = pd.date_range(start=start_date, end=end_date)
    operators = ['Operator 1', 'Operator 2', 'Operator 3']
    data = []
    for date in dates:
        for operator in operators:
            score = np.random.randint(60, 100)
            data.append({'date': date, 'operator': operator, 'score': score})
    return pd.DataFrame(data)

def get_operators(data):
    return data['operator'].unique().tolist()

def evaluate_operator(data, operator):
    operator_data = data[data['operator'] == operator]
    score = operator_data['score'].mean()
    return {
        "score": score,
        "errors": ["Error 1", "Error 2"],
        "recommendations": ["Recommendation 1", "Recommendation 2"]
    }

def evaluate_center(data):
    score = data['score'].mean()
    return {
        "score": score,
        "errors": ["Center Error 1", "Center Error 2"],
        "recommendations": ["Center Recommendation 1", "Center Recommendation 2"]
    }

def generate_report(data, report_type, operator=None):
    if report_type == "Excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Report', index=False)
        output.seek(0)
        return output.getvalue()
    elif report_type == "PDF":
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Заголовок
        title = "Call Center Quality Control Report"
        if operator:
            title += f" for {operator}"
        story.append(Paragraph(title, styles['Title']))
        story.append(Spacer(1, 12))

        # Добавление данных в отчет
        for index, row in data.iterrows():
            story.append(Paragraph(f"Date: {row['date'].strftime('%Y-%m-%d')}", styles['Normal']))
            story.append(Paragraph(f"Operator: {row['operator']}", styles['Normal']))
            story.append(Paragraph(f"Score: {row['score']}", styles['Normal']))
            story.append(Spacer(1, 12))

        # Создание столбчатой диаграммы
        plt.figure(figsize=(6, 4))
        avg_scores = data.groupby('operator')['score'].mean()
        plt.bar(avg_scores.index, avg_scores.values)
        plt.title('Average Operator Scores')
        plt.xlabel('Operator')
        plt.ylabel('Average Score')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Сохранение графика во временный файл
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        # Добавление графика в PDF
        img = Image(img_buffer, width=6*inch, height=4*inch)
        story.append(img)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

# Основное приложение Streamlit
def main():
    st.set_page_config(page_title="Call Center Quality Control", layout="wide")

    # Состояние сессии
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'language' not in st.session_state:
        st.session_state.language = "Russian"

    # Аутентификация
    if not st.session_state.authenticated:
        st.title(translate("Authorization", st.session_state.language))
        username = st.text_input(translate("Username", st.session_state.language))
        password = st.text_input(translate("Password", st.session_state.language), type="password")
        if st.button(translate("Login", st.session_state.language)):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success(translate("Logged in successfully!", st.session_state.language))
                st.experimental_rerun()
            else:
                st.error(translate("Invalid username or password", st.session_state.language))
        return

    # Основное приложение
    st.title("Call Center Quality Control")

    # Выбор языка
    st.sidebar.title(translate("Settings", st.session_state.language))
    languages = ["Russian", "English", "Chinese"]
    selected_language = st.sidebar.selectbox(
        translate("Language", st.session_state.language),
        languages,
        index=languages.index(st.session_state.language)
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.experimental_rerun()

    # Выбор периода
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(translate("Start Date", st.session_state.language))
    with col2:
        end_date = st.date_input(translate("End Date", st.session_state.language))

    if st.button(translate("Select Period", st.session_state.language)):
        if start_date > end_date:
            st.error(translate("Start date cannot be later than end date", st.session_state.language))
            return

        if (end_date - start_date).days > 365:
            st.error(translate("Selected period cannot exceed one year", st.session_state.language))
            return

        data = get_data(start_date, end_date)
        st.session_state.data = data
        st.success(f"{translate('Data loaded for period', st.session_state.language)}: {start_date} to {end_date}")

    # Выбор оператора и оценка
    if 'data' in st.session_state:
        operators = get_operators(st.session_state.data)
        selected_operator = st.selectbox(
            translate("Select Operator", st.session_state.language),
            operators,
            key="operator_selection_for_evaluation"
        )

               # Оценка оператора
        if st.button(translate("Evaluate Operator", st.session_state.language)):
            evaluation = evaluate_operator(st.session_state.data, selected_operator)
            st.subheader(f"{translate('Evaluation for', st.session_state.language)} {selected_operator}")
            st.write(f"{translate('Score', st.session_state.language)}: {evaluation['score']:.2f}/100")
            st.write(f"{translate('Errors', st.session_state.language)}:")
            for error in evaluation['errors']:
                st.write(f"- {error}")
            st.write(f"{translate('Recommendations', st.session_state.language)}:")
            for rec in evaluation['recommendations']:
                st.write(f"- {rec}")

            # Визуализация
            fig, ax = plt.subplots()
            ax.bar([translate('Score', st.session_state.language), translate('Errors', st.session_state.language)], 
                   [evaluation['score'], len(evaluation['errors'])])
            ax.set_ylim(0, 100)
            st.pyplot(fig)

        # Оценка центра
        if st.button(translate("Evaluate Center", st.session_state.language)):
            center_evaluation = evaluate_center(st.session_state.data)
            st.subheader(translate("Center Evaluation", st.session_state.language))
            st.write(f"{translate('Score', st.session_state.language)}: {center_evaluation['score']:.2f}/100")
            st.write(f"{translate('Errors', st.session_state.language)}:")
            for error in center_evaluation['errors']:
                st.write(f"- {error}")
            st.write(f"{translate('Recommendations', st.session_state.language)}:")
            for rec in center_evaluation['recommendations']:
                st.write(f"- {rec}")

            # Визуализация
            fig, ax = plt.subplots()
            ax.bar([translate('Score', st.session_state.language), translate('Errors', st.session_state.language)], 
                   [center_evaluation['score'], len(center_evaluation['errors'])])
            ax.set_ylim(0, 100)
            st.pyplot(fig)

        # Экспорт отчета
        report_type = st.selectbox(translate("Export Report", st.session_state.language), ["Excel", "PDF"])
        
        col1, col2 = st.columns(2)
        with col1:
            report_for = st.radio(translate("Generate report for", st.session_state.language), 
                                  [translate("Operator", st.session_state.language), 
                                   translate("Center", st.session_state.language)])
        with col2:
            if report_for == translate("Operator", st.session_state.language):
                selected_operator_for_report = st.selectbox(
                    translate("Select Operator", st.session_state.language), 
                    get_operators(st.session_state.data),
                    key="operator_selection_for_report"
                )
            else:
                selected_operator_for_report = None

        if st.button(translate("Generate Report", st.session_state.language)):
            if report_for == translate("Operator", st.session_state.language):
                report_data = st.session_state.data[st.session_state.data['operator'] == selected_operator_for_report]
            else:
                report_data = st.session_state.data
            
            report_content = generate_report(report_data, report_type, selected_operator_for_report)
            
            file_extension = "xlsx" if report_type == "Excel" else "pdf"
            file_name = f"{selected_operator_for_report or 'center'}_report.{file_extension}"
            
            st.markdown(get_binary_file_downloader_html(report_content, file_name), unsafe_allow_html=True)
            st.success(f"{translate('Report generated as', st.session_state.language)} {file_name}")

if __name__ == "__main__":
    main()
