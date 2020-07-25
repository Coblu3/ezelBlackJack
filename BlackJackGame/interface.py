import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk,Image
from threading import Timer
import os,sys
import pygame

from BlackJackTkinter import * 


deck = Deck()


player = Player("player")
dealer = Player("dealer")


window = tk.Tk()
window.geometry("1024x768+500+150")
window.title("BlackJack From Akif Beta Version")
window.configure(bg="Green")
window.iconbitmap('icon.ico')



#Ses içerikleri
pygame.mixer.init()

pygame.mixer.music.load("./music/Music_ezel.mp3")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play()


def playFlipSound():
    pygame.mixer.Sound.play(pygame.mixer.Sound('./music/cardflip.wav'))

def playStaySound():
    pygame.mixer.Sound.play(pygame.mixer.Sound('./music/benkaldim.wav'))
    
def playWinSound():
    pygame.mixer.Sound.play(pygame.mixer.Sound('./music/dayiOgretti.wav'))
def playLoseSound():
    pygame.mixer.Sound.play(pygame.mixer.Sound('./music/LoseSound.wav'))
def playExitSound():
    pygame.mixer.Sound.play(pygame.mixer.Sound('./music/exitSound.wav'))

#resim içerikleri
load = Image.open('./photos/cengiz.jpg')
load = load.resize((70,100),Image.ANTIALIAS)
cengiz_img = ImageTk.PhotoImage(load)



#frameler
player_frame = Frame(window,bg='green')
player_frame.pack(side=BOTTOM)

dealer_frame = Frame(window,bg='green')
dealer_frame.pack(side=TOP)

player_cards_frame = Frame(player_frame,bg='green')
player_cards_frame.pack(side=BOTTOM)

dealer_cards_frame = Frame(dealer_frame,bg='green')
dealer_cards_frame.pack(side=TOP)

Button_frame = Frame(window)
Button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

score_text=Label(player_frame,text='score =',bg='green',height=5,font='100')
score_text.pack(side=TOP)

score_text2=Label(dealer_frame,text='score =',bg='green',height=5,font='100')
score_text2.pack(side=BOTTOM)

player_score = Label(player_frame,text="Score = 21 ",width=23,height=5,bg='green',font='100')
player_score.pack()

dealer_score = Label(dealer_frame,text="Score = 21 ",width=23,height=5,bg='green',font='100')
dealer_score.pack()




