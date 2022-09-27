```python
import pandas as pd
import numpy as np

FORMATS = ['clipboard', 'csv', 'feather', 'json', 'parquet', 'pickle', 'stata']

def get_dataset(size):
    # Create Fake Dataset
    df = pd.DataFrame()
    df['size'] = np.random.choice(['big','medium','small'], size)
    df['age'] = np.random.randint(1, 50, size)
    df['team'] = np.random.choice(['red','blue','yellow','green'], size)
    df['win'] = np.random.choice(['yes','no'], size)
    dates = pd.date_range('2020-01-01', '2022-12-31')
    df['date'] = np.random.choice(dates, size)
    df['prob'] = np.random.uniform(0, 1, size)
    return df

def set_dtypes(df):
    df['size'] = df['size'].astype('category')
    df['team'] = df['team'].astype('category')
    df['age'] = df['age'].astype('int16')
    df['win'] = df['win'].map({'yes':True, 'no': False})
    df['prob'] = df['prob'].astype('float32')
    return df
```


```python
for dataset_size, size in [['small', 1e2], ['medium', 1e4], ['large', 1e6]]:
    size = int(size)
    print(f"\n---===Testing {dataset_size} dataset, {size} rows===---")
    df = get_dataset(size)
    df = set_dtypes(df)
    for func in FORMATS:
        print('\t', func, 'writing')
        %time getattr(df, 'to_'+func)('dummy_file_name')
        print('\t', func, 'reading')
        %time getattr(pd, 'read_'+func)('dummy_file_name')

```

    
    ---===Testing small dataset, 100 rows===---
    	 clipboard writing
    CPU times: user 5.61 ms, sys: 1.33 ms, total: 6.94 ms
    Wall time: 11.2 ms
    	 clipboard reading
    CPU times: user 2.41 ms, sys: 2.71 ms, total: 5.12 ms
    Wall time: 9.27 ms
    	 csv writing
    CPU times: user 0 ns, sys: 2.18 ms, total: 2.18 ms
    Wall time: 2.07 ms
    	 csv reading
    CPU times: user 104 µs, sys: 1.64 ms, total: 1.75 ms
    Wall time: 1.78 ms
    	 feather writing
    CPU times: user 6.9 ms, sys: 14.7 ms, total: 21.6 ms
    Wall time: 44.2 ms
    	 feather reading
    CPU times: user 1.94 ms, sys: 2.21 ms, total: 4.16 ms
    Wall time: 7.96 ms
    	 json writing
    CPU times: user 293 µs, sys: 333 µs, total: 626 µs
    Wall time: 555 µs
    	 json reading
    CPU times: user 6.19 ms, sys: 0 ns, total: 6.19 ms
    Wall time: 6.49 ms
    	 parquet writing
    CPU times: user 7.52 ms, sys: 0 ns, total: 7.52 ms
    Wall time: 16.8 ms
    	 parquet reading
    CPU times: user 6.57 ms, sys: 1.04 ms, total: 7.61 ms
    Wall time: 11.4 ms
    	 pickle writing
    CPU times: user 174 µs, sys: 194 µs, total: 368 µs
    Wall time: 327 µs
    	 pickle reading
    CPU times: user 379 µs, sys: 422 µs, total: 801 µs
    Wall time: 722 µs
    	 stata writing
    CPU times: user 8.11 ms, sys: 107 µs, total: 8.22 ms
    Wall time: 7.68 ms
    	 stata reading
    CPU times: user 6.36 ms, sys: 0 ns, total: 6.36 ms
    Wall time: 6.31 ms
    
    ---===Testing medium dataset, 10000 rows===---
    	 clipboard writing
    CPU times: user 44 ms, sys: 2.57 ms, total: 46.6 ms
    Wall time: 50.1 ms
    	 clipboard reading
    CPU times: user 15.5 ms, sys: 3.66 ms, total: 19.2 ms
    Wall time: 25.3 ms
    	 csv writing
    CPU times: user 40.6 ms, sys: 4.56 ms, total: 45.2 ms
    Wall time: 45.3 ms
    	 csv reading
    CPU times: user 5.43 ms, sys: 0 ns, total: 5.43 ms
    Wall time: 5.27 ms
    	 feather writing
    CPU times: user 2.65 ms, sys: 1.44 ms, total: 4.1 ms
    Wall time: 3.18 ms
    	 feather reading
    CPU times: user 1.58 ms, sys: 1.54 ms, total: 3.12 ms
    Wall time: 2.41 ms
    	 json writing
    CPU times: user 3.12 ms, sys: 2.5 ms, total: 5.61 ms
    Wall time: 5.59 ms
    	 json reading
    CPU times: user 23.1 ms, sys: 0 ns, total: 23.1 ms
    Wall time: 23.1 ms
    	 parquet writing
    CPU times: user 4.75 ms, sys: 492 µs, total: 5.24 ms
    Wall time: 4.16 ms
    	 parquet reading
    CPU times: user 3.9 ms, sys: 0 ns, total: 3.9 ms
    Wall time: 2.57 ms
    	 pickle writing
    CPU times: user 293 µs, sys: 278 µs, total: 571 µs
    Wall time: 524 µs
    	 pickle reading
    CPU times: user 511 µs, sys: 483 µs, total: 994 µs
    Wall time: 944 µs
    	 stata writing
    CPU times: user 7.17 ms, sys: 0 ns, total: 7.17 ms
    Wall time: 7.16 ms
    	 stata reading
    CPU times: user 6.87 ms, sys: 0 ns, total: 6.87 ms
    Wall time: 6.85 ms
    
    ---===Testing large dataset, 1000000 rows===---
    	 clipboard writing
    CPU times: user 4.4 s, sys: 57.5 ms, total: 4.45 s
    Wall time: 4.46 s
    	 clipboard reading
    CPU times: user 1.38 s, sys: 120 ms, total: 1.5 s
    Wall time: 1.89 s
    	 csv writing
    CPU times: user 4.22 s, sys: 43.9 ms, total: 4.27 s
    Wall time: 4.28 s
    	 csv reading
    CPU times: user 311 ms, sys: 27.9 ms, total: 339 ms
    Wall time: 338 ms
    	 feather writing
    CPU times: user 49.3 ms, sys: 13.9 ms, total: 63.3 ms
    Wall time: 30.4 ms
    	 feather reading
    CPU times: user 21.6 ms, sys: 9.99 ms, total: 31.6 ms
    Wall time: 13.5 ms
    	 json writing
    CPU times: user 492 ms, sys: 120 ms, total: 612 ms
    Wall time: 644 ms
    	 json reading
    CPU times: user 2.95 s, sys: 344 ms, total: 3.3 s
    Wall time: 3.3 s
    	 parquet writing
    CPU times: user 71.2 ms, sys: 23.9 ms, total: 95.1 ms
    Wall time: 87 ms
    	 parquet reading
    CPU times: user 35.4 ms, sys: 19.5 ms, total: 54.9 ms
    Wall time: 21 ms
    	 pickle writing
    CPU times: user 890 µs, sys: 7.69 ms, total: 8.58 ms
    Wall time: 13.2 ms
    	 pickle reading
    CPU times: user 0 ns, sys: 3.45 ms, total: 3.45 ms
    Wall time: 3.36 ms
    	 stata writing
    CPU times: user 53.9 ms, sys: 24.5 ms, total: 78.4 ms
    Wall time: 77.7 ms
    	 stata reading
    CPU times: user 76.8 ms, sys: 0 ns, total: 76.8 ms
    Wall time: 76.7 ms


### Summary:pickle is the best data format for python by read/write speed. csv is not a good idea for fast reading/writing big files


```python

```
