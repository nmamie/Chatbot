# TODO: intelligence for chatbot
from Brain.ner.entity_matcher import EntityMatcher
from Brain.intent.intent_recognition import IntentRecognizer
from Brain.ner.entity_recognizer import EntityRecognizer

class Brain:
    # initialize brain class
    def __init__(self, graph, ent2lbl, text: str):
        self.graph = graph
        self.ent2lbl = ent2lbl
        self.pred, self.entities = self.ner(text)
        self.movie_intent = self.intent(text)

    # named entity recognition
    def ner(self, text: str) -> tuple:
        # entities from entity recognizer
        movie_ner = EntityRecognizer()
        pred, entities = movie_ner.extract_entities(text)
        print(entities)
        return pred, entities

    # intent recognition
    def intent(self, text: str) -> list:
        recognizer = IntentRecognizer()
        movie_intent = recognizer.extract_intent(text)
        # fuzzy match of movie intent and self.entities
        for int in movie_intent:
            for ent in self.entities.keys():
                if ent.lower() in int[1].lower():
                    intent = int[0]
        if not intent:
            intent = movie_intent[0][0]
        return intent

    # TODO: complete different classes
    # classification of entities
    def ent_classifier(self, entities: dict) -> dict:
        ent_class = {}
        for ent in entities.keys():
            if ent == 'title':
                ent_class[ent] = 'movie'
            elif ent == 'actor':
                ent_class[ent] = 'actor'
            elif ent == 'director':
                ent_class[ent] = 'director'
            elif ent == 'genre':
                ent_class[ent] = 'genre'
            elif ent == 'character':
                ent_class[ent] = 'character'
            elif ent == 'year':
                ent_class[ent] = 'year'
            else:
                ent_class[ent] = 'unknown'
        return ent_class

    # find entities in Knowledge Graph
    def ent_matcher(self, entities: dict) -> str:
        matcher = EntityMatcher(self.graph, self.ent2lbl)
        entity = matcher.match(entities)
        return entity

if __name__ == '__main__':
    # test brain
    text = 'Who is the director of Top Gun: Maverick?'
    brain = Brain(text)
    print(text)
    print(brain.classification)