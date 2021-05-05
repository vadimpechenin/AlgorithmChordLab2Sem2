"""
Классы и их методы, реализующие алгоритм Chord

"""
import numpy as np
import copy

class finger():
    #Класс finger (таблица)
    def __init__(self):
        self.start = []
        self.interval = []
        self.node = []
        self.successor = []

class ChordNode():
    #Класс ChordNode
    def __init__(self, M_intN,m_arPos,number):
        self.m = M_intN
        self.arPos = m_arPos
        self.i = number
        self.finger = [] #Пустой массив объектов
        for i in range(M_intN-1):
            self.finger.append(finger())
            self.finger[i].start.append((number + 2 ** (i)) % 2 ** (M_intN - 1))
            if i<M_intN-2:
                self.finger[i].interval.append((number + 2 ** (i)) % 2 ** (M_intN - 1))
                self.finger[i].interval.append((number + 2 ** (i+1)) % 2 ** (M_intN - 1))
            else:
                self.finger[i].interval.append((number + 2 ** (i)) % 2 ** (M_intN - 1))
                self.finger[i].interval.append(number)
            k = 0
            for j in m_arPos:
                if (j>=self.finger[i].start[0]):
                    self.finger[i].node.append(j)
                    k = 1
                    break
            if (k == 0):
                self.finger[i].node.append(m_arPos[0])



