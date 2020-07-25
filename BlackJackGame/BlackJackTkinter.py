import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
from random import shuffle


#Kart classı ve Kartın gösterilmesi
class Card(object):

    def __init__(self,value,color):

        self.color = color
        self.value = value
        name = value + ' ' +color
        name = name.replace(" ","-")
        self.path = "./Cards/"+name + ".png"


    def show(self):

        load = Image.open(self.path)
        load = load.resize((100,150),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(load)
        return img

        
def calculate(cards):
    score = 0
    AceCounter = 0
    for card in cards:
        if card.value=='1':
            AceCounter+=1
        elif card.value=='11':
            score+=10
        elif card.value=='12':
            score+=10    
        elif card.value=='13':
            score+=10
        else:
            score+= int(card.value)
    if AceCounter == 1 and score <= 10:
        score+=11        
    elif AceCounter ==1 and score > 10:
        score+=1
    return score        
          



class Deck(object):

    def __init__(self): 
        self.cards = []
        self.MakeAdeck()

        shuffle(self.cards)

    def MakeAdeck(self):
        self.cards = []
        k=3
        while k>=0: 
            for i in ['1','13','12','11','10','9','8','7','6','5','4','3','2'] :
                for j in ['h' , 'c' , 'd' , 's']:
                    self.cards.append(Card(i,j))    
            k-=1

    def Çek(self):
        shuffle(self.cards)
        kart = self.cards.pop()
        return kart




class Player(object):
    def __init__(self,name):
        self.name = name
        self.hand = []

    def addCardToHand(self,deck):
        kart = deck.Çek()
        self.hand.append(kart)
        return kart
    
    def clear_hand(self):
        while self.hand:
            self.hand.pop()        

    def show_hand_value(self):
        return calculate(self.hand)        



def get_hidden_card():
    load = Image.open('./Cards/hidden.png')
    load = load.resize((100,150),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(load)

    return img


dek= Deck()

for i in dek.cards:
    print(i)