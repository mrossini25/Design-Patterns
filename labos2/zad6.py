import re
from collections import defaultdict

class Cell:
    def __init__(self, sheet, row, col):
        self.exp = ""
        self.value = None
        self.sheet = sheet
        self.row = row
        self.col = col
        self.observers = set()
    
    def set_exp(self, exp):
        self.exp = exp
        self.sheet.update_dependencies(self)
        self.evaluate()
    
    def evaluate(self): 
        if not self.exp:
            self.value = None
            return
        
        try:
            if '+' in self.exp:
                parts = [part.strip() for part in self.exp.split('+')]
                operand1 = self.nabaviBroj(parts[0])
                operand2 = self.nabaviBroj(parts[1])
                self.value = operand1 + operand2
            else:
                self.value = self.nabaviBroj(self.exp)
        except Exception:
            self.value = None

        for observer in list(self.observers):
            observer.evaluate()
    
    def nabaviBroj(self, operand):
        if re.fullmatch(r'[A-Za-z]\d+', operand):
            ref_cell = self.sheet.cell(operand)
            if ref_cell and ref_cell.value is not None:
                return ref_cell.value
        return float(operand)
    
    def add_observer(self, cell):
        self.observers.add(cell)
    
    def remove_observer(self, cell):
        self.observers.discard(cell)

class Sheet:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(self, r, c) for c in range(cols)] for r in range(rows)]
        self.prikazOvisnosti = defaultdict(set)
    
    def cell(self, ref):
        match = re.fullmatch(r'([A-Za-z])(\d+)', ref)
        if not match:
            return None
        
        col = ord(match.group(1).upper()) - ord('A')
        row = int(match.group(2)) - 1

        return self.cells[row][col]

    
    def set(self, ref, val):
        cell = self.cell(ref)
        if cell:
            cell.set_exp(val)
    
    def getrefs(self, cell):
        if not cell.exp:
            return []
        
        if '+' not in cell.exp:
            exp = cell.exp
            if re.fullmatch(r'[A-Za-z]\d+', exp):
                return [exp.upper()]
            else:
                return []
        
        refs = []
        for part in cell.exp.split('+'):
            part = part.strip()
            if re.fullmatch(r'[A-Za-z]\d+', part):
                refs.append(part.upper())
        return refs
    
    def update_dependencies(self, cell):        
        cell_ref = f"{chr(cell.col + ord('A'))}{cell.row + 1}"
        
        if cell_ref in self.prikazOvisnosti:
            for ref in self.prikazOvisnosti[cell_ref]:
                ref_cell = self.cell(ref)
                if ref_cell:
                    ref_cell.remove_observer(cell)
            del self.prikazOvisnosti[cell_ref]
        
        refs = self.getrefs(cell)
        for ref in refs:
            ref_cell = self.cell(ref)
            if ref_cell:
                ref_cell.add_observer(cell)
                self.prikazOvisnosti[cell_ref].add(ref)
                self.provjeriOvisnost(cell_ref)

    
    def provjeriOvisnost(self, start):
        prodeni = set()
        cells = [cell for cell in s.prikazOvisnosti.get(start, [])]
        #print(cells)
        while cells:
            cell = cells[0]
            prodeni.add(cell)
            #print("prodeni: ", prodeni)
            #print("cells:", cells)
            cells.remove(cell)
            #print("cell: ", cell)
            for c in s.prikazOvisnosti.get(cell, []):
                #print("c:", c)
                if c == start:
                    raise RuntimeError(f"Circular dependency detected involving {start}")
                elif c not in prodeni:
                    cells.append(c)


    def evaluate(self, cell):
        cell.evaluate()
    
    def print(self):
        for r in range(self.rows):
            row_display = []
            for c in range(self.cols):
                cell = self.cells[r][c]
                display = f"{cell.value}" if cell.value is not None else "None"
                row_display.append(f"{chr(c + ord('A'))}{r + 1}:{display}")
            print(" | ".join(row_display))

if __name__ == "__main__":
    s=Sheet(5,5)
    print()

    s.set('A1','2')
    s.set('A2','5')
    s.set('A3','A1+A2')
    s.print()
    print()

    s.set('A1','4')
    s.set('A4','A1+A3')
    s.print()
    print()

    try:
        s.set('A1','A3')
    except RuntimeError as e:
        print("Caught exception:",e)
    s.print()
    print()
    
