#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk 

def on_info(frm, msg):
    md = gtk.MessageDialog( parent=frm,
                       type=gtk.MESSAGE_INFO,
                       flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                       buttons=gtk.BUTTONS_CLOSE,
                       message_format=msg
                       )
    result = md.run() 
    md.destroy()

def on_erro(frm,  msg):
    md = gtk.MessageDialog( parent=frm,
                       type=gtk.MESSAGE_ERROR,
                       flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                       buttons=gtk.BUTTONS_CLOSE,
                       message_format=msg
                       )
    result = md.run() 
    md.destroy()

def on_ques(frm,  msg, on_btn_aplicar_clicked,  on_btn_sair_clicked):
    img = gtk.Image()
    img.set_from_stock('gtk-dialog-question', gtk.ICON_SIZE_DIALOG)
    label = gtk.Label(msg)

    btnA = gtk.Button(label='_Aplicar', stock=gtk.STOCK_APPLY, use_underline=True)
    btnA.connect("clicked", on_btn_aplicar_clicked)
    
    btnC = gtk.Button(label='_Cancelar', stock=gtk.STOCK_CANCEL, use_underline=True)
    btnC.connect("clicked", on_btn_sair_clicked)
    
    md = gtk.Dialog(title="Confirme", parent=frm, flags=gtk.DIALOG_DESTROY_WITH_PARENT) 
    
    layout = gtk.HBox() 
    
    layout.pack_start(img,  False)
    img.show()
    
    layout.pack_start(label,  False) 
    label.show()
    
    md.vbox.pack_start(layout) 
    layout.show()
    
    md.action_area.pack_start(btnA, True, True, 0) 
    btnA.show()
    
    md.action_area.pack_start(btnC, True, True, 0)
    btnC.show()
    
    result = md.run() 
    md.destroy()

def on_warn(frm, msg):
    md = gtk.MessageDialog( parent=frm,
                       type=gtk.MESSAGE_WARNING,
                       flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                       buttons=gtk.BUTTONS_CLOSE,
                       message_format=msg
                       )
    result = md.run() 
    md.destroy()
