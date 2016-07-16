#!/usr/bin/python
# -*- coding: utf-8-*-
import pygtk
pygtk.require('2.0')
import gtk
import pango
import sqlite3
from core import dialogs,  config
"""
Este formulário foi escrito todo na mão, sem glade, por causa da Serialização
que é mais simples de escrever desta maneira
"""
class app():
	def __init__(self):
		db.resultado_consulta = 0
		L = frm_letra()

class db(object):
	resultado_consulta = 0
	text_tag = 0

class frm_letra():
	def __init__(self):
		self.frm_letra = gtk.Window()
		self.frm_letra.set_icon_from_file('icons/icon.png')
		self.frm_letra.set_title("Letra")
		self.frm_letra.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.frm_letra.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000'))
		self.frm_letra.set_default_size(300, 300)		
		self.frm_letra.maximize()
		self.vbox = gtk.VBox(False, 3)

		reload(config) # atualiza as informações do módulo.
		self.lbl_titulo = gtk.Label('<span font_desc="arial '+config.string_db.font_size+'" weight="bold" foreground="red">Título</span>')		
		self.lbl_titulo.set_use_markup(True)
		self.lbl_titulo.set_alignment(0.5,0)
		
		self.hbox_tv = gtk.HBox(False, 2)
		self.ttt_texto1 = gtk.TextTagTable()
		self.tb_texto1 = gtk.TextBuffer(self.ttt_texto1)
		self.tb_texto1.set_text("Primeira metade da letra")
		self.tv_texto1 = gtk.TextView(self.tb_texto1)
		self.tv_texto1.set_wrap_mode(gtk.WRAP_WORD)
		self.tv_texto1.set_editable(False)
		self.tv_texto1.set_border_width(5)
		self.sw_texto1 = gtk.ScrolledWindow()
		self.sw_texto1.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		self.sw_texto1.show()
		self.sw_texto1.add(self.tv_texto1)
		self.hbox_tv.pack_start(self.sw_texto1, True, True, False)

		self.ttt_texto2 = gtk.TextTagTable()
		self.tb_texto2 = gtk.TextBuffer(self.ttt_texto2)
		self.tb_texto2.set_text("Segunda metade da letra")
		self.tv_texto2 = gtk.TextView(self.tb_texto2)
		self.tv_texto2.set_wrap_mode(gtk.WRAP_WORD)
		self.tv_texto2.set_editable(False)
		self.tv_texto2.set_border_width(5)
		self.sw_texto2 = gtk.ScrolledWindow()
		self.sw_texto2.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		self.sw_texto2.show()
		self.sw_texto2.add(self.tv_texto2)
		self.hbox_tv.pack_start(self.sw_texto2, True, True, False)

		self.tbl_rodape = gtk.Table(1,2,False)
		self.tbl_rodape.set_col_spacings(5)
		
		self.tbl_entry = gtk.Table(2,2,False)
		self.tbl_entry.set_col_spacings(5)
		self.lbl_parametro = gtk.Label("ID")
		self.lbl_parametro.set_alignment(0,0)
		self.e_parametro = gtk.Entry()
		self.lbl_fonte = gtk.Label("Tamanho da fonte")
		self.lbl_fonte.set_alignment(0,0)
		self.sb_fonte = gtk.SpinButton(gtk.Adjustment(0, 0, 100, 1, 10, 0))
		self.sb_fonte.set_numeric(True)
		self.sb_fonte.set_value(int(config.string_db.font_size))
		self.tbl_entry.attach(self.lbl_parametro,0, 1, 0, 1)
		self.tbl_entry.attach(self.e_parametro,0, 1, 1, 2)
		self.tbl_entry.attach(self.lbl_fonte, 1,2,0,1)
		self.tbl_entry.attach(self.sb_fonte, 1,2,1,2)
		
		self.tbl_btn = gtk.Table(1,2,False)
		self.tbl_btn.set_col_spacings(5)
		self.btn_localizar = gtk.ToolButton(gtk.STOCK_FIND)
		self.btn_sair = gtk.ToolButton(gtk.STOCK_QUIT)
		self.tbl_btn.attach(self.btn_localizar,0, 1, 0, 1)
		self.tbl_btn.attach(self.btn_sair,1, 2, 0, 1)
		
		self.tbl_rodape.attach(self.tbl_entry,0, 1, 0, 1, xoptions=gtk.EXPAND|gtk.FILL)
		self.tbl_rodape.attach(self.tbl_btn,1, 2, 0, 1, xoptions=gtk.FILL)

		self.vp_consulta = gtk.Viewport()
		self.vp_consulta.add(self.tbl_rodape)
				
		self.vbox.pack_start(self.lbl_titulo, False, True, False)
		self.vbox.pack_start(self.hbox_tv, True, True, True)
		self.vbox.pack_start(self.vp_consulta, False, True, True)

		self.e_parametro.set_property('can-focus',True)
		self.e_parametro.set_property('has-focus',True)
		self.e_parametro.set_property('is-focus',True)

		self.frm_letra.add(self.vbox)

		self.frm_letra.connect("delete-event", lambda w: gtk.main_quit())
		self.frm_letra.connect("key-press-event", self.on_frm_letra_key_press_event)
		self.e_parametro.connect("changed", self.on_e_parametro_changed)
		self.e_parametro.connect("key-press-event", self.on_e_parametro_key_press_event)
		self.sb_fonte.connect("value-changed", self.on_sb_fonte_value_changed)
		self.btn_localizar.connect("clicked", self.on_btn_localizar_clicked)
		self.btn_sair.connect("clicked", self.on_btn_sair_clicked)

		self.frm_letra.show_all()
	
	def get_letra(self):
		try:
			reload(config) # atualiza as informações do módulo.
			self.con = sqlite3.connect(config.string_db.db)
			self.cur_select = self.con.cursor()
			self.parametro = [str(self.e_parametro.get_text())]
			self.cur_select.execute('SELECT id, titulo, letra FROM letras WHERE id=?',self.parametro)
			self.rs_select = self.cur_select.fetchall()
			if self.rs_select != []: # Se a tabela não estiver vazia então prossegue
				for self.rec_select in self.rs_select:
					self.lbl_titulo.set_text('<span font_desc="arial '+config.string_db.font_size+'" weight="bold" foreground="red">'+self.rec_select[1]+'</span>')
					self.lbl_titulo.set_use_markup(True)
					self.metade = len(self.rec_select[2])/2
					self.texto = self.rec_select[2]
					self.tb_texto1.set_text(self.texto[:int(self.metade)])
					self.tb_texto2.set_text(self.texto[int(self.metade):])
				self.formatar_texto()
			else:
				dialogs.on_info(self.frm_letra,"O ID digitado não existe. Tente novamente com um ID diferente.")
			self.con.close()
			self.id = db.resultado_consulta
			self.e_parametro.set_text("")
			db.resultado_consulta = self.id
			self.atualiza_id_palco()
			self.e_parametro.grab_focus()
			db.resultado_consulta = 0
		except:
			dialogs.on_warn(self.frm_letra,"Problemas ao tentar efetuar a consulta ao banco de dados. Caso persista, contate o administrador do sistema.")

	def atualiza_id_palco(self):
		try:
			reload(config) # atualiza as informações do módulo.
			self.con = sqlite3.connect(config.string_db.db)
			self.cur_update = self.con.cursor()
			self.cur_update.execute('UPDATE id_palco SET id_atual=? WHERE id=1',(str(db.resultado_consulta), ))
			self.con.commit()
			self.con.close()            
		except:
			dialogs.on_warn(self.frm_letra,"Problemas ao tentar atualizar ao banco de dados. Caso persista, contate o administrador do sistema.")

	

	def formatar_texto(self):
		# Propriedades da TextTag (exemplo: 'font'): http://www.pygtk.org/docs/pygtk/class-gtktextattributes.html
		# Constantes Pango (exemplo: pango.WEIGHT_BOLD) : http://www.pygtk.org/docs/pygtk/pango-constants.html
		
		# Negrito
		db.text_tag = db.text_tag + 1
		self.tt_bold1 = gtk.TextTag("bold_"+str(db.text_tag))
		self.tt_bold1.set_property("weight", pango.WEIGHT_BOLD)
		self.ttt_texto1.add(self.tt_bold1)
		self.tb_texto1.apply_tag(self.tt_bold1, self.tb_texto1.get_start_iter(), self.tb_texto1.get_end_iter())

		db.text_tag = db.text_tag + 1
		self.tt_bold2 = gtk.TextTag("bold_"+str(db.text_tag))
		self.tt_bold2.set_property("weight", pango.WEIGHT_BOLD)
		self.ttt_texto2.add(self.tt_bold2)
		self.tb_texto2.apply_tag(self.tt_bold2, self.tb_texto2.get_start_iter(), self.tb_texto2.get_end_iter())

		# Alinhamento
		db.text_tag = db.text_tag + 1
		self.tt_justify1 = gtk.TextTag("justify_"+str(db.text_tag))
		self.tt_justify1.set_property("justification", gtk.JUSTIFY_LEFT)
		self.ttt_texto1.add(self.tt_justify1)
		self.tb_texto1.apply_tag(self.tt_justify1, self.tb_texto1.get_start_iter(), self.tb_texto1.get_end_iter())

		db.text_tag = db.text_tag + 1
		self.tt_justify2 = gtk.TextTag("justify_"+str(db.text_tag))
		self.tt_justify2.set_property("justification", gtk.JUSTIFY_LEFT)
		self.ttt_texto2.add(self.tt_justify2)
		self.tb_texto2.apply_tag(self.tt_justify2, self.tb_texto2.get_start_iter(), self.tb_texto2.get_end_iter())

		# Fonte
		reload(config) # atualiza as informações do módulo.
		db.text_tag = db.text_tag + 1
		self.tt_font1 = gtk.TextTag("font_"+str(db.text_tag))
		self.tt_font1.set_property("font", config.string_db.font_size)
		self.ttt_texto1.add(self.tt_font1)
		self.tb_texto1.apply_tag(self.tt_font1, self.tb_texto1.get_start_iter(), self.tb_texto1.get_end_iter())

		db.text_tag = db.text_tag + 1
		self.tt_font2 = gtk.TextTag("font_"+str(db.text_tag))
		self.tt_font2.set_property("font", config.string_db.font_size)
		self.ttt_texto2.add(self.tt_font2)
		self.tb_texto2.apply_tag(self.tt_font2, self.tb_texto2.get_start_iter(), self.tb_texto2.get_end_iter())


	def on_frm_letra_key_press_event(self, widget, event):
		if gtk.gdk.keyval_name(event.keyval) == "Escape":
			self.frm_letra.destroy()

	def on_e_parametro_changed(self,  widget):
		db.resultado_consulta = self.e_parametro.get_text()
		self.atualiza_id_palco()

	def on_e_parametro_key_press_event(self, widget, event):
		if gtk.gdk.keyval_name(event.keyval) == "KP_Enter":
			self.get_letra()
		elif gtk.gdk.keyval_name(event.keyval) == "Return":
			self.get_letra()

	def on_sb_fonte_value_changed(self, widget):
		self.titulo = self.lbl_titulo.get_text()
		self.lbl_titulo.set_text('<span font_desc="arial '+str(self.sb_fonte.get_value_as_int())+'" weight="bold" foreground="red">'+self.titulo+'</span>')
		self.lbl_titulo.set_use_markup(True)

		self.texto1 = self.tb_texto1.get_text(self.tb_texto1.get_start_iter(), self.tb_texto1.get_end_iter(), True)
		self.texto2 = self.tb_texto2.get_text(self.tb_texto2.get_start_iter(), self.tb_texto2.get_end_iter(), True)

		db.text_tag = db.text_tag + 1
		self.tt_font1 = gtk.TextTag("font_"+str(db.text_tag))
		self.tt_font1.set_property("font", str(self.sb_fonte.get_value_as_int()))
		self.ttt_texto1.add(self.tt_font1)
		self.tb_texto1.apply_tag(self.tt_font1, self.tb_texto1.get_start_iter(), self.tb_texto1.get_end_iter())

		db.text_tag = db.text_tag + 1
		self.tt_font2 = gtk.TextTag("font_"+str(db.text_tag))
		self.tt_font2.set_property("font", str(self.sb_fonte.get_value_as_int()))
		self.ttt_texto2.add(self.tt_font2)
		self.tb_texto2.apply_tag(self.tt_font2, self.tb_texto2.get_start_iter(), self.tb_texto2.get_end_iter())


	def on_btn_sair_clicked(self,  widget):
		self.frm_letra.destroy()

	def on_btn_localizar_clicked(self, widget):
		self.get_letra()

if __name__ == "__main__":
    frm = app()
    gtk.main()