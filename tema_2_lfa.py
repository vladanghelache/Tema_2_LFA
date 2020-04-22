f1 = open('lambda_nfa.in')
f2 = open('nfa.in')
f3 = open('dfa.in')
def citire_nfa(f):
    n = int(f.readline())
    lista_stari=[x for x in range(n)]
    m = int(f.readline())
    alfabet = []
    for x in f.readline().split():
        alfabet += x
    q0 = int(f.readline())
    k = int(f.readline())
    stari_finale = []
    for x in f.readline().split():
        stari_finale += [int(x)]
    I = int(f.readline())
    d = {}
    for i in range(I):
        x = f.readline().split()
        if (int(x[0]),x[1]) not in d.keys():
            d[(int(x[0]),x[1])] = {int(x[2])}
        else:
            d[(int(x[0]), x[1])].add(int(x[2]))
    f.close()
    return n,lista_stari,m,alfabet,q0,k,stari_finale,I,d
def citire_dfa(f):
    n = int(f.readline())
    lista_stari=[x for x in range(n)]
    m = int(f.readline())
    alfabet = []
    for x in f.readline().split():
        alfabet += x
    q0 = int(f.readline())
    k = int(f.readline())
    stari_finale = []
    for x in f.readline().split():
        stari_finale += [int(x)]
    I = int(f.readline())
    d = {}
    for i in range(I):
        x = f.readline().split()
        d[(int(x[0]),x[1])] = int(x[2])
    f.close()
    return n, lista_stari, m, alfabet, q0, k, stari_finale, I, d

def l_inchidere(start,stare,dictionar,d):
    if start not in dictionar.keys():
        dictionar[start]={start}
    if (stare,'$') in d.keys():
        for x  in d[(stare,'$')]:
            dictionar[start].add(x)
            l_inchidere(start,x,dictionar,d)

def tranzitie_delta_star(stare,litera,dictionar,d_nfa,d):
    for x in dictionar[stare]:
        if (x, litera) in d.keys():
            for i in d[(x, litera)]:
                if (stare, litera) in d_nfa.keys():
                    d_nfa[(stare, litera)].update(dictionar[i])
                else:
                    d_nfa[(stare, litera)] = dictionar[i].copy()

def inlocuire(x,y,dictionar):           #il inlocuieste pe y cu x in dictionar
    for multime in dictionar.values():
        if y in multime:
            multime.discard(y)
            if x not in multime:
                multime.add(x)
def to_nfa(d,nr_stari,lista_stari,stare_initiala,stari_finale, alfabet):

    #pasul 1.1
    dictionar_inchideri={}        #lambda-inchideri
    for stare in lista_stari:
        l_inchidere(stare,stare,dictionar_inchideri,d)

    #pasul 1.2
    d_nfa={}
    for stare in lista_stari:
        for litera in alfabet:
            tranzitie_delta_star(stare,litera,dictionar_inchideri,d_nfa,d)

    #pasul 1.3
    stari_finale_noi=stari_finale.copy()
    for stare in lista_stari:
        for x in stari_finale:
            if stare not in stari_finale_noi and x in dictionar_inchideri[stare]:
                stari_finale_noi+=[stare]

    #pasul 1.4
    i=0
    while i< nr_stari:
        j=i+1
        while j < nr_stari:
            ok=True
            for litera in alfabet:
                if (lista_stari[i],litera) in d_nfa.keys() and (lista_stari[j],litera) in d_nfa.keys() and d_nfa[(lista_stari[i],litera)]!=d_nfa[(lista_stari[j],litera)]:
                    ok=False        #daca starile nu au aceleasi tranzitii, atunci nu sunt identice
            if (lista_stari[j] not in stari_finale_noi and lista_stari[i] in stari_finale_noi) or (lista_stari[j] in stari_finale_noi and lista_stari[i] not in stari_finale_noi):
                ok=False        #daca una dinre stari e stare finala iar cealalta nu, atunci starile nu sunt identice
            if ok==True:
                inlocuire(lista_stari[i], lista_stari[j], d_nfa) #se inlocuieste starea de pe j cu starea de pe i  in dictionarul d_nfa
                if lista_stari[j] in stari_finale_noi:
                    stari_finale_noi.remove(lista_stari[j])     #se sterge din lista de stari finale, daca e stare finala

                for lit in alfabet:
                    if (lista_stari[j],lit) in d_nfa.keys():
                        d_nfa.pop((lista_stari[j],lit))     #se sterg legaturile cu celelalte stari
                lista_stari.pop(j)      #se sterge starea
                j-=1
                nr_stari-=1
            j+=1
        i+=1
    return d_nfa, nr_stari, lista_stari, stare_initiala, stari_finale_noi, alfabet

