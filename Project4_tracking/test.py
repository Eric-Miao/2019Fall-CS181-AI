import inference

def test1():
  dist = inference.DiscreteDistribution()
  dist['a'] = 1
  dist['b'] = 2
  dist['c'] = 2
  dist['d'] = 0
  dist.normalize()
  print(list(sorted(dist.items())))
  dist['e'] = 4
  print(list(sorted(dist.items())))

  empty = inference.DiscreteDistribution()
  empty.normalize()
  print(empty)

def test2():
  dist = inference.DiscreteDistribution()
  dist['a'] = 1
  dist['b'] = 2
  dist['c'] = 2
  dist['d'] = 0
  N = 100000.0
  samples = [dist.sample() for _ in range(int(N))]
  print(round(samples.count('a') * 1.0/N, 1))  # proportion of 'a'
  print(round(samples.count('b') * 1.0/N, 1))
  print(round(samples.count('c') * 1.0/N, 1))
  print(round(samples.count('d') * 1.0/N, 1))

test1()
test2()