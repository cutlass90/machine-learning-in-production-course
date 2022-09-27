```python
from multiprocessing import Pool
import pandas as pd
import numpy as np
import uuid
```


```python
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

def heavy_function(path):
    df = get_dataset(1000000)
    df = set_dtypes(df)
    name = str(uuid.uuid4())
    df.to_csv(name)
    pd.read_csv(name)
```


```python
def single_process():
    results = []
    for _ in range(10):
        results.append(heavy_function('dummy_file_name'))
    return results
```


```python
print('single process takes')
%time res_single = single_process()
```

    single process takes
    CPU times: user 51.7 s, sys: 1.36 s, total: 53 s
    Wall time: 53 s



```python
def multi_processing():
    with Pool(10) as pool:
        results = pool.map(heavy_function, ['dummy_file_name']*10)
    return results
        
```


```python
print('multi processing takes')
%time res_multi = multi_processing()
```

    multi processing takes
    CPU times: user 9.49 ms, sys: 31.9 ms, total: 41.4 ms
    Wall time: 12.8 s


## Result: multiprocessing 4 times faster than single process for CPU consumption tasks 


```python

```
