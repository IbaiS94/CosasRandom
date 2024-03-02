import re
def calc():
    resultado = 0
    operacion = input("Hola buenas, inserte operacion: ")
    listnum = re.split(r'(\+|\-|\*|\/|\s+)', operacion)
    valores = {
        '-': lambda x, y: x - y,
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y }
    for a in range(0,len(listnum)):
        if(a%2==0 and a!=0):
            try:
                resultado = resultado + valores[listnum[a-1]](int(listnum[a-2]),int(listnum[a]))        
            except ArithmeticError as e: 
                print("ERROR: "+ str(e)) 
    print(resultado)

if __name__ == "__main__":
    calc()