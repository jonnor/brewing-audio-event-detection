
import os

import pandas
from . import labels

data_dir = os.path.join(os.path.dirname(__file__), '../data')

def get_id_from_labelpath(p):
    f = os.path.basename(p)
    prefix, id = f.split('.')
    assert prefix == 'labels', prefix
    return id

def load_labels_dir(label_dir):

    paths = [ os.path.join(label_dir, f) for f in os.listdir(label_dir) ]

    ids = list(map(get_id_from_labelpath, paths))
    
    files = pandas.DataFrame({
        'path': paths,
        'id': ids,
    }).set_index('id')
    
    df = files.groupby(by='id').apply(lambda r: labels.read(r.path.iloc[0]))
    
    return df

def load_files(files_path=None, extension='.opus'):
    if files_path is None:
        files_path = os.path.join(data_dir, 'files.csv')

    df = pandas.read_csv(files_path)
    df['path'] = os.path.relpath(os.path.join(data_dir, 'audio')) + os.path.sep + df.id + extension
    df = df.set_index('id')
    
    return df


def load_labels(label_dir=None):
    if label_dir is None:
        label_dir = os.path.join(data_dir, 'labels')

    labels = load_labels_dir(label_dir)
    labels['duration'] = labels['end'] - labels['start']
    labels['color'] = labels['annotation'].replace(dict(p='green', n='red'))

    return labels
