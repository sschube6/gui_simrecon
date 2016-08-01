import pygtk
import gtk
from subprocess import call
pygtk.require('2.0')


class Base:
    def __init__(self):
        # set global variables
        self.naming_dict = {"1_file": {"strName": "in",
                                       "strLabel": "Input",
                                       "strFname": "test",
                                       "objTextfield": None},
                            "2_otf": {"strName": "otf",
                                      "strLabel": "OTF",
                                      "strFname": "",
                                      "objTextfield": None},
                            "3_out": {"strName": "out",
                                      "strLabel": "Output",
                                      "strFname": "out",
                                      "objTextfield": None}}

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
        box = gtk.VBox(False, 0)

        hbox1 = gtk.HBox(False, 0)
        hbox2 = gtk.HBox(False, 0)
        hbox3 = gtk.HBox(False, 0)
        hbox4 = gtk.HBox(False, 0)
        hbox1.show()
        hbox2.show()
        hbox3.show()
        hbox4.show()

        # We create a horizontal box to pack widgets into. The box is not
        # really visible, it is just used as a tool to arrange widgets.

        # Create a new button for raw data file selection

        for x in self.naming_dict:
            hbox = gtk.HBox(False, 0)

            button = gtk.Button(self.naming_dict[x]["strLabel"])
            button.connect("clicked", self.select_file, x)
            hbox.pack_start(button, False, False, 0)
            button.show()

            textbox = gtk.Entry(max=0)
            textbox.set_text(self.naming_dict[x]["strFname"])
            textbox.set_editable(True)
            textbox.connect("changed", self.update_text, x)
            hbox.pack_start(textbox, True, True, 0)
            textbox.show()

            self.naming_dict[x]["objTextfield"] = textbox
            hbox.show()
            box.pack_start(hbox, False, False, 0)

        # Adding a horizontal seperator
        separator = gtk.HSeparator()
        separator.show()

        # Create sim button
        button_simrecon = gtk.Button("Run SIM Reconstruction")
        button_simrecon.connect("clicked", self.start_simrecon, None)
        hbox4.pack_start(button_simrecon, True, True, 0)
        button_simrecon.show()

        box.pack_start(hbox1, False, False, 0)
        box.pack_start(hbox2, False, False, 0)
        box.pack_start(hbox3, False, False, 0)
        box.pack_start(separator, False, True, 5)
        box.pack_start(hbox4, False, False, 0)

        box.show()
        self.window.add(box)
        self.window.show()

    def update_text(self, widget, strType):
        fname = self.naming_dict[strType]["objTextfield"].get_text()
        self.naming_dict[strType]["strFname"] = fname

    def start_simrecon(self, widget, data):
        for x in self.naming_dict:
            if self.naming_dict[x]["strName"] == "in":
                inFname = self.naming_dict[x]["strFname"]
            elif self.naming_dict[x]["strName"] == "otf":
                otfFname = self.naming_dict[x]["strFname"]
            elif self.naming_dict[x]["strName"] == "out":
                outFname = self.naming_dict[x]["strFname"]
        # print "file", inFname
        # print "otf", otfFname
        # print "output", outFname
        call("~/sim-reconstruction/cudaSirecon/cudaSireconDriver " +
             " --input-file " + inFname +
             " --otf-file " + otfFname +
             " --output-file " + outFname,
             shell=True)

    def select_file(self, widget, strType):
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
            fname = dialog.get_filename()
            self.naming_dict[strType]["strFname"] = fname
            self.naming_dict[strType]["objTextfield"].set_text(fname)
        dialog.destroy()

    def delete_event(self, widget, event, data=None):
        # return False
        raise SystemExit

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
