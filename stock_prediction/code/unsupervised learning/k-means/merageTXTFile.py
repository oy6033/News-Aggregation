#merage AALP.txt and AMZN.txt
filenames =  ["AAPL.txt","AMZN.txt"]
file = open('AAPL+AMZN.txt', 'w')


for filename in filenames:
    filepath = "C:/Users/Michael/PycharmProjects/CSE573/"
    filepath = filepath + filename
    for line in open(filepath):
        file.writelines(line)
    file.write('\n')

file.close()
