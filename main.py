import random
import time

with open("program.txt", "r") as f:
    instrukcje = [linia.strip() for linia in f if linia.strip() != ""]
print(instrukcje)   

command = ""
running = False
MASK = 0xFF
randomNumber = 0

hz = 1
time_for_step = 1 / hz


# Instrukcje
mpointer = 0
line = 0
instruction = "NOP"
arg_1 = 0
arg_2 = 0
arg_3 = 0

#Rejestry
inputIO = [0,0,0,0,0,0,0,0]
outputIO = [0,0,0,0,0,0,0,0]

a_reg = [0,0,0,0,0,0,0,0]
b_reg = [0,0,0,0,0,0,0,0] 

a = 0
b = 0
cout = 0

# RAM
ram = [0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,
       0,0,0,0,0,0,0,0,]
pointer = 0

#Flagi
flagTrue = True
isTrue = True #0
is0 = False #1
not0 = False #2
isCarry = False #3
notParity = False #4
isParity = False #5
notCarry = False #6
AthanB = False #7

def IfChoice(): #wyborflagi do skoku
    global flagTrue
    
    if arg_2 == 0:
        flagTrue = isTrue
    if arg_2 == 1:
        flagTrue = is0
    if arg_2 == 2:
        flagTrue = not0
    if arg_2 == 3:
        flagTrue = isCarry
    if arg_2 == 4:
        flagTrue = notParity
    if arg_2 == 5:
        flagTrue = isParity
    if arg_2 == 6:
        flagTrue = notCarry
    if arg_2 == 7:
        flagTrue = AthanB  
def LoadInst():
    global instruction, arg_1, arg_2, arg_3, mpointer, line

    line = instrukcje[mpointer]
    czesci = line.split()
    
    instruction = czesci[0]
    arg_1 = int(czesci[1]) if len(czesci) > 1 else 0
    arg_2 = int(czesci[2]) if len(czesci) > 2 else 0
    arg_3 = int(czesci[3]) if len(czesci) > 3 else 0
def ArgNum(): # przerzuca liczbe z listy ( rejestru ) do tymczasowych zmiennych na podstawie arg1 i 2
    global a 
    global b 
    a = a_reg[arg_1]
    b = b_reg[arg_2]
def ArgSave(): # przerzuca liczbe wyniku do rejestrow na podstawie arg 3
    global cout
    global a_reg
    global b_reg
    a_reg[arg_3] = cout
    b_reg[arg_3] = cout
def ChkFlag():
    global cout, is0, not0, isCarry, notParity, isParity, notCarry, AthanB

    is0 = not0 = isCarry = notParity = isParity = notCarry = AthanB = False

    if cout > 255 or cout < 0:     
        isCarry = True
    else:
        notCarry = True

    cout = cout & MASK               

    if cout == 0:
        is0 = True
    else:
        not0 = True

    if cout % 2 == 0:
        isParity = True
    else:
        notParity = True

    if a > b:
        AthanB = True
def Jump(): #skok
    global arg_1
    global arg_2
    global mpointer
    global flagTrue

    IfChoice()
    if flagTrue == True:
        mpointer = arg_1
    else:
        print("Warunek nie spełniony!")
def IntLoad():



    global a_reg , b_reg
    a_reg[arg_2] = arg_1
    b_reg[arg_2] = arg_1
def IoLoad():
    global outputIO
