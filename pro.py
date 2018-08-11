from multiprocessing import Pool

def f(n):
	return n*n


p = Pool()
print(p.map(f,range(100000)))
