import json
import createAndSearchCorpus

corpus1 = createAndSearchCorpus.short_desc
#corpus2 = json.dumps(createAndSearchCorpus.short_desc)


def probier_mal_das(suchstring):

    result = createAndSearchCorpus.all_values_containing_substring(corpus1, suchstring)
    result_json = json.dumps(result)

    return result_json
