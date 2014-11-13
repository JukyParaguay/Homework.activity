#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygtk
pygtk.require('2.0')
import gtk
import json
from collections import namedtuple
from array import *
import pango

import random

class SearchTheSame():
	
	def createStoreSelection(self, exercise):
		
		items = exercise.items
		indexsCountUse = [0]*8
		
		storeSelectionState = [[None for i in range(4)] for j in range(4)]
		
		rows = 4
		rowsCount = 0
		columns = 4
		
		while rowsCount < rows :
			columnsCount = 0
			while columnsCount < columns:
				indexFound = False
				while indexFound == False:
					indexToUse = random.randint(0,7)
					if indexsCountUse[indexToUse] < 2:
						
						storeSelectionState[rowsCount][columnsCount] = {"letter": items[indexToUse].letter}					
						indexFound = True
						indexsCountUse[indexToUse] = indexsCountUse[indexToUse] + 1
						
				columnsCount = columnsCount + 1
			
			rowsCount = rowsCount + 1
		
		
		return storeSelectionState
	
	def getWindow(self, exercise, mainWindows):
		
		self.mainWindows = mainWindows
		self.mainWindows.toolbar.get_nth_item(1).set_sensitive(False) 
			
		windowFindTheDifferent = gtk.ScrolledWindow()
		
		label = gtk.Label(exercise.name)
		label.modify_font(pango.FontDescription("Sans 10"))
		
		frameExercises = gtk.Frame() 
		frameExercises.set_label_widget(label)
		frameExercises.set_label_align(0.5, 0)
		
		
		vBoxWindows = gtk.VBox(False, 5)
		vBoxExercises = gtk.VBox(True, 10)
		
		frameExercises.add(vBoxExercises)
		
		items = exercise.items
		
		#self.selectionsState = [None]*3
		
		hBox = gtk.HBox(True, 0)
		
		columns = 4
		rows = 4
		
		rowsCount = 0
		self.storeSelectionState = self.createStoreSelection(exercise)
		while rowsCount < (rows):
			
			vBox = gtk.VBox(True, 0)
			countColumns = 0
			while countColumns < (columns):
				#print self.storeSelectionState[rowsCount][countColumns]
				
				eventBox = gtk.EventBox()
				eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))
				letterLabel = gtk.Label(self.storeSelectionState[rowsCount][countColumns]['letter'])
				letterLabel.modify_font(pango.FontDescription("Courier Bold 70"))
				eventBox.add(letterLabel)
				vBox.pack_start(eventBox, False,False,5)
				countColumns = countColumns + 1
			
			hBox.pack_start(vBox, True,True,5)
			rowsCount = rowsCount + 1
		
		vBoxExercises.pack_start(hBox, False,False,0)
		vBoxWindows.pack_start(frameExercises, False,False,0)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
		
	
		
