import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

GRID_SIZE = 5

class Unit:
    def __init__(self, team, attack=30, hp=100, max_range=3, fire_rate=1):
        self.team = team
        self.hp = hp
        self.attack = attack
        self.max_range = max_range
        self.fire_rate = fire_rate

class Tank(Unit):
    def __init__(self, team):
        super().__init__(team, attack=50, hp=200, max_range=2, fire_rate=1)

class Artillery(Unit):
    def __init__(self,team):
        super().__init__(team, attack=70, hp=80, max_range=4, fire_rate=2)


class WarSim(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WWII War Simulator")
        self.setMinimumSize(400, 400)

        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected = None
        self.turn_team = "Allies"      

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info = QLabel(f"{self.turn_team}'s turn. Select a unit.")
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
        self.grid[0][1] = Tank("Allies")
        self.grid[0][2] = Artillery("Allies")
        self.grid[GRID_SIZE - 1][GRID_SIZE - 1] = Unit("Axis")
        self.grid[GRID_SIZE - 1][GRID_SIZE - 1] = Tank("Axis")
        self.grid[GRID_SIZE - 1][GRID_SIZE - 1] = Artillery("Axis")

        self.update_board()

   
    def update_board(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                btn = self.buttons[y][x]
                unit = self.grid[y][x]
                if unit:
                    color = "lightblue" if unit.team == "Allies" else "black"
                    btn.setStyleSheet(f"background-color: {color}; font-weight: bold;")
                    btn.setText(f"{unit.team}\nHP:{unit.hp}")
                else:
                    btn.setStyleSheet("")
                    btn.setText("")

    def end_turn(self):
        self.turn_team = "Axis" if self.turn_team == "Allies" else "Allies"
        self.info.setText(f"{self.turn_team}'s turn. Select a unit.")

    
    def calculate_damage(self, attacker, sx, sy, tx, ty):
        distance = abs(tx - sx) + abs(ty - sy)

        if distance > attacker.max_range:
            return 0 

        multiplier = max(0.2, 1 - 0.25 * (distance - 1))
        return int(attacker.attack * multiplier)

    def cell_clicked(self, x, y):
        if not self.selected:
            if self.grid[y][x] and self.grid[y][x].team == self.turn_team:
                self.selected = (x, y)
                self.info.setText(f"Selected {self.grid[y][x].team} unit.")
            else:
                self.info.setText("Not your unit or empty.")
            return

        sx, sy = self.selected
        attacker = self.grid[sy][sx]
        target = self.grid[y][x]

        if (x, y) == (sx, sy):
            self.selected = None
            self.info.setText(f"{self.turn_team}'s turn.")
            return

        if target and target.team != attacker.team:
            damage = self.calculate_damage(attacker, sx, sy, x, y)

            if damage <= 0:
                self.info.setText("Target is out of range!")
                return

            target.hp -= damage
            self.info.setText(f"{attacker.team} dealt {damage} damage!")

            if target.hp <= 0:
                self.grid[y][x] = None
                self.info.setText("Enemy destroyed!")

            self.selected = None
            self.update_board()
            self.end_turn()
            return

        if not target and abs(x - sx) <= 1 and abs(y - sy) <= 1:
            self.grid[y][x] = attacker
            self.grid[sy][sx] = None
            self.selected = None
            self.info.setText("Unit moved.")

            self.update_board()
            self.end_turn()
            return

        self.info.setText("Invalid move or target.")
        self.selected = None
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