def to_dfa(d,nr_stari,lista_stari,stare_initiala,stari_finale,alfabet):

    #pasul 2.1
    coada=[{stare_initiala}]
    lista_stari_noi=[{stare_initiala}]
    d_dfa={}
    while coada != []:
        for litera in alfabet:
            q = set()
            for x in coada[0]:
                if(x,litera)in d.keys():
                    q.update(d[x,litera])
            if q!=set():
                if q not in lista_stari_noi:
                    lista_stari_noi+=[q]
                    coada+=[q]
                d_dfa[(frozenset(coada[0]),litera)]=q
        coada.pop(0)

    #pasul 2.2
    stari_finale_noi=[]
    for stare in lista_stari_noi:
        for x in stari_finale:
            if x in stare and stare not in stari_finale_noi:
                stari_finale_noi+=[stare]

    #pasul 2.3--redenumirea starilor
    #fiecare stare va lua denumirea indexului pe care se afla in "lista_stari_noi"
    stare_initiala=0
    for i in range(len(lista_stari_noi)):
        #se redenumeste starea in dictionarul "d_dfa":
        for x in d_dfa.keys():
            if lista_stari_noi[i]==d_dfa[x]:
                d_dfa[x]=i
        for litera in alfabet:
            if (frozenset(lista_stari_noi[i]),litera) in d_dfa.keys():
              d_dfa[(i,litera)]=d_dfa[(frozenset(lista_stari_noi[i]),litera)]
              del d_dfa[(frozenset(lista_stari_noi[i]),litera)]
        #se redenumeste starea in "stari_finale_noi":
        if lista_stari_noi[i] in stari_finale_noi:
            stari_finale_noi.remove(lista_stari_noi[i])
            stari_finale_noi.append(i)
        #se redenumeste starea in "lista_stari_noi":
        print("den veche: ",lista_stari_noi[i]," / den noua: ",i)
        lista_stari_noi[i]=i
    nr_stari=len(lista_stari_noi)
    return d_dfa, nr_stari, lista_stari_noi, stare_initiala, stari_finale_noi, alfabet


def functie_parcurgere(stare,stari_finale_noi,alfabet,d,verif):#trece prin toate starile acesibile pana cand ajunge intr-o stare finala sau pana cand nu mai sunt stari nevizitate
        global o
        if stare not in verif:
            verif.append(stare)
            if set(stare) in stari_finale_noi:
                o = True
            else:
                for litera in alfabet:
                    if (stare,litera) in d.keys():
                        functie_parcurgere(d[(stare,litera)],stari_finale_noi,alfabet,d,verif)


def functie_parcurgere_automat(stare, alfabet, d, verif):#trece prin toate starile accesibile
    if stare not in verif:
        verif.append(stare)
        for litera in alfabet:
            if (stare, litera) in d.keys():
                functie_parcurgere_automat(d[(stare, litera)], alfabet, d, verif)

def sterge(stare,d,lista_stari,alfabet):
    for litera in alfabet:
        if (stare,litera)in d.keys():
            del d[stare,litera]
        for s in lista_stari:
            if (tuple(s), litera) in d.keys() and d[tuple(s),litera]==stare:
                del d[tuple(s),litera]
    lista_stari.remove(set(stare))
