
# Padrón Electoral para Elecciones Municipales y Regionales 2018

The political party "Podemos Perú" was registered presenting almost 1 million 300 thousand signatures to the Organización Nacional de Procesos Electorales (ONPE). However, some adherents say they never signed the planillon.

![padron.png](https://github.com/indobits/2018-Padron-Electoral/raw/master/img/padron.png "Padrón")

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

## Results

![results.png](https://github.com/indobits/2018-Padron-Electoral/raw/master/img/results.png "Results")

## Source

[News](https://www.americatv.com.pe/noticias/actualidad/veronica-linares-figura-padron-podemos-peru-ella-nunca-lo-firmo-n340650)

[Web App](https://padron.americatv.com.pe)