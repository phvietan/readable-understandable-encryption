import os
import json
from cipher import FakeCipher
from random import seed
from random import randint

seed(os.urandom(32))

def get(model, val):
  try:
    res = model[val]
  except:
    res = 0
  return res

def get_trigrams_probability(corpus):
  content = open(corpus, 'r').read().split(' ')
  model, t = {}, {}

  for i in range(len(content)-2):
    w1, w2, w3 = content[i], content[i+1], content[i+2]
    model[(w1, w2, w3)] = get(model, (w1, w2, w3)) + 1
    t[(w1, w2)] = get(t, (w1, w2)) + 1

  for w1_w2_w3 in model:
    w1, w2, w3 = w1_w2_w3
    total_count = get(t, (w1,w2))
    model[w1_w2_w3] /= (total_count+0.0)

  return model

def evaluateText(text, model):
  tmp = text.split(' ')
  text = []
  for val in tmp:
    if val != '': text.append(val)
  sumProb = 0
  for i in range(len(text)-2):
    w1, w2, w3 = text[i], text[i+1], text[i+2]
    sumProb += get(model, (w1, w2, w3))
  return (sumProb+0.0)/(len(text)-2.0)

def evaluateParagraph(paragraph, model):
  paragraph = paragraph.lower()
  tmp = paragraph.split('.')
  texts = []
  for val in tmp:
    if val != '': texts.append(val)
  sumProb = 0
  for t in texts:
    sumProb += evaluateText(t, model)
  return (sumProb+0.0)/(len(texts)+0.0)

def evaluateRealSentences(filename, model):
  print('=====================')

  content = open(filename, 'r').read()
  prob = 0
  for i in range(10):
    value = randint(0, len(content)-50)
    prob += evaluateParagraph(content[value:value+50], model)
  print('Evaluating real sentences on', filename)
  return print((prob+0.0) / 10.0)

def evaluateCiphertext(wordlist, model):
  print('=====================')
  key = os.urandom(32)
  cipher = FakeCipher(key, wordlist)

  message = 'Nạp cho tôi 20k. Password là alo123 nha!'
  c = cipher.encrypt(message)

  print('Evaluating ciphertext:')
  print(c)

  print(evaluateParagraph(c, model))

model = get_trigrams_probability('corpus.txt')

# Evaluate on real sentences
evaluateRealSentences('corpus.txt', model)

# Evaluate ciphertext on subset of corpus
evaluateCiphertext('another.txt', model)

# Evaluate on real sentences
evaluateRealSentences('news-20k-words.txt', model)

# Evaluate ciphertext on related articles of corpus (both files contain news article on e-news website)
evaluateCiphertext('news-20k-words.txt', model)

# Evaluate on real sentences
evaluateRealSentences('literature.txt', model)

# Evaluate ciphertext on a non-related article. Here we use literature on truyen-full
evaluateCiphertext('literature.txt', model)
