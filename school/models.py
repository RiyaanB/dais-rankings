from django.db import models
from datetime import date
class Event(models.Model):
    event_name = models.CharField(max_length=128)
    event_date = models.DateField()
    tigers = models.IntegerField()
    panthers = models.IntegerField()
    lions = models.IntegerField()
    jaguars = models.IntegerField()
    def __str__(self):
        return self.event_name
    @property
    def hasHappened(self):
        return not date.today() < self.event_date

    def getScore(self,name):
        score = 0 if not self.hasHappened else self.panthers if name == "panthers" else (self.jaguars if name == "jaguars" else (self.tigers if name == "tigers" else (self.lions if name == "lions" else 0)))
        return score

    @property
    def getPantherScore(self):
        return self.panthers
    @property
    def getLionScore(self):
        return self.lions
    @property
    def getTigerScore(self):
        return self.tigers
    @property
    def getJaguarScore(self):
        return self.jaguars

    @property
    def getRank(self):
        scores = [['p', self.panthers], ['l', self.lions], ['t', self.tigers], ['j', self.jaguars]]
        scores = sorted(scores, key=lambda student: student[1], reverse=True)
        i = 0
        rankings = []
        equal_score = 149819248192188919129984

        for score in scores:
            if equal_score != score[1]:
                equal_score = score[1]
                i += 1
            rankings.append([score[0], equal_score, i])


        ranks = [0,0,0,0]

        for rank in rankings:
            if rank[0] == 'p':
                ranks[0] = rank[2]
            elif rank[0] == 'l':
                ranks[1] = rank[2]
            elif rank[0] == 't':
                ranks[2] = rank[2]
            elif rank[0] == 'j':
                ranks[3] = rank[2]

        return ranks

    @property
    def getPantherRank(self):
        return self.getRank[0]

    @property
    def getLionRank(self):
        return self.getRank[1]

    @property
    def getTigerRank(self):
        return self.getRank[2]

    @property
    def getJaguarRank(self):
        return self.getRank[3]

    def getRankByName(self,name):
        if name == "panther":
            return self.getPantherRank
        elif name == "lions":
            return self.getLionRank
        elif name == "tigers":
            return self.getTigerRank
        elif name == "jaguars":
            return self.getJaguarRank
