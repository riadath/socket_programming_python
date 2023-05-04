my_dictionary = {'c1':'Red','c2':'Green','c3':None,'c4':'White','c5':'Black'}

#delete all entries with value None
my_dictionary = {
    key:val for key, val in my_dictionary.items() if val != None}
print(my_dictionary)