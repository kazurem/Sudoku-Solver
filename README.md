# Sudoku-Solver
A Python-based Sudoku solver that uses the **Backtracking Algorithm** to solve any valid Sudoku puzzle.  
It also supports **colorful terminal visualization** of the solving process.


## **Screenshots:**
### **Sudoku Solver(Backtracking) with Visualization in Command Line:**
![Command Line Sudoku Solver](images/cl-sudoku-solver.png)
  
## **How to run?**    
  
### **1. Clone the repository:**
  
```bash
git clone https://github.com/kazurem/Sudoku-Solver
cd ./Sudoku-Solver
```
  
### **2. Create a virtual environment:**
  
You do not really need to do this but I will add this step regardless.
```bash
python -m venv ./path-to-venv
```
  
### **3. Activate the virtual environment:**
  
#### **In Windows:**
```bash
.\path-to-venv\Scripts\activate
```
  
#### **In Linux/Mac:**
  
```bash
source .\path-to-venv\bin\activate
```
If the above command failed for you, you can probably use these to solve your problem:  
1. [Stack Overflow: Activating Python Virtual Environments]("https://stackoverflow.com/questions/14604699/how-can-i-activate-a-virtualenv-in-linux")
2. [Python Documentation: Virtual Environments](https://docs.python.org/3/library/venv.html)
  
### **4. Using requirements.txt:** 
  
In this step, we use requirements.txt file to install all the necessary packages.
```bash
pip install -r requirements.txt
```
  
### **5. Run:**
  
```bash
python main.py
```
