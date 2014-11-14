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
		pairTracker = [None]*8
		
		storeSelectionState = [[None for i in range(4)] for j in range(4)]
		
		rows = 4
		rowsCount = 0
		columns = 4
		
		self.lastCellSelected = None
		self.matches = 0
		
		while rowsCount < rows :
			columnsCount = 0
			while columnsCount < columns:
				indexFound = False
				while indexFound == False:
					indexToUse = random.randint(0,7)
					
					if indexsCountUse[indexToUse] < 2:
						
						if indexsCountUse[indexToUse] == 0 :
							pairTracker[indexToUse] = [rowsCount,columnsCount]
						else: 					
							storeSelectionState[rowsCount][columnsCount] = {"letter": items[indexToUse].letter, "pair":pairTracker[indexToUse]}
							storeSelectionState[pairTracker[indexToUse][0]][pairTracker[indexToUse][1]] = {"letter": items[indexToUse].letter, "pair":[rowsCount,columnsCount]}
							
						indexFound = True
						indexsCountUse[indexToUse] = indexsCountUse[indexToUse] + 1
						
				columnsCount = columnsCount + 1
			
			rowsCount = rowsCount + 1
		
		return storeSelectionState
	
	def fakeSelection(self, eventBox):
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('orange'))
	
	def fakeUnselection(self, eventBox)	:
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
	
	def cellSelectedCallBack(self, eventBox, *args):
		
		vBox = eventBox.get_parent()
		rowIndex = vBox.child_get_property(eventBox, "position")
		
		hBox = vBox.get_parent()
		columnIndex = hBox.child_get_property(vBox, "position")
		
		letterLabel = eventBox.get_children()[0]
		letterLabel.set_text(self.storeSelectionState[rowIndex][columnIndex]['letter'])
		self.fakeSelection(eventBox)
		
		if self.lastCellSelected == None:
			self.lastCellSelected = [rowIndex,columnIndex]
		elif self.lastCellSelected != [rowIndex,columnIndex]:
			lastEventBoxSelectedRow = self.lastCellSelected[0]
			lastEventBoxSelectedColumn = self.lastCellSelected[1]
			lastEventBoxSelectedVBox = hBox.get_children()[lastEventBoxSelectedColumn]
			lastEventBoxSelected = lastEventBoxSelectedVBox.get_children()[lastEventBoxSelectedRow]
			if self.lastCellSelected != self.storeSelectionState[rowIndex][columnIndex]['pair']:
				
				self.fakeUnselection(lastEventBoxSelected)
				lastEventBoxSelected.get_children()[0].set_text("")
				self.lastCellSelected =[rowIndex,columnIndex]
			
			else :
				handlerId = self.storeSelectionState[rowIndex][columnIndex]['handlerId']
				lastEventBoxHandlerId = self.storeSelectionState[lastEventBoxSelectedRow][lastEventBoxSelectedColumn]['handlerId']
				self.matches = self.matches + 1
				eventBox.disconnect(handlerId)
				lastEventBoxSelected.disconnect(lastEventBoxHandlerId)
				self.lastCellSelected = None
		
		if self.matches == 8:
			self.mainWindows.exerciseCompletedCallBack()
				
	def getWindow(self, exercise, mainWindows):
		
		self.mainWindows = mainWindows
		self.mainWindows.toolbar.get_nth_item(1).set_sensitive(False) 
			
		windowSearchTheSame= gtk.ScrolledWindow()
		
		eventBoxLabel = gtk.EventBox()
		label = gtk.Label(exercise.name)
		label.modify_font(pango.FontDescription(" 14"))
		eventBoxLabel.add(label)
		eventBoxLabel.modify_bg(gtk.STATE_NORMAL, eventBoxLabel.get_colormap().alloc_color("light blue"))
		
		
		frameExercises = gtk.Frame() 
		
		
		vBoxWindows = gtk.VBox(False, 10)
		vBoxExercises = gtk.VBox(True, 10)
		
		hBoxTitle = gtk.HBox(True, 0)
		hBoxTitle.pack_start(eventBoxLabel, True,True,0)
		vBoxWindows.pack_start(hBoxTitle, True,True,0)
		
		frameExercises.add(vBoxExercises)
		
		items = exercise.items
		
		hBox = gtk.HBox(True, 0)
		
		columns = 4
		rows = 4
		
		rowsCount = 0
		self.storeSelectionState = self.createStoreSelection(exercise)
		while rowsCount < (rows):
			
			vBox = gtk.VBox(True, 0)
			countColumns = 0
			while countColumns < (columns):
				
				eventBox = gtk.EventBox()
				eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color("white"))
				letterLabel = gtk.Label("")
				letterLabel.modify_font(pango.FontDescription("Courier Bold 70"))
				eventBox.add(letterLabel)
				handlerId  = eventBox.connect("button-press-event", self.cellSelectedCallBack)
				self.storeSelectionState[countColumns][rowsCount]['handlerId'] = handlerId
				vBox.pack_start(eventBox, False,False,5)
				countColumns = countColumns + 1
			
			hBox.pack_start(vBox, True,True,5)
			rowsCount = rowsCount + 1
		
		vBoxExercises.pack_start(hBox, False,False,0)
		vBoxWindows.pack_start(frameExercises, False,False,0)
		windowSearchTheSame.add_with_viewport(vBoxWindows)
		
		return windowSearchTheSame
		
