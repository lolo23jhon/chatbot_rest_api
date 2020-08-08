import tensorflow as tf
import numpy as np
import nltk 
import json
import random
import os

PATH = os.path.dirname(os.path.abspath(__file__))

class Chatbot:
  _stemmer = nltk.LancasterStemmer()
  INTENTS_FILENAME = os.path.join(PATH,"intents.json")
  MODEL_FILENAME = os.path.join(PATH, "model.h5")
  EXCLUDED_CHARACTERS = ('?')

  # Returns all the the data for responses from the intents file.
  # Must be the same the bot was trained on.
  @staticmethod
  def _load_intents_data(filename):
    data = {}
    with open(filename) as file:
      data = json.load(file)

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
      for pattern in intent["patterns"]:

        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
          labels.append(intent["tag"])

    words = [Chatbot._stemmer.stem(w.lower()) for w in words if w not in Chatbot.EXCLUDED_CHARACTERS]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    return (data, words, labels, docs_x, docs_y)

  # Create a one-hot enconded word bag
  @staticmethod
  def _word_bag(string, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(string)
    s_words = [Chatbot._stemmer.stem(w.lower()) for w in s_words] 

    for s in s_words:
      for i, w in enumerate(words):
        if w == s:
          bag[i] = 1
    
    bag = np.array(bag)
    bag = bag.reshape(1,max(bag.shape))
    return bag

  def __init__(self):
    self._data, self._words, self._labels, _, _ = Chatbot._load_intents_data(Chatbot.INTENTS_FILENAME)
    self._model = tf.keras.models.load_model(Chatbot.MODEL_FILENAME)

  # Returns the string of the response given by the bot
  def chat(self, input_msg):
    result = np.argmax(self._model.predict(Chatbot._word_bag(input_msg, self._words)))
    tag = self._labels[result]

    response = str()
    for intent in self._data["intents"]:
      if tag == intent["tag"]:
        response = random.choice(intent["responses"])

    return response