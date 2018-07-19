from panda3d.core import *
loadPrcFileData("", "direct-gui-edit #t")
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *



class Editor(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.widgets = {}
        
        self.windowPreview = WindowPreview()
        self.propertiesPanel = PropertiesPanel()
        self.toolbar = Toolbar(self)

        base.setBackgroundColor((1, 1, 1, 1))

        self.accept("p", print, [self.propertiesPanel.scaleLabel.getPos(), self.propertiesPanel.scale.getPos()])


        


class PropertiesPanel(object):
    def __init__(self):
        self.frame = DirectFrame(
            frameSize = (0.6, base.a2dRight,
                         base.a2dBottom + 0.1, base.a2dTop),
            frameColor = (0.2, 0.7, 0.2, 0.6),
            enableEdit = False,
            )

        self.selected = None

        self.scale = self.createSlider(arg = "scale", command = self.adjust)
        self.scaleLabel = self.createLabel(text = "Object Scale")
        self.scale.setScale(0.16)
        self.scale.setPos(1.1, 0, 0.9)
        self.scaleLabel.setPos(0.76, 0, 0.9)

        self.text = DirectEntry(
                                command = self.setText,
                                enableEdit = False,
                                parent = self.frame,
                                #text_scale = 0.0001,
                                
                                )
        self.text.setScale(0.03)
        self.text.setPos(0.9, 0, 0.82)
        self.textLabel = self.createLabel(text = "Text")
        self.textLabel.setPos(0.7, 0, 0.82)

    def createSlider(self, command = lambda: print("No attached function"), arg = "random arg", text = "Function of Slider"):
        return DirectSlider(
            range = (0.001, 1),
            value = 0.1,
            command = command,
            extraArgs = [arg],
            enableEdit = 0,
            parent = self.frame,
            text_scale = 0.15,
            )

    def createLabel(self, text = "Label"):
        return DirectLabel(text = text, parent = self.frame, scale = 0.04, frameColor = (1, 1, 1, 0), enableEdit = 0)
            

    def adjust(self, key):
        if key == "scale" and self.selected:
            self.selected.setScale(self.scale["value"])

    def setText(self, entered):
        self.selected["text"] = entered
        self.selected.setText()

class Toolbar(object):
    def __init__(self, app):
        self.app = app
        self.frame = DirectFrame(
            frameSize = (base.a2dLeft, -0.8,
                         base.a2dBottom + 0.1, base.a2dTop),
            frameColor = (0.2, 0.7, 0.2, 0.6),
            enableEdit = False,
            )

        self.saveLayout = DirectButton(text = "Save Current Layout",
                                  command = self.saveLayout,
                                  enableEdit = False,
                                  parent = self.frame,
                                  scale = 0.04,
                                )
        self.saveLayout.setPos(base.a2dLeft + 0.23, 0, 0.9)


        self.addButton = DirectButton(text = "Add Button",
                                  command = self.add,
                                  extraArgs = ["button"],
                                  enableEdit = False,
                                  parent = self.frame,
                                  scale = 0.06,
                                )
        self.addButton.setPos(base.a2dLeft + 0.23, 0, 0.8)

        self.addText = DirectButton(text = "Add Label",
                                  command = self.add,
                                  extraArgs = ["label"],
                                  enableEdit = False,
                                  parent = self.frame,
                                  scale = 0.06,
                                )
        self.addText.setPos(base.a2dLeft + 0.23, 0, 0.7)

    def add(self, widget):
        name = "Unnamed"
        while name in self.app.widgets:
            name += "1"
        if widget == "button":
            w = DirectButton(text = "Button", scale = 0.1, command = self.setSelected)
            self.app.widgets[name] = w
            w["extraArgs"] = [self.app.widgets[name]]
        elif widget == "label":
            w = DirectLabel(text = "Label", scale = 0.1, frameColor = (1, 1, 1, 0))
            self.app.widgets[name] = w
        
        w.reparentTo(self.app.windowPreview.frame)
        self.app.propertiesPanel.selected = w
        
        print(self.app.widgets)

    def setSelected(self, widget):
        self.app.propertiesPanel.selected = widget

    def saveLayout(self):
        file = open("saved_layout.dgui", "w")

        for name in self.app.widgets:
            file.write(name + ":" + "scale;" + str(self.app.widgets[name].getScale()[0] ) + "-text;" + self.app.widgets[name]["text"] + "\n")
        file.close()

        

class WindowPreview(object):
    def __init__(self):
         self.frame = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (1, 1, 1, 1),
            enableEdit = False,
            )


editor = Editor()
editor.run()
