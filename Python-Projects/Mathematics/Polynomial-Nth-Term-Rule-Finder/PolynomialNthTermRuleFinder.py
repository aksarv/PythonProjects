import os
print('Keep entering the terms of your sequence in order. Please ensure it is a polynomial sequence, e.g., a quadratic, cubic, etc. When you are done, enter s to stop entering terms and to calculate the nth term rule.')
terms = []
def differences(arr):
  diff = []
  for x in range(1, len(arr)):
    diff.append(arr[x] - arr[x - 1])
  return diff
while True:
  term = input('Enter term: ')
  if term == 's':
    break
  else:
    terms.append(float(term))
def factorial(n):
  if n == 0:
    return 1
  result = 1
  for i in range(1, n+1):
    result *= i
  return result
formula = []
copy = terms[:]
copy1 = terms[:]
iterations = 0
while True:
  differencesnum = 0
  while True:
    copy = [round(x, 5) for x in differences(copy)]
    differencesnum += 1
    if len(list(set(copy))) == 1:
      coefficient = copy[0]/factorial(differencesnum)
      highestpower = differencesnum
      formula.append([coefficient, highestpower])
      break
  remainder = [round(copy1[x-1]-coefficient*x**highestpower, 5) for x in range(1, len(copy1)+1)]
  if len(list(set(remainder))) == 1:
    formula.append(remainder[0])
    break
  else:
    copy = remainder[:]
    copy1 = remainder[:]
  iterations += 1
  if iterations > 1000:
    os.system('clear')
    print('Unfortunately, there was something wrong with your sequence, and the program could not identify the nth term rule for the sequence. \nYou may have entered a geometric sequence instead of an arithmatic sequence, or did not provide enough terms to discern a distinct nth term rule, or may not have entered a sequence at all. \nIn general, for an nth term rule for a polynomial where the highest power is x, you should provide at least x+2 terms so that the second difference can be identified.')
    quit()
print('The nth term rule for this polynomial sequence is:')
for x in formula[:-1]:
  print(f'{x[0]}x^{x[1]}', end=' + ')
print(formula[-1])
