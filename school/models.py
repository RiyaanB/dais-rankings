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
        p,l,t,j = self.panthers,self.lions,self.tigers,self.jaguars
        def positions2(p, l, t, j):
            houses = [p, l, t, j]
            houseNames = ["Panthers", "Lions", "Tigers", "Jaguars"]
            first = []
            second = []
            third = []
            fourth = []
            ###########################
            top = max(houses)
            house = 0
            while True:
                if houses[house] == top:
                    first.append(houseNames[house])
                    houses.pop(house)
                    houseNames.pop(house)
                    house -= 1
                house += 1
                if house == len(houses):
                    break
            ###########################
            if len(houses) == 0:
                return first, second, third, fourth
            top = max(houses)
            house = 0
            while True:
                if houses[house] == top:
                    second.append(houseNames[house])
                    houses.pop(house)
                    houseNames.pop(house)
                    house -= 1
                house += 1
                if house == len(houses):
                    break
            ###########################
            if len(houses) == 0:
                return first, second, third, fourth
            top = max(houses)
            house = 0
            while True:
                if houses[house] == top:
                    third.append(houseNames[house])
                    houses.pop(house)
                    houseNames.pop(house)
                    house -= 1
                house += 1
                if house == len(houses):
                    break
            ###########################
            if len(houses) == 0:
                return first, second, third, fourth
            top = max(houses)
            house = 0
            while True:
                if houses[house] == top:
                    fourth.append(houseNames[house])
                    houses.pop(house)
                    houseNames.pop(house)
                    house -= 1
                house += 1
                if house == len(houses):
                    break

            return first, second, third, fourth

        houses = ["Panthers", "Lions", "Tigers", "Jaguars"]
        ranks = positions2(p, l, t, j)
        ranksHouse = [0, 0, 0, 0]

        for house in range(len(houses)):
            for rank in range(len(ranks)):
                if houses[house] in ranks[rank]:
                    ranksHouse[house] = rank + 1
        return ranksHouse

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
