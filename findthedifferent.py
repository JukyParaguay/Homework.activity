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

class FindTheDifferent():
	
	def changeBackgroundColour(self, eventBox, colour):
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color(colour))
	
	def checkCompletedExercise(self):
		
		checkFlag = True
		for selectionState in self.selectionsState:
			if selectionState['selectedIndex'] != selectionState['differentInex']:
				checkFlag = False
				break
	
		if checkFlag:
			self.mainWindows.exerciseCompletedCallBack()
		
		
	def letterSelectedCallBack(self,eventBox, *args):
		
		hVox = args[1]
		vBoxExercises = args[2]
		frame = args[3]
		
		indexHBox = vBoxExercises.child_get_property(frame, "position")
		lastIndexSelected = self.selectionsState[indexHBox]['selectedIndex']
		if lastIndexSelected != -1:
			lastEventBoxSelected = hVox.get_children()[lastIndexSelected]
			self.changeBackgroundColour(lastEventBoxSelected, "white")	
		
		currentIndexEventBox = hVox.child_get_property(eventBox, "position")
		self.changeBackgroundColour(eventBox, "orange")
		self.selectionsState[indexHBox]['selectedIndex'] = currentIndexEventBox
		
		self.checkCompletedExercise();
	
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
		self.selectionsState = [None]*3
		for index, item in enumerate(items):
			
			frame = gtk.Frame()
			
			hVox = gtk.HBox(True, 10)
			frame.add(hVox)
			
			count = 0
			until = 3
			different = 2
			self.selectionsState[index] = {"selectedIndex": -1,"differentInex":different}
			while count <= until:
				eventBox = gtk.EventBox()
				letterLabel = gtk.Label(item.letter)
				if count == different:
					letterLabel = gtk.Label(item.differentLetter)
				letterLabel.modify_font(pango.FontDescription("Courier Bold 60"))
				eventBox.add(letterLabel)
				self.changeBackgroundColour(eventBox, 'white')
				eventBox.connect("button-press-event", self.letterSelectedCallBack, hVox, vBoxExercises, frame)
				hVox.pack_start(eventBox, False,True,0)
				count = count + 1
				
			vBoxExercises.pack_start(frame, False,True,30)
		
		
		vBoxWindows.pack_start(frameExercises, False,False,0)
		windowFindTheDifferent.add_with_viewport(vBoxWindows)
		
		return windowFindTheDifferent
		
	
		
