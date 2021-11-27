import time
import math
import pygame, sys

ADANCIME_MAX=4

#directii pentru mutari
dx=[1,-1,1,-1]
dy=[1,-1,-1,1]

loc = {} #va retine linia 0 pentru culoarea lui JMIN si 7 pentru JMAX si va ajuta la transformarea unui pion in rege

def margini(x,y):
        #verifica daca o pozitie este in cadrul tablei de joc
        if(x>7 or y>7 or x<0 or y<0):
                return False
        return True



def deseneaza_grid(display, tabla):
        w_gr=h_gr=50
        
        alb_img = pygame.image.load('alb.png')
        alb_img = pygame.transform.scale(alb_img, (w_gr,h_gr))
        negru_img = pygame.image.load('negru.png')
        negru_img = pygame.transform.scale(negru_img, (w_gr,h_gr))
        drt=[]
        for ind in range(len(tabla)):
                linie=ind//8
                coloana=ind%8
                patr = pygame.Rect(coloana*(w_gr), linie*(h_gr), w_gr, h_gr)
                print(str(coloana*(w_gr+1)), str(linie*(h_gr+1)))
                drt.append(patr)
                if (linie+coloana)%2==0:
                        pygame.draw.rect(display, (255,255,255), patr)
                else:
                        pygame.draw.rect(display, (0,0,0), patr)
                if tabla[ind].lower()=='a':
                        display.blit(alb_img,(coloana*w_gr,linie*h_gr))
                elif tabla[ind].lower()=='n':
                        display.blit(negru_img,(coloana*w_gr,linie*h_gr))
        pygame.display.flip()
        return drt



