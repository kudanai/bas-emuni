#!/bin/env python
 # -*- coding: utf-8 -*-

 # Thaana/dhivehi boggle game
 # 2013 @kudanai

import pygame,sys,os,random,codecs
from datetime import datetime
from pygame.locals import *
import corpus

# 			  R   G   G 	too hip for proper naming
FG_COLOR  = (244,244,244)
FG_COLOR2 = ( 78, 34, 25)
TRACE_CLR = ( 78, 34,249)

GAME_TITLE   = u"bas_emuni" # really?
FPS 		 = 30 			# how fast to run this
FULLSCR 	 = False			# run in full screen or not
GAME_TIME 	 = 3*60 		# how many seconds in a game (two minutes?)
SCORE_MULTIP = 5 			# score multiplier

corpus=corpus.build_corpus() # corpus...for lack of a better word i guess


class GameBoard(object):

	def __init__(self,screen):
		#setup screen and stuff
		self.screen=screen
		self.clock = pygame.time.Clock()

		#load up all the resources we need
		self.background_image = pygame.image.load(os.path.join('imgs','bg_game.png'))
		self.brick_image=pygame.image.load(os.path.join('imgs','bg_brick.png'))
		self.btn_up=pygame.image.load(os.path.join('imgs','btn_new_up.png'))
		self.btn_dw=pygame.image.load(os.path.join('imgs','btn_new_down.png'))
		self.sfx_btn=pygame.mixer.Sound(os.path.join('sfx','click.wav'))
		self.sfx_error=pygame.mixer.Sound(os.path.join('sfx','error.wav'))
		self.sfx_success=pygame.mixer.Sound(os.path.join('sfx','success.wav'))
		self.fnt_stats=pygame.font.Font(os.path.join('fonts','lcd.ttf'),25)
		self.fnt_dv=pygame.font.Font(os.path.join('fonts','thaanaua.ttf'),24,bold=True)

		#and init some value
		self.wordlist=[]
		with codecs.open('dict.txt',encoding='utf8', mode='rb') as f:
			for line in f:
				self.wordlist.append(line.strip().encode('utf8'))

		self.start_time=None
		self.button_image = self.btn_up # by default button is up
		self.game_running = False		# game isn't started by default
		self.score=0 					# we start at 0
		self.stack=u""					# debug values..prod=""
		self.found=[]					# debug values..prod=[]
		self.board=self.get_new_board() # hold tile texts for writing
		self.tiles=[]					# holds the tile Node()s
		self.trace=[]					# the line that traces the connected tiles

	def start(self):

		#game loop..here we go
		done=False
		while not done:

			#handle events
			for event in pygame.event.get():

				#quit event
				if event.type == QUIT:
					done=True

				#listening for keyboard
				if (event.type==KEYUP) or (event.type==KEYDOWN):
					if(event.key==K_ESCAPE):
						done=True

				#listening for mouse-down
				if (event.type==MOUSEBUTTONDOWN):
					#see if mouse hits new_game button
					if (self.button_rect.collidepoint(pygame.mouse.get_pos())):
						self.sfx_btn.play()
						self.new_game()

				#mouse released
				if (event.type==MOUSEBUTTONUP):
					if(self.game_running):
						self.check_match()
						self.stack=u""	#clear the stack
						self.trace=[]	#clear the trace
						for tile in self.tiles: #reset tiles
							tile.visited=False

				#get button pressed
				if (self.game_running) and (event.type==MOUSEMOTION) and (pygame.mouse.get_pressed()[0]):
					#check collission with tiles
					for tile in self.tiles:
						if not tile.visited and (tile.rect.collidepoint(pygame.mouse.get_pos())):
							tile.visited=True
							self.stack+=tile.text
							self.trace.append(tile.rect.center)

			#listen for input

			#draw stuff
			self.draw_background()
			self.draw_button()
			self.draw_score()
			self.draw_found()
			self.draw_timer()

			if self.game_running: 
				self.draw_bricks()
				self.draw_stack()

				if len(self.trace)>=2:
					self.draw_trace()

			#flip display because...yea
			pygame.display.flip()

			#clock tick
			self.clock.tick(FPS)

	def draw_background(self):
		self.background_rect=self.screen.blit(self.background_image,(0,0))

	def draw_button(self):
		self.button_rect=self.screen.blit(self.button_image,(420,402))
		self.button_image = self.btn_dw if self.button_rect.collidepoint(pygame.mouse.get_pos()) else self.btn_up

	def draw_bricks(self):
		x,y=(61,123)  #inital x,y
		dx,dy=(81,80) #distance between brick-x
		t_spam=[]

		for row in range(4):
			x=61
			for col in range(4):
				tx=self.board[row][col] #which text
				brick_rect=self.screen.blit(self.brick_image,(x,y))
				self.screen.blit(self.fnt_dv.render(tx[::-1], 1, FG_COLOR2), (x+25,y+10))
				t_spam.append(Node(brick_rect,tx)) #very inefficient
				x+=dx
			y+=dy

		# give it up bro
		if not len(self.tiles)>0:
			self.tiles=t_spam

	def draw_trace(self):
		#draw out the line trace
		pygame.draw.lines(self.screen,TRACE_CLR,False,self.trace,5)

	def draw_stack(self):
		if self.game_running and len(self.stack)>0:
			tx=self.stack[::-1]
			w,h=self.fnt_dv.size(tx)
			label = self.fnt_dv.render(tx, 1, FG_COLOR)
			screen.blit(label, (212-(w/2), 61-(h/2)))

	def draw_score(self):
		tx="%03d"%self.score
		w,h=self.fnt_stats.size(tx)
		label = self.fnt_stats.render(tx, 1, FG_COLOR)
		screen.blit(label, (510-(w/2), 240-(h/2)))

	def draw_found(self):
		tx="%03d"%len(self.found)
		w,h=self.fnt_stats.size(tx)
		label = self.fnt_stats.render(tx, 1, FG_COLOR)
		screen.blit(label, (510-(w/2), 330-(h/2)))

	def draw_timer(self):
		#this would be static width anyway
		timer_text="3:00" if self.game_running else "0:00"
		timediff=self.get_time_diff()
		if (timediff != 0):
			timediff=GAME_TIME-timediff
			if(timediff>0):
				timer_text="%d:%02d" % (timediff//60,timediff%60)
			else:
				self.game_running=False

		
		label = self.fnt_stats.render(timer_text, 1, FG_COLOR)
		screen.blit(label, (490, 139))

	def get_time_diff(self):
		if (self.start_time and self.game_running):
			timediff=datetime.now()-self.start_time
			return timediff.seconds
		else:
			return 0

	def check_match(self):
		if (self.stack.encode('utf8') in self.wordlist) and (self.stack not in self.found):
			self.score+=len(self.stack)*5
			self.found.append(self.stack)
			self.sfx_success.play()
		elif(self.game_running and len(self.stack)>0):
			self.sfx_error.play()

	def get_new_board(self):
		board=[]
		for row in range(4):
			lst=[]
			for col in range(4):
				lst.append(random.choice(corpus))
			board.append(lst)

		return board

	def new_game(self):
		#wipe it clean
		self.score=0
		self.stack=""
		self.found=[]

		#reset game board
		self.board=self.get_new_board() # hold tile texts for writing
		self.tiles=[]	

		#do whatever

		#start game
		self.game_running=True
		self.start_time=datetime.now()


class Node(object):
	def __init__(self,rect,text):
		self._rect=rect
		self._text=text
		self._visited=False #if the node has been visited or not

	@property
	def rect(self):
		return self._rect

	@property
	def text(self):
		return self._text

	@property
	def visited(self):
	    return self._visited
	@visited.setter
	def visited(self, value):
	    self._visited = value

if __name__ == '__main__':
	pygame.init()
	screen=pygame.display.set_mode((640,480),FULLSCREEN if FULLSCR else 0,32)
	pygame.display.set_caption(GAME_TITLE)
	GameBoard(screen).start()