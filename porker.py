import random

def main():
    deck = Deck()
    player = Player(deck)
    player.print_my_hand()
    player.exchange(deck)
    player.print_my_hand()
    player.exchange(deck)
    player.print_my_hand()
    player.check_poker_hand()
    player.print_result()

class Card():
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
        self.value = suit + num

    def card_number(self):
        if self.num not in ['A', 'J', 'Q', 'K']:
            return int(self.num)

        card_mapping = {
            'K': 13,
            'Q': 12,
            'J': 11,
            'A': 1 
        }
        return card_mapping[self.num]


class Deck():
    def __init__(self):
        suits = ['♠','♣','♥','♦']
        numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck_list = []
        for s in suits:
            for n in numbers:
                deck_list.append(Card(s, n))
        
        self.deck_list = deck_list

    def draw(self):
        card = random.choice(self.deck_list)
        self.deck_list.remove(card)
        return card

class Player():
    def __init__(self, deck):
        self.hand = Hand()
        for i in range(0, self.hand.max_hand):
            self.draw(deck)

    def draw(self, deck):
        self.hand.add(deck.draw())

    def cut(self, num):
        self.hand.cut(int(num))

    def exchange(self, deck):
        input_value = input()
        if input_value == 'p':
            print('exchange is pass')
            return

        input_list = input_value.split(',')
        input_list.reverse()
        for i in input_list:
            self.cut(i)
            self.draw(deck)

    def print_my_hand(self):
        self.hand.print_my_hand()

    def print_result(self):
        self.hand.porker_hand.display()

    def check_poker_hand(self):
        self.hand.check_porker_hand()

class Hand():
    def __init__(self):
        self.max_hand = 5
        self.hand = []

    def add(self, card):
        self.hand.append(card)

    def cut(self, num):
        del self.hand[num]

    def all(self):
        return self.hand

    def print_my_hand(self):
        for c in self.hand:
            print('[' + c.value + ']', end='')
        print()

    def check_porker_hand(self):
        self.porker_hand = Check().check(self)

    def get_numbers(self):
        numbers = []
        for c in self.hand:
            numbers.append(c.num)
        return numbers

    def get_numbers_as_int(self):
        numbers = []
        for c in self.hand:
            numbers.append(c.card_number())
        return numbers
 
    def get_all_suits(self):
        suits = []
        for h in self.hand:
            suits.append(h.suit)
        return suits


class Check():
    def __init__(self):
        self.initialize_porker_hands()

    def check(self, hand):
        self.flash.check(hand)
        self.straight.check(hand)

        self.straight_flash.check(hand, self.flash.result, self.straight.result)
        if self.straight_flash.result:
            return self.straight_flash

        if self.flash.result:
            return self.flash
            
        if self.straight.result:
            return self.straight 

        self.four_card.check(hand)
        if self.four_card.result:
            return self.four_card

        self.three_card.check(hand)
        self.one_pair.check(hand)

        self.full_house.check(hand, self.one_pair.result, self.three_card.result)
        if self.full_house.result:
            return self.full_house
 
        if self.three_card.result:
            return self.three_card

        self.two_pair.check(hand)
        if self.two_pair.result:
            return self.two_pair

        if self.one_pair.result:
            return self.one_pair 

        return self.peke

    def initialize_porker_hands(self):
        self.straight_flash = StraightFlash()
        self.flash = Flash()
        self.straight = Straight()
        self.four_card = FourCard()
        self.full_house = FullHouse()
        self.three_card = ThreeCard()
        self.two_pair = TwoPair()
        self.one_pair = OnePair()
        self.peke = Peke()

class PorkerHand():
    def __init__(self, porker_hand):
        self.porker_hand = porker_hand 
        self.result = False

    def check_conditions(self, hand):
        print('You should write about conditions for each class.')

    def check(self, hand):
        self.check_conditions(hand)

    def display(self):
        print('My hand is ' + self.porker_hand)

class StraightFlash(PorkerHand):
    def __init__(self):
        super().__init__('StraightFlash')

    def check_conditions(self, hand, straight_result, flash_result):
        if not (straight_result and flash_result):
            return

        if self.is_royal(hand):
            self.porker_hand = 'RoyalStraightFlash'
        
        self.result = True

    def check(self, hand, straight_result, flash_result):
        self.check_conditions(hand, straight_result, flash_result)

    def is_royal(self, hand):
        return ['10', 'J', 'Q', 'K', 'A'].sort() == hand.get_numbers().sort()

class Flash(PorkerHand):
    def __init__(self):
        super().__init__('Flash')

    def check_conditions(self, hand):
        suits = hand.get_all_suits() 
        self.result = (len(set(suits)) == 1) # 重複をはじいた結果が1であればフラッシュ

class Straight(PorkerHand):
    def __init__(self):
        super().__init__('Straight')

    def check_conditions(self, hand):
        numbers = hand.get_numbers_as_int()
        numbers.sort()
        number_list = []
        if (1 in numbers) and (13 in numbers):
            number_list = list(range(10, 10 + 4))
            number_list.insert(0,1)
        else:
            number_list = list(range(numbers[0], numbers[0] + 5))
        self.result = (numbers == number_list)

class Kind(PorkerHand):
    def __init__(self, porker_hand):
        super().__init__(porker_hand)

    def check_conditions(self, hand):
        numbers = hand.get_numbers_as_int()
        for num in numbers:
            if numbers.count(num) == self.card_num:
               self.result = True
               break

class FourCard(Kind):
    def __init__(self):
        super().__init__('FourCard')
        self.card_num = 4

    def check_conditions(self, hand):
        super().check_conditions(hand)

class ThreeCard(Kind):
    def __init__(self):
        super().__init__('ThreeCard')
        self.card_num = 3

    def check_conditions(self, hand):
        super().check_conditions(hand)

class FullHouse(PorkerHand):
    def __init__(self):
        super().__init__('FullHouse')

    def check_conditions(self, hand, onepair_result, three_card_result):
        self.result = (onepair_result and three_card_result)

    def check(self, hand, onepair_result, three_card_result):
        self.check_conditions(hand, onepair_result, three_card_result)

class Pair(PorkerHand):
    def __init__(self, porker_hand):
        super().__init__(porker_hand)

    def check_conditions(self, hand):
        numbers = hand.get_numbers()
        check_dict = {}
        for n in numbers:
            if n in check_dict:
                check_dict[n] += 1
            else:
                check_dict[n] = 1
        self.result = list(check_dict.values()).count(2) == self.pair_num

class TwoPair(Pair):
    def __init__(self):
       super().__init__('TwoPair')
       self.pair_num = 2

    def check_conditions(self, hand):
        super().check_conditions(hand)

class OnePair(Pair):
    def __init__(self):
       super().__init__('OnePair')
       self.pair_num = 1

    def check_conditions(self, hand):
        super().check_conditions(hand)

class Peke(PorkerHand):
    def __init__(self):
        super().__init__('PEKE')

    def display(self):
        print('PE☆KE')

if __name__ == '__main__':
    main()