def to_dfa_min(d,nr_stari,lista_stari,stare_initiala,stari_finale,alfabet):

    #pasul 3.1: --determinarea starilor echivalente
    d_ech={}
    for i in range(nr_stari):
        for j in range(i+1):
            d_ech[i,j]=True

    for x in d_ech.keys():
        if (x[0] in stari_finale and x[1] not in stari_finale) or (x[0] not in stari_finale and x[1] in stari_finale):
            d_ech[x]=False

    ok=1
    while(ok):
        d_copy=d_ech.copy()
        for litera in alfabet:
            for x in d_ech.keys():
                if d_ech[max(d[x[0], litera], d[x[1], litera]), min(d[x[0], litera], d[x[1], litera])]==False:
                    d_ech[x]=False
        if d_copy==d_ech:
            ok=0


    #pasul 3.2
    stari_ech=[]
    for i in range(nr_stari):
        ok=0
        for j in range(i):
            if d_ech[i,j]==True:
                for multime in stari_ech:
                    if j in multime:
                        multime.add(i)
                        break
                ok=1
                break
        if ok==0:
            stari_ech += [{i}]

    d_dfa_min={}
    for multime in stari_ech:
        t=tuple(multime)
        for x in t:
            for litera in alfabet:
                if (x,litera) in d.keys():
                    for m in stari_ech:
                        if d[x,litera] in m:
                            d_dfa_min[t,litera]=tuple(m)
                            break

    #pasul 3.3
    stare_initiala_noua={}
    for multime in stari_ech:
        if stare_initiala in multime:
            stare_initiala_noua = multime
            break

    stari_finale_noi=[]
    for stare in stari_finale:
        for multime in stari_ech:
            if stare in multime and multime not in stari_finale_noi:
                stari_finale_noi.append(multime)
                break

    #pasul 3.4-- Eliminarea starilor dead-end
    for stare in stari_ech:
        stare=tuple(stare)
        global o
        o = False
        verif=[]
        functie_parcurgere(stare,stari_finale_noi,alfabet,d_dfa_min,verif)
        if o==False:
            sterge(stare,d_dfa_min,stari_ech,alfabet)

    #pasul 3.5-- Eliminarea starilor neaccesibile
    verif=[]
    functie_parcurgere_automat(tuple(stare_initiala_noua),alfabet,d_dfa_min,verif)

    for stare in stari_ech:
        if tuple(stare) not in verif:
            sterge(tuple(stare),d_dfa_min,stari_ech,alfabet)

    #pasul 3.6--redenumirea starilor
    #fiecare stare va lua denumirea indexului pe care se afla in "stari_ech"
    stare_initiala=0
    for stare in stari_ech:
        if stare==stare_initiala_noua:
            aux=stari_ech[0]
            stari_ech[0]=stare
            stare=aux
    for i in range(len(stari_ech)):
        #se redenumeste starea in dictionarul "d_dfa_min":
        for x in d_dfa_min.keys():
            if tuple(stari_ech[i])==d_dfa_min[x]:
                d_dfa_min[x]=i
        for litera in alfabet:
            if (tuple(stari_ech[i]),litera) in d_dfa_min.keys():
              d_dfa_min[(i,litera)]=d_dfa_min[(tuple(stari_ech[i]),litera)]
              del d_dfa_min[(tuple(stari_ech[i]),litera)]
        #se redenumeste starea in "stari_finale_noi":
        if stari_ech[i] in stari_finale_noi:
            stari_finale_noi.remove(stari_ech[i])
            stari_finale_noi.append(i)
        #se redenumeste starea in "stari_ech":
        print("den veche: ",stari_ech[i]," / den noua: ",i)
        stari_ech[i]=i
    nr_stari=len(stari_ech)
    return d_dfa_min, nr_stari, stari_ech, stare_initiala, stari_finale_noi, alfabet


print('NFA:')
n, lista_stari, m, alfabet, q0, k, stari_finale, I, d=citire_nfa(f1)
d_nfa,nr_stari,lista_stari,stare_initiala, stari_finale, alfabet=to_nfa(d,n,lista_stari,q0,stari_finale,alfabet)
print('tranzitii: ',d_nfa)
print('nr de stari: ',nr_stari)
print('lista stari: ',lista_stari)
print('stare initiala: ',stare_initiala)
print('stari finale: ',stari_finale)
print('alfabet: ',alfabet)

print('DFA:')
n, lista_stari, m, alfabet, q0, k, stari_finale, I, d=citire_nfa(f2)
d_dfa, nr_stari, lista_stari, stare_initiala, stari_finale, alfabet=to_dfa(d,n,lista_stari,q0,stari_finale,alfabet)
print('tranzitii: ',d_dfa)
print('nr de stari: ',nr_stari)
print('lista stari: ',lista_stari)
print('stare initiala: ',stare_initiala)
print('stari finale: ',stari_finale)
print('alfabet: ',alfabet)

print('DFA minim:')
n, lista_stari, m, alfabet, q0, k, stari_finale, I, d=citire_dfa(f3)
d_dfa_min, nr_stari, lista_stari, stare_initiala, stari_finale, alfabet=to_dfa_min(d,n,lista_stari,q0,stari_finale,alfabet)
print('tranzitii: ',d_dfa_min)
print('nr de stari: ',nr_stari)
print('lista stari: ',lista_stari)
print('stare initiala: ',stare_initiala)
print('stari finale: ',stari_finale)
print('alfabet: ',alfabet)