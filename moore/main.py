# citirea datelor:

tranzitii = {}
cuvinte = []
with open("input.txt", "r") as f:
    fisier = f.readlines()

    n = int(fisier[0].split()[0])
    m = int(fisier[0].split()[1])
    codificare = fisier[1].split()

    # tranzitiile
    for i in range(2, m + 2):
        s1 = fisier[i].split()[0]
        s2 = fisier[i].split()[1]
        cuv = fisier[i].split()[2]

        if s1 not in tranzitii.keys():
            tranzitii[s1] = []
            tranzitii[s1].append((s2, cuv))
        else:
            tranzitii[s1].append((s2, cuv))

    stare_initiala = fisier[m + 2].split()[0]
    stari_finale = fisier[m + 3].split()
    cuvinte = [fisier[i].split()[0] for i in range(m + 5, len(fisier))]

# print(n)
# print(m)
# print(codificare)
# print(tranzitii)
# print(stare_initiala)
# print(stari_finale)
# print(cuvinte)

for c in cuvinte:
    st = stare_initiala
    i = 0
    gata = 0
    traseu = []
    while st not in stari_finale and i < len(c) and gata == 0:
        litera = c[i]
        t = 0
        ok = 0
        while t < len(tranzitii[st]):
            if tranzitii[st][t][1] == litera:  # verific daca tranzitia curenta e buna
                st = tranzitii[st][t][0]
                traseu.append(st)
                t = len(tranzitii[st]) + 1
                ok = 1  # am gasit o tranzitie
            t += 1  # trec la urmatoarea tranzitie

        if ok == 0:  # nu am gasit nicio tranzitie
            gata = 1
        i += 1

    if st not in stari_finale:
        print("NU\n")
    else:
        print("DA")
        print(c, end = " -> ")
        for i in traseu:
            print(codificare[int(i)], end = " ")
        print("\n")


