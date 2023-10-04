import spacy

nlp = spacy.load("./output/model-best")
text = [
'''
    Dipirona é um ótimo analgésico para combater a dor.
    doril contém dipiron e é indicado para dor de cabeça.
'''
]
for doc in nlp.pipe(text, disable=["tagger", "parser"]):
    print([(ent.text, ent.label_) for ent in doc.ents])