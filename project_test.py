import spacy 
from owlready2 import *
import glob
from PyPDF2 import PdfReader

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
    dorflex® (dipirona  monoidratada + citrato  de orfenadrina + cafeína anidra)   sanofi medley  farmacêutica  ltda.  comprimido 300mg + 35mg + 50mg    1  dorflex ® dipirona monoidratada  citrato de orfenadrina  cafeína anidra   apresentaç ões  comprimidos  300 mg + 35 mg + 50 mg: embalagem com 24, 36, 50 ou 300.  uso oral. uso adulto .  composição  cada comprimido contém  300 mg de dipirona monoidratada, 35 mg de citrato de orfenadrina  (equivalente a 20,4 mg de orfenadrina base ) e 50 mg de cafeína anidra.  excipientes : amido de milho, amidoglicolato  de sódio, talco e estearato de magnésio.   1. para que  este medicamento é indicado?  dorflex  é indicado no alívio da dor associada a contraturas musculares , incluindo  dor de cabeça tensional .   2. como este medicamento funciona?  dorflex possui ação analgésica e relaxante muscular.  o início da ação ocorre a partir de 30 minutos.    3. quando não devo usar este medicamento?  dorflex não deve ser utilizado  nos seguintes casos:  - reações alérgicas, tais como reações cutâneas graves  com este medicamento ; - alergia ou intolerância a qualquer um dos componentes da fórmula  ou a analgésicos semelhantes à dipirona –  derivados de pirazolonas (ex.: fenilbutazona, oxifembutazona)  ou a pirazolidinas (ex.: fenilbutazona, oxifembutazona)  – incluindo, por exemplo, casos anteriores de agranulocitose (diminuição acentuada na contagem de leucócitos do sangue – glóbulos brancos) em relação a um destes medicamentos ; - glaucoma  (aumento da pressão intraocular) , obstrução pilórica ou duodenal  (estreitamento da passagem  do conteúdo no estômago e  intestino) , problemas motores no  esôfago (megaesôfago), úlcera péptica estenosante (estreitamento anormal), hipertrofia prostática ( aumento da próstata ), obstrução do colo da bexiga e miastenia grave (doença neuromuscular que causa fraqueza);  - porfiria  hepática aguda intermitente - doença metabólica que se manifesta através de problemas na pele e/ou com complicaçõesdorflex® (dipirona  monoidratada + citrato  de orfenadrina + cafeína anidra)   sanofi medley  farmacêutica  ltda.  comprimido 300mg + 35mg + 50mg    1  dorflex ® dipirona monoidratada  citrato de orfenadrina  cafeína anidra   apresentaç ões  comprimidos  300 mg + 35 mg + 50 mg: embalagem com 24, 36, 50 ou 300.  uso oral. uso adulto .  composição  cada comprimido contém  300 mg de dipirona monoidratada, 35 mg de citrato de orfenadrina  (equivalente a 20,4 mg de orfenadrina base ) e 50 mg de cafeína anidra.  excipientes : amido de milho, amidoglicolato  de sódio, talco e estearato de magnésio.   1. para que  este medicamento é indicado?  dorflex  é indicado no alívio da dor associada a contraturas musculares , incluindo  dor de cabeça tensional .   2. como este medicamento funciona?  dorflex possui ação analgésica e relaxante muscular.  o início da ação ocorre a partir de 30 minutos.     
'''
]


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