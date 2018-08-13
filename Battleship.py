# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 12:01:12 2015

@author: Andrew
"""
DEBUG = True

""" Console of GUI Version """
ApplicationType='Console'
#ApplicationType='GUI'


""" Code Academy Extra Credit Goals"

1. Make multiple battleships: [In Progress]
	-Make sure that you don’t place battleships on top of each other on the game board. 

2. Make battleships of different sizes: [In Progress]
	-All the parts of the battleship need to be vertically or horizontally
	-Make sure you don’t accidentally place part of a ship off the side of the board.

3. Make your game a two-player game. [Done]

4. More features like rematches, statistics and more!

"""

""" Other Goals:

1. Add GUI Interface

2. Add Network Play
	-Create Server Console App; needs to listen and broadcast on a set port
	-Add 'Client' functions to GUI App; needs to listen and broadcast to a set IP:Port

"""


""" Improved version of Battelship App """
from enum import Enum #Import Enum to easily convert numbered grids to character grids
from os import system #Import os.system to determine command to clear console screen
from os import name #Import name to determine which os we are in...since Windows is stupid
from Grids import Grid #Import Grids to use as a matrix class

""" Defines function to clear console screen """
def clear_console():
	""" Clear the console """
	#TODO: Implement a console clear in a manner which does not require a system call to an .exe like cls
	system('cls' if name=='nt' else 'clear')

	
class Console_Input(object):
	""" Class to capture human-player inputs """
	""" Unsure on design. Should this be a sub-class of Player, 
	since only a player will need to provide input, 
	should it be a seperate entity, or should it be part of
	a HumanPlayer Class: an extension of Player? """
	""" Update: I think I should prehaps change display and input around. 
	Either there should be a class InputDisplay() which extends Display()
	OR Input should belong to Display() as "Display" is really the console
	OR We should create a new class Console() which contains the clear method
	and contains Input() and Display()? """
	
	def __init__(self,display):
		self.display = display
		 
	def co_ordinates(self):
		""" Get Co-ord string in from A#, check validity, and return the string """
		if self.INPUTTING == True:
			self.display.ERROR(["INPUT CALLED WHILST INPUTING","Input Error: How Did We Get Here?"])
		else:
			self.INPUTTING = True
			while self.INPUTTING:
				self.display.update([[11,"Input Co-Ordinates (Ex. A9): "]])
				self.display.refresh()
				co_ordinates = input()
				if len(co_ordinates) == 2 and Input.check_co_ordinates(co_ordinates):
					self.INPUTTING = False
					self.display.update([[12,""],[11,""]])
					#print("Good Co-Ords")
					return co_ordinates
				else:
					self.display.update([[12,"Invalid Input"]])
	def player_name(self, player_num = 1):
		""" Get a name string for 'player_num', check it is alphabetic, and return it """
		if self.INPUTTING == True:
			self.display.ERROR(["INPUT CALLED WHILST INPUTING","Input Error: How Did We Get Here?"])
		else:
			self.INPUTTING = True
			while self.INPUTTING:
				name = input("Enter Name for Player "+str(player_num)+":")
				good_name = True			 
				for word in name.rsplit(" "):			 
					if not word.isalpha():
						good_name = False					
				if good_name:
					self.INPUTTING = False
					return name
				else:
					print("Name must be only Alphabetic")

	def place_ship(self,ship):
		""" Asks the player for start co-ords and orient of 'ship' then returns these """
		if self.INPUTTING == True:
			self.display.ERROR(["INPUT CALLED WHILST INPUTING","Input Error: How Did We Get Here?"])
		else:
			print (ship.name)
			input(ship)
			self.display.update([[0,"Place Your "+identify_ship(ship.value)+":"]])
			ship_co_ords = self.co_ordinates()
			self.INPUTTING = True
			while self.INPUTTING:
				self.display.update([[11,"Horizontal or Vertical Orientation?: "]])
				self.display.refresh()
				orientation = input()
				if orientation.lower() == "horizontal" or orientation.lower() == "h"\
				or orientation.lower() == "vertical" or orientation.lower() == 'v':
					self.INPUTTING = False	
					self.display.update([[12,""],[11,""],[0,""]])
					return  ship_co_ords,orientation[0]	
				else:
					self.display.update([[12,"ERROR: Invalid Input"]])

					
