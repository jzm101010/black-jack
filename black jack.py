#A game named black jack

import simplegui
import random

#加载扑克牌
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image('https://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png')

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image('https://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png')

#初始全局变量
opt = 'Hit or Stand'
outcome = ''
score = 0
in_play = True

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

#定义类
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print 'Invalid card:', suit, rank
    def __str__(self):
        return self.suit + self.rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def draw(self, canvas, pos, back):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if back:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], (71, 96))
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], (73, 98))
        
class Hand:
    def __init__(self):
        self.card = []
        self.value = []
        
    def __str__(self):
        return self.card + self.value
        
    def add_card(self, card):
        self.card.append(card)
        self.value = []
        for card in self.card:
            self.value.append(VALUES[card.get_rank()])
        
    def get_value(self):
        value = 0
        for num in self.value:
            value += num
        for card in self.card:
            if 'A' in card.get_rank():
                if value + 11 <= 21:
                    value += 11 
        return value
        
    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False
           
    def draw(self, canvas, character, in_play):
        if character:
            if in_play:
                self.card[0].draw(canvas, [100, 200], True)
                count = 2
                for card in self.card[1:]:
                    card.draw(canvas, [100*count, 200], False)
                    count += 1
                
            else:
                count = 1
                for card in self.card:
                    card.draw(canvas, [100*count, 200], False)
                    count += 1
        else:
            count = 1
            for card in self.card:
                card.draw(canvas, [100*count, 400], False)
                count += 1
            
        
class Deck:
    def __init__(self):
        self.card_rank = []
        self.card_suit = ['C', 'S', 'H', 'D']
        for num in range(0, 4):
            for card in RANKS:
                self.card_rank.append(card)
        
    def shuffle(self):
        random.shuffle(self.card_rank)
        random.shuffle(self.card_suit)
        
    def deal_card(self):
        self.shuffle()
        return self.card_suit[0], self.card_rank[0]
        
#定义事件处理程序
def deal():
    global outcome, player, dealer, cards, in_play
    in_play = True
    outcome = ''
    player = Hand()
    dealer = Hand()
    cards = Deck()
    for num in range(0, 2):
        dealer.add_card(Card(cards.deal_card()[0], cards.deal_card()[1]))
        player.add_card(Card(cards.deal_card()[0], cards.deal_card()[1]))
    
def hit():
    global outcome, player, dealer, cards, opt, score, in_play
    outcome = ''
    opt = 'Hit or Stand'
    player.add_card(Card(cards.deal_card()[0], cards.deal_card()[1]))
    print 'player score' + str(player.get_value())
    print 'dealer score' + str(dealer.get_value())
    print player.busted()
    if not player.busted():
        if dealer.get_value() <17:
            dealer.add_card(Card(cards.deal_card()[0], cards.deal_card()[1]))
            in_play = True
    else:
        outcome = 'You lose!'
        opt = 'New deal?'
        score -= 1
        in_play = False
            
    
def stand():
    global outcome, player, dealer, cards, opt, score, in_play
    in_play = False
    while dealer.get_value() <17:
        print 'stand' + str(dealer.get_value())
        dealer.add_card(Card(cards.deal_card()[0], cards.deal_card()[1]))
    if dealer.busted():
        outcome = 'You Win!'
        opt = 'New deal?'
        print 'player score' + str(player.get_value())
        print 'dealer score' + str(dealer.get_value())
        score += 1
    elif dealer.get_value() >= player.get_value():
        outcome = 'You lose!'
        opt = 'New deal?'
        score -= 1
        print 'player score' + str(player.get_value())
        print 'dealer score' + str(dealer.get_value())
    else:
        outcome = 'You Win!'
        opt = 'New deal?'
        score += 1
        print 'player score' + str(player.get_value())
        print 'dealer score' + str(dealer.get_value())
    
def draw(canvas):
    global outcome, player, dealer, cards, opt, score, in_play
    canvas.draw_text('Blackjack', [180, 75], 30, 'Red')
    canvas.draw_text('Dealer:', [100, 160], 20, 'Black')
    canvas.draw_text('Player:', [100, 360], 20, 'Black')
    canvas.draw_text('Score = ' + str(score), [400, 50], 20, 'Black')
    canvas.draw_text(outcome, [200, 160], 20, 'Black')
    canvas.draw_text(opt, [200, 360], 20, 'Black')
    dealer.draw(canvas, True, in_play)
    player.draw(canvas, False, in_play)
    
    
    
#初始框架    
frame = simplegui.create_frame('Black jack', 600, 600)
frame.set_canvas_background('Green')

#创建按钮和画布
frame.add_button('Deal', deal, 200)
frame.add_button('Hit', hit, 200)
frame.add_button('Stand', stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()