class Joc:
        """
        Clasa care defineste jocul. Se va schimba de la un joc la altul.
        """
        NR_COLOANE=8
        JMIN=None
        JMINK=None
        JMAX=None
        JMAXK=None
        JMIN_piese=None
        JMAX_piese=None
        GOL='#'
        def __init__(self, tabla=None, piese_a= None, piese_b= None):
                if tabla is None:
                        self.matr=[self.__class__.GOL]*64
                        for i in range (3):
                                for j in range(8):
                                        if (i + j) % 2 == 1 :
                                                self.matr[i * 8 + j] = self.__class__.JMAX

                
                        for i in range (5, 8):
                                for j in range(8):
                                        if (i + j) % 2 == 1 :
                                                self.matr[i * 8 + j] = self.__class__.JMIN
                else:
                        self.matr=tabla 
                if piese_a is None:
                        self.JMIN_piese = 12
                else :
                        self.JMIN_piese = piese_a

                if piese_b is None:
                        self.JMAX_piese = 12
                else :
                        self.JMAX_piese = piese_b
                        
                
                
        def final(self):
                #jocul se termina can unul din jucatori ramane fara piese sau nu mai poate realiza mutari
                if self.JMIN_piese==0 or len(self.mutari(self.__class__.JMIN))==0:
                        return self.__class__.JMAX
                elif self.JMAX_piese==0 or len(self.mutari(self.__class__.JMAX))==0:
                        return self.__class__.JMIN
                else:
                        return False

        
        def mutari_piesa(self, i):
                #va genera toate mutarile posibile ale unei piese
                jucator_curr = self.matr[i] #va retine jucatorul curent si daca este rege sau nu
                jucator = jucator_curr.lower() #va retine jucatorul curent
                jucator_opus = self.__class__.JMIN #va retine oponentul
                if jucator.lower() == self.__class__.JMIN:
                        jucator_opus = self.__class__.JMAX
                #print(jucator_opus)
                l_mutari=[]
                #coordonatele initiale
                y_curr = i//8
                x_curr = i%8
                for j in range(4) :
                        if jucator_curr.upper()==jucator_curr or jucator_curr==self.__class__.JMIN and dy[j]<0 or jucator_curr==self.__class__.JMAX and dy[j]>0 :
                                #conditia verifica in cazul unui pion daca acesta merge doar in fata
                                matr_tabla_noua=list(self.matr)
                                #coordonatele pentru mutare
                                x1 = x_curr + dx[j]
                                y1 = y_curr + dy[j]
                                if margini(x1,y1):
                                        if self.matr[y1*8+x1].lower()==jucator_opus:
                                                #in cazul in care pe pozitia aleasa este jucatorul opus se genereaza coordonatel pentru saritura peste acesta
                                                x2 = x1 + dx[j]
                                                y2 = y1 + dy[j]
                                                if margini(x2,y2) and self.matr[y2*8+x2]==self.__class__.GOL :
                                                        #daca pozitia este libera
                                                        c = self.matr[y1*8+x1].lower()
                                                        #este mutata piese pe coordonatele noi
                                                        if y2==loc[jucator_opus]:
                                                                #daca am ajuns pe linia in care un pion devine rege
                                                                matr_tabla_noua[y2*8+x2]=jucator.upper()
                                                        else:
                                                                matr_tabla_noua[y2*8+x2]=jucator
                                                        #pozitia initiala si cea a piesei oponentului devin libere
                                                        matr_tabla_noua[i]=self.__class__.GOL
                                                        matr_tabla_noua[y1*8+x1]=self.__class__.GOL
                                                        #se scada numarul de piese pentru oponent si se adauga mutarea
                                                        if c == self.__class__.JMIN:
                                                                l_mutari.append(Joc(matr_tabla_noua,self.JMIN_piese-1,self.JMAX_piese))
                                                        else :
                                                                l_mutari.append(Joc(matr_tabla_noua,self.JMIN_piese,self.JMAX_piese-1))
                                        elif self.matr[y1*8+x1]==self.__class__.GOL:
                                                #pozitia initiala se elibereaza
                                                matr_tabla_noua[i]=self.__class__.GOL
                                                #este mutata piese pe coordonatele noi
                                                if y1==loc[jucator_opus]:
                                                        #daca am ajuns pe linia in care un pion devine rege
                                                        matr_tabla_noua[y1*8+x1]=jucator.upper()
                                                else:
                                                        matr_tabla_noua[y1*8+x1]=jucator

                                                #se adauga mutarea
                                                l_mutari.append(Joc(matr_tabla_noua,self.JMIN_piese,self.JMAX_piese))
                return l_mutari
        
        def mutari(self, jucator):
                l_mutari1=[]
                #genereaza mutarile pentru toate piese
                for i in range(len(self.matr)) :
                        jucator_curr = self.matr[i]
                        if jucator_curr.lower() == jucator :
                                mutari = self.mutari_piesa(i)
                                l_mutari1+=mutari
                                                               
                return l_mutari1
        

        

        #linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare

        
                
        def estimeaza_scor(self, adancime):
                t_final=self.final()
                #if (adancime==0):
                if t_final==self.__class__.JMAX :
                        return (99+adancime)
                elif t_final==self.__class__.JMIN:
                        return (-99-adancime)
                else:
                        score=0
                        #Jucatorul(JMIN) va avea mereu jumatatea cu liniile 4-7
                        #Jucatorul(JMIN) va avea mereu jumatatea cu liniile 0-3
                        PHP=0 #pioni JMIN in jumatatea lor
                        PHOP=0 #pioni JMAX in jumatatea lor
                        EHP=0 #pioni JMIN in jumatatea opusa
                        EHOP=0 #pioni JMAX in jumatatea opusa
                        K=0 #regi JMIN
                        OK=0 #regi JMAX
                        n=0 #numar total piese
                        K0=K1=K2=0 #regi JMIN pe liniile 0,1,2
                        OK0=OK1=OK2=0 #regi JMIN pe liniile 7,6,5
                        for i in range(32):
                                if self.matr[i]==self.__class__.JMIN:
                                        EHP+=1
                                elif self.matr[i]==self.__class__.JMAX:
                                        PHOP+=1
                                elif self.matr[i]==self.__class__.JMINK:
                                        K+=1
                                        if i//8==0:
                                                K0+=1
                                        elif i//8==1:
                                                K1+=1
                                        elif i//8==2:
                                                K2+=1
                                elif self.matr[i]==self.__class__.JMAXK:
                                        OK+=1
                                
                        for i in range(32,64):
                                if self.matr[i]==self.__class__.JMIN:
                                        PHP+=1
                                elif self.matr[i]==self.__class__.JMAX:
                                        EHOP+=1
                                elif self.matr[i]==self.__class__.JMINK:
                                        K+=1
                                elif self.matr[i]==self.__class__.JMAXK:
                                        OK+=1
                                        if i//8==7:
                                                OK0+=1
                                        elif i//8==6:
                                                OK1+=1
                                        elif i//8==5:
                                                OK2+=1
                        #Ambele formule folosesc valorile calculate mai sus inmultite cu coeficienti care reprezinta importanta lor in calcularea scorului               
                        if not (PHP==0 and PHOP==0):
                                '''cat timp ambii jucatori nu si-au dus pionii in jumatatea opusa este folosita urmatoarea formula care influenteaza
                                fiecare jucator sa isi trimita pionii in jumatatea opusa si mai ales sa creeze regi, pastrandu-si cat mai mare numarul de piese'''
                                score=((PHOP+3*EHOP+5*OK)-(PHP+3*EHP+5*K))
                        else:
                                '''in acest caz este indicat ca regii sa fie trimisi inspre mijlocul tablei de joc pentru a face loc si celorlalti pioni
                                sa devina regi si pentru a se apropia de piesele jucatorului opus'''
                                OK3=OK-(OK0+OK1+OK2) #toti ceilalti regi JMAX
                                K3=K-(K0+K1+K2)
                                #print("###",K0,K1,K2,K3,OK0,OK1,OK2,OK3)
                                score=((3*EHOP+5*OK0+6*OK1+7*OK2+8*OK3)-(3*EHP+5*K0+6*K1+7*K2+8*K3))
                        return score


        def __str__(self):
                sir= "   a b c d e f g h\n   ---------------\n"
                for i in range(8):
                        sir+=str(i)
                        sir+=" |"
                        for j in range(7) :
                              sir += str(self.matr[i * 8 + j])
                              sir += " "
                              
                        sir += str(self.matr[i * 8 + 7])
                        sir += "\n"
 
                return sir
                        

