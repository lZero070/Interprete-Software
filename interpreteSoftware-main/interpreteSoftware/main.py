import gramatica
# Crea instancias de lexer y parser
lexer = gramatica.lexer
parser = gramatica.parser

# Define tu código fuente en una cadena
codigo_fuente = """

ver "Hola, mundo";
x = 5;
y = 3.14;
si (x > 0) {
    ver "x es positivo";
} deloc {
    ver "x es negativo o cero";
}

ciclom (x > 0) {
    x = x - 1;
}

ciclop i = 0; i < 5; i = i + 1 {
    ver "Iteración " yy i;
}

def funcion_sumar(a, b) {
    retornar a + b;
}

ciclom (y > 2) {
    x = x + 1;
    si (x == 10) {
        romper;
    }
}

Evaluar [x + 10];

"""

# Analiza léxica y sintácticamente el código fuente
resultado = parser.parse(codigo_fuente, lexer=lexer)

# Ejecuta las instrucciones y estructuras de control según el resultado del análisis sintáctico
if resultado:
    # Procesa y ejecuta las instrucciones según la estructura de árbol resultante
    print("Análisis sintáctico exitoso. Ejecutando el código...")
    print(resultado)  # Puedes definir cómo ejecutar las instrucciones aquí
else:
    print("Error de análisis sintáctico. El código fuente es inválido.")