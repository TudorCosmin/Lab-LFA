# Tema Tudor Cosmin Oanea - grupa 151
# Fisierul "fisier.in" contine codul

import sys


def elim_com_enter(s):
    x = s.split("#")
    return x[0].strip()

words = []
states = []
transitions = {}
stari_finale = []
sigma = 0
state = 0
transition = 0
stare_start = 0
eroare = 0
with open("fisier.in", "r") as f:
    linii = f.readlines()
    i = 0
    for l in linii:
        l = l.strip()
        i += 1
        if l == "":
            pass
        elif l[0] == "#":
            pass
        else:
            if elim_com_enter(l) == "Sigma:":
                sigma = 1

            if elim_com_enter(l) == "States:":
                state = 1

            if elim_com_enter(l) == "Transitions:":
                transition = 1

            if elim_com_enter(l) == "End":
                sigma = 0
                state = 0
                transition = 0


            if sigma == 1 and elim_com_enter(l) != "Sigma:":
                s = elim_com_enter(l)
                if s in words:
                    print("Eroare la linia", i, "\nExista deja cuvantul " + s + "\n")
                    eroare = 1
                else:
                    words.append(s)


            if state == 1 and elim_com_enter(l) != "States:":
                s = elim_com_enter(l)
                if s[-1] == "S":
                    if stare_start == 0:
                        stare_start = 1
                        stare_initiala = s[:-3]
                    else:
                        print("Eroare la linia", i, "\nExista mai multe stari initiale\n")
                        eroare = 1

                if s in states:
                    print("Eroare la linia", i, "\nExista deja starea ", end="")
                    eroare = 1
                    if "," not in s:
                        print(s + "\n")
                    else:
                        print(s[:-3] + "\n")
                else:
                    if s[-1] == "S" or s[-1] == "F":
                        states.append(s[:-3])
                        if s[-1] == "F":
                            stari_finale.append(s[:-3])
                    else:
                        states.append(s)


            if transition == 1 and elim_com_enter(l) != "Transitions:":
                s = elim_com_enter(l)
                t = s.split(",")

                if t[0].strip() not in states:
                    print("Eroare la linia", i, "\nNu exista starea", t[0].strip(), "\n")
                    eroare = 1

                elif t[1].strip() not in words:
                    print("Eroare la linia", i, "\nNu exista cuvantul", t[1].strip(), "\n")
                    eroare = 1

                elif t[2].strip() not in states:
                    print("Eroare la linia", i, "\nNu exista starea", t[2].strip(), "\n")
                    eroare = 1
                else:
                    if t[0].strip() not in transitions.keys():
                        transitions[t[0].strip()] = []
                        transitions[t[0].strip()].append((t[1].strip(), t[2].strip()))
                    else:
                        transitions[t[0].strip()].append((t[1].strip(), t[2].strip()))

# print(transitions)
# print(stari_finale)

if eroare == 0:
    print("Codul este bun! :)")

    lcuvinte = sys.argv[1:]
    for c in lcuvinte:
        cuvant = c
        st = stare_initiala
        i = 0
        gata = 0
        while st not in stari_finale and i < len(cuvant) and gata == 0:
            t = 0
            ok = 0
            while t < len(transitions[st]):
                if(transitions[st][t][0] == cuvant[i]): # verific daca tranzitia curenta e buna
                    st = transitions[st][t][1]
                    t = len(transitions[st]) + 1
                    ok = 1 # am gasit o tranzitie
                t += 1 # trec la urmatoarea tranzitie

            if ok == 0: # nu am gasit nicio tranzitie
                print("Cuvantul nu este acceptat!")
                gata = 1
            i += 1
        if gata == 0:
            print("Cuvantul este acceptat!")

