#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygtk
pygtk.require('2.0')
import gtk
import json
from collections import namedtuple
from array import *
import pango

from simpleassociationimagesletters import SimpleAssociationImagesLetters
from findthedifferent import FindTheDifferent
from searchthesame import SearchTheSame

class Viewer(gtk.Window):
	def exerciseCompletedCallBack(self):
			
			md = gtk.MessageDialog(self, 
            gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, "¡ Correcto !")
			md.run()
			md.destroy()
			
			botonEjercicioSgte = self.toolbar.get_nth_item(1)
			botonEjercicioSgte.set_sensitive(True)
			
			vBoxMain = self.get_children()[0]
			windowExercise = vBoxMain.get_children()[1]
			frameExercise = windowExercise.get_children()[0]
			'''frameExercise.set_sensitive(False) '''
			
			self.currentIndexExercise = self.currentIndexExercise + 1
			if self.currentIndexExercise == self.amountExercises :
				md = gtk.MessageDialog(self, 
				gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
				gtk.BUTTONS_CLOSE, "¡ Actividad Concluída !")
				md.run()
				md.destroy()
				botonEjercicioSgte.set_sensitive(False)
			
		
	def __init__(self):
		super(Viewer, self).__init__()

		'''Obtenemos el JSON de la Actividad'''
		json_data=open('json.txt')
		self.activity = json.load(json_data, object_hook=lambda d: namedtuple('Activity', d.keys())(*d.values()))
		json_data.close()

		self.set_title(self.activity.name)
		self.set_default_size(1000,600)

		self.set_position(gtk.WIN_POS_CENTER)

		self.toolbar = gtk.Toolbar()
		self.toolbar.set_style(gtk.TOOLBAR_BOTH)


		''' Botones <- -> '''
		botonBefore = gtk.ToolButton(gtk.STOCK_GO_BACK)
		''' Inicialmente deshabilitamos el boton de <--'''
		botonBefore.set_sensitive(False) 


		botonNext = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
		botonNext.connect("clicked", self.nextButtonCallBack)

		self.toolbar.insert(botonBefore, 0)
		self.toolbar.insert(botonNext, 1)


		exit = gtk.MenuItem("Exit")
		exit.connect("activate", gtk.main_quit)

		
		
		vBoxGeneral = gtk.VBox(False, 2)
		vBoxGeneral.pack_start(self.toolbar, False,False,0)
		
		
		
		self.add(vBoxGeneral)

		ejercicioInicial = SimpleAssociationImagesLetters()
		
		self.amountExercises = len(self.activity.exercises)
		self.currentIndexExercise = 0
		
		self.nextButtonCallBack(None, None)
		
		self.connect("destroy", gtk.main_quit)
		self.show_all()
        
	def nextButtonCallBack(self, button, *args):
		newExercise = None
		newWindowExercise = None
		if self.activity.exercises[self.currentIndexExercise].codeType == 1:
			newExercise = SimpleAssociationImagesLetters()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
		elif self.activity.exercises[self.currentIndexExercise].codeType == 2:
			newExercise = FindTheDifferent()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
		elif self.activity.exercises[self.currentIndexExercise].codeType == 3:
			newExercise = SearchTheSame()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
			
		vBoxMain = self.get_children()[0]
		if self.currentIndexExercise > 0 :
			oldWindowExercise = vBoxMain.get_children()[1]
			vBoxMain.remove(oldWindowExercise)
			
		vBoxMain.pack_start(newWindowExercise, True, True, 0)
		self.show_all()

Viewer()
gtk.main()