def Menu():
    global running
    global comand
    global hz
    global time_for_step
    print("=============================================================")
    print("|--------------------OZCORE V | EMULATOR--------------------|")
    print("=============================================================")
    print("RAM |","0-7   | ", f"{ram[0]:03}", f"{ram[1]:03}", f"{ram[2]:03}", f"{ram[3]:03}", f"{ram[4]:03}", f"{ram[5]:03}", f"{ram[6]:03}", f"{ram[7]:03}", "|","Output I/O", "|")
    print("RAM |","8-15  | ", f"{ram[8]:03}", f"{ram[9]:03}", f"{ram[10]:03}", f"{ram[11]:03}", f"{ram[12]:03}", f"{ram[13]:03}", f"{ram[14]:03}", f"{ram[15]:03}", "|","","","",outputIO[1],"","","","","","",   "|")
    print("RAM |","16-23 | ", f"{ram[16]:03}", f"{ram[17]:03}", f"{ram[18]:03}", f"{ram[19]:03}", f"{ram[20]:03}", f"{ram[21]:03}", f"{ram[22]:03}", f"{ram[23]:03}","|", "============")
    print("RAM |","24-31 | ", f"{ram[24]:03}", f"{ram[25]:03}", f"{ram[26]:03}", f"{ram[27]:03}", f"{ram[28]:03}", f"{ram[29]:03}", f"{ram[30]:03}", f"{ram[31]:03}","|","","","HZ",hz ,"","","|")
    print("=============================================================")
    print("REGISTERS | 0-7 | " , f"{a_reg[0]:03}", f"{a_reg[1]:03}", f"{a_reg[2]:03}", f"{a_reg[3]:03}", f"{a_reg[4]:03}", f"{a_reg[5]:03}", f"{a_reg[6]:03}", f"{a_reg[7]:03}", "|" ,"", instruction ,"","", "|")
    print("=============================================================")
    if running == False:
            comand = input("Command :")
            if comand == "start":
                print("=======")
                hz = int(input("hz:"))          
                time_for_step = 1 / hz           
                print("=======")
                running = True
        
Menu()   
while running:
    time.sleep(time_for_step)

    if mpointer >= len(instrukcje):
        running = False
        break
    LoadInst()
    mpointer = mpointer + 1
    
    if instruction == "NOP":
        print("nop")
    elif instruction == "ADD":
        ArgNum()
        print("ADD")
        cout = a + b 
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "SUB":
        ArgNum()
        print("SUB")
        cout = a - b 
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "AND":
        ArgNum()
        print("AND")
        cout = a & b 
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "XOR":
        ArgNum()
        print("XOR")
        cout = a ^ b 
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "XNR":
        ArgNum()
        print("XNR")
        cout = ~(a ^ b) 
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "NOR":
        ArgNum()
        print("NOR")
        cout = ~(a | b)
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "A++":
        print("A++")
        ArgNum() 
        cout = a + 1 
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "A--": # 
        print("A--")
        ArgNum() 
        cout = a - 1 
        ChkFlag()
        print(cout)
        ArgSave()       
    elif instruction == "LSH":
        ArgNum()
        print("LSH")
        cout = a << 1
        ChkFlag()
        print(cout)
        ArgSave()
    elif instruction == "JMP": # skok
        print("JMP")
        Jump()
    elif instruction == "INT": # stala
        print("INT")
        IntLoad()
    elif instruction == "RND": # random number
        print("RND")
        randomNumber = random.randint(0,255)
        a_reg[arg_3] = randomNumber
        b_reg[arg_3] = randomNumber
    elif instruction == "IOR": # io to reg
        print("IOR")
        a_reg[arg_3] = inputIO[arg_1]
        b_reg[arg_3] = inputIO[arg_1]
    elif instruction == "RIO": # reg to i/o
        print("RIO")
        outputIO[arg_3] = a_reg[arg_1]
    elif instruction == "MOV": # reg to reg
        print("MOV")
        a_reg[arg_1] = a_reg[arg_2]
        b_reg[arg_1] = b_reg[arg_2]
    elif instruction == "RTP": # reg to ram pointer
        print("RTP")
        pointer = a_reg[arg_1]
    elif instruction == "CLP": # clean pointer
        print("CLP")
        pointer = 0
    elif instruction == "P++": # pointer ++
        print("P++")
        pointer = pointer + 1
    elif instruction == "P--": # pointer --
        print("P--")
        pointer = pointer - 1
    elif instruction == "LRR": # Load ram to reg
        print("LRR")
        a_reg[arg_3] = ram[pointer]
        b_reg[arg_3] = ram[pointer]
    elif instruction == "SRR": # Save reg into ram
        print("SRR")
        ram[pointer] = a_reg[arg_1]
    elif instruction == "CLR": # Clear reg
        print("CLR")
        a_reg[arg_3] = 0
        b_reg[arg_3] = 0
    elif instruction == "WAT": # Wait for enter
        print("WAT")
        print("Press enter to continiue...")
        input()
    elif instruction == "END": # End program
        print("END")
        running = False
    Menu()