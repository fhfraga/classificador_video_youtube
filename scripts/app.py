import json
import os
import sqlite3
import time

import db_starter
import get_data
import ml_utils
import pandas as pd
import run_backend
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = "super secret key"


def get_predictions():

    videos = []

    novos_videos_json = 'novos_videos.json'
    if not os.path.exists(novos_videos_json):
        run_backend.update_df()

    last_update = os.path.getmtime(novos_videos_json) * 1e9

    if time.time_ns() == last_update > (720*3600*1e9):  # aprox. 1 mes
        run_backend.update_df()

    with open('novos_videos.json', 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
            videos.append(line_json)

    predictions = []
    for video in videos:
        predictions.append(
            (video['video_id'], video['title'], float(video['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

    predictions_formated = []
    for e in predictions:
        predictions_formated.append(
            "<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=e[1], link=e[0], score=e[2]))

    return '\n'.join(predictions_formated), last_update


def get_predictions_sql():
    videos = []

    novos_videos_db = "videos.db"
    if not os.path.exists(novos_videos_db):
        db_starter.initialize_db_sql()
        run_backend.update_db_sqlite()

    last_update = os.path.getmtime(novos_videos_db) * 1e9

    if time.time_ns() - last_update > (720*3600*1e9):  # aprox. 1 mes
        run_backend.update_db_sqlite()

    with sqlite3.connect(run_backend.db_name) as conn:
        c = conn.cursor()
        for line in c.execute("SELECT * FROM videos ORDER BY score DESC"):
            line_json = {"title": line[0], "video_id": line[1],
                         "score": line[2], "update_time": line[3]}
            videos.append(line_json)
    return videos, last_update


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        link = request.form['link']

        try:
            data = get_data.get_data_one_video(link)
        except Exception as error:
            print(error)
            flash('Erro na predição')

        try:
            probabilidade = ml_utils.compute_prediction(data)
            flash(f"Titulo: {data.loc[0, 'titulo']}")
            flash(f"Link: {data.loc[0, 'link']}")
            flash(f"Score: {probabilidade[0]}")
        except Exception as error:
            print(error)
            flash('Erro')
        return render_template('/prediction.html')
    else:
        return render_template('/prediction.html')


@ app.route('/')
def main_page():
    preds, last_update = get_predictions_sql()  # get_predictions()
    return render_template('index.html', videos=preds)
    # return """<head><h1>Recomendador de Vídeos do Youtube</h1><head>
    # <body>
    # Segundos desde a última atualização: {}

    # <table>
    #         {}
    # </table>
    # </body>""".format((time.time_ns() - last_update) / 1e9, preds)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
