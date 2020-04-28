# Constants
suits = 'CDHS'
ranks = '23456789TJQKA'
value = dict(zip(ranks, range(2, 2 + len(ranks))))

from abc import ABCMeta, abstractmethod

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()

class PKCard(Card):
    """Card for Poker game
    """
    def value(self):
        return value[self.card[0]]


if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')
    print(f'{c1} {c2} {c3}')

    # comparison
    print(c1 > c2 == c3)

    # sorting
    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards)

import random
class Deck():
    def __init__(self, cls):
        """Create a deck of 'cls' card class
        """
        self.cards = []
        for suit in suits:
            for rank in ranks:
                card = PKCard(f'{rank}{suit}')
                self.cards.append(card)
    
    def shuffle(self):
        return random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def __str__(self):
        return str(self.cards)
            

    def __len__(self): return len(self.cards)

    def __getitem__(self, index): return self.cards[index]
        


if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)


class Hands():
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = cards                  #sorting 하기
        value_list = []
        for i in self.cards:
            a = PKCard(i)
            value_list.append(a.value())
        value_list.sort(reverse=True)
        list = []
        for j in value_list:
            for k in self.cards:
                if value[k[0]] == j:
                    list.append(k)
                    self.cards.remove(k)
        self.cards = list


    def is_flush(self):
        if self.cards[0][1] == self.cards[1][1] == self.cards[2][1] == self.cards[3][1] == self.cards[4][1]:
            return True
        else:
            return False

    def is_straight(self): 
        if value[self.cards[0][0]] == value[self.cards[1][0]] + 1 == value[self.cards[2][0]] + 2 == value[self.cards[3][0]] + 3 == value[self.cards[4][0]] + 4:
            return True
        else:
            return False


    def classify_by_rank(self):
        list1 = []
        list2 = []
        class_dict = {}
        for i in range(5):
            list1.append(self.cards[i][0])
        for j in list1:
            class_dict[j] = list1.count(j)
        for key in class_dict:
            if class_dict[key] == 1:
                list2.append(key)
        for k in list2:
            del class_dict[k]

        return class_dict

    def find_a_kind(self):
        cards_by_ranks = self.classify_by_rank()
        if len(cards_by_ranks) == 1:
            if list(cards_by_ranks.values()) == [2]:
                return 'one pair'
            elif list(cards_by_ranks.values()) == [3]:
                return 'three of a kind'
            elif list(cards_by_ranks.values()) == [4]:
                return 'four of a kind'

        elif len(cards_by_ranks) == 2:
            if 3 in list(cards_by_ranks.values()):
                return 'full house'
            else:
                return 'two pair'


    def tell_hand_ranking(self):
        if self.is_flush() == True and self.is_straight() == True:
            return 'straight flush'
        elif self.find_a_kind() == 'four of a kind':
            return 'four of a kind'
        elif self.find_a_kind() == 'full house':
            return 'full house'
        elif self.is_flush() == True:
            return 'flush'
        elif self.is_straight() == True:
            return 'straight'
        elif self.find_a_kind() == 'three of a kind':
            return 'three of a kind'
        elif self.find_a_kind() == 'two pair':
            return 'two pair'
        elif self.find_a_kind() == 'one pair':
            return 'one pair'
        else:
            return 'high card'

    def tuple(self):
        hand_ranking = ['straight flush', 'four of a kind', 'full house', 'flush', 'straight', 'three of a kind', 'two pair', 'one pair', 'high card']
        s = dict(zip(hand_ranking, range(9,0,-1)))
        if self.tell_hand_ranking() == 'one pair':              #one pair끼리 비교하기 편하게 튜플만들기
            rank_list = []
            for i in range(5):
                rank_list.append(self.cards[i][0])
            for j in rank_list:
                if rank_list.count(j) == 2:
                    onepair = j
                    break
            for x in range(5):
                if self.cards[x][0] == onepair:
                    a = self.cards.pop(x)
                    break
            self.cards.insert(0, a)                           #one pair에 해당하는 카드를 맨앞으로
            for y in range(4):
                if self.cards[y+1][0] == onepair:
                    b = self.cards.pop(y+1)
                    break
            self.cards.insert(1, b)                           #one pair에 해당하는 카드를 두번째로
            value_list = []
            for k in self.cards:
                c = PKCard(k)
                value_list.append(c.value())
            return (s['one pair'], value_list)                #rank끼리만 비교하기위한 튜플

        elif self.tell_hand_ranking() == 'two pair':          #two pair끼리 비교하기 편하게 튜플만들기
            rank_list = []
            for i in range(5):
                rank_list.append(self.cards[i][0])
            for j in rank_list:
                if rank_list.count(j) == 1:
                    not_twopair = j
                    break
            for k in range(5):
                if self.cards[k][0] == not_twopair:
                    a = self.cards.pop(k)
                    break
            self.cards.insert(4,a)                           #two pair에 해당하지 않는 카드를 맨 뒤로
            value_list = []
            for l in self.cards:
                c = PKCard(l)
                value_list.append(c.value())
            return (s['two pair'], value_list)                  #rank끼리만 비교하기위한 튜플

        elif self.tell_hand_ranking() == 'three of a kind':    #three of a kind끼리 비교하기 편하게 튜플만들기           
            rank_list = []
            for i in range(5):
                rank_list.append(self.cards[i][0])
            for j in rank_list:
                if rank_list.count(j) == 3:
                    triple = j
                    break
            for k in range(5):
                if self.cards[k][0] == triple:
                    a = self.cards.pop(k)
                    break
            self.cards.insert(0,a)                            #three of a kind에 해당하는 카드를 맨 앞으로
            value_list = []
            for l in self.cards:
                c = PKCard(l)
                value_list.append(c.value())
            return (s['three of a kind'], value_list)              #rank끼리만 비교하기위한 튜플

        elif self.tell_hand_ranking() == 'four of a kind':         #four of a kind끼리 비교하기 편하게 튜플만들기
            rank_list = []
            for i in range(5):
                rank_list.append(self.cards[i][0])
            for j in rank_list:
                if rank_list.count(j) == 1:
                    not_four = j
                    break
            for k in range(5):
                if self.cards[k][0] == not_four:
                    a = self.cards.pop(k)
                    break
            self.cards.insert(4,a)                                 #four of a kind에 해당하지 않는 카드를 맨 뒤로
            value_list = []
            for l in self.cards:
                c = PKCard(l)
                value_list.append(c.value())
            return (s['four of a kind'], value_list)               #rank끼리만 비교하기위한 튜플
        
        else:
            value_list = []
            for i in self.cards:
                c = PKCard(i)
                value_list.append(c.value())
            return (s[self.tell_hand_ranking()], value_list)       ##rank끼리만 비교하기위한 튜플

    def __lt__(self, other): return self.tuple() < other.tuple()

    def __gt__(self, other): return self.tuple() > other.tuple()


