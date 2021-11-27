import copy
import json
import time

""" definirea problemei """
class Nod:
        def __init__(self, info, h):
                self.info=info
                self.h=h
                
        def __str__ (self):
                sir="["
                (a,b)=self.info[0]
                sir+="inc("+a+","+str(b)+")"
                for i in range(1,len(self.info)):
                        (a,b)=self.info[i]
                        sir+=", inc("+a+","+str(b)+")"
                sir+="]"
                return sir
        def __repr__ (self):
                return "("+json.dumps(self.info)

        #prima euristica admisibila
        #cauta incuietoarea care a fost de cele mai multe ori inchisa - n
        #deoarece fiecare cheie poate descuia cel mult o singura data orice incuietoare, chiar si daca am avea cheia ideala care deschide orice incuietoare
        #tot ar trebui folosita de n ori, aceasta fiind situatia in care se genereaza costul minim indiferent de nod
        #orice euristica ce poate genera valori mai mari decat aceasta pentru un anumit nod nu mai respecta conditia de admisibilitate
        def calculeaza_h1(self):
                s = 0
                for (x,y) in self.info:
                        if x == 'i':
                                if y > s:
                                        s = y
                self.h = s
                #print(self.h)
        #a doua euristica admisibila
        #cauta incuietoarea care a fost de cele mai putine ori inchisa(cel putin o singura data) - n
        #respecta acelasi principiu ca mai sus, dar are un timp de executie mult mai mare
        def calculeaza_h2(self):
                s = 10000
                for (x,y) in self.info:
                        if x == 'i':
                                if y < s:
                                        s = y
                if s==10000:
                        s=1
                self.h = s
                #print(s)
                
                
        #Urmatoarele euristici nu se respecta conditia de admisibilitate din motivul descris mai sus

        #insumeaza de cate ori a fost incuiata fiecare incuietoare
        def calculeaza_h4(self):
                s = 0
                for (x,y) in self.info:
                        if x == 'i':
                                s += y
                self.h = s
                #print(self.h)
        #numara cate incuietori sunt inchise
        def calculeaza_h3(self):
                s = 0
                for (x,y) in self.info:
                        if x == 'i':
                                s += 1
                self.h = s
                #print(self.h)

class Arc:
        def __init__(self, capat, varf, cost):
                self.capat = capat
                self.varf = varf
                self.cost = cost
                
class Problema:
        def __init__(self, lista_chei):
                self.lungime = len(lista_chei[0])
                self.chei = copy.deepcopy(lista_chei)

                self.noduri = [
                        Nod([('i',1) for i in range(self.lungime)], float('inf')),
                        Nod([('d',0) for i in range(self.lungime)], 0)
                ]

                self.nod_start = self.noduri[0]
                self.nod_scop = self.noduri[1].info
                                


                
        def cauta_nod_nume(self, info):
                for nod in self.noduri:
                        if nod.info==info:
                                return nod
                return None
                

                
""" Sfarsit definire problema """       


                        
""" Clase folosite in algoritmul A* """
                
