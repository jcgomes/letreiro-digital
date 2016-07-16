#!/usr/bin/env python
# -*- coding: cp1252 -*-
import gtk

class frm_sobre():
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("ui/sobre/sobre.glade")
        self.frm_sobre = self.builder.get_object("frm_sobre") 
        self.builder.connect_signals(self)
        self.frm_sobre.show()

