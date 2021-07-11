import csv
import time
from datetime import timedelta, datetime

class worker:
    """Модуль работы с базой"""
    def __init__(self,
                 filename='./app/static/csv/db.csv',
                 timeFormat='%H:%M %d-%m-%Y'):
        """
            filename - имя csv файла с данными
            timeFormat - формат даты csv файла
        """
        self.filename = filename
        self.timeFormat = timeFormat

    def getLast(self):
        '''
        возвращает словарь, где 
        getLast()["date"] - дата последней записи
        getLast()["temp"] - температура в последней записи
        getLast()["temp"] - влажность в последней записи
        '''
        try:
            with open(self.filename, 'r') as file:
                csvReader = csv.DictReader(file, delimiter=';')
                try:
                    return list(csvReader)[-1]
                except IndexError:
                    return None
        except FileNotFoundError:
            self.clear()
            return None

    def clear(self):
        '''
        очищает файл, оставляя только шапку
        '''
        with open(self.filename, 'w') as file:
            file.write('date;temp;hum\n')

    def append(self,
               t, h,
               timeOfData = None):
        """
            t - температура, до 128
            h - влажность, до 100
            timeOfData - время в формате модуля time,
                если None, то ставится текущее время
        """
        if int(t) > 128 or int(h) > 100:
            return
        if timeOfData is None:
            timeOfData = time.strftime(self.timeFormat)
        with open(self.filename, 'a') as file:
            file.write(f'{timeOfData};{t};{h}\n')
            file.close()

    def getByLastTime(self, period):
        '''
        принимает
        period класса period определяет объем выборки и диапозо
        возвращает массив ans, где
        ans[0] - массив температур
        ans[1] - массив влажностей
        ans[2] - массив дат

        '''
        ans = [[],[],[]]
        buff = [[],[],[]]
        try:
            with open(self.filename, 'r') as file:
                csvReader = csv.DictReader(file, delimiter=';')
                if period.limiter is not None:
                    lastTime = datetime.now() - timedelta(hours=period.limiter)
                else:
                    lastTime = None
                for row in csvReader:
                    rowTime = datetime.strptime(row['date'],
                                            self.timeFormat)
                    if not(lastTime) or rowTime > lastTime:
                        buff[0].append(int(row['temp']))
                        buff[1].append(int(row['hum']))
                        buff[2].append(rowTime)
                    else:
                        continue
                    if not(period.averagingRange):
                        ans[0].append(buff[0][0]) 
                        ans[1].append(buff[1][0]) 
                        ans[2].append(buff[2][0]) 
                        buff = [[],[],[]]
                    elif rowTime - buff[2][0] > timedelta(hours=period.averagingRange):
                        ans[0].append(sum(buff[0])/len(buff[0]))
                        ans[1].append(sum(buff[1])/len(buff[1]))
                        ans[2].append(buff[2][-1])
                        buff = [[],[],[]]
                ans[0] += buff[0]
                ans[1] += buff[1]
                ans[2] += buff[2]

        except FileNotFoundError:
            self.clear()
            return [[], [], []]

        return ans

class period:
    """
    хранит в себе значения, необходимые
    для определения периодов значений графиков
    """
    def __init__(self, limiter=None, averagingRange=None, title=None):
        '''
        limiter - значение в часах, которое обозначает край периода, 
            None - все значения
        averagingRange - время (в часах), за которое берутся значения для усреднения
            None - без усреднения
        title - строка, использующаяся в качестве подписи к графику
        '''
        self.limiter = limiter
        self.averagingRange = averagingRange
        self.title = title



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
    formatter = DateFormatter('%m/%d/%y')
    w = worker('./static/csv/db.csv')
    periods = {
        'hour': period(1, None, 'За час'),
        'day': period(24, 1, 'За день'),
        'week': period(24*7, 6, 'За неделю'),
        'month': period(24*28, 24, 'За месяц'),
        '3months': period(24*28*3, 24*3, 'За 3 месяца'),
        'halfyear': period(12*365, 24*3, 'За полгода'),
       'year': period(24*365, 24*6, 'За год'),
        'all': period(None, 24*12, 'За все время')
    }

    for period in periods:
        print(period)
        a = w.getByLastTime(periods[period])

