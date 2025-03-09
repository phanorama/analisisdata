# Setup Environment - Shell/Terminal

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup Environment - Anaconda
```
conda create --name .venv python=3.10
conda activate .venv
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```