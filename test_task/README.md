## Solution for test task for Machine Learning in Production course

### Train
To train model simply run train.py script.
```angular2html
python3 train.py
```
trained model will be saved into ```checkpoint``` dir
<br>Evaluation score RMSE=0.58

### Start API
To start API you should first start ray server
```angular2html
ray start --head
```
Then start API:
```angular2html
python3 start_server.py
```
Simple example that tests server is implemented in clients_test.py
```angular2html
python3 client_test.py
```