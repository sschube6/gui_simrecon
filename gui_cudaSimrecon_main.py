"""
gui_cudaSimrecon_main()

This is a interface for the Betzig cuda SIM reconstruction code. The main
purpose of the gui is to collect the parameters for the reconstruction
e. g. input, otf, output) and calling the cudaSireconDriver in the shell.
The implementation uses pygtk.

Author: Sebastian Schubert, mail: sschube6@gmail.com
"""

import pygtk
import gtk
from subprocess import call
pygtk.require('2.0')


class Gui_cudaSimrecon:
    def __init__(self):
        ###############
        # Set global variables
        self.callto = "~/sim-reconstruction/cudaSirecon/cudaSireconDriver"

        # A dictionary serves for keeping track of how the buttons and text
        # entry fields are named and which parameters for input, otf, output,
        # etc. were selected.
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
        ###############

        # Construct a gtk window in which the gui lives.
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

        # The main layout of the window will consists of boxes that we are
        # filling with buttons, textfields, etc.
        # We create one vertical box (vbox) to pack some horizontal boxes into.
        # This allows us to stack the horizontal boxes filled with buttons one
        # on top of the other in this vbox.
        box = gtk.VBox(False, 0)

        # For every key in the dictionary, we create a horizontal box to pack
        # widgets into. The box is not really visible, it is just used as a
        # tool to arrange widgets.
        # Per box we create a button and a text entry .
        # When the button is pressed we call select_file() and when the text is
        # changed we call update_text().
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
        box.pack_start(separator, False, True, 5)

        # Create a SIM button with callback to start_simrecon()
        hbox = gtk.HBox(False, 0)
        hbox.show()
        button_simrecon = gtk.Button("Run SIM Reconstruction")
        button_simrecon.connect("clicked", self.start_simrecon, None)
        hbox.pack_start(button_simrecon, True, True, 0)
        button_simrecon.show()
        box.pack_start(hbox, False, False, 0)

        box.show()
        self.window.add(box)
        self.window.show()

    def update_text(self, widget, strType):
        # Make sure that the filename stored in the dictionary is updated
        # when it is changed in the textbox.
        fname = self.naming_dict[strType]["objTextfield"].get_text()
        self.naming_dict[strType]["strFname"] = fname

    def start_simrecon(self, widget, data):
        # Here we will call the cudaSireconDriver in shell

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
        call(self.callto +
             " --input-file " + inFname +
             " --otf-file " + otfFname +
             " --output-file " + outFname,
             shell=True)

    def select_file(self, widget, strType):
        # Check for new pygtk: this is new class in PyGtk 2.4
        if gtk.pygtk_version < (2, 3, 90):
            print "PyGtk 2.3.90 or later required for this example"
            raise SystemExit

        # Open a dialog to choose the files
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        # Setting the filters
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("DV files")
        filter.add_pattern("*.dv")
        dialog.add_filter(filter)

        # If a valid file is selected we want to change the fname setting and
        # update the texbox.
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            fname = dialog.get_filename()
            self.naming_dict[strType]["strFname"] = fname
            self.naming_dict[strType]["objTextfield"].set_text(fname)
        dialog.destroy()

    def delete_event(self, widget, event, data=None):
        # We want to close the program and the python execution.
        # Normally a "return False" would be sufficient.
        raise SystemExit

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

if __name__ == "__main__":
    base = Gui_cudaSimrecon()
    base.main()
