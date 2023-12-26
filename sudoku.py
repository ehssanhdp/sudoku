from tkinter import *
from tkinter import messagebox
import random
import numpy as np
from tkinter import filedialog

class Sudoku():

    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]  # 9x9 Sudoku board
        self.board = np.matrix(self.board)
        self.solutions = []


    def possible(self,y,x,n):

        for i in range(0,9):
            if self.board[y,i] == n :
                return False
        for i in range(0,9):
            if self.board[i,x] == n:
                return False
        x0 = (x//3)*3
        y0 = (y//3)*3
        for i in range(0,3):
            for j in range (0,3):
                if self.board[y0+i,x0+j] == n :
                    return False
        return True
    
    def solve_board(self):
        for y in range(9):
            for x in range(9):
                if self.board[y,x] == 0:
                    listNum = [1,2,3,4,5,6,7,8,9]
                    for _ in range(1,10):    
                        num = random.choice(listNum)
                        if self.possible(y,x,num):
                            self.board[y,x] = num
                            if self.solve_board():  # Check if a solution has been found
                                return True
                            self.solve_board()
                            self.board[y,x] = 0
                            listNum.remove(num)
                        else:
                            listNum.remove(num)
                    return
        return True
        
    def erase_cells(self, x):
        # Randomly select cells to erase
        numNotZero = 0
        for y in range(9):
            for i in range(9):
                if self.board[y,i] != 0:
                    numNotZero += 1
        if numNotZero > 31:
            for _ in range(x):
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                self.board[row, col] = 0

    import numpy as np

    # ...

    def check_solution(self):
        # Check each row
        if np.any(self.board == 0):
            return False
        
        for row in self.board:
            row_array = np.asarray(row).flatten()  # Convert row to a 1D array
            if len(set(row_array)) != 9:
                return False

        # Check each column
        for col in self.board.T:
            col_array = np.asarray(col).flatten()  # Convert column to a 1D array
            if len(set(col_array)) != 9:
                return False

        # Check each 3x3 square
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square = self.board[i:i+3, j:j+3]
                square_array = np.asarray(square).flatten()  # Convert square to a 1D array
                if len(set(square_array)) != 9:
                    return False
        return True

    # ...

    def load_sudoku(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
        # Load an unsolved Sudoku board and solve it
        sudoku = []
        for i in range(9):
            row_input = content.splitlines()
            row = [int(num) for num in row_input[i].split(",")]
            sudoku.append(row)
            if i == 8:
                self.board = np.matrix(sudoku)

    
class SudokuGUI(Sudoku):

    def __init__(self):
        global frame1
        super().__init__()
        # Create buttons and difficulty options
        # Implement the logic to create buttons and difficulty options using tkinter
        # Bind functions to buttons        

        self.root = Tk()
        self.sudoku = Sudoku()
        self.root.title("SUDOKU") 
        self.root.geometry("500x550")
        
        frame1 = Frame(self.root)
        frame1.pack(side=TOP)
        self.board_entries = []

        for row in range(9):
            entry_row = []
            for col in range(9):
                entry = Entry(frame1,  width=3, justify='center', font=('Arial', 20))
                entry.grid(row=row, column=col, padx=3, pady=3)
                entry.bind("<KeyRelease>", self.update_board_by_user)
                entry_row.append(entry)
                self.board_entries.append(entry_row)

        create_button = Button(self.root, text='create', font=('Arial'),width=25, height=1, command=lambda: self.generate_board())
        create_button.pack(side=BOTTOM)

        check_button = Button(self.root, text='check', font=('Arial'),width=25, height=1,command=lambda:self.check())
        check_button.pack(side=BOTTOM)

        load_button = Button(self.root, text='load', font=('Arial'),width=25, height=1,command=lambda:self.load())
        load_button.pack(side=BOTTOM)

        solve_button = Button(self.root, text='solve', font=('Arial'),width=25, height=1,command=lambda:self.solve())
        solve_button.pack(side=BOTTOM)

        frame = Frame(self.root)
        frame.pack(side=BOTTOM)
        r = IntVar()
        easyRadioButton = Radiobutton(frame,text="easy",variable=r, value=30,command=lambda: self.change_diffculty(30)).pack(side=LEFT)
        mediumRadioButton = Radiobutton(frame,text="medium",variable=r, value=40,command=lambda: self.change_diffculty(40)).pack(side=LEFT)
        difficultRadioButton = Radiobutton(frame,text="difficult",variable=r, value=50,command=lambda: self.change_diffculty(50)).pack(side=LEFT)
        self.root.mainloop()

    def update_board_by_user(self, event):
        # Get the entered value and its position in the entry widget
        value = event.widget.get()
        row = int(event.widget.grid_info()["row"])
        col = int(event.widget.grid_info()["column"])
        # Update the corresponding position in self.board
        self.board[row, col] = int(value)
    def update_board_by_computer(self):
        for row in range(9):
            entry_row = []
            for col in range(9):
                entry = Entry(frame1, width=3, justify='center', font=('Arial', 20))
                if (row // 3 == 1 and col // 3 == 1) or (row // 3 == 0 and col // 3 == 0) or (row // 3 == 2 and col // 3 == 0) or (row // 3 == 0 and col // 3 == 2) or (row // 3 == 2 and col // 3 == 2):
                    entry.config(bg='light gray')
                else:
                    entry.config(bg='white')
                entry.grid(row=row, column=col, padx=3, pady=3)
                entry.bind("<KeyRelease>", self.update_board_by_user)
                entry_row.append(entry)
                entry.insert(0,self.board[row,col])
                
    def generate_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.board = np.matrix(self.board)
        self.solve_board()
        self.update_board_by_computer()

    def check(self):
        if self.check_solution():
            messagebox.showinfo("Message", "sudoku solved correctly")
        else:
            messagebox.showinfo("Message", "sudoku isn't solved correctly")

    def solve(self):
        if self.solve_board():
            self.update_board_by_computer()
        else:
            messagebox.showinfo("Message", "sudoku is either unsolvableor incorrect")
            
    def load(self):
        self.load_sudoku()
        self.update_board_by_computer()

    def change_diffculty(self,x):
        self.erase_cells(x)
        self.update_board_by_computer()


x = SudokuGUI()

