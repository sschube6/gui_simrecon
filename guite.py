import pygtk
import gtk
pygtk.require('2.0')


class Base:
    def __init__(self):
        # set global variables
        self.filename = 'sss'
        self.otf = ''
        self.out = './out'

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("cudaSIM")

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        # We create a vertical box (vbox) to pack our horizontal boxes into.
        # This allows us to stack the horizontal boxes filled with buttons one
        # on top of the other in this vbox.
        box1 = gtk.VBox(False, 0)

        # We create a horizontal box to pack widgets into. The box is not
        # really visible, it is just used as a tool to arrange widgets.
        hbox1 = gtk.HBox(False, 0)

        # Create a new button for raw data file selection
        button_file = gtk.Button("File")
        button_file.connect("clicked", self.select_file, None)
        hbox1.pack_start(button_file, False, False, 0)
        button_file.show()

        # Create text fields to show file names
        self.text_file = gtk.Entry(max=0)
        self.text_file.set_text(self.filename)
        self.text_file.set_editable(True)
        self.text_file.connect("changed", self.change_text, "file")
        hbox1.pack_start(self.text_file, True, True, 0)
        self.text_file.show()

        box1.pack_start(hbox1, False, False, 0)
        hbox1.show()

        # We create a horizontal box to pack widgets into. The box is not
        # really visible, it is just used as a tool to arrange widgets.
        hbox2 = gtk.HBox(False, 0)

        # Create a new button for otf file selection
        button_otf = gtk.Button("OTF")
        button_otf.connect("clicked", self.select_otf, None)
        hbox2.pack_start(button_otf, False, False, 0)
        button_otf.show()

        # Create text fields to show file names
        self.text_otf = gtk.Entry(max=0)
        self.text_otf.set_text(self.otf)
        self.text_otf.set_editable(True)
        self.text_otf.connect("changed", self.change_text, "otf")
        hbox2.pack_start(self.text_otf, True, True, 0)
        self.text_otf.show()

        box1.pack_start(hbox2, False, False, 0)
        hbox2.show()

        # We create a horizontal box to pack widgets into. The box is not
        # really visible, it is just used as a tool to arrange widgets.
        hbox3 = gtk.HBox(False, 0)

        # Create a new button for output data file selection
        button_out = gtk.Button("Output")
        button_out.connect("clicked", self.select_out, None)
        hbox3.pack_start(button_out, False, False, 0)
        button_out.show()

        # Create text fields to show file names
        self.text_out = gtk.Entry(max=0)
        self.text_out.set_text(self.out)
        self.text_out.set_editable(True)
        self.text_out.connect("changed", self.change_text, "out")
        hbox3.pack_start(self.text_out, True, True, 0)
        self.text_out.show()

        box1.pack_start(hbox3, False, False, 0)
        hbox3.show()

        # Adding a horizontal seperator
        separator = gtk.HSeparator()
        box1.pack_start(separator, False, True, 5)
        separator.show()

        # We create a horizontal box to pack widgets into. The box is not
        # really visible, it is just used as a tool to arrange widgets.
        hbox4 = gtk.HBox(False, 0)

        # Create button
        button_simrecon = gtk.Button("Run SIM Reconstruction")
        button_simrecon.connect("clicked", self.start_simrecon, None)
        hbox4.pack_start(button_simrecon, True, True, 0)
        button_simrecon.show()

        box1.pack_start(hbox4, False, False, 0)
        hbox4.show()

        self.window.add(box1)
        box1.show()
        self.window.show()

    def change_text(self, widget, data):
        options = {"file": self.text_file,
                   "otf": self.text_otf,
                   "out": self.text_out}
        new_value = options[data].get_text()
        options = {"file": self.filename,
                   "otf": self.otf,
                   "out": self.out}
        options[data] = new_value

    def delete_event(self, widget, event, data=None):
        # return False
        raise SystemExit

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

    def start_simrecon(self, widget, data=None):
        from subprocess import call
        # print "file", self.filename
        # print "otf", self.otf
        # print "output", self.out
        call("~/sim-reconstruction/cudaSirecon/cudaSireconDriver " +
             " --input-file " + self.filename +
             " --otf-file " + self.otf +
             " --output-file " + self.out, shell=True)

    def select_file(self, widget, data=None):
        # Check for new pygtk: this is new class in PyGtk 2.4
        if gtk.pygtk_version < (2, 3, 90):
            print "PyGtk 2.3.90 or later required for this example"
            raise SystemExit

        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("DV files")
        filter.add_pattern("*.dv")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.filename = dialog.get_filename()
            self.text_file.set_text(self.filename)
        dialog.destroy()

    def select_otf(self, widget, data=None):
        # Check for new pygtk: this is new class in PyGtk 2.4
        if gtk.pygtk_version < (2, 3, 90):
            print "PyGtk 2.3.90 or later required for this example"
            raise SystemExit

        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("DV files")
        filter.add_pattern("*.dv")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.otf = dialog.get_filename()
            self.text_otf.set_text(self.otf)
        dialog.destroy()

    def select_out(self, widget, data=None):
        # Check for new pygtk: this is new class in PyGtk 2.4
        if gtk.pygtk_version < (2, 3, 90):
            print "PyGtk 2.3.90 or later required for this example"
            raise SystemExit

        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("DV files")
        filter.add_pattern("*.dv")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.out = dialog.get_filename()
            self.text_out.set_text(self.out)
        dialog.destroy()


# print __name__
if __name__ == "__main__":
    base = Base()
    base.main()
