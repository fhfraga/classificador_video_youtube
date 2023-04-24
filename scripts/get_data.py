import datetime

import numpy as np
import pandas as pd
import youtube_dlc


def split(df, coluna, coluna_vazia, padrao):
    for numero, string in enumerate(df[coluna_vazia]):
        index = numero
        if string == 'Sem valor':
            print(df[coluna][index])
            valor = df[coluna][index]
            print(valor)
            df[coluna_vazia][index] = valor.split(padrao)[1]


def get_data_video(query, ydl):
    resultados = []

    resultado = ydl.extract_info(
        'ytsearchdate10:{}'.format(query), download=False)
    for entrada in resultado['entries']:
        if entrada is not None:
            entrada['query'] = query
        resultados += resultado['entries']
        resultados = [valor for valor in resultados if valor is not None]

        df = pd.DataFrame(resultados)

        df[['uploader', 'tags', 'like_count']] = df[[
            'uploader', 'tags', 'like_count']].fillna('Sem valor')

        split(df, 'uploader_url', 'uploader', '@')

        df['tags'] = df['tags'].replace('Sem valor', '')
        df['like_count'] = df['like_count'].replace('Sem valor', 0)

        df_filtrado = df[['id', 'title', 'uploader', 'upload_date', 'categories', 'tags',
                          'duration', 'webpage_url', 'view_count', 'like_count', 'query']]

        df_filtrado['id'] = 'watch?v=' + df_filtrado.loc[:, 'id']

        df_filtrado['upload_date'] = df_filtrado['upload_date'].astype(str).apply(
            lambda x: datetime.datetime.strptime(x, '%Y%m%d').strftime('%Y-%m-%d'))
        df_filtrado['upload_date'] = pd.to_datetime(
            df_filtrado['upload_date'], format='%Y-%m-%d')

        colunas = ['id', 'titulo', 'canal', 'data_upload', 'categoria', 'tags',
                   'duracao_segundos', 'link', 'visualizacoes', 'quantidade_likes',
                   'query']
        df_filtrado.columns = colunas

        return df_filtrado


def get_data_one_video(link):
    ydl = youtube_dlc.YoutubeDL({'ignoreerros': True})

    resultado = ydl.extract_info(link, download=False)

    colunas = ['id', 'title', 'uploader', 'upload_date', 'categories', 'tags',
               'duration', 'webpage_url', 'view_count', 'like_count', 'playlist']

    df = pd.DataFrame(columns=colunas)
    df.loc[0, :] = [resultado[x] for x in colunas]

    df['id'] = 'watch?v=' + df['id']

    df['upload_date'] = df['upload_date'].astype(str).apply(
        lambda x: datetime.datetime.strptime(x, '%Y%m%d').strftime('%Y-%m-%d'))

    df['upload_date'] = pd.to_datetime(
        df['upload_date'], format='%Y-%m-%d')

    colunas = ['id', 'titulo', 'canal', 'data_upload', 'categoria', 'tags',
               'duracao_segundos', 'link', 'visualizacoes', 'quantidade_likes',
               'query']

    df.columns = colunas

    return df
