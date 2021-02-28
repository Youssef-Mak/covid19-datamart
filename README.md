# covid19-datamart
Covid 19 Datamart

## Setup 
Install the requirements 
```
pip install -r requirements.txt
```

## Data Staging

To stage the data a desired dimension:

- `--dimension [-D]` The dimension name

Example:

```
python3 ./src/staging/main.py -D "date"
```
