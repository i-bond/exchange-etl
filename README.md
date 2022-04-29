# exchange-etl

**Описание проекта:**   

ETL процесс с оркестрацией на Airflow для сбора/ выгрузки данных с https://exchangerate.host/ по валютной паре BTC/USD. 
historical_dag.py - загружает исторические данные начиная с 2020 года
latest_dag.py - загружает данные через каждые 3 часа

**Команды для запуска:**
``` bash
docker-compose build 
docker-compose up airflow-init
docker-compose up
docker-compose down --volumes --rmi all
```

Тестирование тасков:  
```bash
airflow tasks test historical_dag historical_rates_task 2021-01-01
docker exec -it exchange_etl_airflow-worker_1 bash
```



