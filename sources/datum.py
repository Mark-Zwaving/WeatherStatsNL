import datetime

class Datum():
    def __init__(self, yyyymmdd):
        self.maanden = ['january','february','march','april','may','june',
                        'july','august','oktober','november', 'december']
        self.dagen = ['monday','tuesday','wednesday','thursday',
                      'friday','saturday','sunday']

        self.y, self.m, self.d = int(yyyymmdd[:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:8])
        self.datum = datetime.date(self.y, self.m, self.d)

    def weekdag(self):
        return self.dagen[self.datum.weekday()]
    def maand(self):
        return self.maanden[self.datum.month-1]
    def yyyy(self):
        return str(self.y)
    def mm(self):
        return str(self.m) if self.m > 9 else "0%i" % self.m
    def dd(self):
        return str(self.d) if self.d > 9 else "0%i" % self.d

    def tekst(self):
        return f'{self.weekdag()}, {self.dd()} {self.maand()} {self.yyyy()}'
