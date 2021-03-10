# covid19-datamart
Covid 19 Datamart

## Setup 
Install the requirements 
```
pip install -r requirements.txt
```

## Data Staging

To stage the data of a desired dimension:

- `--dimension [-D]` The dimension name

Example:

```
python3 ./src/staging/main.py -D "date"
```

To stage the data of all dimensions:

```
python3 ./src/staging/main.py -D "all"
```

To stage the fact table:

```
python3 ./src/staging/main.py -D "fact"
```

To create SQL datamart after staging all dimensions and fact table:

```
psql -h <hostname> -p <port> -d <database> -U <username> -f ./src/database/create_datamart.sql
```
