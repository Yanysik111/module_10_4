from threading import Thread
from time import sleep
from random import randint
from queue import Queue
class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        for i in range(randint(3,10)):
            sleep(i)
    #где происходит ожидание случайным образом от 3 до 10 секунд.

class Cafe:
    thr_l = []
    def __init__(self, *tables):
        self.tables = list(tables)
        self.queue = Queue()

    def guest_arrival(self, *guests):
        list_guests = len(list(guests))
        guests_tabl = min(list_guests,len(self.tables))
        for i in range(guests_tabl):
            self.tables[i].guest = guests[i]
            thr1 = guests[i]
            thr1.start()
            Cafe.thr_l.append(thr1)
            print(f'{list(guests)[i].name} сел(-а) за стол номер {self.tables[i].number}')
        if list_guests > guests_tabl:
            for i in range(guests_tabl, list_guests):
                self.queue.put(guests[i])
                print(f'{list(guests)[i].name} в очереди')
    def discuss_guests(self):
        while not (self.queue.empty()) or Cafe.table_ch(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    thr1 = table.guest
                    thr1.start()
                    Cafe.thr_l.append(thr1)

    def table_ch(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False

tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
for thr in Cafe.thr_l:
    thr.join()