class NodParcurgere:
        """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
                Cuprinde o referinta catre nodul in sine (din graf)
                dar are ca proprietati si valorile specifice algoritmului A* (f si g). 
                Se presupune ca h este proprietate a nodului din graf
        
        """
        problema=None
        def __init__(self, nod_graf ,cheie = "", succesori=[], parinte=None, g=0, f=None):
                self.nod_graf=nod_graf
                self.succesori = succesori
                self.parinte = parinte
                self.g=g
                self.cheie=cheie
                if f is None :
                        self.f=self.g+self.nod_graf.h
                else:
                        self.f=f
                
        def drum_arbore(self):
                """
                        Functie care calculeaza drumul asociat unui nod din arborele de cautare.
                        Functia merge din parinte in parinte pana ajunge la radacina
                """
                '''nod_c=self
                drum=[nod_c]
                while nod_c.parinte is not None :
                        drum=[nod_c.parinte]+drum
                        nod_c= nod_c.parinte
                return drum'''
                nod_c = self
                drum=[]
                drum.append(nod_c)
                while nod_c.parinte is not None:
                        drum.append(nod_c.parinte)
                        nod_c = nod_c.parinte
                drum.reverse()
                return drum
                
        def contine_in_drum(self, nod):
                """
                        Functie care verifica daca nodul se afla in drumul unui alt nod.
                        Verificarea se face mergand din parinte in parinte pana la radacina
                        Se compara doar informatiile nodurilor(proprietatea info)
                """
                nod_c=self
                while nod_c.parinte is not None :
                        if nod.info==nod_c.nod_graf.info:
                                return True
                        nod_c = nod_c.parinte
                return False            


        #se modifica in functie de problema
        def expandeaza(self):
                l_succesori=[]
                config = self.nod_graf.info
                for cheie in self.problema.chei:
                        #aplic fiecare cheie asupra configuratiei curente a lacatului
                        copie = copy.deepcopy(config)
                        ok=True #in aceasta problema pot fi generate o infinitate de stari, asa ca am hotarat sa setez o limita de 5 pentru fiecare incuietoare
                        for i in range(len(cheie)):
                                (a,b) = copie[i] #starea unei incuietori
                                #modific starea incuitorii in functie de valoarelea de pe pozitia i a cheii
                                if cheie[i] == 'd':
                                        if a == 'i':
                                                b -= 1
                                                if b == 0:
                                                       a = 'd'
                                elif cheie[i] == 'i':
                                        if a == 'i':
                                                b += 1
                                                if b>=5:
                                                        ok=False
                                                
                                        else:
                                                b = 1
                                                a = 'i'
                                copie[i] = (a,b)
                        if ok:
                                n = Nod(copie,0)
                                if nr_euristica == 1:
                                        n.calculeaza_h1()
                                elif nr_euristica == 2:
                                        n.calculeaza_h2()
                                else:
                                        n.calculeaza_h3()
                                l_succesori.append((n,cheie,1))
                return l_succesori

        #se modifica in functie de problema
        def test_scop(self):
                return self.nod_graf.info==self.__class__.problema.nod_scop

        def __str__ (self):
                parinte=self.parinte if self.parinte is None else self.parinte.nod_graf.info
                return "("+str(self.nod_graf)+", parinte="+str(parinte)+", f="+str(self.f)+", g="+str(self.g)+")";


""" Algoritmul A* """


def str_info_noduri(l):
        """
                o functie folosita strict in afisari - poate fi modificata in functie de problema
        """


        '''sir="["
        for x in l:
                sir+=str(x)+"  "
        sir+="]\n"
        return sir'''

        sir = "Initial: " + str(l[0].nod_graf) + "\n"
        for i in range (1,len(l)):
                cheie = "[" + l[i].cheie[0]
                for x in range(1,len(l[i].cheie)):
                        cheie += ','+l[i].cheie[x]
                cheie +=']'
                sir+=str(i) +") Incuietori: " + str(l[i].parinte.nod_graf) + "\n" + "Folosim cheia: " +  cheie + " pentru a ajunge la " + str(l[i].nod_graf) + ".\n"
        sir += "\nIncuietori(stare scop): " + str(l[len(l)-1].nod_graf)
        return sir


def afis_succesori_cost(l):
        """
                o functie folosita strict in afisari - poate fi modificata in functie de problema
        """
        sir=""
        for (x, cost) in l:
                sir+="\nnod: "+str(x)+", cost arc:"+ str(cost)
        
        return sir


def in_lista(l,nod):
        for i in range(len(l)):
                if l[i].nod_graf.info==nod.info:
                        return l[i]
        return None

