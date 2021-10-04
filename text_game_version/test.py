import itertools
from itertools import islice
from itertools import count


a = [i for i in filter(lambda x: x % 5, islice(count(5),10))]
print(a)