#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os.path
import xml.dom.minidom
from core import dialogs

# print eval("__import__('os').getcwd()") # return the current working directorys

class changed(object): # Serve para verificar se alguma alteração foi efetuada no form
    status = False

class string_xml(object): # fornece os paths fisico e virtual para manipulação do arquivo xml
    arquivo_fisico = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.xml') #caminho do arquivo fisico 
    if not os.path.exists(arquivo_fisico): # Caso o arquivo fisico nao exista, cria ele
            with open(arquivo_fisico, "w") as arq:  
                arquivo_xml = """<?xml version="1.0"?><config><db>letreiro.db</db><font_size>25</font_size></config>"""
                arq.write(arquivo_xml)
                arq.close()        
    arquivo_virtual = xml.dom.minidom.parse(arquivo_fisico)  # esta variavel será utilizada sempre que precisar ler ou alterar o arquivo fisico

class string_db(object): # fornece a string de conexao para o sqlite
    string_xml()
    db = string_xml.arquivo_virtual.firstChild.childNodes[0].firstChild.data # esta variável recupera do valor do node <db></db>
    font_size = string_xml.arquivo_virtual.firstChild.childNodes[1].firstChild.data
    
class frm_config():
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("core/config.glade")
        self.frm_config = self.builder.get_object("frm_config") 
        self.btn_aplicar = self.builder.get_object("btn_aplicar")
        self.e_banco = self.builder.get_object("e_banco")
        self.sb_fonte = self.builder.get_object("sb_fonte")
        self.sb_fonte.set_adjustment(gtk.Adjustment(0, 0, 100, 1, 10, 0))
        self.builder.connect_signals(self)
        self.frm_config.show()
        
        string_xml()
        self.ler_xml()
        
        changed.status = False

    def ler_xml(self):
        self.e_banco.set_text(string_xml.arquivo_virtual.firstChild.childNodes[0].firstChild.data)
        self.sb_fonte.set_value(int(string_xml.arquivo_virtual.firstChild.childNodes[1].firstChild.data))
    
    def alterar_xml(self):
        string_xml.arquivo_virtual.firstChild.childNodes[0].firstChild.nodeValue = self.e_banco.get_text()
        string_xml.arquivo_virtual.firstChild.childNodes[1].firstChild.nodeValue = self.sb_fonte.get_value_as_int()
        
        with open(string_xml.arquivo_fisico, "w") as self.arq:            
            string_xml.arquivo_virtual.writexml(self.arq)
            self.arq.close()
    
    def on_frm_config_key_press_event(self, widget,  event):
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            if changed.status == True:
                dialogs.on_ques(self.frm_config, " Existem alterações não aplicadas. Deseja aplicar as alterações?",  self.on_btn_aplicar_clicked,  self.on_btn_sair_clicked)
                self.frm_config.destroy()
            else:
                self.frm_config.destroy()

    def on_btn_aplicar_clicked(self,  widget):       
        try:
            self.alterar_xml()
            changed.status = False
            dialogs.on_info(self.frm_config,"Alterações aplicadas com sucesso.")
        except:
           dialogs.on_warn(self.frm_config,"Problemas ao tentar aplicar alterações no arquivo de configuração. Caso persista, contate o administrador do sistema.")
    
    def on_btn_sair_clicked(self,  widget):
        self.frm_config.destroy()
    
    def on_e_banco_changed(self,  widget):
        changed.status = True

if __name__ == "__main__": # Aqui o código só será executado se este for o módulo principal e não quando ele for importado por outro programa
    app = frm_config()
    app.show_all()
    gtk.main()