if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    # your test cases here
    hand1 = Hands(['8C', 'TC', '9C', 'JC', '7C'])                 # straight flush(J)
    hand2 = Hands(['5C', '5D', '5S', 'KD', '5C'])                 # four of a kind(5)
    hand3 = Hands(['6S', 'KH', '6D', 'KC', '6H'])                 # full house(K)
    hand4 = Hands(['4D', '9D', '8D', 'KD', '3D'])                 # flush(K)
    hand5 = Hands(['8D', '9S', 'TH', '7D', '6C'])                 # straight(T)
    hand6 = Hands(['QC', '2S', 'QH', '9H', 'QS'])                 # three of a kind(Q)
    hand7 = Hands(['3S', 'JH', '2H', '3C', 'JS'])                 # two pair(J,3)
    hand8 = Hands(['2S', '2H', '8S', '7H', '4C'])                 # one pair(2)
    hand9 = Hands(['QD', 'KD', '7S', '4S', '3H'])                 # high card(K)
    hand10 = Hands(['4S', 'QH', '3H', '4C', 'QS'])                # two pair(Q,4)
    hand11 = Hands(['3S', '5H', '3C', '6D', '9S'])                # one pair(3)
    hand12 = Hands(['3S', 'QD', '4D', 'QC', '3C'])                # two pair(Q,3)
    hand13 = Hands(['3D', 'QH', '3H', '2C', 'QS'])                # two pair(Q, 3)
    hand14 = Hands(['3S', '9H', '7S', 'QD', 'JS'])                # high card(Q)
    hand15 = Hands(['8D', '4D', '6D', '7D', '5D'])                # straight flush(8)
    hand16 = Hands(['3S', 'QS', '7S', '8S', '4S'])                # flush(Q)
    hand17 = Hands(['TC', '4D', 'TD', 'TS', 'TH'])                # four of a kind(T)
    hand18 = Hands(['QS', 'QD', '4C', 'QC', '4H'])                # full house(Q)
    hand19 = Hands(['6C', '7D', '4H', '5H', '8S'])                # straight(8)
    hand20 = Hands(['AC', '2D', '2C', 'QD', '2S'])                # three of a kind(2)
    hand21 = Hands(['3H', '5D', '4H', '3D', '6S'])                # one pair(3)
    hand22 = Hands(['KH', '4D', '9C', '5C', '3S'])                # high card(K)

    #hand ranking 찾기
    test(hand1.tell_hand_ranking() == 'straight flush')           # testcode - straight flush
    test(hand2.tell_hand_ranking() == 'four of a kind')           # testcode - four of a kind
    test(hand3.tell_hand_ranking() == 'full house')               # testcode - full house
    test(hand4.tell_hand_ranking() == 'flush')                    # testcode - flush
    test(hand5.tell_hand_ranking() == 'straight')                 # testcode - straight
    test(hand6.tell_hand_ranking() == 'three of a kind')          # testcode - three of a kind
    test(hand7.tell_hand_ranking() == 'two pair')                 # testcode - two pair
    test(hand8.tell_hand_ranking() == 'one pair')                 # testcode - one pair 
    test(hand9.tell_hand_ranking() == 'high card')                # testcode - high card

    #다른 hand ranking끼리 비교
    test(hand3 > hand4)                                           # testcode - full house(K)와 flush(K) 비교
    test(hand4 > hand7)                                           # testcode - flush(K)와 two pair(J,3)비교
    test(hand6 < hand19)                                          # testcode - three of a kind(Q)과 straight(8)
    test(hand11 < hand15)                                         # testcode - one pair(3)와 straight flush(8)
    test(hand17 > hand12)                                         # testcode - four of a kind(T)와 two pair(Q,3)비교
    test(hand1 > hand2)                                           # testcode - straight flush(J) 와 four of a kind(5) 비교
    test(hand22 < hand20)                                         # testcode - high card(K)와 three of a kind(2) 비교

    
    #같은 hand ranking끼리 비교(find a kind 제외)
    test(hand1 > hand15)                                          # testcode - straight flush(J)와 straight flush(8) 비교
    test(hand4 > hand16)                                          # testcode - flush(K)와 flush(Q)비교
    test(hand3 > hand18)                                          # testcode - full house(K)와 full house(Q) 비교
    test(hand5 > hand19)                                          # testcode - straight(T)와 straight(8)비교
    test(hand9 > hand14)                                          # testcode - high card(K)와  high card(Q) 비교
    test(hand9 > hand22)                                          # testcode - high card(K)와 high card(K) 남은 카드 중에 더큰 수를 가진쪽은 hand9

    
    #find a kind(one pair, two pair, three of a kind, four of a kind)끼리 비교
    test(hand8 < hand11)                                          # testcode - one pair(2)과 one pair(3) 비교
    test(hand11 > hand21)                                         # testcode - one pair(3)과 one pair(3) 남은 카드중에 더큰 수를 가진쪽은 hand11
    test(hand7 < hand10)                                          # testcode - two pair(J,3)과 two pair(Q,4) 비교
    test(hand10 > hand12)                                         # testcode - two pair(Q,4)와 two pair(Q,3) 비교
    test(hand12 > hand13)                                         # testcode - two pair(Q,3)와 two pair(Q,3) 비교 남은 카드중에 더큰 수를 가진쪽은 hand12
    test(hand6 > hand20)                                          # testcode - three of a kind (Q)와 three of a kind(2)비교
    test(hand2 < hand17)                                          # testcode - four of a kind(5)와 four of a kind(T) 비교
