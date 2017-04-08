
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