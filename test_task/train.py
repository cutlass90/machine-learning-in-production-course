import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import AutoTokenizer
from os.path import join



class TextDataset(Dataset):
    def __init__(self, df, values2label_func, tokenizer):
        self.data = df
        self.encodings = tokenizer(df.excerpt.tolist(), truncation=True, padding='max_length', max_length=512)
        self.values2label = values2label_func
        self.tokenizer = tokenizer

    def __getitem__(self, item):
        sample = {key: val[item] for key, val in self.encodings.items()}
        sample['text'] = self.data.excerpt[item]
        if 'target' in self.data.columns:
            sample['labels'] = int(self.values2label([self.data.target[item]])[0])

        return sample

    def __len__(self):
        return len(self.data)


def main(path2data='data', train_part=0.8):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    train_path = join(path2data, 'train.csv')
    train_df = pd.read_csv(train_path)
    train_df = train_df.sample(frac=1).reset_index(drop=True)
    bins = np.histogram(train_df.target, bins=100)[1]
    def values2label(list_values):
        return np.digitize(list_values, bins)
    ind = int(len(train_df)*train_part)
    train_dataset = TextDataset(train_df[:ind], values2label, tokenizer)
    val_dataset = TextDataset(train_df[ind:], values2label, tokenizer)
    print(train_dataset[0])



    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=100)
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=5,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()
    print()

    # from transformers import pipeline
    # generator = pipeline(task="text-classification", model=model, tokenizer=tokenizer)
    # print(generator("my name is "))
    #
    # model(**tokenizer(tokenized_imdb['test'][0]['text'], truncation=True, padding="max_length", max_length=256, return_tensors="pt"))

if __name__ == "__main__":
    main()
