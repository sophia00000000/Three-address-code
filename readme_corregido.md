# Código Intermedio

Generador de código en 3 direcciones para una gramática simplificada de Python con Esquema de Traducción Dirigida por la Sintaxis (ETDS).

## 📋 Cómo ejecutar

```bash
python3 codigo_intermedio.py
```

---

## 🏗️ Diseño

### 1. Gramática Libre de Contexto (GLC) de Python

```bnf
sentencia  → ID = expresion | expresion
expresion  → termino ((+|-) termino)*
termino    → factor ((*|/|//|%) factor)*
factor     → potencia (** potencia)*
potencia   → ( expresion ) | NUM | ID
```

**Precedencia de operadores (de mayor a menor):**
1. `( )` - Paréntesis
2. `**` - Potenciación (asociativa a la derecha)
3. `*, /, //, %` - Multiplicación, división, división entera, módulo
4. `+, -` - Suma, resta

---

### 2. Atributos de la Gramática

Todos los atributos son **sintetizados** (se calculan de abajo hacia arriba en el árbol).

#### Atributos Teóricos

| **Atributo** | **¿Qué es?** | **Implementación** |
| :--- | :--- | :--- |
| `.val` | Valor semántico del nodo | `return` del método `evaluar()` |
| `.lugar` | Variable/temporal con el resultado | `return` del método `generar_codigo()` |
| `.codigo` | Lista de instrucciones de 3 direcciones | Se acumula en `generador.instrucciones` |

#### Atributos por No Terminal

| **No Terminal** | **Atributo** | **Tipo** | **Descripción** |
| :--- | :--- | :--- | :--- |
| `<sentencia>` | `.val` | `float` | Valor evaluado de la sentencia |
| `<sentencia>` | `.codigo` | `list[string]` | Código de 3 direcciones generado |
| `<sentencia>` | `.lugar` | `string` | Variable donde se guarda el resultado |
| `<expresion>` | `.val` | `float` | Valor de la expresión |
| `<expresion>` | `.codigo` | `list[string]` | Código de 3 direcciones |
| `<expresion>` | `.lugar` | `string` | Temporal con el resultado |
| `<termino>` | `.val` | `float` | Valor del término |
| `<termino>` | `.codigo` | `list[string]` | Código de 3 direcciones |
| `<termino>` | `.lugar` | `string` | Temporal con el resultado |
| `<factor>` | `.val` | `float` | Valor del factor |
| `<factor>` | `.codigo` | `list[string]` | Código de 3 direcciones |
| `<factor>` | `.lugar` | `string` | Temporal con el resultado |
| `<potencia>` | `.val` | `float` | Valor de la potencia |
| `<potencia>` | `.lugar` | `string` | Nombre de variable o valor literal |

---

### 3. Reglas Semánticas y de Traducción

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

### 4. Tabla de Símbolos

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
```python
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
```

---

### 5. Implementación del ETDS

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
# VISUALIZACIÓN: Muestra el AST con o sin valores
class NodoNumero(NodoAST):
    def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
        conector = "└── " if es_ultimo else "├── "
        if con_valores:
            print(f"{prefijo}{conector}NUM: {self.valor} → val={self.valor}")
        else:
            print(f"{prefijo}{conector}NUM: {self.valor}")
```

---

## 🔄 Flujo del Programa

**Por cada sentencia ingresada:**

1. **Inicializar** - Crear Tabla de Símbolos vacía (primera vez) o usar existente
2. **[1] Análisis Léxico** → Genera lista de tokens
3. **[2] Análisis Sintáctico** → Construye AST sin decorar
4. **[3] Análisis Semántico** → Evalúa expresiones y actualiza tabla de símbolos
5. **[4] Generación de Código 3D** → Genera instrucciones intermedias
6. **[5] AST Decorado** → Muestra árbol con valores calculados
7. **[6] Tabla de Símbolos** → Muestra estado actual de variables

---

## ✅ Casos de Prueba

### Caso 1: Asignaciones y expresiones
```python
>>> x = 5
Resultado = 5.0
Código 3D:
  1. x = 5.0

>>> y = x + 3 * 2
Resultado = 11.0
Código 3D:
  1. t0 = 3.0 * 2.0
  2. t1 = x + t0
  3. y = t1

>>> z = (x + y) * 2 ** 3
Resultado = 128.0
Código 3D:
  1. t0 = x + y
  2. t1 = 2.0 ** 3.0
  3. t2 = t0 * t1
  4. z = t2
```

**Tabla de Símbolos final:**
```
Nombre          Tipo       Valor           Línea     
x               float      5.0             1         
y               float      11.0            1         
z               float      128.0           1         
```

---

### Caso 2: Detección de errores
```python
>>> 7 + 8 - 57 / 0 + (2 - 4)
ERROR: División por cero
```

El compilador detecta errores en tiempo de evaluación semántica:
- ✅ División por cero
- ✅ Módulo por cero
- ✅ Variables no definidas
- ✅ Errores de sintaxis

---

## 🎯 Características Implementadas

- ✅ Gramática con 5 niveles de precedencia
- ✅ Operadores: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- ✅ Variables y asignaciones
- ✅ Expresiones con paréntesis
- ✅ Tabla de símbolos persistente
- ✅ Código de tres direcciones
- ✅ AST decorado con valores
- ✅ Detección de errores semánticos
- ✅ Asociatividad correcta (** es asociativa a la derecha)

---

## 📚 Fundamentos Teóricos

Este compilador implementa:
- **GLC (Gramática Libre de Contexto)** para definir la sintaxis
- **GA (Gramática de Atributos)** con atributos sintetizados
- **ETDS (Esquema de Traducción Dirigida por Sintaxis)** para generación de código
- **Análisis sintáctico descendente recursivo**
- **Generación de código intermedio** (cuádruplas simplificadas)

---

## 🔍 Ejemplo Completo de Ejecución

```
>>> y = 2 + 3 * 4

============================================================
[1] ANÁLISIS LÉXICO
============================================================
  Token(ID, y, L1)
  Token(=, =, L1)
  Token(NUM, 2.0, L1)
  Token(+, +, L1)
  Token(NUM, 3.0, L1)
  Token(*, *, L1)
  Token(NUM, 4.0, L1)

============================================================
[2] ANÁLISIS SINTÁCTICO - AST
============================================================
└── ASIG: y
    └── OP(+)
        ├── NUM: 2.0
        └── OP(*)
            ├── NUM: 3.0
            └── NUM: 4.0

============================================================
[3] EVALUACIÓN SEMÁNTICA
============================================================
Resultado = 14.0

============================================================
[4] CÓDIGO DE TRES DIRECCIONES
============================================================
   1. t0 = 3.0 * 4.0
   2. t1 = 2.0 + t0
   3. y = t1

============================================================
[5] AST DECORADO
============================================================
└── ASIG: y → val=14.0
    └── OP(+) → val=14.0
        ├── NUM: 2.0 → val=2.0
        └── OP(*) → val=12.0
            ├── NUM: 3.0 → val=3.0
            └── NUM: 4.0 → val=4.0

============================================================
[6] TABLA DE SÍMBOLOS
============================================================
Nombre          Tipo       Valor           Línea     
y               float      14.0            1         
============================================================
```

---

## 👨‍💻 Autor

Implementación de compilador educativo con fines académicos.
