#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygtk
pygtk.require('2.0')
import gtk
import json
from collections import namedtuple
from array import *
import pango

from simpleassociation import SimpleAssociation
from findthedifferent import FindTheDifferent
from searchthesame import SearchTheSame




class ModalWindowDone:

	def __init__ (self, parent):
		self.parent = parent
		self.modalWindow = gtk.Window ()

		# Disable interaction with parent
		self.modalWindow.set_modal (True)

		# Tell WM this is a dialog
		self.modalWindow.set_type_hint (gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

		# Tell WM this window belongs to parent
		self.modalWindow.set_transient_for (parent)

		self.modalWindow.set_default_size(350,350)
	
		self.modalWindow.set_skip_pager_hint(True)
		self.modalWindow.set_keep_below(True)
		self.modalWindow.set_decorated(False)
		
		frame = gtk.Frame()
		eventBox = gtk.EventBox()
		eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("white"))
		
		frame.add(eventBox)
		
		vBox = gtk.VBox (False, 10)
		eventBox.add(vBox)
		
		doneImageContainer =  gtk.Image()
		buttonImageContainer =  gtk.Image()
		
		if self.parent.currentIndexExercise < (self.parent.amountExercises - 1):
			doneImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/party.png").scale_simple(200, 200, 2))	
			buttonImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/left.png").scale_simple(50, 50, 2))
		else:
			doneImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/prize.png").scale_simple(200, 200, 2))
			buttonImageContainer.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("./images/left.png").scale_simple(50, 50, 2))
		
		
		
		buttonOk = gtk.Button()
		buttonOk.set_image(buttonImageContainer)
		buttonOk.connect ("clicked", self.goBackButtonCallBack)
		
		vBox.pack_start(doneImageContainer, True,True,10)
		
		hBoxButton = gtk.HBox(True,0)
		hBoxButton.pack_start(buttonOk, False,False,0)
		
		vBox.pack_start(hBoxButton, True,False,0)
		
		self.modalWindow.add (frame)

		
	def goBackButtonCallBack(self, button,*args):
		self.modalWindow.destroy()
		
	def show (self):
		self.modalWindow.show_all ()
		


class Viewer(gtk.Window):
	def exerciseCompletedCallBack(self):
			
			self.modalDoneWindow = ModalWindowDone(self)
			self.modalDoneWindow.show()	
		
	def __init__(self):
		super(Viewer, self).__init__()

		'''Obtenemos el JSON de la Actividad'''
		json_data=open('json.txt')
		self.activity = json.load(json_data, object_hook=lambda d: namedtuple('Activity', d.keys())(*d.values()))
		json_data.close()

		self.set_title(self.activity.name)
		self.set_default_size(900,630)

		self.set_position(gtk.WIN_POS_CENTER)

		self.toolbar = gtk.Toolbar()
		self.toolbar.set_style(gtk.TOOLBAR_BOTH)

		''' Botones <- -> '''
		botonBefore = gtk.ToolButton(gtk.STOCK_GO_BACK)
		botonBefore.connect("clicked", self.backButtonCallBack)
		
		botonNext = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
		botonNext.connect("clicked", self.nextButtonCallBack)

		self.toolbar.insert(botonBefore, 0)
		self.toolbar.insert(botonNext, 1)

		exit = gtk.MenuItem("Exit")
		exit.connect("activate", gtk.main_quit)

		vBoxGeneral = gtk.VBox(False, 2)
		vBoxGeneral.pack_start(self.toolbar, False,False,0)
		
		self.add(vBoxGeneral)

		ejercicioInicial = SimpleAssociation()
		
		self.amountExercises = len(self.activity.exercises)
		self.currentIndexExercise = -1
		
		self.nextButtonCallBack(None, None)
		
		self.connect("destroy", gtk.main_quit)
		self.show_all()

	def manageBackNextButtons(self):
		if self.currentIndexExercise == 0:
			self.toolbar.get_nth_item(0).set_sensitive(False) 
			self.toolbar.get_nth_item(1).set_sensitive(True) 
		elif self.currentIndexExercise > 0 and self.currentIndexExercise < (self.amountExercises-1):
			
			self.toolbar.get_nth_item(0).set_sensitive(True) 
			self.toolbar.get_nth_item(1).set_sensitive(True)
		else:
			
			self.toolbar.get_nth_item(0).set_sensitive(True) 
			self.toolbar.get_nth_item(1).set_sensitive(False) 


	def nextButtonCallBack(self, button, *args):
		self.currentIndexExercise = self.currentIndexExercise + 1
		self.createNewWindowExercise()
		
	
	def backButtonCallBack(self, button, *args):
		self.currentIndexExercise = self.currentIndexExercise - 1
		self.createNewWindowExercise()
	
	def createNewWindowExercise(self):
		newExercise = None
		newWindowExercise = None
		if self.activity.exercises[self.currentIndexExercise].codeType == 1:
			newExercise = SimpleAssociation()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
		elif self.activity.exercises[self.currentIndexExercise].codeType == 2:
			newExercise = FindTheDifferent()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
		elif self.activity.exercises[self.currentIndexExercise].codeType == 3:
			newExercise = SearchTheSame()
			newWindowExercise = newExercise.getWindow(self.activity.exercises[self.currentIndexExercise], self)
			
		vBoxMain = self.get_children()[0]
		if len(vBoxMain.get_children()) > 1 :
			oldWindowExercise = vBoxMain.get_children()[1]
			vBoxMain.remove(oldWindowExercise)
			
		vBoxMain.pack_start(newWindowExercise, True, True, 0)
		
		self.manageBackNextButtons()
		self.show_all()
		
	
	
Viewer()
gtk.main()
