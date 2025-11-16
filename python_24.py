import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

GRID_SIZE = 5

class Unit:
    def __init__(self, team):
        self.team = team
        self.hp = 100
        self.attack = 30
class Unittank:
    def __init__(self, team):
        self.team = team
        self.hp = 200
        self.attack = 50
        
class WarSim(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple WWII War Simulator")
        self.setMinimumSize(400, 400)

        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info = QLabel("Click a unit to select it.")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                btn = QPushButton("")
                btn.setFixedSize(60, 60)
                btn.clicked.connect(lambda checked=False, x=x, y=y: self.cell_clicked(x, y))
                self.grid_layout.addWidget(btn, y, x)
                self.buttons[y][x] = btn

        self.grid[0][0] = Unit("Allies")
        self.grid[0][1] = Unittank("Allies")
        self.grid[GRID_SIZE-1][GRID_SIZE-1] = Unit("Axis")

        self.update_board()

    def update_board(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                btn = self.buttons[y][x]
                unit = self.grid[y][x]
                if unit:
                    color = "lightblue" if unit.team == "Allies" else "lightcoral"
                    btn.setStyleSheet(f"background-color: {color}; font-weight: bold;")
                    btn.setText(f"{unit.team[0:100]}\n{unit.hp}")
                else:
                    btn.setStyleSheet("")
                    btn.setText("")

    def cell_clicked(self, x, y):
        if self.selected:
            sx, sy = self.selected
            selected_unit = self.grid[sy][sx]
            target = self.grid[y][x]

            if (x, y) == (sx, sy):
                self.info.setText("Unit deselected.")
                self.selected = None
                return

            if target and target.team != selected_unit.team:
                damage = selected_unit.attack 
                target.hp -= damage
                self.info.setText(f"{selected_unit.team} attacked for {damage} damage!")

                if target.hp <= 0:
                    self.grid[y][x] = None
                    self.info.setText(f"{selected_unit.team} destroyed the enemy!")

                self.selected = None

            elif not target and abs(x - sx) <= 1 and abs(y - sy) <= 1:
                self.grid[y][x] = selected_unit
                self.grid[sy][sx] = None
                self.selected = None
                self.info.setText(f"{selected_unit.team} moved.")
            else:
                self.info.setText("Invalid move.")

        else:
            if self.grid[y][x]:
                self.selected = (x, y)
                self.info.setText(f"Selected {self.grid[y][x].team} unit.")
            else:
                self.info.setText("No unit here.")

        self.update_board()


if __name__ == "__main__":
    print("Starting WarSim...")
    try:
        app = QApplication(sys.argv)
        window = WarSim()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Exception:", e)
        sys.exit(1)
