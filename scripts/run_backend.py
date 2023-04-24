import os
import sqlite3
import time

import youtube_dlc
from get_data import *
from ml_utils import *

queries = ['ciencia+de+dados', 'machine+learning', 'inteligencia+artificial']


def update_df():
    ydl = youtube_dlc.YoutubeDL({'ignoreerrors': True})

    with open('novos_videos.json', 'w+') as output:
        for query in queries:
            print(query)
            try:
                data = get_data_video(query, ydl)
            except Exception as erro:
                print(erro)
                continue

            probabilidade = compute_prediction(data)

            video_id = 'https://www.youtube.com/'+data['id']

            data_front = {'title': data['titulo'],
                          'score': probabilidade, 'video_id': video_id}

            for idx, data_row in pd.DataFrame(data_front).iterrows():
                print(video_id, json.dumps(data_row.to_dict()))
                output.write(f'{json.dumps(data_row.to_dict())}\n')
    return True


db_name = 'videos.db'


# def update_db_sqlite():
#     ydl = youtube_dlc.YoutubeDL({'ignoreerrors': True})

#     with sqlite3.connect(db_name) as conn:
#         for query in queries:
#             print(query)
#             try:
#                 data = get_data_video(query, ydl)
#             except Exception as erro:
#                 print(erro)
#                 continue

#         probabilidade = compute_prediction(data)

#         video_id = 'https://www.youtube.com/'+data['link']
#         data_front = {'title': data['titulo'],
#                       'video_id': video_id, 'score': probabilidade}
#         data_front['update_time'] = time.time_ns()

#         for idx, data_row in pd.DataFrame(data_front).iterrows():
#             cursor = conn.cursor()
#             print(
#                 'INSERT INTO videos VALUES ("{title}", "{video_id}", {score}, {update_time})'.format(**data_row.to_dict()))
#             cursor.execute('INSERT INTO videos VALUES ("{title}", "{video_id}", {score}, {update_time})'.format(
#                 **data_row.to_dict()))
#             conn.commit()
#     return True

def update_db_sqlite():
    ydl = youtube_dlc.YoutubeDL({"ignoreerrors": True})

    with sqlite3.connect(db_name) as conn:
        for query in queries:
            print(query)
            try:
                data = get_data_video(query, ydl)
            except Exception as e:
                print(e)
                # os.remove("novos_videos.json")
                continue

            p = compute_prediction(data)

            video_id = data['link']  # 'https://www.youtube.com/' + \
            # data['link']  # .values.tolist()
            data_front = {"title": data['titulo'],
                          "video_id": video_id, "score": p}
            data_front['update_time'] = time.time_ns()
            # print(data_front)
            for idx, data_row in pd.DataFrame(data_front).iterrows():
                # print(video_id, json.dumps(data_row.to_dict()))
                # print({**data_row.to_dict()})
                c = conn.cursor()
                print('INSERT INTO videos VALUES ("{title}", "{video_id}", {score}, {update_time})'.format(
                    **data_row.to_dict()))
                c.execute('INSERT INTO videos VALUES ("{title}", "{video_id}", {score}, {update_time})'.format(
                    **data_row.to_dict()))
                conn.commit()
    return True
