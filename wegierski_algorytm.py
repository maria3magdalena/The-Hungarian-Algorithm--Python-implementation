# -*- coding: utf-8 -*-


import numpy as np
import copy

print('Podaj wymiar macierzy:')
d = input()
n = int(d)
matrix = []
print('Podaj kolejne elementy macierzy idac wzdluz wierszy: ')
for i in range(n):
    r = []
    for j in range(n):
        r.append(int(input()))
    matrix.append(r)
  

def wegierski(matrix):

  W = copy.deepcopy(matrix)
  n = len(matrix)
  max_skojarzenie = 0
  xlabels = np.zeros(n, np.int)
  ylabels = np.zeros(n, np.int)
  xy = -np.ones(n, np.int)    # gdzie xy[x] to wierzcholek (z Y) polaczony z x
  yx = -np.ones(n, np.int)    # gdzie yx[y] to wierzcholek (z X) polaczony z y
  slack = np.zeros(n, np.int) 
  slackx = np.zeros(n, np.int)   # gdzie slackx[y] = wierzcholek taki, ze xlabels[slackx[y]] + ylabels[y] - W(slackx[y],y) = slack[y]

  
  
# Ten krok teoretycznie mozna pominac, ale zmniejsza on nam liczbe potrzebnych iteracji:
  
  for i in range(n):
        w= W[i][0]
        for j in range(n):
            if W[i][j] < w:
                w = W[i][j]
        for j in range(n):
            W[i][j] = W[i][j] - w
            
  for j in range(n):
        w= W[0][j]
        for i in range(n):
            if W[i][j] < w:
                w = W[i][j]
        for i in range(n):
            W[i][j] = W[i][j] - w
            
# Inicjalizujemy etykiety:
  for x in range(n):
        for y in range(n):
            xlabels[x] = max( xlabels[x], W[x][y])
            

 ## Zasadnicza czesc naszego algorytmu #######################################          
  
  while max_skojarzenie < n:
      
    S = np.zeros(n, np.bool) #zbiory S i T z algorytmu
    T = np.zeros(n, np.bool)
    prev = -np.ones(n, np.int) #tablica do zapamietywania alternujacych sciezek
      
    Queue = []  #kolejka dla BFS
    root = -1
    st = 0

    for x in range(n):
       if xy[x] == -1:
             Queue.append(x)
             root = x
             prev[x] = -2
             S[x] = True
             break
     
    for y in range(n):
          slack[int(y)] = xlabels[root] + ylabels[y] - W[root][y]
          slackx[y] = root
      
    while True:
      
      while st < len(Queue):
        
          x = Queue[st]  #Aktualny wierzcholek ze zbioru X
          st = st+ 1
            
          for y in range(n): #iterujemy po wszystkich krawedziach w Grafie rownosci ("equality graph")
                               # Graf rownosci grafu G: G'(V, E') gdzie E' = {(x,y): l(x) + l(y) =w(x,y)}
             if W[x][y] == (xlabels[x] + ylabels[y]) and not(T[y]):
                 if yx[y] == -1:  
                     break   # zostal znaleziony wolny wierzcholek w Y, 
                                  # wiec sciezka powiekszajaca istnieje
                 T[y] = True # wpp dodajemy y do zbioru T
                 Queue.append(yx[y]) #dodajemy do kolejki wierz. yx[y], ktory jest polaczony z y
                 S, prev, slack, slackx, xlabels, ylabels = dodaj_do_drzewa(yx[y], x, S, xlabels, ylabels, slack, slackx, prev, W)  
                 #dodajemy krawedzie (x,y) oraz (y, xy[y]) do drzewa
                      
          if y<n:
                break   #sciezka powiekszajaca znaleziona!
          
          
     
               
      #nie znaleziono sciezki powiekszajacej, wiec poprawiamy etykiety
      xlabels, ylabels, T, S, slack = aktualizuj_etykiety(xlabels, ylabels, T, S, slack)
                 
      Queue, st = [], 0
      for y in range(n):  #dodajemy krawedzie, ktore zostaly dodane do grafu rownosci w wyniku poprawiania etykiet
          if not(T[y]) and slack[y]==0:
                if yx[y]== -1:    # wolny wierzcholek w Y znaleiony - sciezka powiekszajaca istnieje!
                    x = slackx[y]
                    break
                else:
                     T[y]= True  # wpp. dodajemy y do T
                     if not(S[yx[int(y)]]):
                        Queue.append(yx[y])   #dodajemy wierz. yx[y] do kolejki
                        S, prev, slack, slackx, xlabels, ylabels = dodaj_do_drzewa(yx[y], slackx[y], S, xlabels, ylabels, slack, slackx, prev, W)
                        #dodajemy krawedzie (y,x) oraz (y, yx[y]) do drzewa
      if y<n:
             break
      
    if y<n: #scieka powiekszajaca znaleziona!
          
       max_skojarzenie = max_skojarzenie + 1
       while x != -2:
          yx[int(y)] = x
          ty = xy[x]
          xy[x] = y
          x, y = prev[x], ty
        
      
###############################################################################


      
  suma = 0
  for x in range(n):
            
      print('przypodrzadkuj {} do {}, z waga {:f}'.format(x, xy[x], matrix[x][xy[x]]))
      suma = suma + matrix[x][xy[x]]
        
  print('Suma: {}'.format(suma))    
  return suma



 


def aktualizuj_etykiety(xlabels, ylabels, T, S, slack):
    
# Poniewaz slack[y] = min(l(x) + l(y) - W(x,y)) dla x\in S
# Pozostaje wiec wyliczyc Delta:= min slack[y]
          
 Delta = 2^32  #nieskonczonosc
 
 for y in range(n):
     if not(T[y]):
         Delta = min(Delta, slack[y])
  
 for x in range(n):
     if S[x]:
         xlabels[x] = xlabels[x] - Delta
        
 for y in range(n):
     if T[y]:
         ylabels[y] = ylabels[y] + Delta
         
 for y in range(n):
     if not(T[y]):
         slack[y] = slack[y] - Delta
         
 return xlabels, ylabels, T, S, slack
         
         
def dodaj_do_drzewa(x, prevx, S, xlabels, ylabels, slack, slackx, prev, W):
# x - aktualny wierzcholek, 
# prevx -  wierzcholek z X znajdujacy sie przed x w sciezce alternujacej
# tak wiec dodajemy krawedzie (prevx, xy[x]), (xy[x], x)
    
  S[x] = True  #Dodajemy x do zbioru S
  prev[x] = prevx 
  
  for y in range(n):  #aktualizujemy slacks, poniewaz dodalismy nowy wierzcholek do S
      if xlabels[x] + ylabels[y] - W[x][y] < slack[y]:

         slack[y] = xlabels[x] + ylabels[y] - W[x][y];
         slackx[y] = x
         
  return S, prev, slack, slackx, xlabels, ylabels


wegierski(matrix)
  
  
  