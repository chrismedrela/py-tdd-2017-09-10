class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def bar(self):
        print(self.day)

    @classmethod
    def fromstring(cls, str):
        day = int(str[0:1])
        month = int(str[2:3])
        year = int(str[4:7])
        return cls(day, month, year)

    @staticmethod
    def foo(str):
        print('Cokolwiek', str)

d = Date(5, 6, 2017)
d = Date.fromstring('05062017')
Date.foo('05062017')
d.bar()
Date(5, 6, 2017).bar()