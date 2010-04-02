#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import string
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import operator
import xmpp
import gobject
from xmpp.protocol import *
import os
import malpat
from malpat import *
import pango
import time
import threading
gtk.gdk.threads_init()
BuddylistStore=gtk.ListStore(gobject.TYPE_STRING)
mesg=""
errmesg=""


chatmal=0
roster=''
class loop_thread(threading.Thread):
	"""class to define the thread to run the infinite connection loop"""
	def __init__(self,loop):
		self.loop = loop
		threading.Thread.__init__ ( self )

	def run(self):
		self.loop()
		



class ConnectionError: pass
class AuthorizationError: pass
class NotImplemented: pass
class SANS:

	def __init__(self):

		"""to create the login window"""
		self.signin_widgets = gtk.glade.XML("signin.glade")      
		self.signin = self.signin_widgets.get_widget("login")       
		dic={"on_login_destroy" : self.destroy, "on_signin_clicked" : self.buttonclick,"on_login_destroy_event":self.destroy,"on_login_delete_event":self.destroy}
		self.signin.show_all()
		self.user=self.signin_widgets.get_widget("username")
		self.pwd=self.signin_widgets.get_widget("password")
		self.pwd.set_visibility(False)
		self.signin.set_size_request(200,300)
		self.signin.set_title("SANS CHAT")
		if(self.signin):
			
			self.signin_widgets.signal_autoconnect(dic)   
			
		else:
			print "Cannot connect"





		#to create the buddylist window
		self.home_widgets = gtk.glade.XML("buddylist.glade")      
		self.home = self.home_widgets.get_widget("home")       
		self.home.set_title("Buddies")
		dic={"on_home_destroy" : self.destroy,"on_treeview1_button_press_event":self.chat,"on_logout_clicked":self.logout}
		self.buddylist=self.home_widgets.get_widget("buddylist")
		cell=gtk.CellRendererText()
		global BuddylistStore
		
		
		self.buddylist.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('red'))
		self.buddylist.set_model(BuddylistStore)
		column = gtk.TreeViewColumn('Email-id', cell, text=0, cell_background_set=1)
		self.buddylist.append_column(column)			
		self.buddylist.set_headers_visible(True)
		self.buddylist.show()
		self.entry=""		
		if(self.home):
	
			self.home_widgets.signal_autoconnect(dic)   
			
		else:
			print "Cannot connect"


	
		#to create the error dialog window           
		self.error_widgets = gtk.glade.XML("error.glade")      
		self.error = self.error_widgets.get_widget("error")       
		self.error.set_title("Error")
		self.errorlabel=self.error_widgets.get_widget("errormsg")
		dic={"on_error_destroy":self.destroydialog,"on_error_delete_event":self.destroydialog,"on_error_destroy_event":self.destroydialog,"on_ok_clicked":self.signinagain}
		self.error_widgets.signal_autoconnect(dic)




	def chatbox(self,*user):
		"""to create a chatwindow"""
		self.chat_widgets = gtk.glade.XML("chatwindow.glade")      
		self.chatwindow = self.chat_widgets.get_widget("chat")       
		dic={"on_chat_destroy" : self.chat_close, "on_chatentry_changed":self.keypress,"on_mal_toggled":self.mal, "on_chatentry_insert_at_cursor":    
                self.keypress,"on_chat_destroy_event":self.chat_close,"on_chat_destroy_cb":self.chat_close,  "on_send_clicked":self.snt}
		self.chatentry=self.chat_widgets.get_widget("chatentry")
		self.chatlabel=self.chat_widgets.get_widget("chatlabel")
		self.msg=self.chat_widgets.get_widget("msgbox")
		self.chatwindow.set_size_request(225,300)
		self.msg.set_size_request(200,180)
		self.msg.modify_font(pango.FontDescription("Purisa 10"))
		global chatmal
		chatmal=0
		self.mala=self.chat_widgets.get_widget("mal")
		self.entry=user[0]
		self.chatwindow.set_title(self.entry)
		self.chatwindow.show_all()
		
		global mesg
		mesg=""
		if(self.chatwindow):	
			self.chat_widgets.signal_autoconnect(dic)   
		else:
			print "Cannot connect"



	def destroydialog(self,*x):
		"""on closing the error dialog box"""
		self.error.hide()
		self.user.set_text("")
		self.pwd.set_text("")
		self.signin.show_all()
		

	
	def signinagain(self,*x):
		"""on clicking the error dialog box"""
		self.error.hide()
		self.user.set_text("")
		self.pwd.set_text("")
		self.signin.show_all()

	def destroy(self,*x):
		"""on closing the login window or the buddylist"""
		self.connection.disconnect()
		gtk.main_quit()



	def presenceHandler(self, conn, presence):
		"""to handle presence notification"""
		roster=str(presence.getFrom().getStripped())		
		print roster
		global BuddylistStore
		presentusr=self.username+"@gmail.com"
		if operator.eq(Presence.getType(presence),None):
			if operator.eq(presentusr,roster ):
				pass
			else:
				
				if operator.eq( [roster],[r[0] for r in BuddylistStore]):
					pass
				else:
					
					BuddylistStore.append([roster])
				

 
	def messageHandler(self,conn,msg):	
		"""for receiving messages"""
		jid = xmpp.protocol.JID(msg.getFrom())
    		buddy = jid.getNode()	
		buddy1=buddy+"@gmail.com"
		if self.entry!=buddy1:
			self.chatbox(buddy1)			
		global mesg
		m=msg.getBody()
		length=len(mesg)
		if length > 75:
			mesg=mesg[40:]
		mesg=mesg+"\n"+buddy+":"+m
		self.msg.set_label(mesg)



	def loop(self):
		""" handling new xmpp stanzas. """
		try:
			while self.connection.Process(1):				
				pass
		except KeyboardInterrupt:
			pass



	def buttonclick(self,signin_widgets):				
		"""on clicking the signin button"""
		self.username=self.user.get_text()
		self.pswd=self.pwd.get_text()
		JID=self.username+"@gmail.com"
		jid = xmpp.JID(JID)
		self.connection = xmpp.Client(jid.getDomain(),debug=[])
		result = self.connection.connect()

		if result is "":
			
			self.signin.hide()
 			errmsg="Connection failure.Check ur network manager"	
			self.error.show_all()
                 	self.errorlabel.set_label(errmsg)
		else:
		
			result = self.connection.auth(jid.getNode(), self.pswd)
	
			if result is None:
				
				errmsg="Authentification failed.Reenter username and password"
              	         	self.error.show_all()
              		  	self.errorlabel.set_label(errmsg)
			else:
											
				self.connection.RegisterHandler('presence',self.presenceHandler)
			
				self.connection.sendInitPresence()
				self.connection.RegisterHandler('message',self.messageHandler)
				loop_thread(self.loop).start()
				self.signin.hide()
        		       	self.home.show_all()	
                


 		


	


	def chat(self,home_widgets,event):
		"""for displaying the chatbox on clicking the buddylist item"""
		global BuddylistStore
		selection = self.buddylist.get_selection()
		(model,iter)=selection.get_selected()
		entry = BuddylistStore.get_value(iter, 0)
		self.chatbox(entry)
		

	def logout(self,*x):
		"""function for defining the signout button cick"""
		self.connection.disconnect()
		self.home.hide()
		self.user.set_text("")
		self.pwd.set_text("")
		self.signin.show_all()
		


	def chat_close(self,*x):
		"""on closing the chat window"""
		global mesg
		mesg=""
		self.chatwindow.hide()


			

		
	def snt(self,chat_widgets):
		"""on clicking send button"""
		global mesg
		msg=self.chatlabel.get_text()
		self.connection.send(xmpp.protocol.Message(self.entry,msg))
		self.chatlabel.set_text("")
		self.chatentry.set_text("")	
		length=len(mesg)
		if length > 75:
			mesg=mesg[40:]
		mesg=mesg+"\n"+self.username+":"+msg
		self.msg.set_label(mesg)
		

	
	def keypress(self,chat_widgets):
		"""on typing in the chat entry widget"""
		global chatmal
		text = unicode(self.chatentry.get_text())
		if chatmal==1:
			transobj=trans()
			mal=transobj.transliterate(text)
			self.chatlabel.set_label(mal)
		else:
			self.chatlabel.set_label(text)


	def mal(self,widget):
		"""activating the checkbox"""
		global chatmal
		if widget.get_active():	
			chatmal=1
		else:
			chatmal=0


def main():
	sans = SANS() 
	gtk.main()              

if __name__ == "__main__":
	main()
