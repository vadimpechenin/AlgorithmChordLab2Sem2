"""
Лабораторная работа №2. Алгоритм Chord. Реализация массива объектов
"""
M_intM = 4 # количество бит, используемых для генерации идентификаторов
m_arPos = [0, 1, 3] #Идентификаторы позциций, в которых находятся узлы

from ChordNode import ChordArray

#Задание начального состояния сети
ChordArray1 = ChordArray(M_intM, m_arPos)
ChordArray1.initial_massiv()

#Отображение начального состояния
j=0
print('Изначально даны узлы ', str(m_arPos))
print('')
for i in ChordArray1.myArray:
    print('Таблица finger для узла с id', str(m_arPos[j]))
    for k in i.finger:
        print('start: ' + str(k.start[0]) +  '; interval: [' + str(k.interval[0]) + ','
              + str(k.interval[1]) + '); node: ' + str(k.node[0]))
    j += 1

#myArray = [] #Пустой массив объектов
#for i in m_arPos:
#    myArray.append(ChordNode(M_intM, m_arPos, i))

#Проверка функций поиска узла
id=5
id_0 = 1
print(' ')
print('1. Требуется вывести узел с id = ',str(id))
print('Стоим на узле с id = ', str(m_arPos[id_0]))
r0 = ChordArray1.closest_preceding_finger(m_arPos,id_0,id)
print('Результат функции closest_preceding_finger ', str(r0))
r1 = ChordArray1.find_predecessor(m_arPos,id_0,id)
print('Результат функции find_predecessor ', str(r1.finger[2].interval[1]))
r2 = ChordArray1.find_successor(m_arPos,id_0,id)
print('Результат функции find_successor ', str(r2))

print(' ')

new_id = 6
print('2. Добавление узла с id ', str(new_id))
ChordArray1.join(new_id)

print(' ')
print('Отображение состояния после добавления узла')
j=0
for i in ChordArray1.myArray:
    print('Таблица finger для узла с id', str(m_arPos[j]))
    for k in i.finger:
        print('start: ' + str(k.start[0]) +  '; interval: [' + str(k.interval[0]) + ','
              + str(k.interval[1]) + '); node: ' + str(k.node[0]))
    j += 1

del_id = 3
print(' ')
print('3. Удаление узла с id ', str(del_id))
ChordArray1.remove_node(del_id)
print(' ')
print('Отображение состояния после удаления узла')
j=0
for i in ChordArray1.myArray:
    print('Таблица finger для узла с id', str(m_arPos[j]))
    for k in i.finger:
        print('start: ' + str(k.start[0]) +  '; interval: [' + str(k.interval[0]) + ','
              + str(k.interval[1]) + '); node: ' + str(k.node[0]))
    j += 1

g = 0