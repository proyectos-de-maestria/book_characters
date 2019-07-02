import gender_guesser.detector as gender

from .preprocessing import spacy_names


class Correferents:

    def __init__(self, text):
        # Male homonyms
        self.male_title = ['mr.', 'sir', 'monsieur', 'captain', 'chief', 'master', 'lord', 'baron', 'mister', 'mr',
                           'prince', 'king']
        # Female homonyms
        self.female_title = ['mrs.', 'ms.', 'miss', 'lady', 'mademoiselle', 'baroness', 'mistress', 'mrs', 'ms',
                             'queen', 'princess', 'madam', 'madame']
        self.detector = gender.Detector()

        # base names for removing
        self.all_names = self.all_possible_names(spacy_names(text))

    def all_possible_names(self, names):
        res = {}
        # For each name, return a list with all possible names that contain it (including himself) and the gender
        for name in names:
            if name not in res.keys():
                res[name] = []
            for n in names:
                if n.find(name) != -1:
                    if n == "Elizabeth Bennet":
                        a = 0
                    ge = self.get_gender(n)
                    # res[name] = {"values": names[name], "gender": ge}
                    res[name].append((n, ge))
        return res

    def get_gender(self, name):
        splitted_name = name.split(' ')
        low_name = splitted_name[0].lower()
        if low_name in self.male_title:
            return "male"
        if low_name in self.female_title:
            return "female"
        return self.detector.get_gender(splitted_name[0])

    def remove_correferents(self, names_in_text, search_names):
        res = {}

        for name in names_in_text:
            sp_index = name.find(" ") + 1
            ge = self.get_gender(name)
            rest = name[sp_index:]
            if sp_index != 0:
                category = name[:sp_index-1]
                if category not in self.female_title and category not in self.male_title:
                    rest = category + rest
            f_name = self.full_name(rest, ge, search_names)
            res[f_name] = names_in_text[name] if f_name not in res.keys() else names_in_text[name] + res[f_name]
        return res

    def full_name(self, name, gen, search_names):
        possibles_names = [n for n, g in self.all_names[name] if g == gen and name != n]
        if len(possibles_names) == 1:
            return possibles_names[0]
        possibilities_in_text = [n for n in possibles_names if n in search_names]
        if len(possibilities_in_text) == 1:
            return possibilities_in_text[0]
        # multiple possibilities
        return name
