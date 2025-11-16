# Código intermedio

Generador de códigoen 3 direcciones para una grmática simplificada de Python

## Como ejecutar:

    python3 codigo_intermedio.py 


## Diseño: 

### Gramática sencilla GIC de python

    sentencia  → ID = expresion | expresion
    expresion  → termino ((+|-) termino)*
    termino    → factor ((*|/|//|%) factor)*
    factor     → potencia (** potencia)*
    potencia   → ( expresion ) | NUM | ID

**Precedencia de operadores (de mayor a menor):**
1. `( )` - Paréntesis
2. `**` - Potenciación (asociativa a la derecha)
3. `*, /, //, %` - Multiplicación, división, división entera, módulo
4. `+, -` - Suma, resta

---

### Definir atributos de la gramática

Todos los atributos son **sintetizados** (se calculan de abajo hacia arriba en el árbol):

#### Atributos Teóricos

| **Atributo teórico** | **¿Qué es?** | **¿Dónde se calcula?** |
| :--- | :--- | :--- |
| `.val` | Valor semántico del nodo/sentencia.  | Método `evaluar()` retorna el valor |
| `.lugar`  | Variable/temporal que contiene resultado. | Método `generar_codigo()` retorna `string` |
| `.codigo` | Código de 3 direcciones | Método `generar_codigo()` agrega a lista |

#### Atributos por No Terminal

| **No Terminal** | **Atributo** | **Tipo** | 
| :--- | :--- | :--- |
| `<sentencia>` | `.val` | `float` | 
| `<sentencia>` | `.codigo` | `string` | 
| `<sentencia>` | `.lugar` | `string` | 
| `<expresion>` | `.val` | `float` | 
| `<expresion>` | `.codigo` | `string` | 
| `<expresion>` | `.lugar` | `string` | 
| `<termino>` | `.val` | `float` | 
| `<termino>` | `.codigo` | `string` |
| `<termino>` | `.lugar` | `string` | 
| `<factor>` | `.val` | `float` | 
| `<factor>` | `.codigo` | `string` | Código de 3 direcciones |
| `<factor>` | `.lugar` | `string` | Temporal con el resultado |
| `<potencia>` | `.val` | `float` | Valor de la potencia |
| `<potencia>` | `.lugar` | `string` | Nombre de variable o valor |- Implementar ETDS (Esquema de Traducción)

### Reglas semánticas y de traducción para cada producción 

#### Regla 1: Asignación
```
<sentencia> ::= ID = <expresion>

Reglas semánticas:
  <sentencia>.val = <expresion>.val
  TablaSimbolos.insertar(ID.nombre, <expresion>.val)

Reglas de traducción (Código 3D):
  <sentencia>.lugar = ID.nombre
  <sentencia>.codigo = <expresion>.codigo || 
                       gen(ID.nombre + " = " + <expresion>.lugar)
```

**Implementación:**
```python
def evaluar(self, tabla: TablaSimbolos) -> float:
    valor = self.expresion.evaluar(tabla)
    tabla.insertar(self.variable, "float", valor, self.linea)
    return valor

def generar_codigo(self, generador) -> str:
    expr_var = self.expresion.generar_codigo(generador)
    generador.agregar_instruccion("=", expr_var, None, self.variable)
    return self.variable
```

---

#### Regla 2: Expresión (Suma/Resta)
```
<expresion> ::= <termino₁> + <termino₂>

Reglas semánticas:
  <expresion>.val = <termino₁>.val + <termino₂>.val

Reglas de traducción (Código 3D):
  temp = nuevo_temporal()
  <expresion>.lugar = temp
  <expresion>.codigo = <termino₁>.codigo || 
                       <termino₂>.codigo || 
                       gen(temp + " = " + <termino₁>.lugar + " + " + <termino₂>.lugar)
```

**Implementación:**
```python
def evaluar(self, tabla: TablaSimbolos) -> float:
    val_izq = self.izq.evaluar(tabla)
    val_der = self.der.evaluar(tabla)
    if self.operador == '+':
        return val_izq + val_der
    elif self.operador == '-':
        return val_izq - val_der

def generar_codigo(self, generador) -> str:
    izq_var = self.izq.generar_codigo(generador)
    der_var = self.der.generar_codigo(generador)
    temp = generador.nuevo_temporal()
    generador.agregar_instruccion(self.operador, izq_var, der_var, temp)
    return temp
```

---

#### Regla 3: Término (Multiplicación/División)
```
<termino> ::= <factor₁> * <factor₂>

Reglas semánticas:
  <termino>.val = <factor₁>.val * <factor₂>.val

Reglas de traducción (Código 3D):
  temp = nuevo_temporal()
  <termino>.lugar = temp
  <termino>.codigo = <factor₁>.codigo || 
                     <factor₂>.codigo || 
                     gen(temp + " = " + <factor₁>.lugar + " * " + <factor₂>.lugar)
```

---

#### Regla 4: Factor (Potenciación)
```
<factor> ::= <potencia₁> ** <potencia₂>

Reglas semánticas:
  <factor>.val = <potencia₁>.val ** <potencia₂>.val

Reglas de traducción (Código 3D):
  temp = nuevo_temporal()
  <factor>.lugar = temp
  <factor>.codigo = <potencia₁>.codigo || 
                    <potencia₂>.codigo || 
                    gen(temp + " = " + <potencia₁>.lugar + " ** " + <potencia₂>.lugar)
```

---

#### Regla 5: Número (Terminal)
```
<potencia> ::= NUM

Reglas semánticas:
  <potencia>.val = NUM.valor
  <potencia>.lugar = NUM.valor
  <potencia>.codigo = ε (vacío)
```

**Implementación:**
```python
def evaluar(self, tabla: TablaSimbolos) -> float:
    return self.valor

def generar_codigo(self, generador) -> str:
    return str(self.valor)
```

---

#### Regla 6: Variable (Terminal)
```
<potencia> ::= ID

Reglas semánticas:
  <potencia>.val = TablaSimbolos.buscar(ID.nombre).valor
  <potencia>.lugar = ID.nombre
  <potencia>.codigo = ε (vacío)
```

**Implementación:**
```python
def evaluar(self, tabla: TablaSimbolos) -> float:
    sym = tabla.buscar(self.nombre)
    if sym is None:
        raise Exception(f"Variable '{self.nombre}' no definida")
    return sym.valor

def generar_codigo(self, generador) -> str:
    return self.nombre
```

---

### Tabla de Símbolos

**Estructura de un símbolo:**
- `nombre`: Identificador de la variable (ej: "x")
- `tipo`: Tipo de dato (ej: "float")
- `valor`: Valor almacenado (ej: 5.0)
- `linea`: Línea del código fuente donde se definió

**Operaciones:**
- `insertar(nombre, tipo, valor, linea)`: Agrega o actualiza un símbolo
- `buscar(nombre)`: Busca un símbolo por nombre, retorna `Simbolo` o `None`
- `actualizar(nombre, valor)`: Modifica el valor de un símbolo existente
- `imprimir()`: Muestra el estado actual de la tabla

**Implementación:**


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

      
### Implementar ETDS (Esquema de Traducción)

El **Esquema de Traducción Dirigida por la Sintaxis** se implementa mediante tres métodos en cada nodo del AST:

#### Método `evaluar()` - Calcula `.val`
```python
# REGLA SEMÁNTICA: NUM.val = NUM.valor
class NodoNumero(NodoAST):
    def evaluar(self, tabla: TablaSimbolos) -> float:
        return self.valor
```

#### Método `generar_codigo()` - Calcula `.lugar` y `.codigo`
```python
# REGLA DE TRADUCCIÓN:
#   NUM.lugar = NUM.valor
#   NUM.codigo = ε (vacío)
class NodoNumero(NodoAST):
    def generar_codigo(self, generador) -> str:
        return str(self.valor)  # Retorna .lugar
```

#### Método `imprimir_arbol()` - Visualización
```python
class NodoNumero(NodoAST):
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        conector = "└── " if es_ultimo else "├── "
        if con_valores:
            print(f"{prefijo}{conector}NUM: {self.valor} → val={self.valor}")
        else:
            print(f"{prefijo}{conector}NUM: {self.valor}")
```

  
  
## Programa (por cada sentencia):

- Crear Tabla de Símbolos vacía (primera vez) o usar existente
- Análisis Léxico → lista de Tokens
- Análisis Sintáctico → AST (sin decorar)
- Análisis Semántico → Evaluar + Actualizar Tabla
- Generación Código 3D → Instrucciones intermedias
- Mostrar AST Decorado
- Mostrar Tabla Símbolos → Estado actual



## Casos de prueba
- x = 5
- y = x + 3 * 2
- z = (x + y) * 2 ** 3 -> 128
- Resultado obtenido = 128

<img width="378" height="767" alt="image" src="https://github.com/user-attachments/assets/8c341ede-4f59-4738-b752-81a32dfeeef0" />

---

- 7+8-57/0+(2-4) = error
- Resultado obtenido =  ERROR: División por cero

<img width="268" height="531" alt="imagen" src="https://github.com/user-attachments/assets/951d3927-58eb-4e9a-9b06-b0ad9c41d73e" />


