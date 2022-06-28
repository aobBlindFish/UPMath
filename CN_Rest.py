def cn_rest(a_list, r_list):
    #var security
    pass
    
    #u_list
    u_list = []
    new_u = 1
    for r1 in r_list:
        for r2 in r_list:
            if r2 != r1:
                new_u *= r2
        u_list.append(new_u)
        new_u = 1

    def rel_modulo(lg,sm):
        lg_copy = lg
        counter = 0
        while lg_copy >= sm:
            lg_copy = lg_copy - sm
            counter += 1
        return [counter, lg - counter*sm]

    def relation(a,b): #a,b müssen positiv & teilerfremd sein
        lg = a
        sm = b
        if a < b:
            lg = b
            sm = a
        
        rel_list = [None, None]
        lg_copy = lg
        while rel_list[1] != 1:
            rel_list = rel_modulo(lg_copy,sm)
            lg_copy += lg
        
        sm_factor = -rel_list[0]
        lg_factor = (lg_copy-lg)/lg

        return [1, lg_factor, lg, sm_factor, sm]
    
    output = 0

    for i in range(len(a_list)):
        output += a_list[i]*u_list[i]*relation(r_list[i],u_list[i])[1]

    #product r
    prod_r = 1
    for k in r_list:
        prod_r *= k

    #Darstellung
    while output > 0:
        output -= prod_r
    output = int(output + prod_r)


    print("\nx = " + str(output))
    print("Y = {" + str(output) + " + " + str(prod_r) + "*r | r in Z}")
    for i in range(len(r_list)):
        print(str(output) + " = " + str(int((output-a_list[i])/r_list[i])) + "*" + str(r_list[i]) + " + " + str(a_list[i]))

    print("Output:")
    return output
    
#input taken
input_str_r = input('Welche Werte gibt es für r1, ..., rk? Wenn die ri nicht paarweise teilerfremd sind, dann kommt kein (richtiges) Ergebnis heraus. Zurzeit können nur ri > 0 angenommen werden.\nAm besten genau in der Form "r1,r2,...,rk" angeben: ')
input_str_a = input('Welche Werte gibt es für a1, ..., ak? Zurzeit können nur ai > 0 angenommen werden.\nAm besten genau in der Form "a1,a2,...,ak" angeben: ')

#input checked
input_list_a = input_str_a.split(",")
input_list_r = input_str_r.split(",")
if len(input_list_a) != len(input_list_r):
    print("Die Menge der 'a's und 'r's müssen identisch sein.")
elif len(input_list_a) == 0 or len(input_list_r) == 0:
    print("Die Menge der 'a's und 'r's müssen Elemente beinhalten")
else:
    #input reworked
    list_a = []
    list_r = []
    try:
        for i in range(len(input_list_a)):
            list_a.append(int(input_list_a[i]))
            list_r.append(int(input_list_r[i]))
        
        print(cn_rest(list_a,list_r))
    except ValueError:
        print("Die Schreibweise der Zahlen wurde nocht verstanden. Hier sind ein paar Beispiellisten(für die Form):\n1,2,3,5\n12, 7,97\n22, 3,37, 7,11")