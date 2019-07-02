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
        self.all_names = self.remove_title(spacy_names(text))

    def remove_title(self, names):
        res = {}
        for name in names:
            ge = self.get_gender(name)
            res[name] = {"values": names[name], "gender": ge}
        return res

    def get_gender(self, name):
        splitted_name = name.split(' ')
        if splitted_name[0] in self.male_title:
            return "male"
        if splitted_name[0] in self.female_title:
            return "female"
        if len(splitted_name) > 1:
            return self.detector.get_gender(splitted_name[1])
        return "unknown"

    def remove_correferents(self, names_in_text):
        res = {}

        for name in names_in_text:
            sp_index = name.find(" ") + 1
            if sp_index != 0:
                ge = self.get_gender(name)
                category = name[:sp_index-1]
                rest = name[sp_index:]
                if category not in self.female_title and category not in self.male_title:
                    rest = category + rest
                f_name = self.full_name(rest, ge)
                res[f_name] = names_in_text[name] if f_name not in res.keys() else names_in_text[name] + res[f_name]
        return res

    def full_name(self, name, gen):
        best_match = ""
        for n in self.all_names:
            if n.find(name) != -1 and gen == self.all_names["gender"] and len(n) > len(best_match):
                best_match = n
        return best_match
