# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 16:50:12 2016

@author: Andrew Standley
"""

""" Implements a grid class, which contains a list of row lists """
""" Potentially worth extending to move away from list of list representation """
""" Potentailly worth extending grid to a matrix class """

class Grid(object):
	def __init__(self):
		self.matrix = [[0 for row in range(10)] for column in range(10)]
		
	def set_grid(self,grid):
		#TODO: Check input is a valid grid. IE Length of every row should be equivalent.
		self.matrix = grid
	
	def get_grid(self):
		return self.matrix
	
	def get_rows(self, *rows):
		#TODO: Better Error Handling for invalid row inputs.
		result=[]
		for row in rows:
			result.append(self.matrix[row])
		return result
		
	def set_rows(self,rows,*values):
		#TODO: Error Handing for invalid inputs?
		for row,value in zip(rows,values):
			self.matrix[row]=value
	
	def get_columns(self, *columns):
		#TODO: Better Error Handling for invalid column inputs
		result=[]
		for column in columns:
			temp = []
			for row in self.matrix:
				temp.append(row[column])
			result.append(temp)
		return result
	
	def set_columns(self,columns,*values):
		#TODO: Error Handing for invalid inputs?
		for column,value in zip(columns,values):
			for index in range(len(self.matrix)):
				self.matrix[index][column]=value[index]
	
	def set_values(self,co_ordinates,*values):
		for co_ordinate,value in zip(co_ordinates,values):
			try:
				self.matrix[co_ordinate[0]][co_ordinate[1]]=value
			except IndexError:
				print("Those co-ordinates ({0},{1})are not contained within the {3}x{4} grid.".format(co_ordinate[0],co_ordinate[1],len(self.matrix),len(self.matrix[1])))
				raise
			except:
				raise
			
	def get_values(self,*co_ordinates):
		result=[]
		for co_ordinate in co_ordinates:
			if len(co_ordinate)==2:
				try:
					result.append(self.matrix[co_ordinate[0]][co_ordinate[1]])
				except IndexError:
					print("Those co-ordinates ({0},{1})are not contained within the {3}x{4} grid.".format(co_ordinate[1],co_ordinate[2],len(self.matrix),len(self.matrix[1])))
					raise
				except:
					raise
			else:
				print("Invaid Co-ordinate {0}".format(co_ordinate))
				raise IndexError
		return result
	
	def __str__(self):
		result=''
		for row in self.matrix:
			result+=str(row)+'\n'
		return result
  		
	def __repr__(self):
		return str(self.matrix)

#Debugging Code
if __name__=="__main__":	
	Test= Grid()
	print(Test)
	print(Test.get_grid())
	Test.set_grid([[1,2,3],[4,5,6],[7,8,9]])
	print(Test)
	print(Test.get_rows(0,1,2))
	print(Test.get_columns(0,1,2))
	print(Test.get_values((0,0),(2,2)))
	print(Test.set_values([(0,0)],10))
	print(Test.set_rows([1],[0,0,0]))
	print(Test.set_columns([1],[11,11,11]))
	print(Test)

