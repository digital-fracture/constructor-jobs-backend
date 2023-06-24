# constructor-jobs-backend

This repository contains code for the server-side part of the application.

### [Google Colab notebook with training code](https://colab.research.google.com/drive/18FE7yUcxuOHA1tdX6w5DBWaDptIvoxNs?usp=sharing)

### [GitHub repository with front-end code](https://github.com/digital-fracture/constructor-jobs-frontend)

## Run by yourself

### Docker

```shell
docker pull kruase/constructor-jobs-backend
docker run kruase/constructor-jobs-backend
```

### Pipenv

```shell
git clone https://github.com/digital-fracture/constructor-jobs-backend
cd constructor-jobs-backend
pipenv install
pipenv run python3 server.py
```

### Pure python 3.11

Windows (PowerShell):
```powershell
git clone https://github.com/digital-fracture/constructor-jobs-backend.git
cd constructor-jobs-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

Linux / MacOS:
```shell
git clone https://github.com/digital-fracture/constructor-jobs-backend.git
cd constructor-jobs-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 server.py
```

## Stack

- [python 3.11](https://python.org/) - programming language
- [flask](https://pypi.org/project/Flask/) - web server engine
- [flask-cors](https://pypi.org/project/Flask-Cors/) - CORS for Flask
- [openpyxl](https://pypi.org/project/openpyxl/) - working with MS Excel (.xlsx) spreadsheets
- [reportlab](https://pypi.org/project/reportlab/) - generating PDF documents
- [PIL](https://pypi.org/project/Pillow/) - image processing
- [PyTorch](https://pypi.org/project/torch/), [catboost](https://pypi.org/project/catboost/), [transformers](https://pypi.org/project/transformers/) - model processing
