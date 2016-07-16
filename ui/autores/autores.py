#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import sqlite3
from core import dialogs,  config
import pango

class app():
    builder = gtk.Builder()
    def __init__(self):
        db.resultado_consulta = 0
        cons = frm_consulta()

class db(object):
    resultado_consulta = 0 # resultado das consultas realizadas no formulário (campo id da tabela)
    alterado = False # caso haja alteração no formulário de cadastro, muda para True (para exibir mensagem ao usuário que esquece de aplicar as alterações)
    text_tag = 0 # serve para gerar um numero sequencial das tags (negrito, italico, sublinhado,etc) dos gtk.TextTag para não ocorrer o erro de tag existente
    
class frm_consulta():
    def __init__(self):
        app.builder.add_from_file("ui/consulta.glade")
        self.frm_consulta = app.builder.get_object("frm_consulta")
        self.frm_consulta.set_title("Consulta de Autores") # CONFIGURAR

        # =======================================================================================
        self.ls_tv_consulta = gtk.ListStore(str, str) # CONFIGURAR (deve ter quantidade de campos  igual a quantidade de items do tv_colunas)
        self.tv_consulta = app.builder.get_object("tv_consulta")         
        self.tv_consulta.set_model(self.ls_tv_consulta)
        # =======================================================================================

        # =============================================================================================
        tv_colunas = {'0':'ID',  '1':'Autor'} # CONFIGURAR  (formato: 'numero_sequencial':'texto_a_ser_exibido' )    
        for tv_coluna in sorted(tv_colunas): 
            # Instanciando as colunas da treeview
            exec "self.tvc_"+str(tv_coluna)+"=gtk.TreeViewColumn('"+tv_colunas[str(tv_coluna)]+"', gtk.CellRendererText(), text="+str(tv_coluna)+")"
            # Atrinuindo as propriedades das colunas dinamicamente
            getattr(self, 'tvc_' + str(tv_coluna)).set_property("clickable", True)
            getattr(self, 'tvc_' + str(tv_coluna)).set_sort_column_id(int(tv_coluna)) 
            getattr(self, 'tvc_' + str(tv_coluna)).set_property("resizable", True) 
            getattr(self, 'tvc_' + str(tv_coluna)).set_property("reorderable", True) 
            getattr(self, 'tvc_' + str(tv_coluna)).set_property("expand", True)  
            # Adicionando as colunas à treeview
            self.tv_consulta.append_column(getattr(self, 'tvc_' + str(tv_coluna)))  
        # =============================================================================================

        self.ls_cb_parametro = gtk.ListStore(str, str)
        self.cb_parametro = app.builder.get_object("cb_parametro")
        self.cb_parametro.set_model(self.ls_cb_parametro)
        
        # ======================================================================================
        cb_campos = {'autores.id':'ID',  'autores.autor':'Autor'} # CONFIGURAR (formato: 'campo_tabela':'texto_a_ser_exibido')
        for cb_campo in sorted(cb_campos): 
            self.ls_cb_parametro.append([str(cb_campo), cb_campos[str(cb_campo)]])
        self.cb_parametro.set_active(0) # CONFIGURAR
        # ======================================================================================
        
        self.e_parametro = app.builder.get_object("e_parametro")
        self.btn_localizar = app.builder.get_object("btn_localizar")
        self.btn_adicionar = app.builder.get_object("btn_adicionar")
        self.btn_sair = app.builder.get_object("btn_sair")
        app.builder.connect_signals(self)
        
        self.frm_consulta.show()
        self.consultar('autores.id')
        db.resultado_consulta=0 # self.consultar('id') posiciona o cursor em um determinado registro, mesmo que o parametro da consulta seja %
    
    def consultar(self,  orderby):
        try:
            reload(config) # atualiza as informações do módulo.
            self.ls_tv_consulta.clear() # limpa a consulta anterior para evitar a duplicação de registros
            self.con = sqlite3.connect(config.string_db.db)
            self.cur_select = self.con.cursor()
            self.sql_select = 'SELECT autores.id, autores.autor FROM autores WHERE '  +str(self.cb_parametro.get_active_text())+ ' LIKE ? ORDER BY '+orderby
            self.parametro = ['%'+str(self.e_parametro.get_text())+'%' ]
            self.cur_select.execute(self.sql_select, self.parametro)
            self.rs_select = self.cur_select.fetchall()
            if self.rs_select != []: # Se a tabela não estiver vazia então prossegue
                for self.rec_select in self.rs_select:
                    self.ls_tv_consulta.append([self.rec_select[0],self.rec_select[1]])
                self.con.close()
                db.resultado_consulta =  self.rec_select[0] 
        except:
            dialogs.on_warn(self.frm_consulta,"Problemas ao efetuar a consulta ao banco de dados. Caso persista, contate o administrador do sistema.")

    def on_frm_consulta_key_press_event(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.frm_consulta.destroy()
    
    def on_tv_consulta_row_activated(self, tree, path, column):
        self.model = tree.get_model()
        self.iter = self.model.get_iter(path)
        db.resultado_consulta = self.model.get_value(self.iter, 0) # O numero zero indica o valor da coluna zero do objeto Treeview
        self.cad = frm_cadastro()

    def on_e_parametro_changed(self, widget):
        self.consultar(self.cb_parametro.get_active_text())
    
    def on_e_parametro_key_press_event(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == "KP_Enter":
            self.cad = frm_cadastro()
        elif gtk.gdk.keyval_name(event.keyval) == "Return":
            self.cad = frm_cadastro()
    
    def on_btn_localizar_clicked(self, widget):
        self.cad = frm_cadastro()    
    
    def on_btn_atualizar_clicked(self, widget):
        self.e_parametro.set_text("")
        self.consultar(self.cb_parametro.get_active_text())
        self.e_parametro.grab_focus()
        db.resultado_consulta = 0
    
    def on_btn_adicionar_clicked(self, widget):
        db.resultado_consulta = 0
        self.cad = frm_cadastro()  
    
    def on_btn_sair_clicked(self, widget):        
        self.frm_consulta.destroy()        

class frm_cadastro():
    def __init__(self):
        app.builder.add_from_file("ui/autores/cadastro.glade")        
        self.frm_cadastro = app.builder.get_object("frm_cadastro")
        self.e_autor = app.builder.get_object("e_autor")
        app.builder.connect_signals(self)
        self.frm_cadastro.show()
        
        if db.resultado_consulta > 0:
            self.get_registros()
        else:
            self.limpa_objetos()


    def limpa_objetos(self):
        self.e_autor.set_text("")
        self.e_autor.grab_focus()
        db.resultado_consulta = 0
        db.text_tag = 0
        db.alterado = False

    def get_registros(self):
        try:
            reload(config) # atualiza as informações do módulo.
            self.con = sqlite3.connect(config.string_db.db)
            self.parametro = [str(db.resultado_consulta), ]
            self.cur_select = self.con.cursor()
            self.cur_select.execute('select id, autor from autores where id=?', self.parametro[0])
            self.rs_select = self.cur_select.fetchall()
            
            for self.rec_select in self.rs_select:
                self.e_autor.set_text(self.rec_select[1])
            
            self.con.close()
            db.alterado = False
        except:
            dialogs.on_warn(self.frm_cadastro,"Problemas ao efetuar a consulta ao banco de dados. Caso persista, contate o administrador do sistema.")

    def on_frm_cadastro_key_press_event(self, widget, event):       
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            if db.alterado == True:
                dialogs.on_ques(self.frm_cadastro, " Existem alterações não aplicadas. Deseja aplicar as alterações?",  self.on_btn_aplicar_clicked,  self.on_btn_sair_clicked)
                self.frm_cadastro.destroy()
            else:
                self.frm_cadastro.destroy()

    def on_btn_adicionar_clicked(self, widget):
        self.limpa_objetos()

    def on_aplicar(self, tipo):
        try:
            reload(config) # atualiza as informações do módulo.
            self.con = sqlite3.connect(config.string_db.db)        
            self.parametro = [unicode(str(self.e_autor.get_text()),  'utf-8'),  str(db.resultado_consulta)]
            if tipo == 'update':
                self.cur_update = self.con.cursor()
                self.cur_update.execute('UPDATE autores SET autor=? WHERE id=?', (self.parametro[0],self.parametro[1], ))            
                self.con.commit()
            else:
                self.cur_insert = self.con.cursor()
                self.cur_insert.execute('INSERT INTO autores (autor) VALUES (?)', (self.parametro[0], ))
                self.con.commit()
                # O select abaixo é para o caso do usuário clicar no botão aplicar, mas continuar fazendo alterações no form
                # então o sistema tem que recuperar o id do registro recem salvo para conseguir efetuar o update corretamente
                self.sql_select = "SELECT MAX(id) FROM autores"
                self.cur_select = self.con.cursor()
                self.cur_select.execute(self.sql_select)
                self.rs_select = self.cur_select.fetchall()
                for self.rec_select in self.rs_select:
                    db.resultado_consulta = self.rec_select[0]

            self.con.close()
            db.alterado = False
            dialogs.on_info(self.frm_cadastro,"Alterações aplicadas com sucesso.")
        except:
            dialogs.on_warn(self.frm_cadastro,"Problemas ao tentar aplicar as alterações. Caso persista, contate o administrador do sistema.")
    
    def on_btn_aplicar_clicked(self, widget):
        if db.resultado_consulta > 0:
            self.on_aplicar('update')
        else:
            self.on_aplicar('insert')
    
    def on_btn_sair_clicked(self, widget):
        db.alterado = False
        self.frm_cadastro.destroy()
    
    def on_e_autor_changed(self, widget):
        db.alterado = True
    
if __name__ == "__main__": # Aqui o código só será executado se este for o módulo principal e não quando ele for importado por outro programa
    frm = app()
    frm.show_all()
    gtk.main()
