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

class SimpleAssociationImagesLetters():
	
	def getWindow(self, exercise, mainWindows):
		
		self.mainWindows = mainWindows
		self.mainWindows.toolbar.get_nth_item(1).set_sensitive(False) 
			
		windowInitialExercise = gtk.ScrolledWindow()
		
		
		label = gtk.Label(exercise.name)
		label.modify_font(pango.FontDescription("Sans 10"))
		
		
		
		
		
		vBoxWindows = gtk.VBox(False, 5)
		hBoxExercises = gtk.HBox(True, 50)
		vBoxImages = gtk.VBox(False, 5)
		vBoxOptionPairs = gtk.VBox(False, 5)
		
		frameExercises = gtk.Frame() 
		
		eventBoxLabel = gtk.EventBox()
		label = gtk.Label(exercise.name)
		label.modify_font(pango.FontDescription(" 14"))
		eventBoxLabel.add(label)
		eventBoxLabel.modify_bg(gtk.STATE_NORMAL, eventBoxLabel.get_colormap().alloc_color("light blue"))
		hBoxTitle = gtk.HBox(True, 0)
		hBoxTitle.pack_start(eventBoxLabel, True,True,0)
		vBoxWindows.pack_start(hBoxTitle, False,False,0)
		
		frameExercises.add(hBoxExercises)
		
		'''Colores de seleccion'''
		self.colours = []
		self.colours.append({"colour":"orange", "available":True})
		self.colours.append({"colour":"green", "available":True})
		self.colours.append({"colour":"blue", "available":True})
		
		self.imagesSelectionState = {}
		self.pairSelectionState = {}
		
		self.currentImageSelected = -1
		self.lastImageSelected = -1
		
		self.currentPairSelected = -1
		self.lastPairSelected = -1
		
		imagesList, pairsList = self.disorderPairs(exercise.images)
		firstImageEventBox = None
		for index,  image in enumerate(imagesList):
			
			frameEventBoxImage = gtk.Frame() 
			eventBox = gtk.EventBox()
				
			if index == 0:
				firstImageEventBox = eventBox
			
			imageContainer =  gtk.Image()
			imageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(image['imagePath']).scale_simple(180, 170, 2))
			eventBox.add(imageContainer)
			eventBox.connect("button-press-event", self.imageSelectedCallBack, vBoxOptionPairs)
			eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
			frameEventBoxImage.add(eventBox)
			vBoxImages.pack_start(frameEventBoxImage, False,False,0)
			
			self.imagesSelectionState[index] = {"selected": -1, "pair": image['indexPair'], "colour": None}
			
			
			'''Pairs'''
			frameEventPair = gtk.Frame() 
			eventBoxPair = gtk.EventBox()
			pair = gtk.Label(pairsList[index]['optionPair'])
			self.createEventBoxPair(frameEventPair, eventBoxPair, pair, exercise.codSubType)
			eventBoxPair.connect("button_press_event", self.pairSelectedCallBack, vBoxImages)
			eventBoxPair.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color('white'))
			frameEventPair.add(eventBoxPair)
			vBoxOptionPairs.pack_start(frameEventPair, False,False,0)
			
			self.pairSelectionState[index] = {"selected": -1, "pair": pairsList[index]['indexPair'], "colour": None}	
			
			
		hBoxExercises.pack_start(vBoxImages, False,True,50)
		hBoxExercises.pack_start(vBoxOptionPairs, False,True,50)
		vBoxWindows.pack_start(frameExercises, False,False,0)
		
		windowInitialExercise.add_with_viewport(vBoxWindows)
		
		self.selectFirtImage(firstImageEventBox)
		
		return windowInitialExercise
	
	def createEventBoxPair(self, frame, eventBox, label, codSubType):
		if codSubType == 1:
			label.modify_font(pango.FontDescription("Courier Bold 80"))
		elif codSubType == 2:
			label.modify_font(pango.FontDescription("Courier Bold 50"))
		eventBox.set_size_request(180, 170)
		
		eventBox.add(label)
		
		return eventBox
	def selectFirtImage(self, firstEvenBox):
		availableColour =  self.getAvailableSelectionColour()
		self.changeBackgroundColour(firstEvenBox, availableColour['colour'])
		self.setSelectionStateColour(self.imagesSelectionState, 0, availableColour)
		self.currentImageSelected = 0
		frameImageSelected = firstEvenBox.get_parent()
		self.fakeSelection(frameImageSelected)
		
	def disorderPairs(self, pairList):
		
		imagesList = [None]*len(pairList)
		pairsList = [None]*len(pairList)
		
		indexsList = range(len(pairList))
		random.shuffle(indexsList)
	
		for index, pair in enumerate(pairList):
			imagesList[index] = {"imagePath":pair.imagePath, "indexPair": indexsList[index]}
			pairsList[indexsList[index]] = {"optionPair":pair.optionPair, "indexPair": index}
		
		return (imagesList, pairsList)
	
	def checkCompletedExercise(self):
		result = True
		for key,imageSelectionState in self.imagesSelectionState.items():
			if (imageSelectionState['selected'] != imageSelectionState['pair']) or (self.pairSelectionState[key]['selected'] != self.pairSelectionState[key]['pair']) :
				result = False
				break
		if result:
			self.mainWindows.exerciseCompletedCallBack()
	

	def getAvailableSelectionColour(self):
		for colour in self.colours:
			if colour['available']:
				return colour
	
	def setAvailableColour(self, colour):
		self.colours[self.colours.index(colour)]['available'] = True
	
	def setUnavailableColour(self, colour):
		self.colours[self.colours.index(colour)]['available'] = False
		
	
	def imageSelectedCallBack(self, imageEventBox, *args):
		
		frameImageSelected = imageEventBox.get_parent()
		vBoxImages = imageEventBox.get_parent().get_parent()
		
		allImagesFrames = vBoxImages.get_children()
		
		indexImageSelected = vBoxImages.child_get_property(frameImageSelected, "position")
		self.lastImageSelected = self.currentImageSelected
		self.currentImageSelected = indexImageSelected
		
		vBoxPairs = args[1]
		'''Se des-selecciona el par selecciondo previamente'''
		if self.currentPairSelected != -1:
			framePairSelected = vBoxPairs.get_children()[self.currentPairSelected]
			self.fakeUnselection(framePairSelected)
		
		# Revisamos si la ultima imagen seleccionada no fue asociada
		if self.lastImageSelected != -1 and self.imagesSelectionState[self.lastImageSelected]['selected'] == -1:
			
			# No se ha asociado nada, volvemos a a poner a blanco el bg colour
			lastImageEvenBoxSelected = allImagesFrames[self.lastImageSelected].get_children()[0]
			self.changeBackgroundColour(lastImageEvenBoxSelected, 'white')
			self.setSelectionStateColour(self.imagesSelectionState, self.lastImageSelected, None)
			
			
		# Revisamos si ya existe una asociacion'''
		if self.imagesSelectionState[indexImageSelected]['selected'] == -1:
			# Aun no existe una asociación
			colorAvailable = self.getAvailableSelectionColour()
			self.changeBackgroundColour(imageEventBox, colorAvailable['colour'])
			self.setSelectionStateColour(self.imagesSelectionState, indexImageSelected, colorAvailable)
			
		#cambiamos los colores de los bordes (frames) para notificar la seleccion
		self.fakeSelection(frameImageSelected)
		lastFrameImageSelected = allImagesFrames[self.lastImageSelected]
		self.fakeUnselection(lastFrameImageSelected)
		self.fakeUnselection
		
		#Comprabamos la finalización del ejercicio
		self.checkCompletedExercise()
			
	def pairSelectedCallBack(self, pairEventBox, *args):

		vBoxImages = args[1]
		allFramesImages = vBoxImages.get_children()
				
		framePairSelected = pairEventBox.get_parent()
		vBoxPairs = framePairSelected.get_parent()
		
		allPairFrames = vBoxPairs.get_children()
		
		indexPairSelected = vBoxPairs.child_get_property(framePairSelected, "position")
		self.lastPairSelected = self.currentPairSelected
		self.currentPairSelected = indexPairSelected
		
		lastPairSelectionState = None
		if self.lastPairSelected != -1:
			lastPairSelectionState = self.pairSelectionState[self.lastPairSelected]
		
		pairIndexCurrentImageSelected = -1
		imageEventBoxCurremtSelected = None
		if self.currentImageSelected != -1:
			pairIndexCurrentImageSelected = self.imagesSelectionState[self.currentImageSelected]['selected']
			imageEventBoxCurremtSelected = self.imagesSelectionState[self.currentImageSelected]['colour']
		
		pairEventBoxCurrentImageSelected = None
		if self.currentImageSelected != -1 and pairIndexCurrentImageSelected != -1:
			pairEventBoxCurrentImageSelected = allPairFrames[self.imagesSelectionState[self.currentImageSelected]['selected']].get_children()[0]
		
		
		# Verificamos que el ultimo par seleccionado no tenga una asocicion
		if self.lastPairSelected != -1 and lastPairSelectionState['selected'] == -1:
			lastPairEventBoxSelected = allPairFrames[self.lastPairSelected].get_children()[0]
			self.changeBackgroundColour(self, lastPairEventBoxSelected, 'white')
			self.setAvailableColour(lastPairSelectionState['colour'])
			self.setSelectionStateColour(self.pairSelectionState, self.lastPairSelected, None)
			
		
		#Comprobamos si hay alguna imagen seleccionada 
		if self.currentImageSelected != -1:
			#usamos el color de la imagen seleccionada como bg
			colourImageSelected = self.imagesSelectionState[self.currentImageSelected]['colour']
			self.changeBackgroundColour(pairEventBox, colourImageSelected['colour'])
			self.setSelectionStateColour(self.pairSelectionState, indexPairSelected, colourImageSelected )
			
					
			#La imagen asociada al par poseía otro par asociado anteriormente
			if pairIndexCurrentImageSelected != -1 and pairIndexCurrentImageSelected != self.currentPairSelected:
				#des-asociamos el par aterior
				currentPairEventBoxSelected = allPairFrames[pairIndexCurrentImageSelected].get_children()[0]
				self.changeBackgroundColour(currentPairEventBoxSelected, 'white')
				self.setAvailableColour(self.pairSelectionState[pairIndexCurrentImageSelected]['colour'])
				self.setSelectionStateColour(self.pairSelectionState, pairIndexCurrentImageSelected, None )
				self.pairSelectionState[pairIndexCurrentImageSelected]['selected'] = -1
				
				
			#El par seleccionado ya fue asociado por otra imagen, la cual no es la actualmente seleccionada
			if self.pairSelectionState[indexPairSelected]['selected'] != -1 and self.pairSelectionState[indexPairSelected]['selected'] != self.currentImageSelected:
				#des-asociamos la imagen anterior asociada al par
				imagePairSelectedEventBox= allFramesImages[self.pairSelectionState[indexPairSelected]['selected']].get_children()[0]
				self.changeBackgroundColour(imagePairSelectedEventBox,'white')
				self.setAvailableColour(self.imagesSelectionState[self.pairSelectionState[indexPairSelected]['selected']]['colour'])
				self.setSelectionStateColour(self.imagesSelectionState, self.pairSelectionState[indexPairSelected]['selected'], None )
				self.imagesSelectionState[self.pairSelectionState[indexPairSelected]['selected']]['selected'] = -1
			
			#guardamos los datos de la asociacion actuales de ambos lados
			self.pairSelectionState[indexPairSelected]['selected'] = self.currentImageSelected
			self.imagesSelectionState[self.currentImageSelected]['selected'] = indexPairSelected
			self.setUnavailableColour(colourImageSelected)	
		else:
			# TODO: No hay imagen seleccionada, re-ver!
			'''colourAvailable =  self.getAvailableSelectionColour()
			pairEventBox.modify_bg(gtk.STATE_NORMAL, pairEventBox.get_colormap().alloc_color(colourAvailable['colour']))
			self.pairSelectionState[indexPairSelected]['colour'] = colourAvailable'''
			
		#cambiamos los colores de los bordes (frames) para notificar la seleccion
		self.fakeSelection(framePairSelected)
		lastFramePairSelected = allPairFrames[self.lastPairSelected]
		self.fakeUnselection(lastFramePairSelected)
		
		#Comprabamos la finalización del ejercicio
		self.checkCompletedExercise()
	
	def fakeSelection(self, frame):
		frame.modify_bg(gtk.STATE_NORMAL, frame.get_colormap().alloc_color('black'))
	
	def fakeUnselection(self, frame)	:
		frame.modify_bg(gtk.STATE_NORMAL, frame.get_colormap().alloc_color('white'))
	
	def changeBackgroundColour(self, eventBox, colour):
		eventBox.modify_bg(gtk.STATE_NORMAL, eventBox.get_colormap().alloc_color(colour))
		
		
	def setSelectionStateColour(self,selectionState, index, colour):
		selectionState[index]['colour'] = colour
	