class Stare:
        """
        Clasa folosita de algoritmii minimax si alpha-beta
        Are ca proprietate tabla de joc
        Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
        De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
        """
        def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
                self.tabla_joc=tabla_joc
                self.j_curent=j_curent
                
                #adancimea in arborele de stari
                self.adancime=adancime  
                
                #scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
                self.scor=scor
                
                #lista de mutari posibile din starea curenta
                self.mutari_posibile=[]
                
                #cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
                self.stare_aleasa=None

        def jucator_opus(self):
                if self.j_curent==Joc.JMIN:
                        return Joc.JMAX
                else:
                        return Joc.JMIN

        def mutari(self):               
                l_mutari=self.tabla_joc.mutari(self.j_curent)
                juc_opus=self.jucator_opus()
                l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

                return l_stari_mutari
                
        
        def __str__(self):
                sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
                return sir
        

                        
""" Algoritmul MinMax """

def min_max(stare):
        
        if stare.adancime==0 or stare.tabla_joc.final() :
                stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
                return stare
                
        #calculez toate mutarile posibile din starea curenta
        stare.mutari_posibile=stare.mutari()

        #aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
        mutari_scor=[min_max(mutare) for mutare in stare.mutari_posibile]
        


        if stare.j_curent==Joc.JMAX :
                #daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
                stare.stare_aleasa=max(mutari_scor, key=lambda x: x.scor)
        else:
                #daca jucatorul e JMIN aleg starea-fiica cu scorul minim
                stare.stare_aleasa=min(mutari_scor, key=lambda x: x.scor)
                
        stare.scor=stare.stare_aleasa.scor
        return stare
        

