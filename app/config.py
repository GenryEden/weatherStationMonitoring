from app import dbWorker

# словарь periods содержит пары ключ-значение, где
# ключи - технические названия для файлов
# значения - объекты класса period (см. документацию класса)

periods = {
    'hour': dbWorker.period(1, None, 'За час'),
    'day': dbWorker.period(24, 1, 'За день'),
    'week': dbWorker.period(24*7, 6, 'За неделю'),
    'month': dbWorker.period(24*28, 24, 'За месяц'),
    '3months': dbWorker.period(24*28*3, 24*3, 'За 3 месяца'),
    'halfyear': dbWorker.period(12*365, 24*3, 'За полгода'),
    'year': dbWorker.period(24*365, 24*6, 'За год'),
    'all': dbWorker.period(None, 24*12, 'За все время')
}

updateTime = 1 # период обновления графиков (в минутах)

apiPassword = 'changemeplz'