class ChordArray():
    #Класс, реализующий функции
    def __init__(self, M_intN, m_arPos):
        self.m = M_intN
        self.arPos = m_arPos
        self.myArray = []

    def initial_massiv(self):
        # Пустой массив объектов
        for i in self.arPos:
            self.myArray.append(ChordNode(self.m, self.arPos, i))

    # return closest finger preceding id
    def closest_preceding_finger(self,m_arPos,id_n, id):
        for i in reversed(range(self.m - 1)):
            if (id>=m_arPos[id_n]):
                if (self.myArray[id_n].finger[i].node[0] <= id)and(self.myArray[id_n].finger[i].node[0] > m_arPos[id_n]):
                    for j in range(len(self.arPos)):
                        if (self.myArray[id_n].finger[i].node[0]==self.arPos[j]):
                            idx = j
                            return idx #self.myArray[idx],
            else:
                right = 2** (self.m-1)
                left = 0
                if (self.myArray[id_n].finger[i].node[0] >= left) and (self.myArray[id_n].finger[i].node[0] < right):
                    for j in range(len(self.arPos)):
                        if (self.myArray[id_n].finger[i].node[0] == self.arPos[j]):
                            idx = j
                            return idx
        return id_n #self.myArray[id_n]

    def find_predecessor(self,m_arPos,id_n,id):
        n_ = copy.deepcopy(self.myArray[id_n])
        """
        if (self.myArray[id_n].finger[0].node[0]>=m_arPos[id_n]):
            left=m_arPos[id_n]
            right = self.myArray[id_n].finger[0].node[0]
        else:
            left = self.myArray[id_n].finger[0].node[0]
            right = m_arPos[id_n]
        """
        left = m_arPos[id_n]
        right = self.myArray[id_n].finger[0].node[0]
        if (self.myArray[id_n].finger[0].node[0]==0):
            right = 2** (self.m-1)
        while (id<left)or(id>right):
            id_n=self.closest_preceding_finger(m_arPos,id_n,id)
            n_ = copy.deepcopy(self.myArray[id_n])
            """
            if (self.myArray[id_n].finger[0].node[0] >= m_arPos[id_n]):
                left = m_arPos[id_n]
                right = self.myArray[id_n].finger[0].node[0]
            else:
                left = self.myArray[id_n].finger[0].node[0]
                right = m_arPos[id_n]
            left = m_arPos[id_n]
            """
            left = m_arPos[id_n]
            right = self.myArray[id_n].finger[0].node[0]
            if (self.myArray[id_n].finger[0].node[0] == 0):
                right = 2 ** (self.m - 1)
        return n_

    def find_successor(self,m_arPos,id_n,id):
        n_ = self.find_predecessor(m_arPos,id_n,id)
        return n_.finger[0].node[0]

    #Методы для добавления узла в систему
    def init_finger_table(self,id_n):
        self.arPos.append(id_n)
        num = len(self.arPos)
        self.myArray.append(ChordNode(self.m, self.arPos, self.arPos[num-1]))

        print('Таблица finger для добавленного узла с id', str(self.arPos[num-1]))
        for k in self.myArray[num-1].finger:
            print('start: ' + str(k.start[0]) + '; interval: [' + str(k.interval[0]) + ','
                  + str(k.interval[1]) + '); node: ' + str(k.node[0]))

        # Поиск ближайшего узла с id finger[0].start
        t = np.array(self.arPos)
        r = self.myArray[num-1].finger[0].start[0]
        id_start = np.argmin(abs(np.array(self.arPos)-self.myArray[num-1].finger[0].start[0]))
        self.myArray[num-1].finger[0].node[0] = self.find_successor(self.arPos,id_start,id_n)


    #Метод обновления других узлов
    def update_others(self, pos_new_id):
        for i in range(self.m-1):
            print('Поиск для обновления в цикле по i=', str(i))
            #Поиск последнего узла p, чей i-й finger может быть n
            t = self.arPos[pos_new_id]-2 ** (i)
            if (t<0):
                t = 2 ** (self.m - 1) + t
            p = self.find_predecessor(self.arPos,pos_new_id,t)
            print('Результат функции find_predecessor ', str(p.finger[self.m-2].interval[1]))
            k=0
            for j in self.arPos:
                if (p.finger[self.m-2].interval[1] == j):
                    pos_new_id_ = k
                k += 1
            self.update_finger_table(self.arPos,pos_new_id_,self.arPos[pos_new_id],i)

    # Обновление конкретной finger
    def update_finger_table(self,m_arPos,id_n,s,i):
        left = m_arPos[id_n]
        right = self.myArray[id_n].finger[i].node[0]
        if (self.myArray[id_n].finger[i].node[0] == 0):
            right = 2 ** (self.m - 1)
        if (s >= left) and (s < right):
            self.myArray[id_n].finger[i].node[0] = s
            print('Обновлен node в узле ' + str(m_arPos[id_n])+ '; finger номер ' + str(m_arPos[i]))
            r1 = self.find_predecessor(m_arPos, id_n, m_arPos[id_n])
            k = 0
            for j in self.arPos:
                if (r1.finger[self.m-2].interval[1] == j):
                    pos_new_id1 = k
                k += 1
            #if (pos_new_id1>0):
            #    pos_new_id1=pos_new_id1-1
            self.update_finger_table(m_arPos,pos_new_id1,s,i)
            #Добавление для обновления крайнего узла
            if i == self.m-2:
                pos_new_id1 = pos_new_id1 - 1
                self.update_finger_table(m_arPos, pos_new_id1, s, i)

    #Метод добавления узла в систему
    def join(self, id_n):
        if len(self.arPos)>0:
            self.init_finger_table(id_n)
            k = 0
            for j in self.arPos:
                if (id_n == j):
                    pos_new_id = k
                k += 1

            self.update_others(pos_new_id)
        else:
            self.init_finger_table(id_n)

    # Метод обновления других узлов
    def update_others_del(self, pos_new_id, succeccor_id):
        for i in range(self.m - 1):
            print('Поиск для обновления в цикле по i=', str(i))
            # Поиск последнего узла p, чей i-й finger может быть n
            t = self.arPos[pos_new_id] - 2 ** (i)
            if (t<0):
                t = 2 ** (self.m - 1) + t
            p = self.find_predecessor(self.arPos, pos_new_id, t)
            print('Результат функции find_predecessor ', str(p.finger[self.m-2].interval[1]))
            k = 0
            for j in self.arPos:
                if (p.finger[self.m-2].interval[1] == j):
                    pos_new_id_ = k
                k += 1
            for j in range(self.m - 1):
                self.update_finger_table_del(self.arPos, pos_new_id_, self.arPos[pos_new_id], succeccor_id, j)

    # Обновление конкретной finger
    def update_finger_table_del(self, m_arPos, id_n, s, succeccor_id, i):
        left = m_arPos[id_n]
        right = self.myArray[id_n].finger[i].node[0]
        if (self.myArray[id_n].finger[i].node[0] == 0):
            right = 2 ** (self.m - 1)
        if (self.myArray[id_n].finger[i].node[0] == s):
            self.myArray[id_n].finger[i].node[0] = succeccor_id
            print('Обновлен node в узле ' + str(m_arPos[id_n]) + '; finger номер ' + str(m_arPos[i]))
            r1 = self.find_predecessor(m_arPos, id_n, m_arPos[id_n])
            k = 0
            for j in self.arPos:
                if (r1.finger[self.m-2].interval[1] == j):
                    pos_new_id1 = k
                k += 1
            self.update_finger_table_del(m_arPos, pos_new_id1, s,succeccor_id, i)
            # Добавление для обновления крайнего узла
            #if i == self.m - 2:
            pos_new_id1 = pos_new_id1 - 1
            if (pos_new_id1>0):
                pos_new_id1 = pos_new_id1 - 1
            else:
                pos_new_id1 = len(m_arPos) - 1
            self.update_finger_table_del(m_arPos, pos_new_id1, s,succeccor_id, i)

    # Метод удаление узла из системы
    def remove_node(self, id_n):
        k = 0
        for j in self.arPos:
            if (id_n == j):
                pos_del = k
            k += 1
        #ID следующего узла
        succeccor_id = self.find_successor(self.arPos, pos_del, id_n)

        k = 0
        for j in self.arPos:
            if (succeccor_id == j):
                pos_new_id = k
            k += 1
        # Обновление данных об узлах
        self.update_others_del(pos_del, succeccor_id)

        # Собственно удаление узла
        del self.arPos[pos_del]
        num = len(self.arPos)
        del self.myArray[pos_del]





