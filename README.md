
# Padrón Electoral para Elecciones Municipales y Regionales 2018

![alt text](https://github.com/indobits/2018-Padron-Electoral/raw/master/img/web.png "Padrón")

## Configuration

```
➜ ~ git clone https://github.com/indobits/2018-Padron-Electoral.git
➜ ~ virtualenv -p python3.6 2018-Padron-Electoral --no-wheel
➜ ~ cd 2018-Padron-Electoral
➜ 2018-Padron-Electoral cp .env.example .env
➜ 2018-Padron-Electoral vim .env
➜ 2018-Padron-Electoral source bin/activate
(2018-Padron-Electoral) ➜ 2018-Padron-Electoral pip install --upgrade pip
(2018-Padron-Electoral) ➜ 2018-Padron-Electoral sudo apt update
(2018-Padron-Electoral) ➜ 2018-Padron-Electoral sudo apt install libmysqlclient-dev
(2018-Padron-Electoral) ➜ 2018-Padron-Electoral pip install -r requirements.txt
(2018-Padron-Electoral) ➜ 2018-Padron-Electoral python app.py
```
