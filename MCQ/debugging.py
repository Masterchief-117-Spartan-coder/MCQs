lister = []
num = []
dic_lul = {"â€“": "-", "Ã—": "X", "  ": " x ",  " –": " - ", "Ï„": "(torque)", "Î»": "(lambda)",
           "(a)": "(A)", "(b)": "(B)", "(c)": "(C)", "(d)": "(D)", "μ0": "(Epsilon naught)",
           "a)": "(A)", "b)": "(B)", "c)": "(C)", "d)": "(D)",
           "Ï€": "(Pi)", "â†’": "->", "Â±": "(+-)", "ï»¿": "",
           "Î±": "(alpha)", "Î": "(alpha)", "µ": "(Epsilon)", "(alpha)¼0": "(Epsilon naught)",
           "(alpha)¼o": "(Epsilon naught)", "Â(Epsilon)": "(micro)", "(alpha)¸": "(Theta)",
           "(alpha)©": "(ohm)", "(alpha)£": "(Sigma)", "(alpha)¦": "(Phi)", "Â°": "(degree)", "(alpha)”": "(Delta)",
           "(alpha)²": "(Beta)", "Â²": "^2",}
with open("data_physics_exampler.txt") as text:
    text_vomit = text.read().splitlines()
    for i in text_vomit:
        for k in dic_lul:
            i = i.replace(k, dic_lul[k])
        num.append(i)
        print(num)
text.close()
# print(text_vomit)
for i in num:
    # print(i)
    string = i.encode("ascii", errors="ignore")
    string.decode()
    for j in range(len(dic_lul)):
        str(string).replace(list(dic_lul.keys())[j], list(dic_lul.values())[j])
    lister.append(((str(string)).lstrip('b\'')).rstrip("'"))
# print(lister[(lister.index("46")):(lister.index("46"))+6])
print(lister)
for i in lister:
    print(i)
