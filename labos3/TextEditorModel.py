from dataclasses import dataclass
from typing import List, Optional, Set

@dataclass
class Location:
    line: int
    column: int

@dataclass
class LocationRange:
    start: Location
    end: Location
    
    def normalized(self):
        if (self.start.line > self.end.line) or (self.start.line == self.end.line and self.start.column > self.end.column):
            return LocationRange(self.end, self.start)
        return self
    
class CursorObserver:
    def updateCursorLocation(self, loc: Location):
        pass
    
class TextObserver:
    def updateText(self):
        pass

class TextEditorModel:
    def __init__(self, initial_text: str = ""):
        self.lines: List[str] = initial_text.splitlines() or [""]
        self.cursorLocation: Location = Location(0, 0)
        self.selectionRange: Optional[LocationRange] = None
        self.shiftPressed: bool = False
        self.cursor_observers: List[CursorObserver] = []
        self.text_observers: List[TextObserver] = []
            
            
    def add_cursor_observer(self, observer: CursorObserver):
        self.cursor_observers.append(observer)

    def remove_cursor_observer(self, observer: CursorObserver):
        self.cursor_observers.remove(observer)

    def notify_cursor_observers(self):
        for observer in self.cursor_observers:
            observer.updateCursorLocation(self.cursorLocation)
            
            
    def add_text_observer(self, observer: TextObserver):
        self.text_observers.append(observer)

    def remove_text_observer(self, observer: TextObserver):
        self.text_observers.remove(observer)

    def notify_text_observers(self):
        for observer in self.text_observers:
            observer.updateText()
            
            
    def moveCursorLeft(self):
        self.moveCursor(0, -1)

    def moveCursorRight(self):
        self.moveCursor(0, 1)

    def moveCursorUp(self):
        self.moveCursor(-1, 0)

    def moveCursorDown(self):
        self.moveCursor(1, 0)

    def moveCursor(self, dline: int, dcol: int):
        line = self.cursorLocation.line + dline
        col = self.cursorLocation.column + dcol

        line = max(0, min(line, len(self.lines) - 1))
        col = max(0, min(col, len(self.lines[line])))
        
        newLoc = Location(line, col)

        if newLoc != self.cursorLocation:
            oldLoc = self.cursorLocation
            self.cursorLocation = newLoc
            if self.shiftPressed:
                if not self.selectionRange:
                    self.setSelectionRange(LocationRange(oldLoc, newLoc))
                else:
                    self.selectionRange.end = newLoc 
            else:
                self.setSelectionRange(None)
                
            self.notify_cursor_observers()
            
            
    def setSelectionRange(self, locRange: LocationRange):
        self.selectionRange = locRange
        
    
    def deleteBefore(self):
        line = self.cursorLocation.line
        col = self.cursorLocation.column
        if col > 0:
            current_line = self.lines[line]
            self.lines[line] = current_line[:col-1] + current_line[col:]
            self.moveCursor(0, -1)
            
        elif line > 0:
            prev_line = self.lines[line - 1]
            self.lines[line - 1] = prev_line + self.lines[line]
            del self.lines[line]
            self.cursorLocation = Location(line - 1, len(prev_line))
            
        self.notify_cursor_observers()
        self.notify_text_observers()
            
            
    def deleteAfter(self):
        line = self.cursorLocation.line
        col = self.cursorLocation.column
        if col < len(self.lines[line]):
            current_line = self.lines[line]
            self.lines[line] = current_line[:col] + current_line[col+1:]

        elif line < len(self.lines) - 1:
            next_line = self.lines[line + 1]
            self.lines[line] = self.lines[line] + next_line
            del self.lines[line + 1]

        self.notify_cursor_observers()
        self.notify_text_observers()
        

    def deleteRange(self, locRange: LocationRange):
        normRange = locRange.normalized()
        start, end = normRange.start, normRange.end

        if start.line == end.line:
            line = self.lines[start.line]
            self.lines[start.line] = line[:start.column] + line[end.column:]
        else:
            first_line = self.lines[start.line][:start.column]
            last_line = self.lines[end.line][end.column:]
            self.lines[start.line] = first_line + last_line
            del self.lines[start.line + 1:end.line + 1]

        self.cursorLocation = start
        self.setSelectionRange(None)
        self.notify_cursor_observers()
        self.notify_text_observers()

                
    
    def insert(self, char: str):
        line = self.cursorLocation.line
        col = self.cursorLocation.column
        current_line = self.lines[line]
        self.lines[line] = current_line[:col] + char + current_line[col:]
        self.moveCursor(0, 1)
        self.notify_text_observers()
    
        
    def insert_newline(self):
        line = self.cursorLocation.line
        col = self.cursorLocation.column
        current_line = self.lines[line]

        left_part = current_line[:col]
        right_part = current_line[col:]

        self.lines[line] = left_part
        self.lines.insert(line + 1, right_part)

        self.cursorLocation = Location(line + 1, 0)
        self.notify_text_observers()
        

    def get_lines(self):
        return self.lines
