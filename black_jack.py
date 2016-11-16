# Mini-project #6 - Blackjack

import simplegui
import random

# frame size
FRAME_HEIGHT = 600
FRAME_WIDTH = 600

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Stand or Hit"
score = 0
text_score = "Score " + str(score)
#text constants
dealer = "Dealer"
player = "Player"
font_size = 40
text_score = "Score " + str(score)
name_of_game = "Blackjack"


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

    def draw_face(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def draw_back(self, canvas, pos):
        card_loc = CARD_BACK_CENTER = (36, 48)
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
            
    '''def __iter__(self):
        return self.hand
    
    def next(self):
        for i in self.hand:
            try:
                return self.hand[i]
            except IndexError:
                raise StopIteration'''
                
    def reverse(self):
        a = list(self.hand)
        a.reverse()
        return a

    def __str__(self):
        hand_str = ""
        for i in self.hand:
            hand_str += " " + str(i.rank) +  str(i.suit)
        return hand_str
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = sum([VALUES[i.get_rank()] for i in self.hand])
        rank_of_hand = [i.get_rank() for i in self.hand]
        if 'A' not in rank_of_hand:
            return hand_value
        elif 'A' in rank_of_hand and hand_value + 10 <= 21:
            return hand_value + 10
        else: 
            return hand_value
            

    def draw_dealer(self, canvas, pos):
        a = list(self.hand)
        a.reverse()
        for card in a:
            if in_play:
                if self.hand.index(card) == 0:
                    card.draw_back(canvas, [pos[0] - self.hand.index(card)*CARD_SIZE[0]/3, pos[1]])  
                else:
                    card.draw_face(canvas, [pos[0] - self.hand.index(card)*CARD_SIZE[0]/3, pos[1]])
            else:
                card.draw_face(canvas, [pos[0] - self.hand.index(card)*CARD_SIZE[0]/3, pos[1]])
                
    def draw_player(self, canvas, pos):
        a = list(self.hand)
        a.reverse()
        for card in a:
            card.draw_face(canvas, [pos[0] - self.hand.index(card)*CARD_SIZE[0]/3, pos[1]])
        
                
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i,j)) 
                
        

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        deck_str = ""
        for i in self.deck:
            print str(i.get_rank()) + str(i.get_suit()) + " "



#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, new_deck, score
    if in_play:
        score -= 1
        outcome = "Dealer win. New deal?"
    else:

        outcome = "Stand or Hit"
        new_deck = Deck()
        new_deck.shuffle()
        dealer_hand = Hand()
        player_hand = Hand()
        print type(dealer_hand)
        for i in range(2):
            dealer_hand.add_card(new_deck.deal_card())
            player_hand.add_card(new_deck.deal_card())
        # your code goes here

        print "dealer_hand: ", dealer_hand, dealer_hand.get_value()
        print "player_hand: ", player_hand, player_hand.get_value()

        in_play = True

def hit():
    global outcome, in_play, score
    if player_hand.get_value() < 21 and in_play:
        player_hand.add_card(new_deck.deal_card())
        
        print player_hand, player_hand.get_value()
        
    if player_hand.get_value() > 21 and in_play:
        in_play = False
        score -= 1
        print  "Player are busted" , player_hand.get_value()
        outcome = "Player are busted. New deal?"
        
        
        
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    
       
def stand():
    global score,text_score, outcome, in_play
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(new_deck.deal_card())
        print "dealer_hand", dealer_hand, dealer_hand.get_value()
       

        
        #outcome = "Dealer are busted. Player win"
    if  dealer_hand.get_value() <= 21 and dealer_hand.get_value() >= player_hand.get_value() and in_play:
        score -= 1
        in_play = False
        #text_score = "Score " + str(score)
        outcome = "Dealer win. New deal?"
    elif in_play:
        score += 1
        #text_score = "Score " + str(score)
        outcome = "Player win. New deal?"
        in_play = False

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    '''for i in range(0, FRAME_HEIGHT, FRAME_HEIGHT/100):
        if  i%50 ==0 :
            canvas.draw_line((0,i),(FRAME_HEIGHT,i), 1, 'White')
            canvas.draw_line((i,0),(i,FRAME_HEIGHT), 1, 'White')
        else:
            canvas.draw_line((0,i),(FRAME_HEIGHT,i), 1, 'Black')
            canvas.draw_line((i,0),(i,FRAME_HEIGHT), 1, 'Black')'''
        
    text_score = "Score " + str(score)      
    canvas.draw_text(name_of_game, (FRAME_WIDTH/2 - len(name_of_game)*3*FRAME_HEIGHT/100/2, FRAME_HEIGHT/8), font_size, "Black")
    canvas.draw_text(text_score, (FRAME_WIDTH/2 - len(text_score)*3*FRAME_HEIGHT/100/2 , FRAME_HEIGHT/4 ), font_size, 'White')
    canvas.draw_text(player , (FRAME_WIDTH/4 - len(player)*4*FRAME_HEIGHT/100/2 , FRAME_HEIGHT/2), font_size, 'Black')
    canvas.draw_text(dealer, (FRAME_WIDTH*3/4 - len(player)*4*FRAME_HEIGHT/100/2  , FRAME_HEIGHT/2), font_size, 'Black')
    canvas.draw_text(outcome, (FRAME_WIDTH*1/2 - len(outcome)*1.7*FRAME_HEIGHT/100/2  , FRAME_HEIGHT*3/8), font_size/2, 'White')
    player_hand.draw_player(canvas,[FRAME_WIDTH*1/4, FRAME_HEIGHT/1.5])
    dealer_hand.draw_dealer(canvas,[FRAME_WIDTH*3/4, FRAME_HEIGHT/1.5])
    

    '''.draw(canvas, (FRAME_WIDTH*3/4 - i*CARD_SIZE[0]/2  , FRAME_HEIGHT/1.5))
    .draw(canvas, (FRAME_WIDTH*3/4 + CARD_SIZE[0]/2  , FRAME_HEIGHT/1.5))
    .draw(canvas, (FRAME_WIDTH/4 - CARD_SIZE[0]/2 , FRAME_HEIGHT/1.5))
    .draw(canvas, (FRAME_WIDTH/4 + CARD_SIZE[0]/2 , FRAME_HEIGHT/1.5))'''
    #dealer_hand.draw(canvas, (FRAME_WIDTH*3/4 - CARD_SIZE[0]/2  , FRAME_HEIGHT/1.5))'''
# initialization frame
frame = simplegui.create_frame("Blackjack", FRAME_HEIGHT, FRAME_WIDTH)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)



# get things rolling
deal()
frame.start()


# remember to review the gradic rubric


