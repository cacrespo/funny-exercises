"""
Recorridos de Bicicletas de la Ciudad
https://data.buenosaires.gob.ar/dataset/bicicletas-publicas

Imprime las tres estaciones de origen más “calientes” en la mañana (de 6 a
11:59)
"""

import pandas as pd

URL = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/transporte-y-obras-publicas/bicicletas-publicas/"  # noqa
FILE = "recorridos-realizados-2023.zip"
TOP_N = 3


def load_file(file):
    """Carga el file .csv por chunks y retorna un dataframe."""
    chunk_list = []
    size = 10 ** 5
    cols = ['fecha_origen_recorrido',
            'Id_recorrido',
            'id_estacion_origen',
            'nombre_estacion_origen',
            ]

    df_chunk = pd.read_csv(file, chunksize=size, sep=',', compression='zip')
    for chunk in df_chunk:
        _ = chunk.set_index(pd.to_datetime(chunk['fecha_origen_recorrido']))[
            cols].between_time('6:00', '11:59', inclusive='both')

        _ = _.groupby(['id_estacion_origen', 'nombre_estacion_origen']).agg(
            {
                'Id_recorrido': 'nunique',
            })
        chunk_list.append(_)

    df = pd.concat(chunk_list)
    return df


def top_recorridos(df, n):
    """Recibe el dataframe y retorna los n recorridos más frecuentes."""
    df.groupby(['id_estacion_origen', 'nombre_estacion_origen']).agg({
        'Id_recorrido': 'sum',
    })
    df = df.groupby(['id_estacion_origen', 'nombre_estacion_origen']).agg(
        n_recorridos=('Id_recorrido', 'sum'))
    df.reset_index(inplace=True)
    df.columns = ['id_estacion', 'nombre', 'n_recorridos']
    df = df.sort_values('n_recorridos', ascending=False)[0:n]
    return df


file_2023 = load_file(URL+FILE)
results = top_recorridos(file_2023, TOP_N)

print(results)
