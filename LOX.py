class T:
    def __init__(self,p):
        self.p = p

    @property
    def getP(self):
        self.p += 1
        return self.p
