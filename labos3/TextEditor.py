import tkinter as tk
from TextEditorModel import LocationRange, TextEditorModel, Location, CursorObserver, TextObserver

class TextEditor(tk.Canvas, CursorObserver, TextObserver):
    def __init__(self, master, model: TextEditorModel):
        super().__init__(master, bg="white", width=600, height=400)
        self.model = model
        self.model.add_cursor_observer(self)
        self.model.add_text_observer(self)

        self.font = ("Courier New", 12)
        self.line_height = 20
        self.char_width = 10

        self.focus_set()
        self.bind("<Key>", self.onKeyPressed)
        self.bind("<KeyRelease>", self.onKeyReleased)

        self.redraw()

    def redraw(self):
        self.delete("all")
        for i, line in enumerate(self.model.get_lines()):
            self.create_text(5, i * self.line_height + 5, anchor='nw', text=line, font=self.font, fill="black")
            
        if self.model.selectionRange:
            self.drawSelected(self.model.selectionRange)

        kursor = self.model.cursorLocation
        x = kursor.column * self.char_width + 5
        y = kursor.line * self.line_height + 5
        self.create_line(x, y, x, y + self.line_height, fill="black", width=1)
        
    def drawSelected(self, locRange: LocationRange):
        normRange = locRange.normalized()
        start, end = normRange.start, normRange.end
        for line in range(start.line, end.line + 1):
            text = self.model.lines[line]
            if line == start.line:
                line_start_col = start.column
            else:
                line_start_col = 0
            if line == end.line:
                line_end_col = end.column
            else: 
                line_end_col = len(text)

            selected_text = text[line_start_col:line_end_col]
            x = line_start_col * self.char_width + 5
            y = line * self.line_height + 5
            self.create_text(x, y, anchor='nw', text=selected_text, font=self.font, fill="red")
    
    def updateCursorLocation(self, loc: Location):
        self.redraw()
        
    def updateText(self):
        self.redraw()

    def onKeyPressed(self, event):
        if event.keysym in ["Shift_L", "Shift_R"]:
            self.model.shiftPressed = True
        elif event.keysym == "Return":
            self.model.insert_newline()
        elif event.keysym == "BackSpace":
            if self.model.selectionRange:
                self.model.deleteRange(self.model.selectionRange)
            else:
                self.model.deleteBefore()
        elif event.keysym == "Delete":
            if self.model.selectionRange:
                self.model.deleteRange(self.model.selectionRange)
            else:
                self.model.deleteAfter()
        elif event.keysym == "Left":
            self.model.moveCursorLeft()
        elif event.keysym == "Right":
            self.model.moveCursorRight()
        elif event.keysym == "Up":
            self.model.moveCursorUp()
        elif event.keysym == "Down":
            self.model.moveCursorDown()
        elif event.char.isprintable():
            self.model.insert(event.char)

    
    def onKeyReleased(self, event):
        if event.keysym in ["Shift_L", "Shift_R"]:
            self.model.shiftPressed = False
            if not self.model.shiftPressed:
                self.model.selectionRange = None
                self.model.notify_cursor_observers()
                
        
if __name__ == "__main__":
    root = tk.Tk()
    model = TextEditorModel("Moj Notepad\nBašćanska ploča.")
    editor = TextEditor(root, model)
    editor.pack(fill="both", expand=True)
    root.mainloop()

