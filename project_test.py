import spacy 
from owlready2 import *
import glob
from PyPDF2 import PdfReader

onto = get_ontology("OntoMedBR")

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

entities = {}
for bula in glob.glob("dataset/*.pdf"):
  drugName = bula.split("/")[-1][:-4]
  drug = Drug(drugName)
  print(drugName)
  reader = PdfReader(bula)
  text = ""
  for page in reader.pages:
      text+=page.extract_text()
  text = text.replace("\n", "").replace(".", "").lower().strip()[:2000]
  #print(text)
  for doc in nlp.pipe([text], disable=["tagger"]):
    for ent in doc.ents:
      #print(ent.text, ent.label_)
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
print(entities.keys())
onto.save(file = "ontology.owl")

with onto:
  sync_reasoner()