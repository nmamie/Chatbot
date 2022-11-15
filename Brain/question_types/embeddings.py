import numpy as np
from sklearn.metrics import pairwise_distances


class EmbeddingSimilarity:
    def __init__(self, entity_emb, relation_emb, ent2lbl, lbl2ent, ent2id, id2ent, rel2id, WD, WDT):
        self.entity_emb = entity_emb
        self.relation_emb = relation_emb
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.ent2id = ent2id
        self.id2ent = id2ent
        self.rel2id = rel2id
        self.WD = WD
        self.WDT = WDT

    def most_similar(self, subject, predicate, topn=10):
        """
        Returns the closest entities to the tail found by TransE
        """
        # parsing inputs
        subject = self.lbl2ent[list(subject.values())[0]]
        predicate = self.WDT[predicate.split('/')[-1]]
        # entity embedding
        head = self.entity_emb[self.ent2id[subject]]
        # relation embedding
        rel = self.relation_emb[self.rel2id[predicate]]
        # combine according to the TransE scoring function
        tail = head + rel

        # compute distance to *any* entity
        distances = pairwise_distances(tail.reshape(1, -1), self.entity_emb).reshape(-1)

        # find most plausible tails
        most_likely = np.argsort(distances)

        # convert idx to ent
        label = []
        for idx in most_likely[:topn]:
            ent = self.id2ent[idx]
            lbl = self.ent2lbl[ent]
            label.append(lbl)

        # return the topn most plausible entities
        return label