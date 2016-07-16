#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import sqlite3
import gobject
import datetime
from core import dialogs,  config

class app():
    builder = gtk.Builder()
    def __init__(self):
        db.resultado_consulta = 0
        cons = frm_consulta()
    
class frm_id():
    def __init__(self):
        app.builder.add_from_file("ui/palco/id.glade")
        self.frm_id = app.builder.get_object("frm_id")
        self.lbl_id = app.builder.get_object("lbl_id")
        self.lbl_hora = app.builder.get_object("lbl_hora")
        app.builder.connect_signals(self)
        self.frm_id.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.frm_id.show()
        self.frm_id.maximize()
        
        self.timer = gobject.timeout_add(1000, self.get_id) # Temporizador

    def on_frm_id_key_press_event(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.frm_id.destroy()

    def get_id(self):
        try:
            self.hora = datetime.datetime.now().time().isoformat().split('.')[0]
            self.lbl_hora.set_text(self.hora)
            
            reload(config) # atualiza as informações do módulo.
            self.con = sqlite3.connect(config.string_db.db)
            self.cur_select = self.con.cursor()
            self.cur_select.execute('select id, id_atual from id_palco where id=1')
            self.rs_select = self.cur_select.fetchall()
            for self.rec_select in self.rs_select:
                self.lbl_id.set_text(str(self.rec_select[1]))            
            self.con.close()
            
            return True # Faz com que o temporizador rode de novo
        except:
            dialogs.on_warn(self.frm_id,"Problemas ao efetuar a consulta ao banco de dados. Caso persista, contate o administrador do sistema.")

    
if __name__ == "__main__": # Aqui o código só será executado se este for o módulo principal e não quando ele for importado por outro programa
    frm = app()
    frm.show_all()
    gtk.main()

