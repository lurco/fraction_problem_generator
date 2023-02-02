import random   # Biblioteka do RNG
import sys      # Na potrzeby argumentów z linii poleceń
import time     # Pozwala na zdobycie informacji, jaki jest dzień (na potrzeby SEEDa)
import fractions# Pozwala liczyć na ułamkach zwykłych
import pdb      # Python Debugger

NR_OF_FRACTIONS = 4 # Number of fractions appearing in one equation

try:
    assert(len(sys.argv) <= 2)
except AssertionError:
    print('Za dużo argumentów - potrzebny tylko jeden jako SEED')

if len(sys.argv) == 2:
    random.seed(int(sys.argv[1]))    # SEED - brany jako argument z wiersza poleceń
elif len(sys.argv) == 1:        # SEED (domyślnie brany jako numer dnia licząc od 24 czerwca 2018 (e.g. 24 lipca => SEED = 30))
    year = time.gmtime().tm_year - 2018
    day = time.gmtime().tm_yday - 31 - 28 - 31 - 30 - 31 - 24
    random.seed(day + 365 * year) # SEED domyślny
    
zeroDigits = list(map(str, list(range(10))))    # 0-9 Digits
oneDigits = list(map(str, list(range(1,10))))   # 1-9 Digits

simple = 0
decimal = 1

def simple(firstDigit, secondDigit):
    return '\\frac{' + firstDigit + '}{' + secondDigit + '}'

def decimal(firstDigit, secondDigit):
    return firstDigit + '.' + secondDigit

fractionTypes = (simple,decimal)  # krotka
operationTypes = [" + ", " \\cdot ", " - ", " \\div "]
hasParenthesesTypes = (True,False)

def fraction():
    fractionType = random.choice(fractionTypes)
    firstDigit = random.choice(zeroDigits if (fractionType == decimal) else oneDigits)
    secondDigit = random.choice(oneDigits)
    return fractionType(firstDigit,secondDigit)

def operation():
    return random.choice(operationTypes)

class parentheses():
    def __init__(self, hasParentheses, leftParenthesis, rightParenthesis):
        self.hasParentheses = hasParentheses
        self.leftParenthesis = leftParenthesis
        self.rightParenthesis = rightParenthesis

def makeParentheses(parentheses):
    weights = [1,3]
    parentheses.hasParentheses = random.choices(hasParenthesesTypes, weights)[0]
    if parentheses.hasParentheses == True:
        parentheses.leftParenthesis = random.randint(0, NR_OF_FRACTIONS-2)
        parentheses.rightParenthesis = random.randint(parentheses.leftParenthesis+1, NR_OF_FRACTIONS-1)
        return parentheses
    else:
        parentheses.leftParenthesis = float("NaN")
        parentheses.rightParenthesis = float("NaN")
        return parentheses

# def generateEquation(plikZadania, 
# def equation(hasParentheses):
#     return 0

equationParentheses = parentheses(False, float("NaN"), float("NaN"))

plikZadania = open("zadania" + '2' + ".tex", "w")

for i in range(15):
    makeParentheses(equationParentheses)
    plikZadania.write('\\item $') 
    for j in range(2*NR_OF_FRACTIONS-1):
        #pdb.set_trace()
        if (j//2 == equationParentheses.leftParenthesis) and j%2 == 0:
            plikZadania.write("(")
        plikZadania.write(fraction() if j%2==0 else operation()) 
        if (j//2 == equationParentheses.rightParenthesis) and j%2 == 0:
            plikZadania.write(")")
    plikZadania.write('$ =\n')
    plikZadania.write('\\vspace{2ex}\n')
plikZadania.close()
