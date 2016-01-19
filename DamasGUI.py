#!/usr/bin/python
# -*- coding: utf-8 -*-
# Luis Alberto Centeno Bragado y Rafael Sillero Navajas

""" 
Juego de las Damas para la asignatura de Paradigmas de Programacion del Grado en Ingenieria Informatica de la Universidad de Valladolid.
Este juego se ha realizado con la libreria PYGTK para la implementacion grafica.
"""
__author__ = "Rafael Sillero <rafael.silnav[at]gmail.com>\nLuis Alberto Centeno <luiscbr92[at]gmail.com>"
__version__ = "1.0"
__date__ = "26 de Mayo 2014"

import gtk, os

class GUI:
    """Esta clase se encarga de manejar la interfaz grafica mediante sus procedimientos."""

    ''' Procedimientos de los botones del menu superior '''

    def menu_new(self, widget, data=None):
        """
        Crea una nueva partida, si se pulsa la opcion del menu superior.
        LLAMADAS A PROCEDIMIENTOS:
            - self.actualizar(self)
        OBJETOS:
            - Se reinicializa el atributo game que contiene una instancia de Game
        """

        self.game = Game()
        self.actualizar()

    def menu_load(self, widget, data=None):
        """
        Muestra un dialogo para elegir un archivo que contenga una partida guardada. Accede al fichero que se elige en modo lectura.
        LLAMADAS A PROCEDIMIENTOS:
            - self.actualizar(self)
            - self.add_filters(self, dialog)
            - Game.realizarMovimientosFichero(self, fich)
            - self.ponerEstado2(self, texto)
            - self.show_endgame(self, winner)
        OBJETOS:
            - Se reinicializa el atributo game que contiene una instancia de Game.
        """

        self.dialog = gtk.FileChooserDialog("Please choose a file", self.window, gtk.FILE_CHOOSER_ACTION_OPEN, 
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        self.dialog.set_current_folder(self.pathsaves)
        self.add_filters(self.dialog)
        self.response = self.dialog.run()
        if self.response == gtk.RESPONSE_OK:
            self.game = Game()
            error = self.game.realizarMovimientosFichero(self.dialog.get_filename())

            self.dialog.destroy()
            if error == "":
                self.actualizar()
            elif error == "Error: Fichero corrupto":
                self.game = Game()
                self.actualizar()
                self.ponerEstado2(error)
            elif error == "Han ganado las oscuras" or error == "Han ganado las claras":
                self.actualizar()
                self.ponerEstado2(error)
                self.show_endgame(error)
            else:
                self.ponerEstado2(error)
        else:
            self.dialog.destroy()

    def add_filters(self, dialog):
        """Establece y agrega filtros de extension de los archivos que contienen partidas guardadas."""

        self.filter_chk = gtk.FileFilter()
        self.filter_chk.set_name("DamasGUI UVa files")
        self.filter_chk.add_pattern("*.uva")
        dialog.add_filter(self.filter_chk)

    def menu_save(self, widget, data=None):
        """
        Muestra un menu para guardar la partida en un archivo. Accede al fichero que se elige en modo escritura.
        LLAMADAS A PROCEDIMIENTOS:
            - self.add_filters(self, dialog)
        """

        self.dialog = gtk.FileChooserDialog("Please choose where to save your file", self.window,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        self.dialog.set_current_folder(self.pathsaves)
        self.add_filters(self.dialog)
        self.response = self.dialog.run()
        if self.response == gtk.RESPONSE_OK:
            mov = self.game.moves
            f = open(self.dialog.get_filename() + ".uva", "w")
            for m in mov:
                f.write(m + "\n")
            f.close()
        self.dialog.destroy()

    def menu_preferences(self, widget, data=None):
        """
        Muestra y construye el menu de opciones del juego.
        LLAMADAS A PROCEDIMIENTOS:
            - self.actualizarconfig(self)
            - self.actualizar(self)
        """

        dialogo = gtk.Dialog("Preferencias",
                                  self.window,
                                  gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                  (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                   gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
                                 )

        etq = gtk.Label('Introduzca el nombre de los jugadores')
        etq.show()

        sep1 = gtk.HSeparator()
        sep1.show()

        c_entry1 = gtk.HBox(False,0)
        c_entry1.show()
        etq1 = gtk.Label('J1 (Fichas claras)')
        etq1.show()
        self.e_player1 = gtk.Entry(max=20)
        self.e_player1.set_text(self.name_player1)
        self.e_player1.show()
        c_entry1.pack_start(etq1,False,False,5)
        c_entry1.pack_start(self.e_player1,False,False,0)

        c_entry2 = gtk.HBox(False,0)
        c_entry2.show()
        etq2 = gtk.Label('J2 (Fichas oscuras)')
        etq2.show()
        self.e_player2 = gtk.Entry(max=20)
        self.e_player2.set_text(self.name_player2)
        self.e_player2.show()
        c_entry2.pack_start(etq2,False,False,5)
        c_entry2.pack_start(self.e_player2,False,False,0)

        sep2 = gtk.HSeparator()
        sep2.show()

        t = os.listdir(os.getcwd() + "/img/")

        c_entry3 = gtk.HBox(False,0)
        c_entry3.show()

        combobox = gtk.combo_box_new_text()
        combobox.append_text('Selecciona un template:')
        for template in t:
            combobox.append_text(template)
        combobox.set_active(0)
        combobox.show()

        etq3 = gtk.Label('(actual: ' + self.template + ')')
        etq3.show()

        c_entry3.pack_start(combobox,False,False,5)
        c_entry3.pack_start(etq3,False,False,5)

        sep3 = gtk.HSeparator()
        sep3.show()

        dialogo.vbox.pack_start(etq,True,False,2)
        dialogo.vbox.pack_start(sep1,True,False,2)
        dialogo.vbox.pack_start(c_entry1,True,False,2)
        dialogo.vbox.pack_start(c_entry2,True,False,2)
        dialogo.vbox.pack_start(sep2,True,False,2)
        dialogo.vbox.pack_start(c_entry3,True,False,2)
        dialogo.vbox.pack_start(sep3,True,False,2)

        response = dialogo.run()

        if response == gtk.RESPONSE_ACCEPT:
            self.name_player1 = self.e_player1.get_text()
            self.name_player2 = self.e_player2.get_text()

            model = combobox.get_model()
            index = combobox.get_active()
            if index:
                self.template = model[index][0]

            self.actualizarconfig()
            self.actualizar()

        dialogo.destroy()

    def menu_contents(self, widget, data=None):
        """
        Muestra y construye el dialogo de ayuda.
        LLAMADAS A PROCEDIMIENTOS:
            - self.click(self, widget, data=None)
        """

        self.dialog = gtk.Dialog("Ayuda", self.window)

        self.btn_ok = gtk.Button("Ok", gtk.STOCK_OK)
        self.dialog.action_area.pack_start(self.btn_ok, gtk.TRUE, gtk.TRUE, 0)
        self.dialog.connect("delete_event", self.click)
        self.btn_ok.connect("clicked", self.click)

        self.btn_ok.show()

        txt = '''
        Estás jugando a las damas con variaciones dadas por la Universidad de Valladolid.
        Empiezan jugando las fichas de arriba (las claras). Para mover, pulsa en la casilla donde está la ficha a mover    
        y después pulsa en la casilla de destino a la que quieres mover dicha ficha.
        También tienes la opción de escribir el movimiento directamente en el campo de texto.
        Para deshacer el último movimiento pulsa el botón para tal fin que se encuentra en la parte de la derecha.
        Puedes deshacer todos los movimientos de la partida, los cuales veras en la lista situada al lado.
        '''

        self.lb = gtk.Label(txt)
        self.dialog.vbox.pack_start(self.lb)
        self.lb.show()

        self.dialog.run()

    def menu_about(self, widget, data=None):
        """Muestra el dialogo con informacion sobre los autores."""

        self.about = gtk.AboutDialog()
        self.about.set_program_name("DamasGUI")
        self.about.set_version("1.0")
        self.about.set_copyright("(c) Luis Alberto Centeno & Rafael Sillero")
        self.about.set_comments("Esta es una version personalizada del juego de las damas para la asignatura de Paradigmas de Programacion del Grado en Ingeniería Informática de la Universidad de Valladolid.")
        self.about.set_website("http://inf.uva.es")
        self.about.run()
        self.about.destroy()  

    ''' ***** '''

    ''' Procedimientos de muestreo de informacion en el juego '''

    def actualizar(self):
        """
        Se encarga de llamar a todas los procedimientos que actualizan la informacion que se muestra en la ventana del juego.
        LLAMADAS A PROCEDIMIENTOS:
            - self.actualizarTablero(self)
            - self.actualizarMoves(self)
            - self.actualizarEstado(self)
            - self.actualizarTablaRonda(self)
        """

        self.actualizarTablero()
        self.actualizarMoves()
        self.actualizarEstado()
        self.actualizarTablaRonda()

    def actualizarEstado(self):
        """
        Actualiza la barra de estado, que esta en la parte inferior de la ventana.
        LLAMADAS A PROCEDIMIENTOS:
            - self.ponerEstado1(self, texto)
            - self.ponerEstado2(self, texto)
        """

        txt = ""
        if self.game.turno:
            txt = self.name_player1
        else:
            txt = self.name_player2
        self.ponerEstado1("Turno de " + txt)
        self.ponerEstado2("Pulse la ficha que desea mover.")

    def ponerEstado1(self, texto):
        """Pone la informacion que recibe en el parametro texto en el estado de la izquierda."""

        self.st1.push(self.context_id1, texto)

    def ponerEstado2(self, texto):
        """Pone la informacion que recibe en el parametro texto en el estado de la derecha."""

        self.st2.push(self.context_id2, texto)

    def actualizarMoves(self):
        """
        Actualiza la tabla de movimientos realizados en la partida. Tambien se encarga de activar y desactivar el boton de deshacer.
        LLAMADAS A PROCEDIMIENTOS:
            - self.anadirMovimiento(self, move)
        """

        mov = self.game.moves
        if mov == []:
            self.btnUndo.set_sensitive(False)
            self.liststore.clear()
        else:
            self.btnUndo.set_sensitive(True)
            self.liststore.clear()
            for i in range(len(mov)):
                self.anadirMovimiento([self.name_player1 if (i%2)==0 else self.name_player2, mov[i]])

    def anadirMovimiento(self, move):
        """ Agrega un movimiento a la lista de movimientos de la tabla """

        self.liststore.append(move)

    def actualizarTablero(self):
        """Se encarga de actualizar el tablero del juego, colocando las imagenes de las fichas correspondientes a cada boton."""

        tab = self.game.tablero
        tab = tab[::-1]
        for row in range(8):
            for cell in range(8):
                if not tab[row][cell][0]:
                    if tab[row][cell][1]:
                        if tab[row][cell][2]:
                            img = "blancasd.png"
                        else:
                            img = "blancas.png"
                    else:
                        if tab[row][cell][2]:
                            img = "negrasd.png"
                        else:
                            img = "negras.png"
                else:
                    if (row + cell) % 2 != 0:
                        img = "white.png"
                    else:
                        img = "black.png"
                image = gtk.Image()
                image.set_from_file("img/" + self.template + "/" + img)
                image.show()
                self.botones[cell][row].set_image(image)

    def actualizarTablaRonda(self):
        """
        Actualiza la tabla que indica las fichas restantes de cada jugador.
        LLAMADAS A PROCEDIMIENTOS:
            - Game.contar_fichas(self)
        OBJETOS:
            - Se trabaja con el atributo game que contiene una instancia de Game.
        """

        fblancas, fnegras = self.game.contar_fichas()

        cad = "Fichas claras"
        if self.name_player1 != cad:
            cad += " (" + str(self.name_player1) + ")"
        self.tablej1.set_text(cad)

        cad = "Fichas oscuras"
        if self.name_player2 != cad:
            cad += " (" + str(self.name_player2) + ")"
        self.tablej2.set_text(cad)

        self.tableblancas.set_text(str(fblancas))

        self.tablenegras.set_text(str(fnegras))

    def show_endgame(self, winner):
        """
        Hace aparecer un dialogo al final de la partida que muestra el ganador y pregunta si se desea reiniciar el juego.
        Si se reinicia el juego, se inicializa una nueva instancia de Game, que se guarda sobre el mismo atributo que albergaba la anterior instancia.
        Si no se reinicia el juego se cierra el programa.
        LLAMADAS A PROCEDIMIENTOS:
            - self.actualizar(self)
            - self.quit_program(self, widget=None, event=None, data=None)
        OBJETOS:
            - Se reinicializa el atributo game que contiene una instancia de Game.
        """

        dialogo = gtk.Dialog("Fin del juego",
                                  self.window,
                                  gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                  (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                   gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
                                 )

        cad = "Ha ganado "
        if winner == "Han ganado las claras":
            cad += self.name_player1
        else:
            cad += self.name_player2
        cad += ".\n¿Desean volver a jugar?"
        etq = gtk.Label(cad)
        etq.show()

        dialogo.vbox.pack_start(etq,True,False,2)
        response = dialogo.run()
        if response == gtk.RESPONSE_ACCEPT:
            self.game = Game()
            self.actualizar()
        else:
            self.quit_program()

        dialogo.destroy()

    ''' ***** '''

    ''' Procedimeintos de los botones de la interfaz '''
    
    def btn_send(self, widget, data=None):
        """
        Este procedimiento se activa cuando el programa recibe la orden de hacer algun movimiento. Se encarga de enviarselo al objeto game.
        Si el movimiento recibido no es valido, muestra el error en el estado de la derecha.
        LLAMADAS A PROCEDIMIENTOS:
            - Game.realizarMovimiento(self, play)
            - self.actualizar(self)
            - self.ponerEstado2(self, texto)
        OBJETOS:
            - Se trabaja con el atributo game que contiene una instancia de Game.
        """

        error = self.game.realizarMovimiento((self.entry.get_text()).upper())
        if error == "":
            self.actualizar()
        else:
            self.ponerEstado2(error)

    def btn_undo(self, widget, data=None):
        """
        Se encarga de deshacer el ultimo movimiento. Para ello, reinicializa la instancia de Game, y realiza todos los movimientos realizados hasta el momento, salvo el ultimo.
        Dicho movimiento es borrado de la lista de movimientos.
        LLAMADAS A PROCEDIMIENTOS:
            - Game.realizarMovimiento(self, play)
            - self.actualizar(self)
        OBJETOS:
            - Se reinicializa el atributo game que contiene una instancia de Game.
        """

        movimientos = self.game.moves[:-1]
        self.game = Game()
        for m in movimientos:
            self.game.realizarMovimiento(m)
        self.liststore.remove(self.liststore[-1].iter)  
        self.actualizar()

    def callback(self, widget, data=None):
        """
        Se encarga de gestionar las entrada de movimientos a partir de los clicks en el tablero. Diferencia entre el primer click para el origen, y el segundo para el destino.
        Seguidamente construye el movimiento en formato string y lo envia para que se procese.
        LLAMADAS A PROCEDIMIENTOS:
            - Game.realizarMovimiento(self, play)
            - self.actualizar(self)
            - self.ponerEstado2(self, texto)
            - self.show_endgame(self, winner)
            OBJETOS:
            - Se trabaja con el atributo game que contiene una instancia de Game.
        """

        if self.hapulsado == True:
            self.hapulsado = False
            error = self.game.realizarMovimiento("%s%s" % (self.prevmove,chr(65+int(data[0][0])) + str(int(data[0][1])+1)))
            if error == "":
                self.actualizar()
            elif error == "Han ganado las oscuras" or error == "Han ganado las claras":
                self.actualizar()
                self.ponerEstado2(error)
                self.show_endgame(error)
            else:
                self.ponerEstado2(error)
        else:
            self.prevmove = chr(65+int(data[0][0])) + str(int(data[0][1])+1)
            self.ponerEstado2("Pulse en la posición de destino.")
            self.hapulsado = True

    ''' ***** '''

    ''' Procedimientos relacionados con el fichero de configuracion '''

    def initconfig(self):
        """
        Se encarga de manejar el fichero de configuracion del juego. Si dicho fichero no existe, lo crea y lo establece con los valores predeterminados.
        El fichero de configuracion contiene los nombres de usuario y la plantilla de tablero.
        """

        try:
            f = open("DamasGUI.cfg", "r")
            self.name_player1 = f.readline().rstrip()
            self.name_player2 = f.readline().rstrip()
            self.template = f.readline().rstrip()
        except IOError:
            f = open("DamasGUI.cfg", "w")
            f.write(self.name_player1 + "\n")
            f.write(self.name_player2 + "\n")
            self.template = "default"
            f.write(self.template + "\n")
        finally:
            f.close()

    def actualizarconfig(self):
        """Actualiza el fichero de configuracion del juego."""

        f = open("DamasGUI.cfg", "w")
        f.write(self.name_player1 + "\n")
        f.write(self.name_player2 + "\n")
        f.write(self.template + "\n")
        f.close()

    ''' ***** '''

    ''' Otros procedimientos '''

    def click(self, widget, data=None):
        """Se encarga de cerrar el dialogo de ayuda cuando se pulsa uno de los botones destinados a ello."""

        self.dialog.destroy()

    def quit_program(self, widget=None, event=None, data=None):
        """Cierra el programa."""
        gtk.main_quit()

    ''' ***** '''

    ''' Procedimientos relacionados con la inicializacion de la clase '''

    def initmenu(self):
        """
        Se encarga de iniciar el menu de opciones. Asigna atajos de teclado para cada opcion y de conectarlos con su funcion correspondiente.
        LLAMADAS A PROCEDIMIENTOS:
            - self.menu_new(self, widget, data=None)
            - self.menu_save(self, widget, data=None)
            - self.menu_load(self, widget, data=None)
            - self.quit_program(self, widget=None, event=None, data=None)
            - self.menu_preferences(self, widget, data=None)
            - self.menu_contents(self, widget, data=None)
            - self.menu_about(self, widget, data=None)
        """

        self.agr = gtk.AccelGroup()
        self.window.add_accel_group(self.agr)

        self.menu_bar = gtk.MenuBar()
        self.mainbox.pack_start(self.menu_bar, False, False, 0)
        self.menu_bar.show()

        # Menu desplegable de Juego
        self.root_juego = gtk.MenuItem("Juego")
        self.root_juego.show()
        self.menu_juego = gtk.Menu()

        self.menu_juego_item1 = gtk.ImageMenuItem(gtk.STOCK_NEW, self.agr)
        self.key, self.mod = gtk.accelerator_parse("<Control>N")
        self.menu_juego_item1.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_juego_item1.connect("activate", self.menu_new, "Nuevo")
        self.menu_juego.append(self.menu_juego_item1)
        self.menu_juego_item1.show()

        self.menu_juego_item2 = gtk.ImageMenuItem(gtk.STOCK_SAVE, self.agr)
        self.key, self.mod = gtk.accelerator_parse("<Control>S")
        self.menu_juego_item2.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_juego_item2.connect("activate", self.menu_save, "Guardar")
        self.menu_juego.append(self.menu_juego_item2)
        self.menu_juego_item2.show()

        self.menu_juego_item3 = gtk.ImageMenuItem(gtk.STOCK_OPEN, self.agr)
        self.key, self.mod = gtk.accelerator_parse("<Control>O")
        self.menu_juego_item3.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_juego_item3.connect("activate", self.menu_load, "Cargar")
        self.menu_juego.append(self.menu_juego_item3)
        self.menu_juego_item3.show()

        self.menu_juego_item4 = gtk.ImageMenuItem(gtk.STOCK_QUIT, self.agr)
        self.key, self.mod = gtk.accelerator_parse("<Control>Q")
        self.menu_juego_item4.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_juego_item4.connect("activate", self.quit_program)
        self.menu_juego.append(self.menu_juego_item4)
        self.menu_juego_item4.show()

        # menu desplegable de Editar
        self.root_editar = gtk.MenuItem("Editar")
        self.root_editar.show()
        self.menu_editar = gtk.Menu()

        self.menu_editar_item1 = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES, self.agr)
        self.key, self.mod = gtk.accelerator_parse("<Control>P")
        self.menu_editar_item1.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_editar_item1.connect("activate", self.menu_preferences, "Preferencias")
        self.menu_editar.append(self.menu_editar_item1)
        self.menu_editar_item1.show()

        # menu desplegable de Ayuda
        self.root_ayuda = gtk.MenuItem("Ayuda")
        self.root_ayuda.show()
        self.menu_ayuda = gtk.Menu()

        self.menu_ayuda_item1 = gtk.ImageMenuItem(gtk.STOCK_HELP)
        self.key, self.mod = gtk.accelerator_parse("F1")
        self.menu_ayuda_item1.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_ayuda_item1.connect("activate", self.menu_contents, "Contenidos")
        self.menu_ayuda.append(self.menu_ayuda_item1)
        self.menu_ayuda_item1.show()

        self.menu_ayuda_item2 = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.key, self.mod = gtk.accelerator_parse("F2")
        self.menu_ayuda_item2.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.menu_ayuda_item2.connect("activate", self.menu_about, "Acerca de")
        self.menu_ayuda.append(self.menu_ayuda_item2)
        self.menu_ayuda_item2.show()

        self.root_juego.set_submenu(self.menu_juego)
        self.root_editar.set_submenu(self.menu_editar)
        self.root_ayuda.set_submenu(self.menu_ayuda)

        self.menu_bar.append(self.root_juego)
        self.menu_bar.append(self.root_editar)
        self.menu_bar.append(self.root_ayuda)

    def initcontent(self):
        """
        Se encarga de iniciar todo el contenido principal de la ventana del programa: el tablero y los controles del juego que hay en la parte derecha.
        LLAMADAS A PROCEDIMIENTOS:
            - self.btn_send(self, widget, data=None)
            - self.btn_undo(self, widget, data=None)
            - self.callback(self, widget, data=None)
        """

        self.contentbox = gtk.HBox(False, 20)
        self.contentbox.set_border_width(20)
        self.mainbox.pack_start(self.contentbox)

        self.table = gtk.Table(9, 9, True)
        self.contentbox.pack_start(self.table)
        
        self.separator2 = gtk.VSeparator()
        self.contentbox.pack_start(self.separator2)

        # Caja vertical situada a la derecha para ubicar los controles
        self.rightbox = gtk.VBox(False, 20)
        self.contentbox.pack_start(self.rightbox)

        # Caja para el campo de texto y enviar
        self.inputbox = gtk.HBox(False, 30)
        self.rightbox.pack_start(self.inputbox, False, False, 100)

        # Campo de texto para la jugada
        self.entry = gtk.Entry()
        self.entry.set_max_length(50)
        self.entry.connect("activate", self.btn_send, [])
        self.entry.select_region(0, len(self.entry.get_text()))
        self.inputbox.pack_start(self.entry)
        self.entry.show()

        # Boton para enviar la jugada escrita en el entry
        self.btnSend = gtk.Button("Enviar", gtk.STOCK_OK)
        self.inputbox.pack_start(self.btnSend, False, False)
        self.btnSend.connect("clicked", self.btn_send, [])

        # Tabla de estado de la partida
        self.round_status_table = gtk.Table(2, 2, True)
        self.rightbox.pack_start(self.round_status_table, False, False)
        self.tablej1 = gtk.Label()
        self.round_status_table.attach(self.tablej1, 0, 1, 0, 1)
        self.tablej2 = gtk.Label()
        self.round_status_table.attach(self.tablej2, 0, 1, 1, 2)
        self.tableblancas = gtk.Label()
        self.round_status_table.attach(self.tableblancas, 1, 2, 0, 1)
        self.tablenegras = gtk.Label()
        self.round_status_table.attach(self.tablenegras, 1, 2, 1, 2)


        self.btnUndo = gtk.Button("Deshacer", gtk.STOCK_UNDO)
        self.key, self.mod = gtk.accelerator_parse("<Control>Z")
        self.btnUndo.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
        self.rightbox.pack_start(self.btnUndo, False, False)
        self.btnUndo.connect("clicked", self.btn_undo, [])

        self.initlist()

        for i in xrange(1, 9):
            lb = gtk.Label(chr(73-i))
            self.table.attach(lb, 0, 1, i , i+1)

        for i in xrange(1, 9):
            lb = gtk.Label(i)
            self.table.attach(lb, i, i+1, 0, 1)

        self.botones = []
            
        for i in xrange(1, 9):
            temp = []
            for j in xrange(1, 9):
                button = gtk.Button()

                button.set_focus_on_click(False)
                button.set_relief(gtk.RELIEF_NONE)
                button.connect("clicked", self.callback, [str(8-j) + str(i-1)])
                self.table.attach(button, i, i+1, j, j+1)
                temp.append(button)
                
            self.botones.append(temp)

        self.window.set_focus(self.entry)
        self.contentbox.show()
        self.tablero = gtk.VBox

    def initlist(self):
        """Se encarga de iniciar la tabla donde se muestra la lista de movimientos de la partida actual."""

        self.liststore = gtk.ListStore(str, str)

        treeview = gtk.TreeView(model=self.liststore)

        renderer_text1 = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Jugador", renderer_text1, text=0)
        treeview.append_column(column_text)

        renderer_text2 = gtk.CellRendererText()
        column_toggle = gtk.TreeViewColumn("Movimiento", renderer_text2, text=1)
        treeview.append_column(column_toggle)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.add_with_viewport(treeview)
        scrolled_window.set_size_request(300,200)
        scrolled_window.show()

        self.rightbox.pack_start(scrolled_window, False, False)

    def initstatus(self):
        """Inicia la barra de estado."""

        self.bottombox = gtk.HBox(False, 0)
        self.mainbox.pack_start(self.bottombox)
        self.bottombox.show()

        # Barra de estado izquierda
        self.st1 = gtk.Statusbar()   
        self.st1.set_has_resize_grip(False)
        self.bottombox.pack_start(self.st1, True, True, 0)
        self.context_id1 = self.st1.get_context_id("Statusbar example")
        self.st1.show()

        # Barra de estado derecha
        self.st2 = gtk.Statusbar()
        self.st2.set_has_resize_grip(False)
        self.bottombox.pack_start(self.st2, True, True, 0)
        self.context_id2 = self.st2.get_context_id("Statusbar example")
        self.st2.show()

    def __init__(self):
        """
        Inicializa las instancias de esta clase.
        LLAMADAS A PROCEDIMIENTOS:
            - self.initconfig(self)
            - self.quit_program(self, widget=None, event=None, data=None)
            - self.initmenu(self)
            - self.initcontent(self)
            - self.initstatus(self)
            - self.actualizar(self)
        OBJETOS:
            - Se inicializa el atributo game que contiene una instancia de Game
        """

        self.game = Game()

        self.hapulsado = False
        self.prevmove = ""
        self.name_player1 = "Fichas claras"
        self.name_player2 = "Fichas oscuras"

        self.pathimg = "img/"
        self.pathsaves = "saves/"

        self.initconfig()


        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(False)
        self.window.set_icon_from_file("icon.ico")
        self.window.move(200,200)

        self.window.set_title("DamasGUI")
        self.window.connect("delete_event", self.quit_program)
        self.window.set_border_width(0)

        self.mainbox = gtk.VBox(False, 0)
        self.window.add(self.mainbox)
        self.mainbox.show()

        self.initmenu()
        self.initcontent()
        self.initstatus()

        self.window.show_all()

        self.actualizar()

    ''' ***** '''

pila = []

class Game:
    """ Esta clase se encarga de controlar las reglas del juego."""

    ''' Procedimientos que devuelven informacion para el muestreo de informacion por parte de la clase GUI '''

    def getTablero(self):
        """
        Devuelve el tabero interno.
        RETORNOS:
            - self.tablero
        """

        return self.tablero

    def getMoves(self):
        """
        Devuelve la lista de movimientos realizados durante la partida actual.
        RETORNOS:
            - self.moves
        """

        return self.moves

    ''' ***** '''

    ''' Procedimientos relacionados con la realizacion de movimientos '''
    def realizarMovimientosFichero(self, fich):
        """
        Se encarga de realizar los movimientos que se indican desde un fichero con una partida guardada.
        Es capaz de detectar errores en el fichero, su existencia, o si la partida guardada llega a su fin. Estos escenarios solo pueden darse si se fuerza en el propio fichero.
        LLAMADAS A PROCEDIMIENTOS:
            - self.verificar_jugada(self, tablero, turno, jugada)
            - self.jugar(self, tablero, jugada, turno, pila)
        RETORNOS:
            - endgame: string que contiene incidencias sobre el fichero (si esta corrupto o si hay fin de partida).
        """

        endgame = ""

        try:
            f = open(fich, "r")

            for linea in f:
                linea = linea.rstrip()

                if len(linea) != 4:
                    jugada = (-1,-1,-1,-1)
                else:
                    jugada = (ord(linea[0])-ord("A"),ord(linea[1])-ord("1"),ord(linea[2])-ord("A"),ord(linea[3])-ord("1"))

                res = self.verificar_jugada(self.tablero,self.turno,jugada)

                if res < 0:
                    self.moves.append(linea)
                    self.jugar(self.tablero,jugada,self.turno,pila)
                    self.turno = not self.turno
                else:
                    endgame = "ERROR: Fichero corrupto"
                    break
                # Deteccion de final de partida
                if self.num_piezas(self.tablero,self.turno) == 0:
                    if self.turno:
                        endgame = "Han ganado las oscuras"
                    else:
                        endgame = "Han ganado las claras"
                    break

            f.close()

        except IOError:
            endgame = "ERROR: El fichero no existe"

        finally:
            return endgame

    def realizarMovimiento(self, play):
        """
        Se encarga de procesar una jugada que recibe en el parametro play.
        LLAMADAS A PROCEDIMIENTOS:
            - self.verificar_jugada(self, tablero, turno, jugada)
            - self.jugar(self, tablero, jugada, turno, pila)
            - self.num_piezas(self, tablero, turno)
        RETORNOS:
            - Devuelve un string que puede contener incidencias de la partida.
        """

        play = play.rstrip()

        if len(play) != 4:
            jugada = (-1,-1,-1,-1)
        else:
            jugada = (ord(play[0])-ord("A"),ord(play[1])-ord("1"),ord(play[2])-ord("A"),ord(play[3])-ord("1"))

        res = self.verificar_jugada(self.tablero,self.turno,jugada)

        if res < 0:
            self.moves.append(play)
            self.jugar(self.tablero,jugada,self.turno,pila)
            self.turno = not self.turno
        else:
            return "ERROR: " + self.MSG_STATUS[res]

        # Deteccion de final de partida
        if self.num_piezas(self.tablero,self.turno) == 0:
            if self.turno:
                return "Han ganado las oscuras"
            else:
                return "Han ganado las claras"

        return ""

    def signo(self, x):
        """
        Devuelve 0, 1 o -1 en funcion del parametro x.
        RETORNOS:
            - 1 si x es positivo
            - -1 si x es negativo
            - 0 si x es 0
        """

        return 1 if x > 0 else (-1 if x < 0 else 0)

    def verificar_jugada(self, tablero, turno, jugada):
        """
        Comprueba si la jugada puede realizarse o no.
        LLAMADAS A PROCEDIMIENTOS:
            - self.signo(self, x)
        RETORNOS:
            - Un entero. Puede referirse al indice de la lista MSG_STATUS. Ver codigo para mas informacion.
        """

        # Sintaxis valida
        for i in jugada:
            if i < 0 or i > 7:
                return 0
        (f0,c0,f1,c1) = jugada

        # Casilla de origen vacia
        if tablero[f0][c0] == self.CASILLA_VACIA:
            return 1

        # Casilla de origen con pieza de color distinto al turno
        if tablero[f0][c0][self.SEL_COLOR] != turno:
            return 2

        # Movimiento diagonal
        # Nota: No es necesario comprobar que d > 0, error captura pieza propia
        d = abs(f1-f0)
        if d != abs(c1-c0):
            return 3
        sf, sc = self.signo(f1-f0), self.signo(c1-c0)

        # Movimiento adyacente si es un peon o libre de obstaculos si reina
        if tablero[f0][c0][self.SEL_REINA]:
            for i in range(1,d):
                if tablero[f0+i*sf][c0+i*sc] != self.CASILLA_VACIA:
                    return 4
        else:
            if d != 1:
                return 5

        # Casilla de destino vacia (resultado correcto, no hay captura)
        if tablero[f1][c1] == self.CASILLA_VACIA:
            return -1

        # Casilla de destino ocupada:
        # Comprobar que es pieza de distinto color al del turno
        if tablero[f1][c1][self.SEL_COLOR] == turno:
            return 6

        # Captura: Calcular celda de destino tras captura
        f2, c2 = f1+sf, c1+sc

        # Comprobar que este en rango y vacia
        if f2 < 0 or f2 > 7 or c2 < 0 or c2 > 7:
            return 7
        if tablero[f2][c2] != self.CASILLA_VACIA:
            return 8

        # Movimiento correcto y se produce captura
        return -2

    def hacer_movimiento(self, tablero, jugada, pila):
        """
        Se encarga de realizar un movimiento de ficha, detectando promocion a reina y captura
        LLAMADAS A PROCEDIMIENTOS:
            - self.signo(self, x)
        RETORNOS:
            - captura: valor logico.
        """

        (f0,c0,f1,c1) = jugada

        # Detectar si es captura y calcular posicion final
        captura = tablero[f1][c1] != self.CASILLA_VACIA
        if captura:
            f2,c2 = f1+self.signo(f1-f0), c1+self.signo(c1-c0)
        else:
            f2,c2 = f1,c1

        # Detectar si es promocion a reina
        color = tablero[f0][c0][self.SEL_COLOR]
        if tablero[f0][c0][self.SEL_REINA]:
            promocion = False
        else:
            promocion = (color and f2 == 0) or (not color and f2 == 7)

        # Incluir movimiento en pila
        pila.append((f0,c0,f1,c1,f2,c2,tablero[f1][c1],promocion))

        # Actualizar tablero
        if promocion:
            tablero[f2][c2] = (False, color, True)
        else:
            tablero[f2][c2] = tablero[f0][c0]
        if captura:
            tablero[f1][c1] = self.CASILLA_VACIA
        tablero[f0][c0] = self.CASILLA_VACIA
        return captura

    def deshacer_movimiento(self, tablero, pila):
        """Se encarga de deshacer el ultimo movimiento que hay en la pila."""

        (f0,c0,f1,c1,f2,c2,casilla,promocion) = pila.pop()
        color = tablero[f2][c2][self.SEL_COLOR]
        if promocion:
            tablero[f0][c0] = (False, color, False)
        else:
            tablero[f0][c0] = tablero[f2][c2]
        tablero[f2][c2] = self.CASILLA_VACIA
        if f1 != f2: # Captura
            tablero[f1][c1] = casilla

    def jugar(self, tablero, jugada, turno, pila):
        """
        Se encarga de buscar nuevas posibles capturas en caso de que ya se haya producido una.
        LLAMADAS A PROCEDIMIENTOS:
            - self.explorar(self, tablero, f0, c0, turno, pila)
            - self.jugar(self, tablero, jugada, turno, pila)    RECURSIVIDAD
        """

        if self.hacer_movimiento(tablero, jugada, pila):

            # Se ha producido una captura: Explorar posibles nuevas capturas
            (_,_,_,_,f0,c0,_,_) = pila[-1]
            (n,f1,c1) = self.explorar(tablero, f0, c0, turno, pila)
            if n > 0: # Existen nuevas capturas, la optima comienza por (f1,c1)
                self.jugar(tablero, (f0,c0,f1,c1), turno, pila)

    def explorar(self, tablero, f0, c0, turno, pila):
        """
        Se encarga de explorar las 4 diagonales alrededor en busca de nuevas capturas.
        LLAMADAS A PROCEDIMIENTOS:
            - self.verificar_jugada(self, tablero, turno, jugada)
            - self.hacer_movimiento(self, tablero, pila)
            - self.explorar(self, tablero, f0, c0, turno, pila)     RECURSIVIDAD
            - self.deshacer_movimiento(self, tablero, pila)
        RETORNOS:
            - (nmax,fmax,cmax): una tupla con informacion sobre el camino que mas fichas opuestas elimina.
        """

        nmax = 0 # Numero maximo de capturas
        fmax = cmax = -1 # Movimiento con mayor numero de capturas
        reina = tablero[f0][c0][self.SEL_REINA]

        # Examinar las 4 diagonales
        for (sf,sc) in self.DIRS:
            f1, c1 = f0+sf, c0+sc

            # Si es reina, avanzar por la diagonal hasta encontrar una pieza
            if reina:
                while 0 <= f1 <= 7 and 0 <= c1 <= 7 and tablero[f1][c1][self.SEL_VACIA]:
                    f1 += sf
                    c1 += sc

            # Si el movimiento es valido y es una captura..
            if self.verificar_jugada(tablero, turno, (f0,c0,f1,c1)) == -2:

                # Hacer movimiento
                self.hacer_movimiento(tablero, (f0,c0,f1,c1), pila)

                # Explorar a partir del movimiento
                (_,_,_,_,f2,c2,_,_) = pila[-1]
                (n,_,_) = self.explorar(tablero, f2, c2, turno, pila)

                # Deshacer movimiento
                self.deshacer_movimiento(tablero, pila)

                # Comprobar si las capturas superan el maximo
                n += 1
                if n > nmax:
                    nmax, fmax, cmax = n, f1, c1

        # Devolver el resultado
        return (nmax,fmax,cmax)

    ''' ***** '''

    ''' Proceidmientos para contar fichas '''

    def num_piezas(self, tablero, turno):
        '''
        Cuenta las fichas restantes del jugador opuesto.
        RETORNOS:
            - n: numero de fichas del jugador opuesto
        '''

        n = 0
        for fila in tablero:
            for (vacia,color,_) in fila:
                if not vacia and color == turno:
                    n += 1
        return n

    def contar_fichas(self):
        '''
        Cuenta las fichas restantes de cada jugador.
        RETORNOS:
            - fblancas: numero de fichas blancas restantes.
            - fnegras: numero de fichas negras restantes.
        '''

        fblancas = 0
        fnegras = 0

        for i in range(8):
            for j in range(8):
                if self.tablero[i][j] == self.PEON_BLANCO or self.tablero[i][j] == self.REINA_BLANCA:
                    fblancas += 1
                elif self.tablero[i][j] == self.PEON_NEGRO or self.tablero[i][j] == self.REINA_NEGRA:
                    fnegras += 1

        return fblancas, fnegras

    ''' ***** '''

    ''' Procedimientos relacionados con la inicializacion de la clase '''

    def __init__(self):
        """
        Inicializa las instancias de esta clase.
        LLAMADAS A PROCEDIMIENTOS:
            - self.initTablero(self)
        """

        self.SEL_VACIA = 0
        self.SEL_COLOR = 1
        self.SEL_REINA = 2

        # Las 5 posibilidades para cada casilla:
        self.PEON_BLANCO   = (False,True,False)
        self.PEON_NEGRO    = (False,False,False)
        self.REINA_BLANCA  = (False,True,True)
        self.REINA_NEGRA   = (False,False,True)
        self.CASILLA_VACIA = (True,False,False)

        # Para pasar de coordenadas numericas a caracteres
        self.NOM_FIL = "ABCDEFGH"
        self.NOM_COL = "12345678"

        # Mensajes asociados al valor devuelto por verificar_jugada
        self.MSG_STATUS = [
            "Sintaxis no valida",
            "Casilla origen vacia",
            "Casilla origen no contiene pieza del color correspondiente al turno actual",
            "Movimiento no diagonal",
            "Existen piezas intermedias en el movimiento",
            "Casilla de destino no es adyacente",
            "Casilla de destino ocupada por pieza del mismo color",
            "No se puede capturar una pieza en el borde del tablero",
            "Captura bloqueada por otra pieza adyacente"]

        # DIRS es una lista con las direcciones de las 4 diagonales
        self.DIRS = [(-1,-1),(-1,1),(1,-1),(1,1)]

        self.tablero = self.initTablero()
        self.moves = []
        self.turno = True

    def initTablero(self):
        """
        Inicializa el tablero interno del programa.
        RETORNOS:
            - tab: contiene el tablero interno del programa.
        """

        tab = [[],[],[],[],[],[],[],[]]
        for fil in range(8):
            for col in range(8):
                if (fil+col) % 2 == 1:
                    if fil < 3:
                        tab[fil].append(self.PEON_NEGRO)
                    elif fil > 4:
                        tab[fil].append(self.PEON_BLANCO)
                    else:
                        tab[fil].append(self.CASILLA_VACIA)
                else:
                    tab[fil].append(self.CASILLA_VACIA)
        return tab

    ''' ***** '''


if __name__=='__main__':
    app = GUI()
    gtk.main()