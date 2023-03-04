import stockReader as sr


def stockRunner():
    data = sr.readAllFileStocks()
    print(data)
    print('\n\n', len(data))
