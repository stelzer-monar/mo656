import spacy 
from owlready2 import *

onto = get_ontology("newOntology")

with onto:
  class Drug(Thing):
    pass
  class Ingredient(Thing):
    pass
  class Action(Thing):
    pass
  class Use(Thing):
    pass
  class isComposedOf(ObjectProperty):
    domain    = [Drug]
    range     = [Ingredient]
  class isUsedFor(ObjectProperty):
    domain    = [Drug]
    range     = [Use]
  class actAs(ObjectProperty):
    domain    = [Drug]
    range     = [Action]


nlp = spacy.load("./ner_component/output/model-best")
text = [
'''
    Dipirona é um ótimo analgésico para combater a dor.
    doril contém dipirona e é indicado para dor de cabeça.
'''
]

entities = {}

drug = Drug("doril")
for doc in nlp.pipe(text, disable=["tagger"]):
  for ent in doc.ents:
    print(ent.text, ent.label_)
    if ent.label_ == "INGREDIENT":
      if ent.text not in entities:
        entities[ent.text] = Ingredient(ent.text)
      drug.isComposedOf.append(entities[ent.text])
    elif ent.label_ == "ACTION":
      if ent.text not in entities:
        entities[ent.text] = Action(ent.text)
      drug.actAs.append(entities[ent.text])
    elif ent.label_ == "USE":
      if ent.text not in entities:
        entities[ent.text] = Use(ent.text)
      drug.isUsedFor.append(entities[ent.text])
  #print([(ent.text, ent.label_) ])

onto.save(file = "ontology.owl")