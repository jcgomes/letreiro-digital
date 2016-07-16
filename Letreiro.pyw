#!/usr/bin/python
# -*- coding: utf-8-*-
import pygtk
pygtk.require('2.0')
import gtk
from core import config
from ui.autores import autores
from ui.letras import letras
from ui.palco import id,  letra
from ui.sobre import sobre

class frm_principal(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_icon_from_file('icons/icon.png')
        self.set_title("Letreiro Digital")
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.set_resizable(False)
        self.maximize()

        self.connect("destroy", gtk.main_quit)

        self.ui = self.gerar_ui()
        self.add_accel_group(self.ui.get_accel_group())
        self.toolbar1 = self.ui.get_widget("/toolbar")
        self.menubar = self.ui.get_widget("/menubar")

        self.layout = gtk.VBox()
        self.layout.pack_start(self.menubar, False)
        self.layout.pack_start(self.toolbar1, False)
        self.add(self.layout)

    def gerar_ui(self):
        ui_def = """
        <ui>
          <menubar name="menubar">
            <menu action="menu_arquivo">
              <menuitem action="sair" />
            </menu>
            <menu action="menu_cadastros">
              <menuitem action="autores" />
              <menuitem action="letras" />
            </menu>
            <menu action="menu_edit">
              <menuitem action="config" />
            </menu>
            <menu action="menu_palco">
              <menuitem action="id" />
              <menuitem action="letra" />
            </menu>
            <menu action="menu_ajuda">
              <menuitem action="sobre" />
            </menu>
          </menubar>
          <toolbar name="toolbar">
            <toolitem action="id" />
            <separator />
            <toolitem action="letra" />
            <separator />
            <toolitem action="sair" />
          </toolbar>
        </ui>
        """

        actions = gtk.ActionGroup("Actions")
        actions.add_actions([
          ("menu_arquivo", None, "_Arquivo"),
          ("menu_cadastros", None, "_Cadastros"),
          ("menu_edit", None, "_Editar"),
          ("menu_palco", None, "_Palco"),
          ("menu_ajuda", None, "_Ajuda"),

          ("sair", gtk.STOCK_QUIT, "_Sair", None, "Sair do sistema", self.on_sair),

          ("autores", None, "_Autores", None, None, self.on_autores),
          ("letras", None, "_Letras", None, None, self.on_letras),

          ("config", None, "_Configurações", None, None, self.on_config),

          ("id", gtk.STOCK_MEDIA_PLAY, "_ID", None, "ID",  self.on_id),
          ("letra", gtk.STOCK_BOLD, "_Letra",  None, "Letra", self.on_letra),

          ("sobre", gtk.STOCK_ABOUT, "Sobre", None, None, self.on_sobre),
        ])

        ui = gtk.UIManager()
        ui.insert_action_group(actions)
        ui.add_ui_from_string(ui_def)
        return ui

    def on_sair(self, action):
        raise SystemExit
    def on_autores(self, action):
        self.cons_autores = autores.frm_consulta()
    def on_letras(self, action):
        self.cons_letras = letras.frm_consulta()
    def on_config(self, action):
        self.config = config.frm_config()
    def on_letra(self, action):
        self.letra = letra.frm_letra()
    def on_id(self, action):
        self.id_atual = id.frm_id()
    def on_sobre(self, action):
        self.sobre = sobre.frm_sobre()

if __name__ == "__main__": # Aqui o código só será executado se este for o módulo principal e não quando ele for importado por outro programa
    app = frm_principal()
    app.show_all()
    gtk.main()
