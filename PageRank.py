
import math

G4 = r'G4.txt'
G3 = r'G3.txt'
G1 = r'G1.txt'
G2 = r'G2.txt'
sinks = []
Map_OLC = {}
Map = {}
Map_list = []

N1 = 1000
N2 = 183811
N3 = 6
d = 0.85

# create an outlink map, return sink(no out link page)
def outLinkHelper(graph, MapList):
    n = 0
    for each in MapList:
        Map_OLC[each] = 0
    tmp = open(graph, 'r')
    lines = tmp.read().splitlines()
    for line in lines:
        tmp = line.split(' ')
        if len(tmp) == 1:
            continue
        tmp.pop()
        tmp.pop(0)
        list = []
        while len(tmp) != 0:
            node = tmp.pop(0)
            if node not in list:
                list.append(node)
                Map_OLC[node] += 1
    for sink in MapList:
       if Map_OLC[sink] == 0:
           sinks.append(sink)
           n += 1
    return n

# return inlink map
def inLinkHelper(Map):
    Map_ILC ={}
    for item in Map:
            Map_ILC[item] = len(Map.get(item))

    return Map_ILC

# return source(no inlink page)
def sourceHelper(Map):
    n = 0
    Map_ILC ={}
    for item in Map:
        Map_ILC[item] = len(Map.get(item))
        if Map_ILC[item] == 0:
            n += 1
    return n

# statistic for source and sink proportion
def statistic(m,n,N,name):
    fx = open(name + r'-statistic.txt', 'w')
    fx.write('In G1: \n')
    fx.write('total = ' + str(N) + '\n')
    fx.write('Num_source = ' + str(m) + '   ' + 'Num_sink = ' + str(n) + '\n')
    fx.write('Pro(source) = '+  str(m/N) + '    ' + 'Pro(sink) = ' +str(n/N) + '\n')
    fx.close()


# calculate perplexity
def Perplexity(PR, list):
        hpr = 0
        for page in list:
            hpr = hpr + (PR[page] * math.log2(PR[page]))
        HPR = -1 * hpr
        lastPer = math.pow(2, HPR)
        return lastPer



# fetch Map from text file
def ReadMap(graph):
    tmp = open(graph, 'r')
    lines = tmp.read().splitlines()
    for line in lines:
        tmp = line.split(' ')
        if len(tmp) == 1:
            dangling = tmp.pop()
            Map_list.append(dangling)
            Map[dangling] = []
            continue
        tmp.pop()
        vertex = tmp.pop(0)
        list = []
        while len(tmp) != 0:
            node = tmp.pop(0)
            if node not in list:
                list.append(node)
        Map_list.append(vertex)
        Map[vertex] = list
    print("ReadMap end")



# print Map
def printMap(Map):
    for vertex in Map:
        print(vertex + ': ' + str(Map.get(vertex)))

# write Map into a txt file
def writeMap(name,Map):
    file_loc = name + r'.txt'
    fx = open(file_loc, "w")
    for vertex in Map:
        fx.write(vertex + ' ' + str(Map.get(vertex)) + '\n')
    fx.close()



# calculate score for each page in the Map
def Ranking(MapList, N, name):
    PR = {}
    newPR = {}

    file_list = MapList
    for file in file_list:
        PR[file] = 1/N

    count = 0
    round = 0
    lastPer = 0
    fx = open(name + r'-pp-each-round.txt', 'w')
    while (1):
        fx.write('Round: ' + str(round) + ' ' + 'Consecutive time: ' + str(count) + '\n')
        fx.write('Perplexity: ' + str(lastPer) + '\n\n')
        round += 1
        if (count == 4):
            return PR
        if abs(Perplexity(PR,file_list) - lastPer) < 1:
            count = count + 1
        if abs(Perplexity(PR,file_list) - lastPer) >= 1 and count > 0:
            count = count - 1
        sinkPR = 0
        lastPer = Perplexity(PR, file_list)
        for sink in sinks:
            sinkPR += PR[sink]
        for page in file_list:
            newPR[page] = (1 - d)/N
            newPR[page] += d * sinkPR/N
            for q in Map[page]:
                if q not in file_list:
                    continue
                newPR[page] += d * PR[q] / Map_OLC[q]
            PR[page] = newPR[page]
    fx.close()
    # printMap(PR)
    # print(count)

# sorting map in incremental sequence
def sorting(Map,name):
    tmp = Map
    list = (sorted(tmp.items(),key = lambda d:d[1], reverse = True))
    fx = open(name + r'.txt','w')
    i = 0
    for item in list:
        if i < 50:
            i += 1
            fx.write('Rank '+ str(i) + ':' + str(item) + '\n')
    fx.close()


# output hw assignment
def main(graph, Map, MapList, N, name):
    ReadMap(graph)
    sink = outLinkHelper(graph, MapList)
    PR = Ranking(Map, N, name)
    ILC = inLinkHelper(Map)
    sorting(PR,name + '-PR')
    #writeMap(name + '-PR', PR)
    sorting(ILC,name + '-ILC')
    #writeMap(name + '-ILC', ILC)
    source = sourceHelper(Map)
    statistic(source, sink, N, name)

# avoid running main(G1) and main(G2) at the same time to avoid ZaroDevidedException()
main(G1,Map,Map_list,N1,'G1')
# main(G1,Map,Map_list,N1,'G1')

