import numpy as np
import plotly.graph_objs as go
import plotly.offline as opy
import plotly.express as px
import pandas as pd


def plot_feedback_distribution(dataframe, type_plot='pie'):
    fig = None
    
    values = dataframe['question_1'].value_counts().values
    names = dataframe['question_1'].value_counts().index.tolist()
    title ='Распределение отзывов по курсам'
    
    if type_plot == 'pie':
        fig = px.pie(values=values, names=names, title=title, labels={'values': 'Количество отзывов', 'names': 'Курс'})
    elif type_plot == 'bar':
        fig = px.bar(x=values, y=names, title=title, labels={'x': 'Количество отзывов', 'y': 'Курс'})
    
    return fig

def distribution_relevant_reviews(dataframe, type_plot='pie'):
    type_relevant_reviews = {0: 'Неинформативные', 1: 'Информативные'}
    
    values = dataframe['is_relevant'].value_counts().values
    names = [type_relevant_reviews[item] for item in dataframe['is_relevant'].value_counts().index.tolist()]
    
    title ='Распределение релевантных и нерелевантных отзывов'
    
    if type_plot == 'pie':
        fig = px.pie(values=values, names=names, title=title, labels={'names': 'Релевантность отзывов', 'values': 'Количество отзывов'})
    elif type_plot == 'bar':
        fig = px.bar(x=names, y=values, title=title, labels={'x': 'Релевантность отзывов', 'y': 'Количество отзывов'})
    
    return fig

def plot_relevant_reviews(dataframe, courses_to_plot=None):
    data = dataframe.copy(deep=True)
    data['is_relevant'] = data['is_relevant'].map({0: 'Неинформативные', 1: 'Информативные'})
    
    if courses_to_plot is not None:
        filtered_data = data[data['question_1'].isin(courses_to_plot)]
    else:
        filtered_data = data
    
    data_plotly = filtered_data.groupby(['question_1', 'is_relevant']).size().reset_index(name='count')
    fig = px.bar(data_plotly, x='question_1', y='count', color='is_relevant', barmode='group',
                 labels={'count':'Количество отзывов', 'question_1':'Курс', 'is_relevant':'Релевантность'},
                 title='Количество отзывов по релевантности для каждого курса')

    fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
    fig.update_layout(xaxis_title='Курс', yaxis_title='Количество отзывов',
                      legend_title='Релевантность', legend=dict(x=1, y=1, bgcolor='rgba(255, 255, 255, 0.5)'),
                      xaxis={'categoryorder':'total descending'})
    
    return fig

def distribution_positivity_feedback(dataframe, type_plot='pie'):
    type_positivity_reviews = {0: 'Негативные', 1: 'Позитивные'}
    
    values = dataframe['is_positive'].value_counts().values
    names = [type_positivity_reviews[item] for item in dataframe['is_positive'].value_counts().index.tolist()]
    
    title ='Распределение по позитивности отзывов'
    
    if type_plot == 'pie':
        fig = px.pie(values=values, names=names, title=title, labels={'names': 'Позитивность отзывов', 'values': 'Количество отзывов'})
    elif type_plot == 'bar':
        fig = px.bar(x=names, y=values, title=title, labels={'x': 'Позитивность отзывов', 'y': 'Количество отзывов'})
    
    return fig

def plot_positivity_feedback(dataframe, courses_to_plot=None):
    data = dataframe.copy(deep=True)
    data['is_positive'] = data['is_positive'].map({0: 'Отрицательные', 1: 'Положительные'})
    
    if courses_to_plot is not None:
        filtered_data = data[data['question_1'].isin(courses_to_plot)]
    else:
        filtered_data = data
    
    data_plotly = filtered_data.groupby(['question_1', 'is_positive']).size().reset_index(name='count')
    fig = px.bar(data_plotly, x='question_1', y='count', color='is_positive', barmode='group',
                 labels={'count':'Количество отзывов', 'question_1':'Курс', 'is_positive':'Позитивность'},
                 title='Количество отзывов по позитивности для каждого курса')

    fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
    fig.update_layout(xaxis_title='Курс', yaxis_title='Количество отзывов',
                      legend_title='Позитивность', legend=dict(x=1, y=1, bgcolor='rgba(255, 255, 255, 0.5)'),
                      xaxis={'categoryorder':'total descending'})
    
    return fig

def distribution_object_feedback(dataframe, type_plot='bar'):
    type_object_feedback = {0: 'Вебинар', 1: 'Программа', 2: 'Преподаватель'}
    
    values = dataframe['object'].value_counts().values
    names = [type_object_feedback[item] for item in dataframe['object'].value_counts().index.tolist()]
    
    title ='Распределение отзывов по объектам'
    
    if type_plot == 'pie':
        fig = px.pie(values=values, names=names, title=title, labels={'names': 'Объект отзыва', 'values': 'Количество отзывов'})
    elif type_plot == 'bar':
        fig = px.bar(x=names, y=values, title=title, labels={'x': 'Объект отзыва', 'y': 'Количество отзывов'})
    
    return fig

def plot_object_feedback(dataframe, courses_to_plot=None):
    data = dataframe.copy(deep=True)
    data['object'] = data['object'].map({0: 'Вебинар', 1: 'Программа', 2: 'Преподаватель'})
    
    if courses_to_plot is not None:
        filtered_data = data[data['question_1'].isin(courses_to_plot)]
    else:
        filtered_data = data
    
    data_plotly = filtered_data.groupby(['question_1', 'object']).size().reset_index(name='count')
    fig = px.bar(data_plotly, x='question_1', y='count', color='object', barmode='group',
                 labels={'count':'Количество отзывов', 'question_1':'Курс', 'object':'Позитивность'},
                 title='Количество отзывов по назначению для каждого курса')

    fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
    fig.update_layout(xaxis_title='Курс', yaxis_title='Количество отзывов',
                      legend_title='Назначение', legend=dict(x=1, y=1, bgcolor='rgba(255, 255, 255, 0.5)'),
                      xaxis={'categoryorder':'total descending'})
    
    return fig

def plot_positivity_feedback_facilities(dataframe):
    data = dataframe.copy(deep=True)
    data['object'] = data['object'].map({0: 'Вебинар', 1: 'Программа', 2: 'Преподаватель'})

    # Группировка данных по объектам и позитивности, подсчет количества отзывов
    data_grouped = data.groupby(['object', 'is_positive']).size().reset_index(name='count')


    # Преобразование данных в проценты
    total_reviews = data_grouped.groupby('object')['count'].transform('sum')
    data_grouped['percentage'] = (data_grouped['count'] / total_reviews) * 100

    # Переименование значений в столбце 'is_positive' для наглядности
    data_grouped['is_positive'] = data_grouped['is_positive'].map({0: 'Негативные', 1: 'Позитивные'})

    # Создание столбчатой диаграммы для показа процентной доли отзывов
    fig = px.bar(data_grouped, x='object', y='percentage', color='is_positive', text='percentage',
                 barmode='group', labels={'percentage':'Процент отзывов', 'object':'Объект'},
                 title='Сравнение процента позитивных и негативных отзывов по объектам')

    # Настройки отображения
    fig.update_layout(xaxis_title='Объект', yaxis_title='Процент отзывов', yaxis=dict(ticksuffix="%"))
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(legend_title_text='Тип отзыва')
    
    return fig