class Game():
    
    def __init__(self):
        self.StartPosition()
        
            
    def clean_table(self):
        frames = [player_cards_frame,dealer_cards_frame]
        for frame in frames:
            delete= frame.winfo_children()

            for widget in delete:
                widget.forget()

    def StartPosition(self):
        #ilk kartı çek
        kart1 = player.addCardToHand(deck)
        img1 = kart1.show()
        label1 = Label(player_cards_frame,image = img1)
        label1.pack(side=LEFT)
        label1.image = img1
        #ikinci kartı çek
        kart2 = player.addCardToHand(deck)
        img2 = kart2.show()
        label2 = Label(player_cards_frame,image = img2)
        label2.pack(side=LEFT)
        label2.image = img2

        

        #kurpiyer ilk kart çek
        kurpiyer_kart1 = dealer.addCardToHand(deck)
        img3 = kurpiyer_kart1.show()
        kurpiyer_label1 = Label(dealer_cards_frame,image = img3)
        kurpiyer_label1.pack(side=LEFT)
        kurpiyer_label1.image = img3
        #kurpiyer ikinci kart hidden
        hidden_card_img = get_hidden_card()
        self.kurpiyer_label2 = Label(dealer_cards_frame,image = hidden_card_img)
        self.kurpiyer_label2.pack(side=LEFT)
        self.kurpiyer_label2.image = hidden_card_img
        #score göster
        player_score['text'] =  player.show_hand_value()
        dealer_score['text'] =  dealer.show_hand_value()
        #21mi

        

    def change_score_insta(self):
        player_score['text'] = '00'

    def message_box(self,mesaj):
        messagebox.showinfo(title='stat',message=mesaj)
        

    def Hit(self):
        #flip sound
        playFlipSound()
        #kart çek
        kart3 = player.addCardToHand(deck)
        img4 = kart3.show()
        label3 = Label(player_cards_frame,image = img4)
        label3.pack(side=LEFT)
        label3.image = img4
        #score göster
        player_score['text'] =  player.show_hand_value()
        #şartlar
        if player.show_hand_value() > 21:
            #sound
            playLoseSound()
            #kurpiyerin hidden kartını göster
            kurpiyer_kart2 = dealer.addCardToHand(deck)
            img5 = kurpiyer_kart2.show()
            self.kurpiyer_label2['image']=img5
            
            #kurpiyer score göster
            dealer_score['text'] = dealer.show_hand_value()

            #oyuncuların ellerindeki kartları temizle
            player.clear_hand()
            dealer.clear_hand()
            
            #sorun oluşturduğu için bu yapıyı kullandım
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Kaybettin (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()
        if player.show_hand_value() == 21:
            #sound
            playWinSound()
            #kurpiyerin hidden kartını göster
            kurpiyer_kart2 = dealer.addCardToHand(deck)
            img5 = kurpiyer_kart2.show()
            self.kurpiyer_label2['image']=img5

            #kurpiyer score göster
            dealer_score['text'] = dealer.show_hand_value()
            
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('BlackJack!!! (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()

    def restart(self):

        python = sys.executable
        os.execl(python, python, * sys.argv)


    def stay(self):

        #kurpiyerin hidden kartını göster
        kurpiyer_kart2 = dealer.addCardToHand(deck)
        img5 = kurpiyer_kart2.show()
        self.kurpiyer_label2['image']=img5
        self.kurpiyer_label2.image = img5

        #kurpiyer score göster 
        dealer_score['text'] = dealer.show_hand_value()

        #şartlar
        
        if player.show_hand_value() == 21 and dealer.show_hand_value() == 21:
            
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Berabere (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()

        if player.show_hand_value() == 21:
            #sound
            playWinSound()
            
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('BlackJack !!! (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()
        
        
        
        if dealer.show_hand_value() <= 16:
            while dealer.show_hand_value() <= 16:
                #kart çek 16 yi aşana kadar
                kurpiyer_kart3 = dealer.addCardToHand(deck)
                img6 = kurpiyer_kart3.show()
                kurpiyer_label3 = Label(dealer_cards_frame,image = img6)
                kurpiyer_label3.pack(side=LEFT)
                kurpiyer_label3.image = img6
                #kurpiyer score göster
                dealer_score['text'] = dealer.show_hand_value()
                    
        if dealer.show_hand_value() > 21:
            #sound
            playWinSound()
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Kurpiyer Battı !!! (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()
        
        elif dealer.show_hand_value() == 21:
            #sound
            playLoseSound()
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Kurpiyer 21(BlackJack) oldu !!! (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()

        elif dealer.show_hand_value() == player.show_hand_value():
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Berabere skorlar eşit (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()

        elif player.show_hand_value() > dealer.show_hand_value():
            #sound
            playWinSound()
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Kazandın !!!! (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()

        else:
            #sound
            playLoseSound()
            #sorun oluşturduğu için bu yapıyı kullandım
            player.clear_hand()
            dealer.clear_hand()
            
            t = Timer(2,self.clean_table, args=None, kwargs=None)
            t.start()
            self.message_box('Kaybettin !!! (1sn bekle)')
            self.change_score_insta()
            self.StartPosition()

        


                
            

            



        


game = Game()

hit_button = Button(Button_frame,text="Hit",bg='red',width=5,height=3,command=game.Hit)
hit_button.pack(side=LEFT)

stay_button = Button(Button_frame,text="Stay",bg='Blue',width=5,height=3,command=game.stay)
stay_button.pack(side=LEFT)

res_button = Button(Button_frame,text="Restart",bg='Black',fg='white',width=5,height=3,command=game.restart)
res_button.pack(side=LEFT)

exit_button =Button(Button_frame,text='Exit',bg='Yellow',fg='Black',width=5,height=3,command=playExitSound)
exit_button.pack()


window.mainloop()