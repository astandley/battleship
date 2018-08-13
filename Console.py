# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 15:47:12 2016

@author: Andrew Standley
"""

""" Implements a method of creating linked text-based consoles to use as either display or input windows """
#Note it's a hacky method which would be better solved by a GUI, but we want to start with a purely console based solution for the challenge

""" Input and Display are the main classes for input/output 
	The remaining classes and methods are intended for
	internal usuage. """



""" Dependancies """
from Grids import Grid #Import Grids to use as a matrix class. This implementation is subject to change, but it encapsulated so no worries.

class Console_Display(object):
	display_table = []

	
	def __init__(self):

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


if __name__=="__main__":
		TestScreen=[ /
		["Welcome to BATTLESHIP"]
		["*** ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
		["**** ~ ~ ~ ~ ~ ~ ~  | ~ ~ ~ ~")
		["*** ~ ~ ~ ~ ~ ~ ~ ~ | ~ ~ ~ ~ ~")
		["* ~ ~ ~ ~ ~ ~ ~ ~  -&-\~ ~ ~ ~ ~ ~")
		["**** ~ ~ ~ ~ ~ ~ ~ (&)| \ ~ ~ ~ ~ ~")
		["***** ~ ~ ~ ~ ~ ~ ={O}| | ~ ~ ~ ~ ~")
		["****^* ~ ^ ~ ==={()} / / ~ ~ ~ ~ ~")
		["***^^^^ ^^^ ~ ~ /	/ / ~ ~ ~ ~ ~")
		["*****^^^%^^^==={()}/ / ~ ~ ~ ~ ~")
		["~ *****^^^^^ ~/	/_/ ~ ~ ~ ~ ~")
		["~ ~ ******* ~ \--// ~ ~ ~ ~ ~ ")
		["Press Enter to Begin...."      ]
