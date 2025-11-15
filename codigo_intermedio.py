from dataclasses import dataclass
from typing import Any, Dict, List, Optional

#TABLA DE SÍMBOLOS
@dataclass
class Simbolo:
    nombre: str
    tipo: str
    valor: Any
    linea: int
    
class TablaSimbolos:
    def __init__(self):
        self.simbolos: Dict[str, Simbolo] = {}
    
    def insertar(self, nombre: str, tipo: str, valor: Any, linea: int):
        self.simbolos[nombre] = Simbolo(nombre, tipo, valor, linea)
    
    def buscar(self, nombre: str) -> Optional[Simbolo]:
        return self.simbolos.get(nombre)
    
    def actualizar(self, nombre: str, valor: Any):
        if nombre in self.simbolos:
            self.simbolos[nombre].valor = valor
    
    def imprimir(self):
        print("\n[6] TABLA DE SÍMBOLOS")
        if not self.simbolos:
            print("(no hay variables definidas)")
        else:
            print(f"{'Nombre':<15} {'Tipo':<10} {'Valor':<15} {'Línea':<10}")
            for sym in self.simbolos.values():
                print(f"{sym.nombre:<15} {sym.tipo:<10} {str(sym.valor):<15} {sym.linea:<10}")


# GENERADOR DE CÓDIGO DE TRES DIRECCIONES
class GeneradorCodigoTresDirecciones:
    def __init__(self):
        self.contador_temp = 0
        self.instrucciones = []
    
    def nuevo_temporal(self) -> str:
        temp = f"t{self.contador_temp}"
        self.contador_temp += 1
        return temp
    
    def agregar_instruccion(self, op: str, arg1: str, arg2: str = None, resultado: str = None):
        if arg2 is None:
            # Instrucción de copia: resultado = arg1
            self.instrucciones.append(f"{resultado} = {arg1}")
        else:
            # Instrucción binaria: resultado = arg1 op arg2
            self.instrucciones.append(f"{resultado} = {arg1} {op} {arg2}")
    
    def imprimir_codigo(self):
        print("\n[4] CÓDIGO DE TRES DIRECCIONES")
        if not self.instrucciones:
            print("(no hay instrucciones generadas)")
        else:
            for i, instr in enumerate(self.instrucciones, 1):
                print(f"  {i:2d}. {instr}")
    
    def limpiar(self):
        self.contador_temp = 0
        self.instrucciones = []


# NODOS DEL AST (Árbol de Sintaxis Abstracta)
@dataclass
class NodoAST:
    tipo: str
    def evaluar(self, tabla: TablaSimbolos) -> Any:
        raise NotImplementedError
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        raise NotImplementedError
    
    def generar_codigo(self, generador: GeneradorCodigoTresDirecciones) -> str:
        raise NotImplementedError

@dataclass
class NodoNumero(NodoAST):
    valor: float
    
    def __init__(self, valor: float):
        super().__init__("numero")
        self.valor = valor
    
    def evaluar(self, tabla: TablaSimbolos) -> float:
        return self.valor
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        conector = "└── " if es_ultimo else "├── "
        if con_valores:
            print(f"{prefijo}{conector}NUM: {self.valor} → val={self.valor}")
        else:
            print(f"{prefijo}{conector}NUM: {self.valor}")
    
    def generar_codigo(self, generador: GeneradorCodigoTresDirecciones) -> str:
        # Los números se representan directamente
        return str(self.valor)

@dataclass
class NodoVariable(NodoAST):
    nombre: str
    linea: int
    
    def __init__(self, nombre: str, linea: int):
        super().__init__("variable")
        self.nombre = nombre
        self.linea = linea
    
    def evaluar(self, tabla: TablaSimbolos) -> float:
        sym = tabla.buscar(self.nombre)
        if sym is None:
            raise Exception(f"Variable '{self.nombre}' no definida (línea {self.linea})")
        return sym.valor
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        conector = "└── " if es_ultimo else "├── "
        if con_valores and tabla:
            try:
                val = self.evaluar(tabla)
                print(f"{prefijo}{conector}VAR: {self.nombre} → val={val}")
            except:
                print(f"{prefijo}{conector}VAR: {self.nombre} → (no definida)")
        else:
            print(f"{prefijo}{conector}VAR: {self.nombre}")
    
    def generar_codigo(self, generador: GeneradorCodigoTresDirecciones) -> str:
        return self.nombre

