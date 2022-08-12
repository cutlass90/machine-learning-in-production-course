import pickle
import scipy
import numpy as np
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import AutoTokenizer
from os.path import join
import pickle
from sklearn.metrics import mean_squared_error



def main(path2data, path2predictions):
    train_part = 0.8
    train_path = join(path2data, 'train.csv')
    train_df = pd.read_csv(train_path)
    bins = np.histogram(train_df.target, bins=100)[1]

    def vector2prediction(x):
        x = scipy.special.softmax(x, axis=1)
        y = np.array([(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)])
        return (x[:,:100]*y[None, :]).sum(1)

    with open(path2predictions, 'rb') as f:
        data = pickle.load(f)

    predictions = vector2prediction(data.predictions)
    ind = int(len(train_df) * train_part)
    targets = train_df[:ind].target.values
    rms = mean_squared_error(targets, predictions, squared=False)
    print('rms', rms)
    return predictions




if __name__ == "__main__":
    main('data', 'predicted_train', )

print()