import random
class Domanda:
    pass
    def __init__(self,testo, livello, risp_corr, risp):
        self.testo = testo
        self.livello = livello
        self.risp_corr = risp_corr
        self.risp = risp

    def __str__(self):
        return f"{self.testo} \n Livello: {self.livello}\n Risposte:{', '.join(self.risp)}"


def carica_domande(nome_file):
    domande = []
    with open(nome_file, "r",encoding="utf-8") as file:
        righe = [riga.strip() for riga in file.readlines()]

    i = 0
    while i<len(righe):
        if(righe[i] == ""):
            i+= 1
            continue

        testo = righe[i].strip()
        livello = righe[i+1].strip()
        risp_corr = righe[i+2].strip()
        risp = [ righe[i+3].strip(), righe[i+4].strip(), righe[i+5].strip()]

        domanda = Domanda(testo, livello, risp_corr, risp)

        domande.append(domanda)

        i += 6
    return domande


#domande = carica_domande("domande.txt")
#for d in domande:
 #    print(d)
  #   print()

def gioca_quiz(domande):
    domande.sort(key = lambda d:d.livello)
    punteggio = 0
    livelli = sorted(set(d.livello for d in domande))
    livello_corrente = livelli[0]

    print("\n---INIZIO DEL QUIZ ---- \n")

    while True:
        domande_livello = [d for d in domande if d.livello == livello_corrente]

        if not domande_livello:
            print("\n Nessuna domanda disponibile per questo livello.")
            break

        domanda = random.choice(domande_livello)

        opzioni = domanda.risp.copy()
        opzioni.append(domanda.risp_corr)
        random.shuffle(opzioni)

        print(f"Livello {livello_corrente}) {domanda.testo} ")
        for i, risposta in enumerate(opzioni, 1):
            print(f"{i}, {risposta}")

        #try:
        scelta = int(input("\n Inserisci la tua risposta ")) - 1
           # if scelta < 0 or scelta >= len(opzioni):
            #    raise ValueError
        risposta_utente = opzioni[scelta]
        #except ValueError:
         #   print("\n Risposta non valida! Inserisci un numero valido.")
          #  continue

        if risposta_utente == domanda.risp_corr:
            punteggio += 1
            print("Risposta corretta! \n")
            indice_livello = livelli.index(livello_corrente)
            if indice_livello + 1 <len(livelli):
                livello_corrente = livelli[indice_livello + 1]
            else:
                print("\n Hai risposto correttamente alla domanda più difficile!!!!")
                break
        else:
            print(f"Risposta sbagliata! La risposta corretta  era {domanda.risp_corr}")
            print(f"Punteggio totale: {punteggio}")
            nickname = input("Inserisci il tuo nickname: ")
            aggiungi_punteggio(nome_file="punti.txt", nickname=nickname, punteggio=punteggio)
            break

def aggiungi_punteggio(nome_file, nickname, punteggio):
    try:
        with open(nome_file, "r", encoding="utf-8") as file:
            punti = [line.strip().split() for line in file.readlines()]
            punti = [(nome, int(p)) for nome, p in punti]
    except FileNotFoundError:
        punti = []

    punti.append((nickname, punteggio))

    punti.sort(key = lambda x:x[1], reverse=True)

    with open(nome_file, "w", encoding="utf-8") as file:
        for nome, p in punti:
            file.write(f"{nome} {p} \n")

domande = carica_domande("domande.txt")
gioca_quiz(domande)