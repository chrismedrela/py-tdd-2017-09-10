class RecentlyUsedList(list):
    def append(self, elem):
        if elem in self:
            self.remove(elem)
        super().append(elem)


if __name__ == "__main__":
    rul = RecentlyUsedList()
    rul.append('first')
    rul.append('second')
    rul.append('third')
    rul.append('second')
    print(rul)
