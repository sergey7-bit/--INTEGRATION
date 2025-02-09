import streamlit as st
import os
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Функция-заглушка для транскрипции и анализа
def transcription_analysis(file_path):
    time.sleep(3)  # Имитация работы
    return "Анализ завершен"

# Функция для загрузки данных оператора
def load_operator_data(operator, start_date, end_date):
    return pd.DataFrame({
        'Метрика': ['Чек-лист', 'Стандарт', 'Запретные фразы'],
        'Значение': [85, 90, 80]
    })

# Функция для загрузки данных центра
def load_center_data(start_date, end_date):
    return pd.DataFrame({
        'Оператор': ['Оператор 1', 'Оператор 2', 'Оператор 3'],
        'Производительность': [85, 90, 80]
    })

def main():
    # Словарь для мультиязычности
    translations = {
        "Русский": {
            "title": "Система анализа работы колл-центра",
            "select_record": "Выбор записи",
            "start_analysis": "Запуск анализа",
            "select_operator": "Выбор оператора",
            "evaluate_operator": "Оценка оператора",
            "evaluate_center": "Оценка центра",
            "export_report": "Экспорт отчета",
            "language": "Язык",
            "select_date_range": "Выберите период",
            "start_date": "Начальная дата",
            "end_date": "Конечная дата",
            "operator_summary": "Краткая сводка о работе оператора",
            "final_score": "Итоговая оценка",
            "recommendations": "Рекомендации",
            "center_statistics": "Статистика работы всех операторов",
            "export_format": "Выберите формат экспорта",
            "download_excel": "Скачать отчет Excel",
            "pdf_not_implemented": "Экспорт в PDF пока не реализован"
        },
        "English": {
            "title": "Call Center Analysis System",
            "select_record": "Select Record",
            "start_analysis": "Start Analysis",
            "select_operator": "Select Operator",
            "evaluate_operator": "Evaluate Operator",
            "evaluate_center": "Evaluate Center",
            "export_report": "Export Report",
            "language": "Language",
            "select_date_range": "Select Date Range",
            "start_date": "Start Date",
            "end_date": "End Date",
            "operator_summary": "Operator Performance Summary",
            "final_score": "Final Score",
            "recommendations": "Recommendations",
            "center_statistics": "All Operators Statistics",
            "export_format": "Select Export Format",
            "download_excel": "Download Excel Report",
            "pdf_not_implemented": "PDF export is not implemented yet"
        },
        "中文": {
            "title": "呼叫中心分析系统",
            "select_record": "选择记录",
            "start_analysis": "开始分析",
            "select_operator": "选择操作员",
            "evaluate_operator": "评估操作员",
            "evaluate_center": "评估中心",
            "export_report": "导出报告",
            "language": "语言",
            "select_date_range": "选择日期范围",
            "start_date": "开始日期",
            "end_date": "结束日期",
            "operator_summary": "操作员表现摘要",
            "final_score": "最终得分",
            "recommendations": "建议",
            "center_statistics": "所有操作员统计",
            "export_format": "选择导出格式",
            "download_excel": "下载Excel报告",
            "pdf_not_implemented": "PDF导出尚未实现"
        }
    }

    # Выбор языка
    lang = st.sidebar.selectbox(
        "Язык / Language / 语言",
        ["Русский", "English", "中文"]
    )
    t = translations[lang]

    st.title(t["title"])

    # Кнопка выбора записи
    st.header(t["select_record"])
    audio_dir = "https://drive.google.com/drive/folders/1XGWXwb0PegaL8frvQE592Ji1YYVuDR0w?usp=sharing"
    st.write(f"Директория аудиофайлов: {audio_dir}")

    # Кнопка запуска анализа
    if st.button(t["start_analysis"]):
        with st.spinner('Выполняется анализ...'):
            result = transcription_analysis("dummy_path")
        st.success(result)

    # Кнопка выбора оператора
    st.header(t["select_operator"])
    operator_dir = "https://drive.google.com/drive/folders/11tY7hlni_THw1-m4zeGTvQOHpy4IOQrq"
    st.write(f"Директория результатов анализа: {operator_dir}")
    
    operator = st.selectbox(t["select_operator"], ["Оператор 1", "Оператор 2", "Оператор 3"])

       # Выбор периода
    st.header(t["select_date_range"])
    start_date = st.date_input(t["start_date"])
    end_date = st.date_input(t["end_date"])

    # Кнопка оценки оператора
    if st.button(t["evaluate_operator"]):
        data = load_operator_data(operator, start_date, end_date)
        
        st.write(t["operator_summary"])
        st.dataframe(data)

        fig, ax = plt.subplots()
        ax.bar(data['Метрика'], data['Значение'])
        ax.set_ylim(0, 100)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.write(f"{t['final_score']}: 85/100")
        st.write(f"{t['recommendations']}: Улучшить работу с запретными фразами")

    # Кнопка оценки центра
    if st.button(t["evaluate_center"]):
        data = load_center_data(start_date, end_date)
        
        st.write(t["center_statistics"])
        st.dataframe(data)

        fig, ax = plt.subplots()
        ax.bar(data['Оператор'], data['Производительность'])
        ax.set_ylim(0, 100)
        st.pyplot(fig)

        st.write(f"{t['recommendations']}: Провести дополнительное обучение для Оператора 3")

    # Кнопка экспорта отчетов
    export_format = st.selectbox(t["export_format"], ["Excel", "PDF"])
    if st.button(t["export_report"]):
        if export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                load_operator_data(operator, start_date, end_date).to_excel(writer, sheet_name='Оператор', index=False)
                load_center_data(start_date, end_date).to_excel(writer, sheet_name='Центр', index=False)
            st.download_button(
                label=t["download_excel"],
                data=output.getvalue(),
                file_name="report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.write(t["pdf_not_implemented"])

if __name__ == "__main__":
    main()

