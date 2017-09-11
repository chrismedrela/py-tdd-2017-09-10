class RecentlyUsedList:
    def __init__(self):
        self._list = []

    def append(self, elem):
        if elem in self._list:
            self._list.remove(elem)
        self._list.append(elem)

    def __str__(self):
        return str(self._list)


if __name__ == "__main__":
    rul = RecentlyUsedList()
    rul.append('first')
    rul.append('second')
    rul.append('third')
    rul.append('second')
    print(rul)
