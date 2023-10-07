# Projeto Prático da disciplina: MO656 -  Introdução a Web Semântica
## Instituto de Computação - UNICAMP
### Autores: @stelzer-monar e @mc-castro

# Estrutura do repositório

|dataset : pasta com os conjuntos de dados usados no projeto
|_raw: pdfs obtidos a partir do site da anvisa
|_arquivos pdf: bulas renomeadas para contextualização
|_final_annotation.tsv: anotação das entidades para o NER
|_final_annotation.json: anotação das relações para o REL
|ner_component: arquivos para o treinamento do modelo de reconhecimento de entidades
|rel_component: arquivos para o treinamento do modelo de extração de relações
|test_ner.ipynb: experimento de treinar um NER com BERT
|project_test.py : arquivo principal que realiza a metodologia apresentada (definição da metodologia, extração do pdf e aplicação do modelo NER treinado)
|ontology.owl: arquivo rdf/xml com todas as triplas geradas
|ontology.svg: resumo gráfico das relações geradas