def alpha_beta(alpha, beta, stare):
        if stare.adancime==0 or stare.tabla_joc.final() :
                stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
                return stare
        
        if alpha>beta:
                return stare #este intr-un interval invalid deci nu o mai procesez
        
        stare.mutari_posibile=stare.mutari()
                

        if stare.j_curent==Joc.JMAX :
                scor_curent=float('-inf')
                
                for mutare in stare.mutari_posibile:
                        #calculeaza scorul
                        stare_noua=alpha_beta(alpha, beta, mutare)
                        
                        if (scor_curent<stare_noua.scor):
                                stare.stare_aleasa=stare_noua
                                scor_curent=stare_noua.scor
                        if(alpha<stare_noua.scor):
                                alpha=stare_noua.scor
                                if alpha>=beta:
                                        break

        elif stare.j_curent==Joc.JMIN :
                scor_curent=float('inf')
                for mutare in stare.mutari_posibile:
                        
                        stare_noua=alpha_beta(alpha, beta, mutare)
                        
                        if (scor_curent>stare_noua.scor):
                                stare.stare_aleasa=stare_noua
                                scor_curent=stare_noua.scor

                        if(beta>stare_noua.scor):
                                beta=stare_noua.scor
                                if alpha>=beta:
                                        break
                
        stare.scor=stare.stare_aleasa.scor

        return stare
        






def afis_daca_final(stare_curenta):
        final=stare_curenta.tabla_joc.final()
        if(final):
                if (final=="remiza"):
                        print("Remiza!")
                else:
                        print("A castigat "+final)
                        print("Numar piese jucator: ", stare_curenta.tabla_joc.JMIN_piese)
                        print("Numar piese calculator: ", stare_curenta.tabla_joc.JMAX_piese)
                        
                return True
                
        return False
                
        

