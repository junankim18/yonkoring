a = '#1 #2 #3'
a.split('#')
interest_num = len(a.split('#'))
for i in range(interest_num):
    globals()["new_interest{}".format(i)] = a.split('#')[i]
    print(globals()["new_interest{}".format(i)])