class Console_Display(object):
	display_table = []
	"""
	display_board()
	update_board()
	"""
	
	def __init__(self):
		#print ("Building Initial Display...")
		self.display_table = ["Welcome to BATTLESHIP"]
		self.display_table.append("*** ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
		self.display_table.append("**** ~ ~ ~ ~ ~ ~ ~  | ~ ~ ~ ~")
		self.display_table.append("*** ~ ~ ~ ~ ~ ~ ~ ~ | ~ ~ ~ ~ ~")
		self.display_table.append("* ~ ~ ~ ~ ~ ~ ~ ~  -&-\~ ~ ~ ~ ~ ~")
		self.display_table.append("**** ~ ~ ~ ~ ~ ~ ~ (&)| \ ~ ~ ~ ~ ~")
		self.display_table.append("***** ~ ~ ~ ~ ~ ~ ={O}| | ~ ~ ~ ~ ~")
		self.display_table.append("****^* ~ ^ ~ ==={()} / / ~ ~ ~ ~ ~")
		self.display_table.append("***^^^^ ^^^ ~ ~ /	/ / ~ ~ ~ ~ ~")
		self.display_table.append("*****^^^%^^^==={()}/ / ~ ~ ~ ~ ~")
		self.display_table.append("~ *****^^^^^ ~/	/_/ ~ ~ ~ ~ ~")
		self.display_table.append("~ ~ ******* ~ \--// ~ ~ ~ ~ ~ ")
		self.display_table.append("Press Enter to Begin....")
		return
	
	def refresh(self):
		clear_console()
		system("mode con: cols=50 lines=20") ##This should resize the window
		for row in self.display_table:
			print (row)
		return
		
	def update(self, row_update_list):
		""" Update the display_table. row_update is a list len(n) of a list len (2) which contains [0] row_index [1] row_string """
		#input(row_update_list)
		#clear_console()		
		for row_complex in row_update_list:
			self.display_table[(row_complex[0])]=row_complex[1]
		return

	def update_grids(self,Player_List, Active_Player, rows):
		""" Updates display_table. When the row to be updated includes a player grid we must convert it before updating """
		##NOTE Grid rows differ from table_display rows by 1!		
		##ToDo. Write method such that grid is seperated from score, then write update score method. May need to rethink using only one display_table? 
		converted_rows=[]
		for row in rows:
			converted_rows.append([(row+1),"|"])
			if row <= 9 and row >= 0:
				for player_num,player in enumerate(Player_List):
					for column in player.grid:
						if column[row]==0:
							converted_rows[row][1]+=" ~"
						elif column[row] == 10:
							converted_rows[row][1]+=" X"
						elif column[row] == 11:
							converted_rows[row][1]+=" O"
						else:
							if Active_Player!=player_num:
								converted_rows[row][1]+=" ~"
							else:
								converted_rows[row][1]+=" "+Ship_Type(column[row]).name #This will have to change once Ship becomes a class
					converted_rows[row][1]+="|"
			if row == 0:
				converted_rows[row][1]+="		  Ship Status"
			elif row < 6:
				converted_rows[row][1]+="	"+identify_ship(row)+": " #+Health_by_Square+Ship_Status
			elif row == 7:
				converted_rows[row][1]+="	Score: "+str(Player_List[Active_Player].score)
			elif row == 10:
				for player in Player_List:
					for i in range(int((23-len(player.name))/2)):
						converted_rows[row][1]+=" "
					converted_rows[row][1]+=player.name
					for i in range(int((23-len(player.name))/2)):
						converted_rows[row][1]+=" "
			#print(converted_rows[row])
		#input()  
		#input(len(converted_rows))
		#clear_console()
		self.update(converted_rows)
		return
		
	def ERROR(self,errorstrings):
		clear_console()
		system("mode con: cols=50 lines=20") ##This should resize the window
		print ("ERROR")
		for string in errorstrings:
			print (string)
		return

	def print_grid(self,row,hidden = False):
		return
		""" Return a print formated row on of the player grid. Hidden determines whether ships are displayed or hidden """
		"""Design Note: This should instead return a formatted grid
		Then annother "display" function can be in charge of taking this and displaying it """
		"""grid2print = "|"
		for column in self.grid:
			if column[row] == 0:
				grid2print.append(" "+"~")
			elif column[row] == 10:
				grid2print.append(" "+"X")
			elif column[row] == 11:
				grid2print.append(" "+"O")
			else:
				if hidden:
					grid2print.append(" "+"~")
				else:
					grid2print.append(" "+Ship_Type(column[row]).name)
					#grid2print = " "+chr(2011)
			grid2print.append(" |")
		return grid2print
	#def print_ships(self):			 
			print_row+=self.grid[row]
			if row == 0:
				print_row+="		  Ship Status"
			elif row < 6:
				print_row+= "	"+identify_ship(row)+": " #+Health_by_Square+Ship_Status
			elif row == 8:
				print_row+= "	Score: "+str(self.Player_list[self.active_player].score)
		print(print_row)
		
		return"""

class Interface(object):
	def __inti__(self):
		if ApplicationType=='Console':
			self.Input=Console_Input()
			self.Display=Console_Display()
		else:
			print("ERROR NOT WRITTEN YET")
			return -1
		
				
class Ship_Type(Enum):
	""" Defines the Ships by number """
	#I put these in as a safety, but it's unnessasary
	#They are removed so I can loop over Ship_Type when placing ships	
	#WATER = 0
	#HIT = 10
	#MISS = 11
	P = 1 #Patrol Boat
	D = 2 #Destroyer
	S = 3 #Submarine
	B = 4 #Battleship
	C = 5 #Aircraft_Carrier


class Ship_Size(Enum):
	""" Defines the Ships sizes """
	P = 2 #Patrol Boat
	D = 3 #Destroyer
	S = 3 #Submarine
	B = 4 #Battleship
	C = 5 #Aircraft_Carrier

	
class Column(Enum):
	A = 0
	B = 1
	C = 2
	D = 3
	E = 4
	F = 5
	G = 6
	H = 7
	I = 8
	J = 9


class Player(object):
	""" Player Object """
	""" Design note: I'm begingin to think that Grid should be a seperate class,
	However unsure whether each player would have one grid or two.
	One makes more sense as each player 'owns' just their grid, but then
	grid would need a "print_tracking_grid" method to print the opponents grid
	with all the information except hits and misses hidden. Which is easy, but is that the best design? """ 
	""" All returning functions must first return a list with any display lines to be edited. Even if this list is empty.	"""
	#These are NOT class variables so they don't go here
	#grid = []	
	#score = 0 
	#ships = []
	
	def __init__(self,player_number = 1,player_name = "Test"):
		""" Initialization """
		#Instance variables should be created here
		#self.input = Input() #Fix this later.
		self.set_grid()
		self.set_score()
		self.set_number(player_number)
		self.set_name(player_name)
		self.ship_status ={} #Dictionary of Ships
		
		
	def set_grid(self,newgrid = None): 
		""" Sets player's grid from input, or empty(0) 10x10 grid [columns[rows]] if no input """
		if getattr(self,'grid',1) or newgrid == None:
			self.grid = Grid()
			co_ordiantes=[]
			for row in range(10):
				for column in range(10):
					co_ordiantes.append([row,column])
			self.grid.set_value(newgrid)
		  
	def get_grid(self):
		""" Since Python has no private varibles this is just fluff """
		return [],self.grid

	def set_score(self,score = 0):
		""" Unessasary in Python. Score defaults to 0 """
		self.score = score
	
	def get_score(self):
		""" Unessasary in Python. """
		return [],self.score
		
	def set_number(self,player_number):
		""" Unessasary in Python. """
		self.number = player_number
	
	def get_number(self):
		""" Unessasary in Python. """
		return [],self.number
		
	def set_name(self, player_name):
		""" Unessasary in Python. """
		self.name = player_name #Comment During Testing
	
	def get_name(self):
		""" Unessasary in Python. """
		return [],self.name
		
	def place_ship(self,ship,co_ords,orientation):
		""" Attempts to place a ship on the player's grid. """
		try:
			self.ship_status(ship)
			return [[10],["Ship Already Placed!!"]], False
		except KeyError:
			try:
				self.check_ship_placement(Ship_Size(ship).value,co_ords,orientation)
				# return [range(10),self.print_grid(range(10))],True ##  Need to work out now how to call print_grid muliple times and output to list, without a for loop.
				return [],True
			except PlacementOutsideGrid:
				return [[10],["Ship Placement Falls Outside Grid"]],False
			except ShipsOverlap:
				return [[10],["Ship Placement Overlaps Annother Ship"]],False
			except :
				print("How did we get here?")
				return [],False
		except:
			print("How did we get here?")
			return [],False
		  
	def check_ship_placement(self,size,co_ords,orientation):
		if orientation == 'v':
			if (co_ords[1]+size) < 9:
				for square in range(size):
					if self.grid[co_ords[0]][co_ords[1]+square] != 0:
						pass
					else:
						elf.grid[co_ords[0]][co_ords[1]+square] == Ship_Type(ship).value
			elif orientation == 'h':
				for square in range(Ship_Size(ship).value):
					self.grid[co_ords[0]+square][co_ords[1]] == Ship_Type(ship).value
			for square in range(size):
				if self.grid[co_ords[0]][co_ords[1]+square] != 0:
					return [],False		  
		elif orientation == 'h' and (co_ords[0]+size) < 9:
			for square in range(size):
				if self.grid[co_ords[0]][co_ords[1]] != 0:
					return [],False
		else:
			return [],True
			
	def check_co_ordinates(co_ordinates):
		""" Check string 'co-ordinates' to ensure they are value. Returns bool . Update: This should happen in Grid"""
		good_co_ordinates = False
		#print("Check Starts False")
		for letter in 'ABCDEFGHIJ':
			if letter == co_ordinates[0]:
				#print("Letter was good")
				good_co_ordinates = True
				break
			elif letter == co_ordinates[0].upper():
				print("Letter must be Uppercase")
		for number in '0123456789':
			if number == co_ordinates[1]:
				#print("Number was good")
				good_co_ordinates= (True and good_co_ordinates)
				break
		return good_co_ordinates
				
	def update_grid(self,co_ordinates):
		""" Updates the Grid for a single square. Returns the value that WAS there, or -1 if space has been attacked """
		space = self.grid[Column[co_ordinates[0]].value][co_ordinates[1]]
		if space == 0:
		  #Miss
		  self.grid[Column[co_ordinates[0]].value][co_ordinates[1]] = 11
		elif space == 11 or space ==10:
		  #These are bad co-ordinates. They have already been attacked.
		  space = -1
		else:
		  #Hit
		  self.grid[Column[co_ordinates[0]].value][co_ordinates[1]] = 10
		return space
	
	""" Design Question. Should Player or Game class we be responisble for "attacks"? """
	def attack(self,player): #NEED TO TEST
		""" Uses Input() to get co-ords to attack, updates the grid of the targeted 'player', then returns a string describing the result. """
		while True:
			#co_ordinates = self.input.co_ordinates()
			#space = player.update_grid(co_ordinates)
			space=0
			if space < 0:
				print ("You've already attacked there!")
			else:
				if space == 0:			 
					return "MISS"
				else:
					return "You Hit"

	
class Game():
	
	def __init__(self):
		self.number_of_players = 0
		self.player_list = []
		self.display = Display()
		self.input = Input(self.display)
		self.display.refresh()
		input()
		self.display.update([[11,""],[12,""]])
		self.active_player = 0
		self.setup()
		self.display.refresh()
		
		
		
		
	def setup(self):
		#Add option for VS or AI
		clear_console()
		if DEBUG:
			num_players = 1
		else:
			#This should become an input.
			pass
		for player in range(num_players):
			active_player = player
			#Name should become an input() method. Then passed to add_Player
			self.add_player(player)
			self.display.update_grids(self.player_list,active_player,range(10))
			#Place the Ships
			if False:  #AI Shipe Placement
				pass
			else:	 #Player Ship Placement
				print("Place Your Ships...")
				for ship in Ship_Type:
					pass
				placement = self.input.place_ship(ship)
					##player.place_ship()
			self.display.update_grids(self.player_list,active_player,range(10))
			self.display.update([[0,(self.player_list[self.active_player].name+"'s Turn")]])
		return
		 
	def add_player(self,player):
		self.number_of_players+=1
		if (DEBUG):
			self.player_list.append(Player(player))
		else:
			self.player_list.append(Player(player,self.input.player_name(player))) ##Distiguish VS or AI Player
		return
		
	def run(self):
		while True:
			#Game Loop
			###(Player_list[self.active_player].name+"'s Turn")
			return


""" Funciton to return formated names """
def identify_ship(flag):
	if flag == Ship_Type.P.value:
		return "Patrol Boat"
	elif flag == Ship_Type.D.value:
		return "Destroyer"
	elif flag == Ship_Type.S.value:
		return "Submarine"
	elif flag == Ship_Type.B.value:
		return "Battleship"
	elif flag == Ship_Type.C.value:
		return "Aircraft Carrier"
	else:
		return "Error invalid ship flag"

	
if __name__ == "__main__":
	TestInterface = Interface()
	Testgrid = Grid()
	print(Testgrid)
		
	#test_grid = [[0,0,0,0,0,0,0,1,1,0],[0,2,0,0,0,0,0,0,0,3],[0,2,0,0,0,0,0,0,0,3],[0,2,0,0,4,0,0,0,0,3],[0,0,0,0,4,0,0,0,0,0],[0,0,0,0,4,0,0,0,0,0],[0,0,0,0,4,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,5,5,5,5,5,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
	#Display = Console_Display()
	#Display.update_grids(['Test'],0,TestGrid)
	
	#game = Game()
	#game.run()
	#game.display()
		
	#Andrew = Player()
	#Andrew.set_grid(test_grid)
	#New_input = Input()
	#print (New_input.attack())
	#print (New_input.player_name())
	#print (Andrew.print_grid())
	#for ship in range(6):
	#	print (identify_ship(ship))
	input("End Testing......")