def a_star():
        rad_arbore=NodParcurgere(NodParcurgere.problema.nod_start);
        open=[rad_arbore]
        closed=[]
        while len(open) > 0 :
                #print(str_info_noduri(open))
                nod_curent=open.pop(0)
                closed.append(nod_curent)
                #print(nod_curent)
                if nod_curent.test_scop(): #testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
                        break

                l_succesori=nod_curent.expandeaza()
                for (nod_succesor, cheie, cost_succesor) in l_succesori:
                        #daca nu e in drum
                        nod_nou=None
                        if(not nod_curent.contine_in_drum(nod_succesor)):
                                g_succesor=nod_curent.g+cost_succesor
                                f=g_succesor+nod_succesor.h
                                #verific daca se afla in closed (si il si sterg, returnand nodul sters in nod_parcg_vechi
                                nod_parcg_vechi=in_lista(closed,nod_succesor)

                                if nod_parcg_vechi is not None:
                                        #print("a")
                                        if(f<nod_parcg_vechi.f):
                                                closed.remove(nod_parcg_vechi)
                                                nod_parcg_vechi.parinte=nod_curent
                                                nod_parcg_vechi.g=g_succesor
                                                nod_parcg_vechi.f=f
                                                nod_parcg_vechi.cheie=cheie
                                                closed.append(nod_parcg_vechi)
                                                nod_nou=nod_parcg_vechi
                                                #print("A")
                                                
                                else :
                                        #verific daca se afla in open
                                        nod_parcg_vechi=in_lista(open,nod_succesor)
                                        if nod_parcg_vechi is not None:
                                                #print("b")
                                                if(f<nod_parcg_vechi.f):
                                                #if(nod_parcg_vechi.g>g_succesor):
                                                        open.remove(nod_parcg_vechi)
                                                        nod_parcg_vechi.parinte=nod_curent
                                                        nod_parcg_vechi.g=g_succesor
                                                        nod_parcg_vechi.f=f
                                                        nod_parcg_vechi.cheie=cheie
                                                        nod_nou=nod_parcg_vechi
                                                        #print("B")
                                                        
                                        else: # cand nu e nici in closed nici in open           
                                                
                                                nod_nou=NodParcurgere(nod_graf=nod_succesor,cheie=cheie, parinte=nod_curent,g=g_succesor);#se calculeaza f automat in constructor
                                                #print("c")
                                        
                                if nod_nou is not None:     
                                        #inserare in lista sortata crescator dupa f (si pentru f-uri egale descrescator dupa g
                                        
                                        #print("###")
                                        i=0
                                        while i<len(open):
                                                if open[i].f<nod_nou.f:
                                                        i+=1
                                                else:
                                                        while i<len(open) and open[i].f==nod_nou.f and open[i].g>nod_nou.g:
                                                                i+=1    
                                                        break

                                        open.insert(i, nod_nou)
                
        if(len(open)==0):
                return "Lista open e vida, nu avem drum de la nodul start la nodul scop"
        else:
                return str_info_noduri(nod_curent.drum_arbore())
        

        
        
        
if __name__ == "__main__":
        fisiere_input = ["input1.txt", "input2.txt", "input3.txt"]
        fisiere_output = ["output1.txt", "output2.txt", "output3.txt"]
        for i in range(3):
                fisier_in = open(fisiere_input[i], "r")
                global nr_euristica
                problema=Problema(fisier_in.read().splitlines())
                NodParcurgere.problema=problema
                fisier_out=open(fisiere_output[i], "w")
                print("Timpi de rulare pentru fisierul " + str(i+1)+":")
                
                nr_euristica=3
                t_inainte=int(round(time.time() * 1000))
                rezultat=a_star()
                t_dupa=int(round(time.time() * 1000))
                print("Timp de rulare pentru prima euristica: "+str(t_dupa-t_inainte)+" milisecunde.")
                fisier_out.write(rezultat)
                
                nr_euristica=1
                t_inainte=int(round(time.time() * 1000))
                a_star()
                t_dupa=int(round(time.time() * 1000))
                print("Timp de rulare pentru a doua euristica: "+str(t_dupa-t_inainte)+" milisecunde.")
                
                fisier_out.close()
                fisier_in.close()
