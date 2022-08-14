import pickle
from os.path import join

import pandas as pd
import torch
from sklearn.metrics import mean_squared_error
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

from train import vector2prediction


class Predictor:
    def __init__(self, path2checkpoint):
        with open(join(path2checkpoint, 'bins'), 'rb') as f:
            self.bins = pickle.load(f)
        self.model = AutoModelForSequenceClassification.from_pretrained(path2checkpoint)
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    def __call__(self, text):
        with torch.no_grad():
            preictions = self.model(torch.tensor(self.tokenizer(text)['input_ids']).unsqueeze(0)).logits.cpu().numpy()
        result = vector2prediction(preictions, self.bins)
        return result[0]


def main(path2checkpoint, path2data, train_part):
    predictor = Predictor(path2checkpoint)

    df = pd.read_csv(join(path2data, 'train.csv'))
    ind = int(len(df) * train_part)
    predicted = []
    for text in tqdm(df.excerpt.to_list()[ind:]):
        value = predictor(text)
        predicted.append(value)
    targets = df[ind:].target.values
    rms = mean_squared_error(targets, predicted, squared=False)
    print('rms', rms)


if __name__ == '__main__':
    main(path2checkpoint='checkpoints',
         path2data='data',
         train_part=0.8)
