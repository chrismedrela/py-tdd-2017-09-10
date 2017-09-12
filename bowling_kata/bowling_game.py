class BowlingGame:
    FRAMES_IN_GAME = 10
    NUMBER_OF_PINS = 10

    def __init__(self):
        self._rolls = []

    def roll(self, pins):
        self._rolls.append(pins)

    def score(self):
        frame_index = 0
        total = 0
        for _ in range(self.FRAMES_IN_GAME):
            first_roll = self._rolls[frame_index]

            is_strike = first_roll == self.NUMBER_OF_PINS

            bonus = 0
            if is_strike:
                frame_sum = first_roll
                bonus = self._rolls[frame_index+1] + self._rolls[frame_index+2]

            else:
                second_roll = self._rolls[frame_index+1]
                frame_sum = first_roll + second_roll
                
                is_spare = frame_sum == self.NUMBER_OF_PINS
                if is_spare:
                    bonus = self._rolls[frame_index+2]

            total += frame_sum + bonus

            if is_strike:
                frame_index += 1
            else:
                frame_index += 2

        return total