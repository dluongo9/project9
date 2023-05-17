import collections
from collections import defaultdict

import collections
import re
import string

freq_list = {}
word_freq = collections.Counter()
corpus_vocabulary = dict()
user_vocabulary = set()


class Word:
    def __init__(self, shape):
        self.shape = shape
        self.example_sentences = []

    def add_sentence(self, sentence):
        self.example_sentences.append(sentence)

    def __eq__(self, other):
        return self.shape == other.shape

    def __repr__(self):
        return self.shape

    def __hash__(self):
        return hash(self.shape)


class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence
        self.words = sentence_to_words(self, sentence)

    def __repr__(self):
        return "<" + self.sentence + ">"# + "\n" + "words: " + str(self.words)


def main():
    sentences = {"Hello", "Hello, Martin", "Hello, Mr. Martin", "man", "a man", "Mr. Martin is a man",
                 "Dr. Martin is a Martin man", "gone walking"}

    with open("BlackSwan_eng_ara.txt", encoding="utf-8") as opened_file:
        lines = opened_file.readlines()
        sentences = []
        for line in lines:
            line = line.split("\t")
            if len(line[1]) != 0:
                sentences.append(line[1])
        print(sentences)

    process_sentences(sentences)
    print("corpus vocabulary before ordering sentences: " + str(corpus_vocabulary))
    result = order_sentences()
    print("user vocabulary: " + str(user_vocabulary))
    print("sentence order: " + str(result))
    #result = n_plus_one_sentences(sentences)


def order_sentences():
    order = []
    unknown_limit = 0
    while len(user_vocabulary) < len(corpus_vocabulary):
        unknown_limit += 1
        print("current unknown word limit: " + str(unknown_limit))
        for candidate in word_freq.most_common():
            print("candidate to check: " + str(candidate))
            if candidate[0] not in user_vocabulary:
                print("not yet in user vocabulary")
                audit_result = audit_candidate(candidate[0], unknown_limit)
                print("is it n + " + str(unknown_limit) + "? " + str(audit_result))
                if audit_result is not False:
                    user_vocabulary.add(audit_result[0])
                    order.append(audit_result[1])
                    print(order)
                    unknown_limit = 0
                    break
            else:
                print("already in user vocabulary")

        print("finished iterating through candidates")

    return order


def audit_candidate(candidate_word: Word, unknown_limit):
    for sentence in candidate_word.example_sentences:
        unknown_count = 0
        for word in sentence.words:
            if word not in user_vocabulary:
                unknown_count += 1
        if unknown_count == unknown_limit:
            return candidate_word, sentence
    return False


def process_sentences(sentences):
    for sentence in sentences:
        sentence_obj = Sentence(sentence)
        print(sentence_obj)


def pick_candidate_sentences(sentences, known_words):
    candidates = defaultdict()
    for sentence in sentences:
        print(sentence)
        unknown_word_count = 0
        unknown_words = set()
        for word in sentence.split():
            if word not in known_words:
                unknown_word_count += 1
                unknown_words.add(word)
        print(unknown_words)
        #print(candidates)
        if candidates.get(unknown_word_count) is not None:
            candidates[unknown_word_count] += [(sentence, unknown_words)]
        else:
            candidates[unknown_word_count] = [(sentence, unknown_words)]
    sort = sorted(candidates.items())
    print(sort)
    return sort[0][1]


def n_plus_one_sentences(sentences):
    # Use the translate() method to remove punctuation from input_string
    translator = str.maketrans('', '', string.punctuation)

    # Count the frequency of each word in the sentences
    word_freq = collections.Counter([word.translate(translator).lower() for sent in sentences for word in
                                     sent.split()])
    print(word_freq)

    known_words = {}

    # while len(sentences) > 0:
    candidates = pick_candidate_sentences(sentences, known_words)
    print("candidates")
    print(candidates)

    new_words_in_candidates = [candidate[1] for candidate in candidates]
    print(new_words_in_candidates)
    next_sentence = candidates[max([word_freq[candidate] for candidate in candidates])]
    print(next_sentence)



    # Initialize the list of n+1 sentences
    n_plus_one_sents = []

    for word in word_freq:
        print(word)

    #
    # # Iterate over the remaining sentences
    # for sent in sentences[1:]:
    #     # Get the set of known words from previous sentences
    #     known_words = set([word.lower() for prev_sent in n_plus_one_sents for word in prev_sent.split()])
    #
    #     # Split the current sentence into words
    #     words = sent.split()
    #
    #     # Find the first word that is not already known
    #     new_word = None
    #     for word in words:
    #         if word.lower() not in known_words:
    #             new_word = word
    #             break
    #
    #     # If there is no new word, skip this sentence
    #     if new_word is None:
    #         continue
    #
    #     # Find the most frequent unknown word
    #     new_word_counts = [(w, word_freq[w.lower()]) for w in words if w.lower() not in known_words]
    #     new_word_counts.sort(key=lambda x: x[1], reverse=True)
    #     if len(new_word_counts) == 0:
    #         continue
    #     most_frequent_unknown_word = new_word_counts[0][0]
    #
    #     # If the new word is the most frequent unknown word, add the sentence
    #     if new_word.lower() == most_frequent_unknown_word.lower():
    #         # Highlight the new word in the sentence
    #         highlighted_sent = sent.replace(new_word, f"[{new_word}]")
    #
    #         # Add the sentence to the n+1 list
    #         n_plus_one_sents.append(highlighted_sent)

    return n_plus_one_sents


class Candidate:
    def __init__(self, new_words, sentence, known_words):
        self.new_words = set()
        self.sentence = sentence

    def update(self, learned_word):
        self.new_words.remove(learned_word)


class Vocabulary:
    def __init__(self, new_words, sentences, known_words):
        self.sentences = set()
        self.sentence = sentence


def sentence_to_words(sentence_obj, sentence):
    translator = str.maketrans('', '', string.punctuation)
    words = [word.translate(translator).lower() for word in sentence.split()]
    result_words = []
    for word in words:
        if word in corpus_vocabulary:
            corpus_vocabulary[word].add_sentence(sentence_obj)
        else:  # add word and sentence to corpus vocabulary
            word_obj = Word(word)
            word_obj.add_sentence(sentence_obj)
            corpus_vocabulary[word] = word_obj
        result_words.append(corpus_vocabulary[word])
    word_freq.update(result_words)
    return result_words


if __name__ == "__main__":
    main()

#print(result)
