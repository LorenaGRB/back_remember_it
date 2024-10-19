def sentence_data(sentence):
    return{
        "sentence": sentence["sentence"] ,
        "date": sentence["date"]
    }

def word_data(word):
    return{
        "id": str(word["_id"]),
        "name": word["name"],
        "context": word["context"],
        "sentences": [sentence_data(sentence) for sentence in word["sentences"]] ,
    }

def all_words(words):
    return [word_data(word) for word in words]