@dataclass
class NodoBinario(NodoAST):
    operador: str
    izq: NodoAST
    der: NodoAST
    
    def __init__(self, operador: str, izq: NodoAST, der: NodoAST):
        super().__init__("binario")
        self.operador = operador
        self.izq = izq
        self.der = der
    
    def evaluar(self, tabla: TablaSimbolos) -> float:
        val_izq = self.izq.evaluar(tabla)
        val_der = self.der.evaluar(tabla)
        
        if self.operador == '+':
            return val_izq + val_der
        elif self.operador == '-':
            return val_izq - val_der
        elif self.operador == '*':
            return val_izq * val_der
        elif self.operador == '/':
            if val_der == 0:
                raise Exception("División por cero")
            return val_izq / val_der
        elif self.operador == '**':
            return val_izq ** val_der
        elif self.operador == '//':
            if val_der == 0:
                raise Exception("División por cero")
            return val_izq // val_der
        elif self.operador == '%':
            if val_der == 0:
                raise Exception("Módulo por cero")
            return val_izq % val_der
        else:
            raise Exception(f"Operador desconocido: {self.operador}")
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        conector = "└── " if es_ultimo else "├── "
        if con_valores and tabla:
            try:
                val = self.evaluar(tabla)
                print(f"{prefijo}{conector}OP({self.operador}) → val={val}")
            except Exception as e:
                print(f"{prefijo}{conector}OP({self.operador}) → ERROR: {e}")
        else:
            print(f"{prefijo}{conector}OP({self.operador})")
        
        extension = "    " if es_ultimo else "│   "
        self.izq.imprimir_arbol(prefijo + extension, False, con_valores, tabla)
        self.der.imprimir_arbol(prefijo + extension, True, con_valores, tabla)
    
    def generar_codigo(self, generador: GeneradorCodigoTresDirecciones) -> str:
        # Generar código para el operando izquierdo
        izq_var = self.izq.generar_codigo(generador)
        
        # Generar código para el operando derecho
        der_var = self.der.generar_codigo(generador)
        
        # Crear un temporal para el resultado
        temp = generador.nuevo_temporal()
        
        # Agregar la instrucción de tres direcciones
        generador.agregar_instruccion(self.operador, izq_var, der_var, temp)
        
        return temp

@dataclass
class NodoAsignacion(NodoAST):
    variable: str
    expresion: NodoAST
    linea: int
    
    def __init__(self, variable: str, expresion: NodoAST, linea: int):
        super().__init__("asignacion")
        self.variable = variable
        self.expresion = expresion
        self.linea = linea
    
    def evaluar(self, tabla: TablaSimbolos) -> float:
        valor = self.expresion.evaluar(tabla)
        tabla.insertar(self.variable, "float", valor, self.linea)
        return valor
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        conector = "└── " if es_ultimo else "├── "
        if con_valores and tabla:
            try:
                val = self.evaluar(tabla)
                print(f"{prefijo}{conector}ASIG: {self.variable} → val={val}")
            except Exception as e:
                print(f"{prefijo}{conector}ASIG: {self.variable} → ERROR: {e}")
        else:
            print(f"{prefijo}{conector}ASIG: {self.variable}")
        
        extension = "    " if es_ultimo else "│   "
        self.expresion.imprimir_arbol(prefijo + extension, True, con_valores, tabla)
    
    def generar_codigo(self, generador: GeneradorCodigoTresDirecciones) -> str:
        # Generar código para la expresión del lado derecho
        expr_var = self.expresion.generar_codigo(generador)
        
        # Agregar la instrucción de asignación
        generador.agregar_instruccion("=", expr_var, None, self.variable)
        
        return self.variable


# ANALIZADOR LÉXICO
class Token:
    def __init__(self, tipo: str, valor: Any, linea: int):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, L{self.linea})"

class AnalizadorLexico:
    def __init__(self, texto: str):
        self.texto = texto
        self.pos = 0
        self.linea = 1
        self.tokens = []
    
    def tokenizar(self) -> List[Token]:
        while self.pos < len(self.texto):
            char = self.texto[self.pos]
            
            # Ignorar espacios en blanco
            if char.isspace():
                if char == '\n':
                    self.linea += 1
                self.pos += 1
                continue
            
            # Números
            if char.isdigit():
                self.tokens.append(self.leer_numero())
                continue
            
            # Identificadores y palabras clave
            if char.isalpha() or char == '_':
                self.tokens.append(self.leer_identificador())
                continue
            
            # Operadores de dos caracteres
            if self.pos + 1 < len(self.texto):
                dos_chars = self.texto[self.pos:self.pos+2]
                if dos_chars in ['**', '//', '==', '!=', '<=', '>=']:
                    self.tokens.append(Token(dos_chars, dos_chars, self.linea))
                    self.pos += 2
                    continue
            
            # Operadores de un carácter
            if char in '+-*/%()=<>':
                self.tokens.append(Token(char, char, self.linea))
                self.pos += 1
                continue
            
            raise Exception(f"Carácter no reconocido: '{char}' (línea {self.linea})")
        
        self.tokens.append(Token('EOF', None, self.linea))
        return self.tokens
    
    def leer_numero(self) -> Token:
        inicio = self.pos
        tiene_punto = False
        
        while self.pos < len(self.texto):
            char = self.texto[self.pos]
            if char.isdigit():
                self.pos += 1
            elif char == '.' and not tiene_punto:
                tiene_punto = True
                self.pos += 1
            else:
                break
        
        valor = float(self.texto[inicio:self.pos])
        return Token('NUM', valor, self.linea)
    
    def leer_identificador(self) -> Token:
        inicio = self.pos
        while self.pos < len(self.texto) and (self.texto[self.pos].isalnum() or self.texto[self.pos] == '_'):
            self.pos += 1
        valor = self.texto[inicio:self.pos]
        
        # Palabras reservadas de Python (subset)
        palabras_clave = ['if', 'else', 'while', 'for', 'def', 'return', 'print']
        if valor in palabras_clave:
            return Token('KEYWORD', valor, self.linea)
        
        return Token('ID', valor, self.linea)

