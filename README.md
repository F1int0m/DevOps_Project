Интернет магазин

Учебный проект, в котором реализован функционал интернет магазина, с небольшой админкой.
Умеет валидировать почту и отправлять напоминание о покупке



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