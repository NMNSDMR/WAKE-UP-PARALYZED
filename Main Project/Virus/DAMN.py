import multiprocessing
          
          
def f(_):
    while True:
        pass


if __name__ == '__main__':
    n = multiprocessing.cpu_count()
    with multiprocessing.Pool(n) as p:
        p.map(f, [None] * n)
