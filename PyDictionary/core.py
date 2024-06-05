from __future__ import print_function
import sys, re, goslate
try:
    from .utils import _get_soup_object
except:
    from utils import _get_soup_object

python2 = False
if list(sys.version_info)[0] == 2:
    python2 = True

class PyDictionary(object):

    def __init__(self, *args):
        try:
            if isinstance(args[0], list):
                self.args = args[0]
            else:
                self.args = args
        except:
            self.args = args
        """Initializes an object of the PyDictionary class.

                        Parameters
                        ------------
                        object: :class:`tuple`
                            The words included in the dictionary instance.
                        """

    
    def printMeanings(self):
        dic = self.getMeanings()
        for key in dic.keys():
            print(key.capitalize() + ':')
            for k in dic[key].keys():
                print(k + ':')
                for m in dic[key][k]:
                    print(m)
        """Prints the meanings of the words in the class instance in the terminal."""

    def printAntonyms(self):
        antonyms = dict(zip(self.args,self.getAntonyms(False)))
        for word in antonyms:
            print(word+':')
            print(', '.join(antonyms[word]))
        """Prints the antonyms of the words in the class instance in the terminal."""

    def printSynonyms(self):
        synonyms = dict(zip(self.args,self.getSynonyms(False)))
        for word in synonyms:
            print(word+':')
            print(', '.join(synonyms[word]))
        """Prints the synonyms of the words in the class instance in the terminal."""

    def getMeanings(self):
        out = {}
        for term in self.args:
            out[term] = self.meaning(term)
        return out
        """Returns the meanings of the words in the class instance in the terminal."""

    def translateTo(self, language):
        return [self.translate(term, language) for term in self.args]
        """Returns the translations of the words in the class instance.
    
                            Parameters
                            ------------
                            language: :class:`Any`
                                The language to translate the words to.
                            """

    def translate(self, term, language):
        if len(term.split()) > 1:
            print("term must be only a single word")
        else:
            try:
                gs = goslate.Goslate()
                word = gs.translate(term, language)
                return word
            except:
                print("Invalid parameter")
        """Returns the translation of the word passed as an argument.
    
                            Parameters
                            ------------
                            term: :class:`str`
                                The word to return the translation of.
                            language: :class:`Any`
                                The language to translate the word to.
                            """

    def getSynonyms(self, formatted=True):
        return [self.synonym(term, formatted) for term in self.args]
        """Returns the synonyms of the words in the class instance.
    
                            Parameters
                            ------------
                            term: :class:`str`
                            The word to return the synonyms for.
                            formatted: :class:`bool`
                            Formats and returns the tuple.
                            """

    def __repr__(self):
        return "<PyDictionary Object with {0} words>".format(len(self.args))

    def __getitem__(self, index):
        return self.args[index]

    def __eq__(self):
        return self.args

    def getAntonyms(self, formatted=True):
        return [self.antonym(term, formatted) for term in self.args]

    @staticmethod
    def synonym(term, formatted=False):
        if len(term.split()) > 1:
            print("term must be only a single word")
        else:
            try:
                data = _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
                section = data.find('div', {'class': 'section-list-wrapper', 'data-section': 'synonyms'})
                spans = section.findAll('a')
                synonyms = [span.text.strip() for span in spans]
                if formatted:
                    return {term: synonyms}
                return synonyms
            except:
                print("{0} has no synonyms in the API".format(term))
        """Returns synonyms of the word passed as an argument.

                                    Parameters
                                    ------------
                                    term: :class:`str`
                                    The word to return the synonyms for.
                                    formatted: :class:`bool`
                                    Formats and returns the tuple.
                                    """

    @staticmethod
    def antonym(term, formatted=False):
        if len(term.split()) > 1:
            print("term must be only a single word")
        else:
            try:
                data = _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
                section = data.find('div', {'class': 'section-list-wrapper', 'data-section': 'antonyms'})
                spans = section.findAll('a')
                antonyms = [span.text.strip() for span in spans]
                if formatted:
                    return {term: antonyms}
                return antonyms
            except:
                print("{0} has no antonyms in the API".format(term))
        """Returns antonyms of the word passed as an argument.

                                    Parameters
                                    ------------
                                    term: :class:`str`
                                    The word to return the antonyms for.
                                    formatted: :class:`bool`
                                    Formats and returns the tuple.
                                    """

    @staticmethod
    def meaning(term, disable_errors=False):
        if len(term.split()) > 1:
            print(f"Meaning command run with parameter {term}. Returned no results as term was not a single word.")
        else:
            try:
                html = _get_soup_object("http://wordnetweb.princeton.edu/perl/webwn?s={0}".format(
                    term))
                types = html.findAll("h3")
                length = len(types)
                lists = html.findAll("ul")
                out = {}
                for a in types:
                    reg = str(lists[types.index(a)])
                    meanings = []
                    for x in re.findall(r'\((.*?)\)', reg):
                        if 'often followed by' in x:
                            pass
                        elif len(x) > 5 or ' ' in str(x):
                            meanings.append(x)
                    name = a.text
                    out[name] = meanings
                return out
            except Exception as e:
                if disable_errors == False:
                    print("Error: The following error occurred: %s" % e)
        """Returns the definition of the word passed as an argument.

                Parameters
                ------------
                term: :class:`str`
                    The word to return a definition for.
                disable_errors: :class:`bool`
                    Disables error messages in cases where the passed
                    argument is longer than a single word or there are
                    no results.
                """

if __name__ == '__main__':
    d = PyDictionary('honest','happy')
    d.printSynonyms()

