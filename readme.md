# Setup Environment - Shell/Terminal

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```