class AnalizadorSintactico:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.token_actual = tokens[0]
    
    def avanzar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_actual = self.tokens[self.pos]
    
    def coincidir(self, tipo: str):
        if self.token_actual.tipo == tipo:
            token = self.token_actual
            self.avanzar()
            return token
        else:
            raise Exception(f"Se esperaba '{tipo}', se encontró '{self.token_actual.tipo}' (línea {self.token_actual.linea})")
    
    def sentencia(self) -> NodoAST:
        """sentencia -> ID = expresion | expresion"""
        if self.token_actual.tipo == 'ID':
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].tipo == '=':
                nombre = self.token_actual.valor
                linea = self.token_actual.linea
                self.avanzar()
                self.coincidir('=')
                expr = self.expresion()
                return NodoAsignacion(nombre, expr, linea)
        
        return self.expresion()
    
    def expresion(self) -> NodoAST:
        """expresion -> termino ((+|-) termino)*"""
        nodo = self.termino()
        
        while self.token_actual.tipo in ['+', '-']:
            op = self.token_actual.tipo
            self.avanzar()
            der = self.termino()
            nodo = NodoBinario(op, nodo, der)
        
        return nodo
    
    def termino(self) -> NodoAST:
        """termino -> factor ((*|/|//|%) factor)*"""
        nodo = self.factor()
        
        while self.token_actual.tipo in ['*', '/', '//', '%']:
            op = self.token_actual.tipo
            self.avanzar()
            der = self.factor()
            nodo = NodoBinario(op, nodo, der)
        
        return nodo
    
    def factor(self) -> NodoAST:
        """factor -> potencia (** potencia)*"""
        nodo = self.potencia()
        
        # La potencia se asocia a la derecha en Python
        if self.token_actual.tipo == '**':
            op = self.token_actual.tipo
            self.avanzar()
            der = self.factor()  # Recursión para asociatividad derecha
            nodo = NodoBinario(op, nodo, der)
        
        return nodo
    
    def potencia(self) -> NodoAST:
        """potencia -> ( expresion ) | NUM | ID"""
        if self.token_actual.tipo == '(':
            self.avanzar()
            nodo = self.expresion()
            self.coincidir(')')
            return nodo
        elif self.token_actual.tipo == 'NUM':
            valor = self.token_actual.valor
            self.avanzar()
            return NodoNumero(valor)
        elif self.token_actual.tipo == 'ID':
            nombre = self.token_actual.valor
            linea = self.token_actual.linea
            self.avanzar()
            return NodoVariable(nombre, linea)
        else:
            raise Exception(f"Factor inválido: {self.token_actual.tipo} (línea {self.token_actual.linea})")


# PROCESADOR ETDS 
def procesar_sentencia(expresion: str, tabla: TablaSimbolos, generador: GeneradorCodigoTresDirecciones):
    # Limpiar generador de código para nueva sentencia
    generador.limpiar()
    
    print("[1] ANÁLISIS LÉXICO")
    lexico = AnalizadorLexico(expresion)
    tokens = lexico.tokenizar()
    for token in tokens:
        if token.tipo != 'EOF':
            print(f"  {token}")
    
    print("[2] ANÁLISIS SINTÁCTICO - AST")
    sintactico = AnalizadorSintactico(tokens)
    ast = sintactico.sentencia()
    ast.imprimir_arbol(con_valores=False, tabla=None)
    
    print("[3] EVALUACIÓN SEMÁNTICA")
    resultado = ast.evaluar(tabla)
    print(f"Resultado = {resultado}")
    
    ast.generar_codigo(generador)
    generador.imprimir_codigo()
    
    print("[5] AST DECORADO")
    ast.imprimir_arbol(con_valores=True, tabla=tabla)
    
    tabla.imprimir()
    return resultado

def main():  
    tabla = TablaSimbolos()
    generador = GeneradorCodigoTresDirecciones()
    
    while True:
        try:
            # Solicitar entrada
            expresion = input("> ").strip()
            # Ignorar líneas vacías
            if not expresion:
                continue
            
            # Procesar la sentencia
            procesar_sentencia(expresion, tabla, generador)
            
        except Exception as e:
            print(f"\nERROR: {e}")
            print()


if __name__ == "__main__":
    main()