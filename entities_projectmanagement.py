import spacy
from spacy.util import minibatch, compounding
import random

#load the model
nlp = spacy.load('en_core_web_sm')

#zugriff auf named entity recognizer (ner)
ner = nlp.get_pipe('ner')

#dem entity recognizer das neue label "projectmanagement" hinzufügen
ner.add_label('PROJECTMANAGEMENT')

train_data = [
    ("The appointment of a project manager led integrated consultant team to include:",
     {"entities": [(4, 6, "PROJECTMANAGEMENT")]}),
    ("project management, provision of architectural, structural, civil, building services design, and lead designer services for input and development of design proposals to RIBA Plan of Work 2013 Stage 4 and to successfully obtain planning approval prior to engaging upon the procurement of an integrated supply team (IST) to undertake the construction of the new School.",
     {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("Procurement of a 'system for financial follow-up in projects (project management system)' for investment projects in the Agency for Urban Environment.In order to manage the finances and general status in this portfolio in an efficient and professional way, there is a need for a system that secures the performance measurements connected to time, cost and quality in the projects.The system is a vital management tool for financial management in the Agency for Urban Environment, and the objective of the procurement is that project managers get a better and more user-friendly tool that gives both project managers and managers a better overview of progress and central financial key parameters in the projects.",
     {"entities": [(13, 16, "PROJECTMANAGEMENT")]}),
    ( "The sub-project managers must support the project managers and the construction managers in the Norwegian Public Roads Administration's project organisation and work as a link between the project manager and the construction manager and make sure that staff resources contribute to the sub-projects. The sub-project shall be responsible for one or several sub-stretches for the two corridors, E16 Valdres. National road 4.",
     {"entities": [(1, 5, "PROJECTMANAGEMENT")]}),
    ("DIN 69900", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("DIN 69901", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("DIN 69902", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("DIN 69903", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("DIN 69904", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("DIN 69905", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("ISO 10006", {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("Project Management Body of Knowledge Guide: PM-Standard of the Project Management Institute",
     {"entities": [(0, 5, "PROJECTMANAGEMENT")]}),
    ("PMBOK Guide: PM-Standard of the Project Management Institute",
     {"entities": [(0, 2, "PROJECTMANAGEMENT")]}),
    ("IPMA: PM-Standard des Projektmanagementverbandes International Project Management Association/ Deutsche Gesellschaft für Projektmanagement (GPM)",
     {"entities": [(0, 1, "PROJECTMANAGEMENT")]}),
    ("Individual Competence Baseline: PM-Standard des Projektmanagementverbandes International Project Management Association/ Deutsche Gesellschaft für Projektmanagement (GPM)",
     {"entities": [(0, 3, "PROJECTMANAGEMENT")]}),
    ("PRINCE2: is a structured project management method and practitioner certification programme. It emphasises dividing projects into manageable and controllable stages.",
     {"entities": [(0, 1, "PROJECTMANAGEMENT")]}),
    ("P3M3, Portfolio, Programme and Project Management Maturity Model",
     {"entities": [(0, 1, "PROJECTMANAGEMENT")]}),
    ("V-Modell: Vorgehensmodell; Standard für Projektmanagement IT-Entwicklung im öffentlichen Dienst in Deutschland",
     {"entities": [(0, 3, "PROJECTMANAGEMENT")]})
    ]

# die labels zum `ner` hinzufügen
for _, annotations in train_data:
  for ent in annotations.get("entities"):
      ner.add_label(ent[2])

# Die nicht betroffenen pipeline components deaktivieren
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# TRAINING
with nlp.disable_pipes(*unaffected_pipes):

# Training for 30 iterations
    for iteration in range(30):

        # shuffling examples  before every iteration
        random.shuffle(train_data)
        losses = {}
    # batch up the examples using spaCy's minibatch
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

# Test
doc = nlp("The project will comprise of a full design team to provide project management and design consultancy services for the full design, statutory approvals, planning, fire and DAC, tendering process, procurement and subsequent periodic inspections and certification of construction of the following works to Glencastle National School, Ballina, Co. Mayo through an open procedure on eTenders.")
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])