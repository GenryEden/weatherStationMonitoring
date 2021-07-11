# weatherStationMonitoring
## этот проект поможет вам следить за показаниями вашей метеостанции
Проект уже преднастроен, но в config.py можно (и нужно!) внести изменения:

- словарь **periods** содержит пары ключ-значение, где
  - ключи - технические названия для файлов
  - значения - объекты класса period (см. документацию класса)

- updateTime - период обновления графиков (в минутах)
- apiPassword - пароль для API

## API
для добавления новых значений - "**/api?t={}&h={}&auth={}**", где:
- t - температура
- h - влажность
- auth - пароль
Ответы:
- Nice - записано
- None - ошибка (отустствие одного из параметров / неверный пароль)

**run.py** запускает весь проект
