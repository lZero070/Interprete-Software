import ply.lex as lex

palabrasReservadas = {
    "ver": "print",  # print  
    "obt": "input",  # input
    "es": "if",  # if
    "deloc": "else",  # else
    "yy": "and",  # and
    "oo": "or",  # or
    "negar": "not",  # not
    "ciclom": "while",  # while
    "ciclop": "for",  # for
    "func": "def",  # def
    "fin": "break",  # break
    "devol": "return"  # return
}

literales = (
    "CIERTO",
    "FALSO"
)

tiposDeToken = (
    "ID",
    "PALABRA_RESERVADA",
    "LITERAL"
)

tokens = [
    'ID',
    'IMPRIMIR',
    'LEER',
    'SI',
    'SINO',
    'Y',
    'O',
    'NEGAR',
    'MIESTRAS',
    'FUNCION',
    'BREAK',
    'RETORNAR',
    'REVALUAR',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'DECIMAL',
    'ENTERO',
    'PTCOMA',
    'MENOR',
    'MAYOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUAL',
    'ASIGNACION',
    'DISTINTO',
    'IDENTIFICADOR',
    'BLOQUE',
    'CICLOP',
    'CICLOHACERR',
] + list(palabrasReservadas.values())


# Tokens
t_REVALUAR = r'Evaluar'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PTCOMA = r';'
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUAL = r'=='
t_ASIGNACION = r'='
t_DISTINTO = r'!='


def t_IMPRIMIR(t):
    r'ver'
    return t

def t_CICLOHACERM(t):
    r'ciclohacerm'
    return t


def t_LEER(t):
    r'obt'
    return t


def t_SI(t):
    r'es'
    return t


def t_SINO(t):
    r'deloc'
    return t


def t_Y(t):
    r'yy'
    return t


def t_O(t):
    r'oo'
    return t


def t_NEGAR(t):
    r'negar'
    return t


def t_MIESTRAS(t):
    r'ciclom'
    return t


def t_FUNCION(t):
    r'ciclop'
    return t


def t_BREAK(t):
    r'fin'
    return t


def t_RETORNAR(t):
    r'devol'
    return t

def t_CICLOP(t):
    r'ciclop'
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Valor flotante demasiado grande %d", t.value)
        t.value = 0
    return t


#identificar si un identificador es una palabra reservada o un identificador común.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabrasReservadas.get(t.value, 'ID')  # Verificar palabras reservadas
    return t

def t_BLOQUE_ignorar_espacios(t):
    r'\{([^}]*(\s|\\t)*)+[^}]*\}'
    t.type = 'BLOQUE'  # Establece el tipo de token
    t.value = t.value[1:-1]  # Elimina las llaves y guarda el contenido del bloque sin espacios en blanco
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor entero demasiado grande %d", t.value)
        t.value = 0
    return t


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Caracter invalido '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
lexer = lex.lex()
#---------------------------------------------------------- Parser---------------------------------------------

# Asociación de operadores y precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL', 'IGUAL', 'DISTINTO', 'ASIGNACION'),
    ('right', 'UMENOS'),
)

#Evaluar expresiones
def p_instrucciones_evaluar(t):
    'instruccion : REVALUAR CORIZQ expresion CORDER PTCOMA'
    print('El valor de la expresión es: ' + str(t[3]))

# calculo de operaciones binarias basicas
def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]

#expresiones negativas
def p_expresion_unitaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

#Expresion para parentesis
def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

#Expresiom para enteros o decimales
def p_expresion_number(t):
    '''expresion    : ENTERO
                    | DECIMAL'''
    t[0] = t[1]

#Expresdion para condiconales menor, mayor, etc
def p_expresion_condicional(t):
    '''expresion : expresion MENOR expresion
                | expresion MAYOR expresion
                | expresion MENORIGUAL expresion
                | expresion MAYORIGUAL expresion
                | expresion IGUAL expresion
                | expresion DISTINTO expresion
                | expresion ASIGNACION expresion'''

    t[0] = t[1] < t[3]
    if t[2] == '<':
        t[0] = t[1] < t[3]
    elif t[2] == '>':
        t[0] = t[1] > t[3]
    elif t[2] == '<=':
        t[0] = t[1] <= t[3]
    elif t[2] == '>=':
        t[0] = t[1] >= t[3]
    elif t[2] == '==':
        t[0] = t[1] == t[3]
    elif t[2] == '!=':
        t[0] = t[1] != t[3]
    elif t[2] == '=':
        t[0] = t[3]

def p_condicional_anidado(t):
    '''
    condicional : condicional SINO condicional
    '''
    t[0] = ("nested-if-else", t[1], t[3])


def p_instrucciones_lista(t):
    '''
    instrucciones    : instruccion instrucciones
                     | condicional instrucciones
                     | instruccion
                     | condicional
                     | ciclo instrucciones
                     | funcion instrucciones
                     | instruccion_break instrucciones
    '''
    pass  # Esta regla no hace nada por ahora

def p_definicion_funcion(t):
    '''
    funcion : FUNCION ID PARIZQ parametros PARDER PTCOMA instrucciones PTCOMA
    '''
    t[0] = ("function", t[2], t[4], t[7])

def p_parametros(t):
    '''
    parametros : ID
               | ID COMA parametros
    '''
    t[0] = [t[1]] if len(t) == 2 else [t[1]] + t[3]

def p_ciclo_mientras(t):
    '''
    ciclo : MIESTRAS expresion PTCOMA instrucciones PTCOMA
    '''
    t[0] = ("while", t[2], t[4])

def p_ciclo_for(t):
    '''
    ciclo : CICLOP ID ASIGNACION expresion PTCOMA expresion PTCOMA expresion PTCOMA instrucciones PTCOMA
    '''
    t[0] = ("for", t[2], t[4], t[6], t[8], t[10])

def p_condicional(t):
    '''
    condicional : SI expresion PTCOMA instrucciones PTCOMA
                | condicional condicional
                | condicional condicional_si_sino
                | ciclo condicional
    '''
    if len(t) == 3:
        t[0] = ("nested-if", t[1], t[2])
    elif len(t) == 2 and isinstance(t[1], tuple):
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_instruccion_break(t):
    '''
    instruccion : BREAK PTCOMA
    '''
    t[0] = ("break",)

def p_ciclo_do_while(t):
    '''
    ciclo : CICLOHACERM instrucciones MIENTRAS expresion PTCOMA
    '''
    t[0] = ("do-while", t[2], t[4])

#Asignacion de valores a varibales
def p_instruccion(t):
    '''
    instruccion : ID '=' expresion PTCOMA
    '''
    t[0] = t[3]  # Almacenar el valor de la expresión en la variable asignada
    # Escribir el valor de x en un archivo .txt
    if t[1] == 'x':
        t[0] = t[3]

import ply.yacc as yacc
parser = yacc.yacc()
