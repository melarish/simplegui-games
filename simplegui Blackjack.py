# Blackjack card game
#http://www.codeskulptor.org/#user39_v9IZ8A4Hcz_12.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_pos = (100,400)
dealer_pos = (100,100)

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    def __str__(self):        
        s = "Hand: "
        for card in self.cards:
            s += card.__str__()+" "
        return s # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value 
        #if it doesn't bust
        value = 0
        has_ace = False
        for card in self.cards:
            value += VALUES[card.rank]
            if card.rank == 'A':
                has_ace = True
        if has_ace and value <= 11:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        pos = list(pos)
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()	# deal a card object from the deck
    
    def __str__(self):                
        s = "Deck: "
        for card in self.cards:
            s += card.__str__()+" "
        return s 	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, score, deck, player_hand, dealer_hand
    if in_play:
        outcome = "Player lost"
        score -= 1
    else:
        outcome = "Hit or stand?"
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    in_play = True

def hit():
    global outcome, in_play, score
    if in_play:
        player_hand.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score  
        if player_hand.get_value() > 21:
            outcome = "Player busted"
            in_play = False
            score -= 1
    else:
        outcome = "New deal?" 
        
def stand():   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global outcome, in_play, score
    # assign a message to outcome, update in_play and score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted"
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer wins"
            score -= 1
        else:
            outcome = "Player wins"
            score += 1
        in_play = False
    else:
        outcome = "New deal?"

# draw handler    
def draw(canvas):
    player_hand.draw(canvas, player_pos)
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [dealer_pos[0] + CARD_BACK_CENTER[0], dealer_pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)        
        dealer_hand.cards[1].draw(canvas, [dealer_pos[0]+CARD_SIZE[0],dealer_pos[1]])    
    else:
        dealer_hand.draw(canvas, dealer_pos)
        canvas.draw_text(str(dealer_hand.get_value()), [50, 100], 36, "Plum")    
    canvas.draw_text("Blackjack", [150, 50], 36, "Cyan")
    canvas.draw_text(outcome, [350, 50], 36, "Lime")
    canvas.draw_text("Score: " + str(score), [350, 550], 36, "Orange")
    canvas.draw_text(str(player_hand.get_value()), [50, 400], 36, "Plum")
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()