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

"""	org_index = 0
	usr_index = 0
	org_len = len(org_phrase)
	usr_len = len(usr_phrase)
	errors = abs(len(org_phrase) - len(usr_phrase))	

	while org_index < org_len:
		org_char = org_phrase[org_index]
		aux_errors = errors
		aux_index = usr_index

		#won't continue if usr_len is lt org_len 
		if org_index < usr_len:
			usr_char = usr_phrase[usr_index]

			if org_char != usr_char:
				#if it's the first element or the previous element it's right and it's the last element or the next element its right
				if ((usr_index == 0) or (usr_phrase[usr_index - 1] == org_phrase[org_index - 1])) and \
				((usr_index == len(usr_phrase) - 1) or (org_index == len(org_phrase) - 1) or (usr_phrase[usr_index + 1] == org_phrase[org_index + 1])):
						#then we supouse that the curren letter is the one wichs it's wrong
						errors += 1
				#else we look for the position where the strings match again
				else:
					while (org_char != usr_char) and (usr_index < usr_len - 1):
						errors += 1
						usr_index += 1
						usr_char = usr_phrase[usr_index]
				#if the strings don't match again 
				if usr_index == usr_len:
					errors = aux_errors + 1
					usr_index = aux_index + 1
				#if the strings match again
				else:
					#if the context say that this match is good
					if ((usr_index == 0) or (usr_phrase[usr_index - 1] == org_phrase[org_index - 1])) and \
					((usr_index == len(usr_phrase) - 1) or (org_index == len(org_phrase) - 1) or (usr_phrase[usr_index + 1] == org_phrase[org_index + 1])):
						usr_index += 1
					else:
						errors = aux_errors + 1
						usr_index = aux_index + 1
			else:
				usr_index += 1

		org_index += 1"""