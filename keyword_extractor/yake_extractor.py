import yake

def extract_keywords(text:str) -> tuple[int,str]:
    """Extrae las keywords de una palabra

    Args:
        text (str): El texto de donde extraer las keywords

    Returns:
        tuple[int,str]: Devuelve el score y la palabra extraida
    """

    keyword_extractor = yake.KeywordExtractor(n=3, top=13)
    keywords = keyword_extractor.extract_keywords(text)
    return keywords

def find_keyword_in_json(json:list[dict], phrase_to_search:int):

    for index, word in enumerate(json):
    
        current_word = word["word"]

        split_words = phrase_to_search.split()
        first_word_to_search = split_words[0]

        if current_word != first_word_to_search:
            continue
        else:
            try: 
                if json[index+1]["word"] != split_words[1]:
                    continue
                else:
                    return word
            except IndexError:
                return word
