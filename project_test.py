import random 

import typer 

from pathlib import Path 

import spacy 
from spacy.tokens import DocBin, Doc 

from spacy.training.example import Example 
from rel_component.scripts.rel_pipe import make_relation_extractor, score_relations 
from rel_component.scripts.rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

#We load the relation extraction (REL) model

nlp2 = spacy.load("./rel_component/training/model-best")

nlp = spacy.load("./ner_component/output/model-best")
text = [
'''
    Dipirona é um ótimo analgésico para combater a dor.
    doril contém dipiron e é indicado para dor de cabeça.
'''
]

for doc in nlp.pipe(text, disable=["tagger"]):
    print([(ent.text, ent.label_) for ent in doc.ents])

#We take the entities generated from the NER pipeline and input them to the REL pipeline

for name, proc in nlp2.pipeline:
   doc = proc(doc)

#Here, we split the paragraph into sentences and apply the relation extraction for each pair of entities found in each sentence.

for value, rel_dict in doc._.rel.items(): 

 for sent in doc.sents:

   for e in sent.ents:

     for b in sent.ents:

       if e.start == value[0] and b.start == value[1]:

         if rel_dict['EXPERIENCE_IN'] >=0.9 :

            print(f" entities: {e.text, b.text} --> predicted relation: {rel_dict}")