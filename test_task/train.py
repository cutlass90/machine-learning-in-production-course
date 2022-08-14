import pickle
from os.path import join

import numpy as np
import pandas as pd
import scipy
from sklearn.metrics import mean_squared_error
from torch.utils.data import Dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import AutoTokenizer
from transformers import EarlyStoppingCallback, IntervalStrategy


class TextDataset(Dataset):
    def __init__(self, df, bins, tokenizer):
        self.is_train = 'target' in df.columns
        self.data = df
        self.encodings = tokenizer(df.excerpt.tolist(), truncation=True, padding=True)
        self.bins = bins

    def __getitem__(self, item):
        sample = {key: val[item] for key, val in self.encodings.items()}
        if self.is_train:
            sample['labels'] = int(values2label([self.data.target.values[item]], self.bins)[0])

        return sample

    def __len__(self):
        return len(self.encodings.encodings)


def values2label(list_values, bins):
    return np.digitize(list_values, bins) - 1


def vector2prediction(x, bins):
    x = scipy.special.softmax(x, axis=1)
    y = np.array([(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)] + [bins.max()])
    return (x * y[None, :]).sum(1)


def compute_metrics(p):
    with open('bins', 'rb') as f:
        bins = pickle.load(f)
    pred = vector2prediction(p.predictions, bins)
    b = np.zeros((p.label_ids.size, p.predictions.shape[1]))
    b[np.arange(p.label_ids.size), p.label_ids] = 1
    targets = vector2prediction(b * 1e3, bins)
    rms = mean_squared_error(targets, pred, squared=False)
    return {"rmse": rms}


def main(path2data='data', train_part=0.8):
    N_classes = 100
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    train_path = join(path2data, 'train.csv')
    train_df = pd.read_csv(train_path)
    bins = np.histogram(train_df.target, bins=N_classes - 1)[1]
    with open('bins', 'wb') as f:
        pickle.dump(bins, f)

    ind = int(len(train_df) * train_part)
    train_dataset = TextDataset(train_df[:ind], bins, tokenizer)
    val_dataset = TextDataset(train_df[ind:], bins, tokenizer)

    test_path = join(path2data, 'test.csv')
    test_df = pd.read_csv(test_path)
    test_dataset = TextDataset(test_df, bins, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=N_classes)
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=20,
        weight_decay=0.01,
        load_best_model_at_end=True,
        evaluation_strategy=IntervalStrategy.STEPS,
        eval_steps=50,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    trainer.train()
    trainer.save_model('checkpoints')

    print('!!!evaluation train', trainer.evaluate(train_dataset))
    print('!!!evaluation val', trainer.evaluate(val_dataset))
    predicted = trainer.predict(test_dataset)
    with open('predicted_test', 'wb') as f:
        pickle.dump(predicted, f)

    predicted = trainer.predict(val_dataset)
    with open('predicted_val', 'wb') as f:
        pickle.dump(predicted, f)

    predicted = trainer.predict(train_dataset)
    with open('predicted_train', 'wb') as f:
        pickle.dump(predicted, f)



if __name__ == "__main__":
    main()
