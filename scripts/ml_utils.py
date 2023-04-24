import datetime
import json
import re

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack

random_forest = joblib.load('./modelos/random_forest_2023_04_19.pkl.z')
lgbm = joblib.load('./modelos/lgbm_2023_04_19.pkl.z')
title_vec = joblib.load('./modelos/title_vectorize_2023_04_19.pkl.z')


def compute_features(data):
    # para evitar divisões por zero
    dia_posterior_atual = str(datetime.date.today() + datetime.timedelta(1))

    titulo = data['titulo']
    features = pd.DataFrame(index=data.index)
    features['visualizacoes'] = data['visualizacoes']

    features['tempo_desde_pub'] = (pd.to_datetime(
        dia_posterior_atual) - data['data_upload']) / np.timedelta64(1, 'D')
    features['visualizacoes_por_dia'] = features['visualizacoes'] / \
        features['tempo_desde_pub']
    del features['tempo_desde_pub']
    features = features.astype('float')

    title_vec = joblib.load("./modelos/title_vectorize_2023_04_19.pkl.z")
    vectorized_title = title_vec.transform(titulo)
    feature_array = hstack([features, vectorized_title])
    return feature_array


def compute_prediction(data):
    feature_array = compute_features(data)

    if feature_array is None:
        return 0

    lgbm = joblib.load('./modelos/lgbm_2023_04_19.pkl.z')
    random_forest = joblib.load('./modelos/random_forest_2023_04_19.pkl.z')

    probabilidade_lgbm = lgbm.predict_proba(feature_array)[:, 1]
    probabilidade_random_forest = random_forest.predict_proba(feature_array)[
        :, 1]

    probabilidade_final = (
        0.3 * probabilidade_random_forest + 0.7 * probabilidade_lgbm) / 2
    return probabilidade_final
