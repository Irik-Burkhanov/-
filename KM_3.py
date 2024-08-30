import math
import random
import numpy as np
from prettytable import PrettyTable

# VARIABLES
tt = 10.0
T = 19
Tp = 0.0
Na = 0
Nd = 0
n = 0
intensity = 3.0
lambd = 3.0
Amount = 0
Work = 0.0

# LISTS
A = []
W = []
D = []
TimeEvent = []
N = []
Event = []
ClientOfEvent = []

# FUNCTIONS
def lambdaFunc(t):
    if ( 0 <= t < 3):
        t = 1 + 1/(t + 1)
    if ( 3 <= t < 5):
        t = 1.5 + 3/t
    if ( 5 <= t < 9):
        t = 2 + 4/t
    return t

def poisson(t, lambd):
    while(1):
        u1 = random.random()
        t -= math.log(u1) / lambd
        u2 = random.random()
        if (u2 <= lambdaFunc(t) / lambd):
            return t

def exponentional(lambd):
    return -math.log(random.random()) / lambd

def add():
    global tt, Ta, Na, n, Amount, Td
    tt = Ta
    Na += 1
    n += 1
    Ta = poisson(tt, intensity)
    if (n == 1):
        Td = tt + exponentional(lambd)
    A.append(tt)
    Amount += 1
    N.append(n)
    TimeEvent.append(tt)
    Event.append('Клиент ' + str(Na) + ' прибыл')

def leaving():
    global Td, Nd, n, tt
    tt = Td
    Nd += 1
    n -= 1
    if (n == 0):
        Td = 1e6
    else:
        Td = tt + exponentional(lambd)
    D.append(tt)
    N.append(n)
    TimeEvent.append(tt)
    Event.append('Уход клиента: ' + str(Nd))

def last():
    global Td, Nd, n, tt
    tt = Td
    Nd += 1
    n -= 1
    if (n > 0):
        Td = tt + exponentional(lambd)
    D.append(tt)
    TimeEvent.append(tt)
    N.append(n)
    Event.append('Уход клиента: ' + str(Nd))

def end():
    global n, Tp, tt, T
    Tp = max(tt - T, 0)
    N.append(n)

# MAIN
t_start = int(input('Введите начало рабочего дня: '))
t_finish = int(input('Введите конец рабочего дня: '))
T = t_finish - t_start
Ta = exponentional(lambd)
Td = 1e6

while(1):
    if (Ta <= Td) and (Ta <= T):
        add()
    if (Td < Ta) and (Td <= T):
        leaving()
    if (min(Ta, Td) > T) and (n > 0):
        last()
    if (min(Ta, Td) > T) and (n == 0):
        end()
        break

table1 = PrettyTable(['Событие', 'Время события', 'В очереди'])

for i in range(len(TimeEvent)):
    table1.add_row([Event[i], TimeEvent[i], N[i]])

    if (Event[i][0] == 'К') and (N[i] <= 1):
        W.append(0)
    elif (Event[i][0] == 'К'):
        ClientOfEvent.append(TimeEvent[i])
    if (Event[i][0] == 'У') and (len(ClientOfEvent) != 0):
        elem = ClientOfEvent[0]
        ClientOfEvent = ClientOfEvent[1:]
        W.append(TimeEvent[i] - elem)
    if (Event[i][0] == 'К'):
        if (i == 0) or (N[i - 1] == 0):
            if (i == 0):
                Work = TimeEvent[i]
            else:
                Work = TimeEvent[i] - TimeEvent[i - 1]
print(table1)

table2 = PrettyTable(['№', 'Ai - приход', 'Di - уход', 'Vi - время обсл.', 'Wi - время в очер.', 'Ai - Di'])
for i in range(len(D)):
    table2.add_row([i + 1, A[i], D[i], D[i] - A[i] - W[i], W[i], D[i] - A[i]])
print(table2)

print('Количество клиентов за смену: ', Amount)
print('Время задержки закрытия: ', Tp)
print('Среднее время клиентов в очереди: ', np.mean(W))
print('Среднее время клиента в системе: ', np.mean(np.array(D) - np.array(A)))
print('Коэффициент занятости устройства: ', 1-(Work / T))
print('Средняя длина очереди: ', np.mean(N))
