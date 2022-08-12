import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import AutoTokenizer
from os.path import join
import pickle
from transformers import EarlyStoppingCallback, IntervalStrategy



class TextDataset(Dataset):
    def __init__(self, df, values2label_func, tokenizer):
        self.is_train = 'target' in df.columns
        self.data = df
        self.encodings = tokenizer(df.excerpt.tolist(), truncation=True, padding=True)
        self.values2label = values2label_func

    def __getitem__(self, item):
        sample = {key: val[item] for key, val in self.encodings.items()}
        if self.is_train:
            sample['labels'] = int(self.values2label([self.data.target.values[item]])[0])

        return sample

    def __len__(self):
        return len(self.encodings.encodings)


def main(path2data='data', train_part=0.8):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    train_path = join(path2data, 'train.csv')
    train_df = pd.read_csv(train_path)
    bins = np.histogram(train_df.target, bins=100)[1]
    def values2label(list_values):
        return np.digitize(list_values, bins)
    ind = int(len(train_df)*train_part)
    train_dataset = TextDataset(train_df[:ind], values2label, tokenizer)
    val_dataset = TextDataset(train_df[ind:], values2label, tokenizer)
    val_dataset[0]

    test_path = join(path2data, 'test.csv')
    test_df = pd.read_csv(test_path)
    test_dataset = TextDataset(test_df, values2label, tokenizer)



    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=102)
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
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
