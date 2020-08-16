import random as rng

writeout =""
while(True):
    for i in range(0,35):
        writeout = writeout + str(rng.randint(0,1))
    print(writeout)
