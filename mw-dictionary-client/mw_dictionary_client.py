# built-ins
import json

# PyPI packages
from bs4 import BeautifulSoup
import requests

# Constants
MAX_RETRY = 3


class MWDictionaryClient():

    """
    Wrapper and convenience functions for dictionary functions of Google search.
    """
    BASE_URL = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"

    def __init__(self, key):
        self.SEARCH_URL = self.BASE_URL + "%s" + "?key=%s" % key
        self.session = requests.Session()

    def _run_search(self, search):
        """
        Request URL based on search object, return raw results.
        """
        search_url = self.SEARCH_URL % search["word"]
        retry = 0
        while retry < MAX_RETRY:
            try:
                resp = self.session.get(search_url)
            except requests.exceptions.ConnectionError:
                retry += 1
                if retry < MAX_RETRY:
                    continue
            else:
                break
        return self._parse_search_results(BeautifulSoup(resp.text), search)

    def _parse_search_results(self, soup, search):
        """
        Parse search results based on search object preferences.
        """
        dictionary_entries = soup.find_all("entry")
        entries = []
        for entry in dictionary_entries:
            entry_word = entry.find("ew").get_text()
            if entry_word == search["word"]:
                entry_dict = {
                    "meanings": {}
                }
                meanings = entry.find_all("dt")
                for i, meaning in enumerate(meanings):
                    entry_dict["meanings"].update({i: self._clean_entry(meaning.get_text())})
                    if search["top_result"]:
                        break
                if search["part-of-speech"]:
                    entry_dict.update({"part-of-speech": entry.find("fl").get_text()})
                if search["etymology"]:
                    entry_dict.update({"etymology": entry.find("et").get_text()})
                if search["phonetic"]:
                    entry_dict.update({"phonetic": entry.find("pr").get_text()})
                entries.append(entry_dict)
        return {"results": entries}

    def _clean_entry(self, entry):
        """
        Clean up entry (entirely cosmetic)
        """
        return entry.replace(":", "", 1).replace(" :", "; ")

    def search(self, word, part_of_speech=True, phonetic=True, etymology=False, top_result=True):
        """
        Get Google dictionary search results based on word.

        Flags for part_of_speech and phonetic specify whether or not to include those
        results in the return object.
        """
        search = {
            "word": word,
            "part-of-speech": part_of_speech,
            "phonetic": phonetic,
            "etymology": etymology,
            "top_result": top_result
        }
        return self._run_search(search)


def main():
    """
    Test and example usage.
    """
    from secrets import MIRRIAMWEBSTER_DICT_KEY
    dictionary_client = MWDictionaryClient(MIRRIAMWEBSTER_DICT_KEY)
    search = dictionary_client.search("love", top_result=False, etymology=True)
    print(json.dumps(search, indent=4))

if __name__ == "__main__":
    main()
