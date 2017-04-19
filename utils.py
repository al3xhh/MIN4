# -*- coding: utf-8 -*-

import difflib

def get_failed_words(org_phrase, usr_phrase):
	org_words = org_phrase.split()
	usr_words = usr_phrase.split()
	n_errors = 0

	for i, j in zip(org_words, usr_words):
		if len(i) == len(j):
			for a, b in zip(i, j):
				if a != b:
					n_errors = n_errors + 1
					continue
		else:
			n_errors = n_errors + 1

	return n_errors

def get_num_failed_chars(org_phrase, usr_phrase):
	org_phrase = org_phrase.strip().split()
	usr_phrase = usr_phrase.strip().split()
	errors = 0

	for org_word, usr_word in zip(org_phrase, usr_phrase):
		errors += find_word_errors(org_word, usr_word)

	return errors

def find_word_errors(org_word, usr_word):
	size = 0
	s = difflib.SequenceMatcher(None, org_word, usr_word)
	matches = s.get_matching_blocks()

	for i in matches:
			size += i.size

	return max(len(org_word), len(usr_word)) - size

def find_accent_marks(org_phrase):
    words = org_phrase.strip().split()
    accent_letters = ["á", "é", "í", "ó", "ù", "Á", "É", "Í", "Ó", "Ú"].encode('utf8')
    accent_marks = [0] * len(words)
    i = 0

    for word in words:
        for letter in accent_letters:
            if letter in word:
                accent_marks[i] = 1
                break
        i += 1

    return accent_marks

def find_question_marks(org_phrase):
    return "?" in org_phrase

def find_exclamation_marks(org_phrase):
    return "!" in org_phrase

def find_punctuation_marks(org_phrase, find):
    words = org_phrase.strip().split()
    punctuation = [0] * len(words)
    i = 0

    for word in words:
        if find in word:
            punctuation[i] = 1
        i += 1

    return punctuation
