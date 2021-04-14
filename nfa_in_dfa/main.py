# Tema Tudor Cosmin Oanea - grupa 151
# Fisierul "fisier.in" contine inputul

import sys


def elim_com_enter(s):
    x = s.split("#")
    return x[0].strip()

def in_ordine(x):
    l = set(int(x) for x in str(x))
    x = 0
    for cif in l:
        x = x * 10 + cif
    return x

def eFinala(st):
    for s in st:
        if s in stari_finale:
            return True
    return False

lcuvinte = []
lstari = []
tranzitii = {}
stari_finale = []
sigma = 0
stare = 0
tranzitie = 0
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
                stare = 1

            if elim_com_enter(l) == "Transitions:":
                tranzitie = 1

            if elim_com_enter(l) == "End":
                sigma = 0
                stare = 0
                tranzitie = 0


            if sigma == 1 and elim_com_enter(l) != "Sigma:":
                s = elim_com_enter(l)
                if s in lcuvinte:
                    print("Eroare la linia", i, "\nExista deja cuvantul " + s + "\n")
                    eroare = 1
                else:
                    lcuvinte.append(s)


            if stare == 1 and elim_com_enter(l) != "States:":
                s = elim_com_enter(l)
                if s[-1] == "S":
                    if stare_start == 0:
                        stare_start = 1
                        stare_initiala = s[:-3]
                    else:
                        print("Eroare la linia", i, "\nExista mai multe stari initiale\n")
                        eroare = 1

                if s in lstari:
                    print("Eroare la linia", i, "\nExista deja starea ", end="")
                    eroare = 1
                    if "," not in s:
                        print(s + "\n")
                    else:
                        print(s[:-3] + "\n")
                else:
                    if s[-1] == "S" or s[-1] == "F":
                        lstari.append(s[:-3])
                        if s[-1] == "F":
                            stari_finale.append(s[:-3])
                    else:
                        lstari.append(s)


            if tranzitie == 1 and elim_com_enter(l) != "Transitions:":
                s = elim_com_enter(l)
                t = s.split(",")

                if t[0].strip() not in lstari:
                    print("Eroare la linia", i, "\nNu exista starea", t[0].strip(), "\n")
                    eroare = 1

                elif t[1].strip() not in lcuvinte:
                    print("Eroare la linia", i, "\nNu exista cuvantul", t[1].strip(), "\n")
                    eroare = 1

                elif t[2].strip() not in lstari:
                    print("Eroare la linia", i, "\nNu exista starea", t[2].strip(), "\n")
                    eroare = 1
                else:
                    if t[0].strip() not in tranzitii.keys():
                        tranzitii[t[0].strip()] = []
                        tranzitii[t[0].strip()].append((t[1].strip(), t[2].strip()))
                    elif (t[1].strip(), t[2].strip()) in tranzitii[t[0].strip()]:
                        print("Eroare la linia", i, "\nTranzitia (" + t[0].strip() + ", " +
                              t[1].strip() + ", " + t[2].strip() + ") a mai fost introdusa odata!\n")
                        eroare = 1
                    else:
                        tranzitii[t[0].strip()].append((t[1].strip(), t[2].strip()))

# print("tranzitii: ", tranzitii)
# print("stari finale: ", stari_finale)
# print("cuvinte: ", lcuvinte)
# print("stari: ", lstari)

if eroare == 0:
    print("Fisierul de intrare este valid! :)\n")


# fac transformarea din nfa in dfa
if eroare == 0:
    dfa_tranzitii = {}
    dfa_lstari = []
    coada = []
    stare_noua = 0

    # plec din starea initiala
    dfa_lstari.append(stare_initiala)
    coada.append(stare_initiala)
    while coada: # cat timp nu e vida
        # am treaba doar cu coada[0], dupa ii dau pop
        stare = coada[0]
        coada.pop(0)

        for c in lcuvinte:
            # calculez in ce stare ma duc din starea curenta cu cuvantul c
            stare_noua = 0
            if 0 <= int(stare) and int(stare) <= 9:  # e una dintre starile de la inceput
                if stare in tranzitii.keys():
                    for t in tranzitii[stare]:
                        if t[0] == c:
                            stare_noua = stare_noua * 10 + int(t[1])

            else: # e o stare compusa din doua sau mai multe stari mici
                #descompun starea asta compusa in stari mici
                stari_mici = [x for x in str(stare)]
                for st in stari_mici:
                    if st in tranzitii.keys():
                        for t in tranzitii[st]:
                            if t[0] == c:
                                stare_noua = stare_noua * 10 + int(t[1])


            stare_noua = in_ordine(stare_noua)
            # daca starea noua nu e nula
            if stare_noua != 0:
                stare_noua = str(stare_noua)
                # fac o tranzitie pentru dfa din starea curenta in starea noua cu c
                if stare not in dfa_tranzitii.keys():
                    dfa_tranzitii[stare] = []
                    dfa_tranzitii[stare].append((c, stare_noua))
                elif (c, stare_noua) not in dfa_tranzitii[stare]:
                    dfa_tranzitii[stare].append((c, stare_noua))

                # daca nu am mai verificat o pana acum o pun in coada
                if stare_noua not in dfa_lstari:
                    dfa_lstari.append(stare_noua)
                    coada.append(stare_noua)

    # print("tranzitii dfa: ", dfa_tranzitii)
    # print("stari dfa: ", dfa_lstari)

    # transform starile din "134" in "5" de ex
    dfa_afisare_stari = {}
    dfa_codificare = {}

    dfa_afisare_stari[stare_initiala] = '1' + ", S"
    dfa_codificare[stare_initiala] = '1'
    i = 1
    for s in dfa_lstari[1:]:
        i += 1
        dfa_codificare[s] = str(i)
        if eFinala(s):
            dfa_afisare_stari[s] = str(i) + ", F"
        else:
            dfa_afisare_stari[s] = str(i)

    # afisez dfa ul creat in fisier
    with open("nfa_in_dfa.txt", "w") as f:
        f.write("Sigma:\n")
        for cuv in lcuvinte:
            f.write("\t" + str(cuv) + "\n")
        f.write("End\n\n")

        f.write("States:\n")
        for s in dfa_lstari:
            f.write("\t" + dfa_afisare_stari[s] + "\n")
        f.write("End\n\n")

        f.write("Transitions:\n")
        for s in dfa_tranzitii.keys():
            for t in dfa_tranzitii[s]:
                f.write("\t" + dfa_codificare[s] + ", " + str(t[0]) + ", " + dfa_codificare[str(t[1])] + "\n")
        f.write("\n")





# # aici verific cuvintele pentru un dfa (adica lab 2 sau cv):
# if eroare == 0:
#     lcuvinte_citite = sys.argv[1:]
#     for c in lcuvinte_citite:
#         cuvant = c
#         st = stare_initiala
#         i = 0
#         gata = 0
#         while st not in stari_finale and i < len(cuvant) and gata == 0:
#             t = 0
#             ok = 0
#             while t < len(tranzitii[st]):
#                 if(tranzitii[st][t][0] == cuvant[i]): # verific daca tranzitia curenta e buna
#                     st = tranzitii[st][t][1]
#                     t = len(tranzitii[st]) + 1
#                     ok = 1 # am gasit o tranzitie
#                 t += 1 # trec la urmatoarea tranzitie
#
#             if ok == 0: # nu am gasit nicio tranzitie
#                 print("Cuvantul nu este acceptat!")
#                 gata = 1
#             i += 1
#         if gata == 0:
#             print("Cuvantul este acceptat!")