def main():
        #initializare algoritm
        mutari_JMIN=0
        mutari_JMAX=0
        if(len(sys.argv)==1):
                raspuns_valid=False
                while not raspuns_valid:
                        dif=input("Nivel de dificultate? (raspundeti cu 1, 2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n")
                        if dif in ['1','2','3']:
                                raspuns_valid=True
                                if dif=='1':
                                        ADANCIME_MAX=4
                                elif dif=='2':
                                        ADANCIME_MAX=5
                                else:
                                        ADANCIME_MAX=6
                        else:
                                print("Nu ati ales o varianta corecta.")
                
                raspuns_valid=False
                while not raspuns_valid:
                        tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
                        if tip_algoritm in ['1','2']:
                                raspuns_valid=True
                        else:
                                print("Nu ati ales o varianta corecta.")
                #initializare jucatori
                raspuns_valid=False
                while not raspuns_valid:
                        Joc.JMIN=input("Doriti sa jucati cu a sau cu n? ").lower()
                        if (Joc.JMIN in ['a', 'n']):
                                raspuns_valid=True
                        else:
                                print("Raspunsul trebuie sa fie a sau n.")
                Joc.JMAX= 'n' if Joc.JMIN == 'a' else 'a'
                loc[Joc.JMAX]=0
                loc[Joc.JMIN]=7
                Joc.JMAXK = Joc.JMAX.upper()
                Joc.JMINK = Joc.JMIN.upper()
                #initializare tabla
                tabla_curenta=Joc();
                print("Tabla initiala")
                print(str(tabla_curenta))
                #creare stare initiala
                stare_curenta=Stare(tabla_curenta,'a',ADANCIME_MAX)
                
                t_inceput=int(round(time.time() * 1000))
                
                while True :
                        if (stare_curenta.j_curent==Joc.JMIN):
                        #muta jucatorul
                                t_inainte=int(round(time.time() * 1000))
                                oprire=False
                                raspuns_valid=False
                                while not raspuns_valid:
                                        try:
                                                print("Introduceti pozitia piesei")
                                                raspuns=input("linie_piesa=")
                                                if raspuns=="exit":
                                                        print("Numar piese jucator: ", stare_curenta.tabla_joc.JMIN_piese)
                                                        print("Numar piese calculator: ", stare_curenta.tabla_joc.JMAX_piese)
                                                        oprire=True
                                                        break
                                                else:
                                                        linie1=int(raspuns)
                                                coloana4=(input("coloana_piesa="))
                                                coloana1 = ord(coloana4)-ord('a')
                                                if (linie1 in range(0,8) and coloana1 in range(0,8)):
                                                        if stare_curenta.tabla_joc.matr[linie1*8+coloana1].lower() == Joc.JMIN:                                    
                                                                raspuns_valid=True
                                                        else:
                                                                print("Nu puteti alege aceasta pozitie.")
                                                else:
                                                        print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2,..,7, respectiv una din literele a,b,..,h).")                
                                
                                        except ValueError:
                                                print("Linia si coloana trebuie sa fie numer intreg respectiv caracter")
                                if oprire:
                                        break
                                raspuns_valid=False
                                while not raspuns_valid:
                                        try:
                                                print("Introduceti mutarea")
                                                linie2=int(input("linie_mutare="))
                                                coloana5=(input("coloana_mutare="))
                                                coloana2 = ord(coloana5)-ord('a')
                                                linie3=linie2
                                                coloana3=coloana2
                                                if (linie2 in range(0,8) and coloana2 in range(0,8)):
                                                        if (stare_curenta.tabla_joc.matr[linie1*8+coloana1]==Joc.JMINK and abs(linie1-linie2)==2 and abs(coloana1-coloana2)==2) or (stare_curenta.tabla_joc.matr[linie1*8+coloana1]==Joc.JMIN and linie1-linie2==2 and abs(coloana1-coloana2)==2):
                                                                linie3 = linie1-(linie1-linie2)//2
                                                                coloana3 = coloana1-(coloana1-coloana2)//2
                                                                if stare_curenta.tabla_joc.matr[linie2*8+coloana2] == Joc.GOL and stare_curenta.tabla_joc.matr[linie3*8+coloana3].lower()==Joc.JMAX:
                                                                        raspuns_valid=True
                                                                else:
                                                                        print("Mutarea aleasa nu este valida.")
                                                        elif (stare_curenta.tabla_joc.matr[linie1*8+coloana1]==Joc.JMINK and abs(linie1-linie2)==1 and abs(coloana1-coloana2)==1) or (stare_curenta.tabla_joc.matr[linie1*8+coloana1]==Joc.JMIN and linie1-linie2==1 and abs(coloana1-coloana2)==1):
                                                                if stare_curenta.tabla_joc.matr[linie2*8+coloana2] == Joc.GOL:
                                                                        raspuns_valid=True
                                                                else:
                                                                        print("Mutarea aleasa nu este valida.")
                                                        else:
                                                                print("Mutarea aleasa nu este valida.")
                                                else:
                                                        print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2,..,7, respectiv una din literele a,b,..,h).")                
                                
                                        except ValueError:
                                                print("Linia si coloana trebuie sa fie numer intreg respectiv caracter")
                                                
                                #dupa iesirea din while sigur am valide atat linia cat si coloana
                                #deci pot plasa simbolul pe "tabla de joc"
                                if abs(linie1-linie2)==2:
                                        print(linie3,coloana3)
                                        stare_curenta.tabla_joc.matr[linie3*8+coloana3]=Joc.GOL
                                        stare_curenta.tabla_joc.JMAX_piese-=1
                                stare_curenta.tabla_joc.matr[linie2*8+coloana2]=stare_curenta.tabla_joc.matr[linie1*8+coloana1]
                                stare_curenta.tabla_joc.matr[linie1*8+coloana1]=Joc.GOL
                                
                                #afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print("Numar piese jucator: ", stare_curenta.tabla_joc.JMIN_piese)
                                print("Numar piese calculator: ", stare_curenta.tabla_joc.JMAX_piese)
                                print(str(stare_curenta))
                                t_dupa=int(round(time.time() * 1000))
                                mutari_JMIN+=1
                                print("Jucatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")

                                #testez daca jocul a ajuns intr-o stare finala
                                #si afisez un mesaj corespunzator in caz ca da
                                if (afis_daca_final(stare_curenta)):
                                        break
                                        
                                        
                                #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent=stare_curenta.jucator_opus()
                        
                        #--------------------------------
                        else: #jucatorul e JMAX (calculatorul)
                                #Mutare calculator
                                
                                #preiau timpul in milisecunde de dinainte de mutare
                                t_inainte=int(round(time.time() * 1000))
                                if tip_algoritm=='1':
                                        stare_actualizata=min_max(stare_curenta)
                                else: #tip_algoritm==2
                                        stare_actualizata=alpha_beta(-500, 500, stare_curenta)
                                stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc
                                print("Tabla dupa mutarea calculatorului")
                                print("Numar piese jucator: ", stare_curenta.tabla_joc.JMIN_piese)
                                print("Numar piese calculator: ", stare_curenta.tabla_joc.JMAX_piese)
                                print(str(stare_curenta))
                                
                                #preiau timpul in milisecunde de dupa mutare
                                t_dupa=int(round(time.time() * 1000))
                                print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                mutari_JMAX+=1
                                
                                if (afis_daca_final(stare_curenta)):
                                        break
                                        
                                #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent=stare_curenta.jucator_opus()
                t_final=int(round(time.time() * 1000))
                print("Jocul a durat "+str(t_final-t_inceput)+" milisecunde.")
                                
        elif len(sys.argv)==2 and sys.argv[1]=="-gui":
                raspuns_valid=False
                while not raspuns_valid:
                        dif=input("Nivel de dificultate? (raspundeti cu 1, 2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n")
                        if dif in ['1','2','3']:
                                raspuns_valid=True
                                if dif=='1':
                                        ADANCIME_MAX=4
                                elif dif=='2':
                                        ADANCIME_MAX=5
                                else:
                                        ADANCIME_MAX=6
                        else:
                                print("Nu ati ales o varianta corecta.")
                raspuns_valid=False
                while not raspuns_valid:
                        tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
                        if tip_algoritm in ['1','2']:
                                raspuns_valid=True
                        else:
                                print("Nu ati ales o varianta corecta.")
                #initializare jucatori
                raspuns_valid=False
                while not raspuns_valid:
                        Joc.JMIN=input("Doriti sa jucati cu a sau cu n? ").lower()
                        if (Joc.JMIN in ['a', 'n']):
                                raspuns_valid=True
                        else:
                                print("Raspunsul trebuie sa fie a sau n.")
                Joc.JMAX= 'n' if Joc.JMIN == 'a' else 'a'
                loc[Joc.JMAX]=0
                loc[Joc.JMIN]=7
                Joc.JMAXK = Joc.JMAX.upper()
                Joc.JMINK = Joc.JMIN.upper()
                #initializare tabla
                tabla_curenta=Joc();
                print("Tabla initiala")
                print(str(tabla_curenta))
                #creare stare initiala
                stare_curenta=Stare(tabla_curenta,'a',ADANCIME_MAX)
                pygame.init()
                pygame.display.set_caption('Dame')
                ecran=pygame.display.set_mode(size=(410,410))
                
                
                patratele=deseneaza_grid(ecran,tabla_curenta.matr)
                
                t_inceput=int(round(time.time() * 1000))
                while True :
                        if (stare_curenta.j_curent==Joc.JMIN):
                                t_inainte=int(round(time.time() * 1000))
                                #muta jucatorul
                                linie1=0
                                coloana1=0
                                st = 0
                                fin=False
                                while st < 3:
                                       for event in pygame.event.get():
                                                if event.type== pygame.QUIT:
                                                        pygame.quit()
                                                        sys.exit()
                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                        pos = pygame.mouse.get_pos()
                                                        
                                                        for np in range(len(patratele)):
                                                                if patratele[np].collidepoint(pos):
                                                                        linie=np//8
                                                                        coloana=np%8
                                                                        if stare_curenta.tabla_joc.matr[linie*8+coloana] == Joc.JMIN:                                   
                                                                                st = 1
                                                                                linie1=linie
                                                                                coloana1=coloana
                                                                        elif stare_curenta.tabla_joc.matr[linie*8+coloana] == Joc.JMINK:                                        
                                                                                st = 2
                                                                                linie1=linie
                                                                                coloana1=coloana
                                                                        elif stare_curenta.tabla_joc.matr[linie*8+coloana].lower() == Joc.GOL and st > 0:
                                                                                #dupa iesirea din while sigur am valide atat linia cat si coloana
                                                                                #deci pot plasa simbolul pe "tabla de joc"

                                                                                if st == 1:
                                                                                        if abs(coloana1 - coloana)==1 and linie1-linie==1:
                                                                                                if linie==loc[Joc.JMAX]:
                                                                                                        stare_curenta.tabla_joc.matr[linie*8+coloana]=Joc.JMINK
                                                                                                else:
                                                                                                        stare_curenta.tabla_joc.matr[linie*8+coloana]=Joc.JMIN
                                                                                                stare_curenta.tabla_joc.matr[linie1*8+coloana1]=Joc.GOL
                                                                                                st=3
                                                                                        
                                                                                                #afisarea starii jocului in urma mutarii utilizatorului
                                                                                                print("\nTabla dupa mutarea jucatorului")
                                                                                                print(str(stare_curenta))
                                                                                                patratele=deseneaza_grid(ecran,stare_curenta.tabla_joc.matr)
                                                                                                t_dupa=int(round(time.time() * 1000))
                                                                                                mutari_JMIN+=1
                                                                                                print("Jucatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                                                                                #testez daca jocul a ajuns intr-o stare finala
                                                                                                #si afisez un mesaj corespunzator in caz ca da
                                                                                                if (afis_daca_final(stare_curenta)):
                                                                                                        fin=True
                                                                                                        
                                                                                                        
                                                                                                #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                                                                                stare_curenta.j_curent=stare_curenta.jucator_opus()
                                                                                        elif abs(coloana1 - coloana)==2 and linie1-linie==2:
                                                                                                linie2 = linie1-(linie1-linie)//2
                                                                                                coloana2 = coloana1-(coloana1-coloana)//2
                                                                                                if stare_curenta.tabla_joc.matr[linie2*8+coloana2].lower() == Joc.JMAX:
                                                                                                        if linie==loc[Joc.JMAX]:
                                                                                                                stare_curenta.tabla_joc.matr[linie*8+coloana]=Joc.JMINK
                                                                                                        else:
                                                                                                                stare_curenta.tabla_joc.matr[linie*8+coloana]=Joc.JMIN
                                                                                                        stare_curenta.tabla_joc.matr[linie1*8+coloana1]=Joc.GOL
                                                                                                        stare_curenta.tabla_joc.matr[linie2*8+coloana2]=Joc.GOL
                                                                                                        stare_curenta.tabla_joc.JMAX_piese-=1
                                                                                                        st=3
                                                                                                
                                                                                                        #afisarea starii jocului in urma mutarii utilizatorului
                                                                                                        print("\nTabla dupa mutarea jucatorului")
                                                                                                        print(str(stare_curenta))
                                                                                                        patratele=deseneaza_grid(ecran,stare_curenta.tabla_joc.matr)
                                                                                                        t_dupa=int(round(time.time() * 1000))
                                                                                                        mutari_JMIN+=1
                                                                                                        print("Jucatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                                                                                        #testez daca jocul a ajuns intr-o stare finala
                                                                                                        #si afisez un mesaj corespunzator in caz ca da
                                                                                                        if (afis_daca_final(stare_curenta)):
                                                                                                                fin=True        
                                                                                                                
                                                                                                                
                                                                                                        #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                                                                                        stare_curenta.j_curent=stare_curenta.jucator_opus()

                                                                                if st == 2:
                                                                                        if abs(coloana1 - coloana)==1 and abs(linie1-linie)==1:
                                                                                                stare_curenta.tabla_joc.matr[linie*8+coloana]=Joc.JMINK
                                                                                                stare_curenta.tabla_joc.matr[linie1*8+coloana1]=Joc.GOL
                                                                                                st=3
                                                                                        
                                                                                                #afisarea starii jocului in urma mutarii utilizatorului
                                                                                                print("\nTabla dupa mutarea jucatorului")
                                                                                                print(str(stare_curenta))
                                                                                                patratele=deseneaza_grid(ecran,stare_curenta.tabla_joc.matr)
                                                                                                t_dupa=int(round(time.time() * 1000))
                                                                                                mutari_JMIN+=1
                                                                                                print("Jucatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                                                                                #testez daca jocul a ajuns intr-o stare finala
                                                                                                #si afisez un mesaj corespunzator in caz ca da
                                                                                                if (afis_daca_final(stare_curenta)):
                                                                                                        fin=True
                                                                                                        
                                                                                                        
                                                                                                #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                                                                                stare_curenta.j_curent=stare_curenta.jucator_opus()
                                                                                        elif abs(coloana1 - coloana)==2 and abs(linie1-linie)==2:
                                                                                                linie2 = linie1-(linie1-linie)//2
                                                                                                coloana2 = coloana1-(coloana1-coloana)//2
                                                                                                if stare_curenta.tabla_joc.matr[linie2*8+coloana2].lower() == Joc.JMAX:
                                                                                                        stare_curenta.tabla_joc.matr[linie*8+coloana]=Joc.JMINK
                                                                                                        stare_curenta.tabla_joc.matr[linie1*8+coloana1]=Joc.GOL
                                                                                                        stare_curenta.tabla_joc.matr[linie2*8+coloana2]=Joc.GOL
                                                                                                        stare_curenta.tabla_joc.JMAX_piese-=1
                                                                                                        st=3
                                                                                                
                                                                                                        #afisarea starii jocului in urma mutarii utilizatorului
                                                                                                        print("\nTabla dupa mutarea jucatorului")
                                                                                                        print(str(stare_curenta))
                                                                                                        patratele=deseneaza_grid(ecran,stare_curenta.tabla_joc.matr)
                                                                                                        #testez daca jocul a ajuns intr-o stare finala
                                                                                                        #si afisez un mesaj corespunzator in caz ca da
                                                                                                        t_dupa=int(round(time.time() * 1000))
                                                                                                        mutari_JMIN+=1
                                                                                                        print("Jucatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                                                                                        if (afis_daca_final(stare_curenta)):
                                                                                                                fin=True
                                                                                                                
                                                                                                                
                                                                                                        #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                                                                                        stare_curenta.j_curent=stare_curenta.jucator_opus()

                                
                                if fin:
                                        break
                        #--------------------------------
                        else: #jucatorul e JMAX (calculatorul)
                                #Mutare calculator
                                
                                #preiau timpul in milisecunde de dinainte de mutare
                                t_inainte=int(round(time.time() * 1000))
                                if tip_algoritm=='1':
                                        stare_actualizata=min_max(stare_curenta)
                                else: #tip_algoritm==2
                                        stare_actualizata=alpha_beta(-500, 500, stare_curenta)
                                stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc
                                print("Tabla dupa mutarea calculatorului")
                                print(str(stare_curenta))
                                
                                patratele=deseneaza_grid(ecran,stare_curenta.tabla_joc.matr)
                                #preiau timpul in milisecunde de dupa mutare
                                t_dupa=int(round(time.time() * 1000))
                                print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                                mutari_JMAX+=1
                                
                                if (afis_daca_final(stare_curenta)):
                                        break
                                        
                                #S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent=stare_curenta.jucator_opus()
                t_final=int(round(time.time() * 1000))
                print("Jocul a durat "+str(t_final-t_inceput)+" milisecunde.")
                print("Jucatorul a realizat " +str(mutari_JMIN)+" mutari")
                print("Calculatorul a realizat " +str(mutari_JMAX)+" mutari")
        else:
                print("Comanda introdusa gresit")
        
if __name__ == "__main__" :
        main()
