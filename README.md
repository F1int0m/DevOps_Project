Hi!
It's my study project ^_^



## Как запустить?
1. Скопировать файлик `.env.example` и переименовать его в `.env`

2.  ```commandline
    pip install -r requirements.txt
    ```
    
3.  ```commandline
    docker-compose up -d redis
    ```
    
4.  ```commandline
    flask run
    ```

Если надо заполнить базу данными, то:
```commandline
python3 db_filling.py 
```