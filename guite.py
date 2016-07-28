import pygtk
import gtk
pygtk.require('2.0')

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2, 3, 90):
    print "PyGtk 2.3.90 or later required for this example"
    raise SystemExit


class Base:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("cudaSIM")

        # # When the window is given the "delete_event" signal (this is given
        # # by the window manager, usually by the "close" option, or on the
        # # titlebar), we ask it to call the delete_event () function
        # # as defined above. The data passed to the callback
        # # function is NULL and is ignored in the callback function.
        # self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        # We create a box to pack widgets into.  This is described in detail
        # in the "packing" section. The box is not really visible, it
        # is just used as a tool to arrange widgets.
        self.box1 = gtk.HBox(False, 0)

        # Put the box into the main window.
        self.window.add(self.box1)

        # Creates a new button with the label "Hello World".
        self.button_simrecon = gtk.Button("Run SIM Reconstruction")
        self.button_simrecon.connect("clicked", self.start_simrecon, None)
        # We pack this button into the invisible box, which has been
        # packed into the window.
        self.box1.pack_start(self.button_simrecon, True, True, 0)

        # self.window.add(self.button_simrecon)
        self.button_simrecon.show()

        # Creates a new button with the label "Hello World".
        self.button_file = gtk.Button("File")
        self.button_file.connect("clicked", self.select_file, None)
        self.box1.pack_start(self.button_file, True, True, 0)
        self.button_file.show()

        
        self.box1.show()
        self.window.show()

    def delete_event(self, widget, event, data=None):
        return False

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

    def start_simrecon(self, widget, data=None):
        print "Hi"

    def select_file(self, widget, data=None):
        print "Ho"

# print __name__
if __name__ == "__main__":
    base = Base()
    base.main()
