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
  
### Definir atributos de la gramática

Todos los atributos son **sintetizados** (se calculan de abajo hacia arriba en el árbol):

| **Atributo teórico** | **¿Qué es?** | **¿Dónde se calcula?** |
| :--- | :--- | :--- |
| `.val` | Valor semántico del nodo/sentencia.  | Método `evaluar()` retorna el valor |
| `.lugar`  | Variable/temporal que contiene resultado. | Método `generar_codigo()` retorna `string` |
| `.codigo` | Código de 3 direcciones | Método `generar_codigo()` agrega a lista |



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

**Regla Asignación**
```
<sentencia> ::= <ID> = <expresion>

Semántica:
  <sentencia>.val = <expresion>.val
  TablaSimbolos.insertar(ID.nombre, <expresion>.val)

Código 3D:
  <sentencia>.codigo = <expresion>.codigo || 
                       gen(ID.nombre + " = " + <expresion>.lugar)
```

**Regla Expresión Suma/Resta**
```
<expresion> ::= <termino₁> + <termino₂>

Semántica:
  <expresion>.val = <termino₁>.val + <termino₂>.val

Código 3D:
  temp = nuevo_temporal()
  <expresion>.lugar = temp
  <expresion>.codigo = <termino₁>.codigo || 
                       <termino₂>.codigo || 
                       gen(temp + " = " + <termino₁>.lugar + " + " + <termino₂>.lugar)
```

 **Regla Término Multiplicación/División**
```
<termino> ::= <factor₁> * <factor₂>

Semántica:
  <termino>.val = <factor₁>.val * <factor₂>.val

Código 3D:
  temp = nuevo_temporal()
  <termino>.lugar = temp
  <termino>.codigo = <factor₁>.codigo || 
                     <factor₂>.codigo || 
                     gen(temp + " = " + <factor₁>.lugar + " * " + <factor₂>.lugar)
```

**Regla Potencia**
```
<factor> ::= <potencia₁> ** <potencia₂>

Semántica:
  <factor>.val = <potencia₁>.val ** <potencia₂>.val

Código 3D:
  temp = nuevo_temporal()
  <factor>.lugar = temp
  <factor>.codigo = <potencia₁>.codigo || 
                    <potencia₂>.codigo || 
                    gen(temp + " = " + <potencia₁>.lugar + " ** " + <potencia₂>.lugar)
```

**Regla Número**
```
<potencia> ::= <NUM>

Semántica:
  <potencia>.val = NUM.valor
  <potencia>.lugar = NUM.valor
  <potencia>.codigo = ε (vacío)
```

**Regla Variable**
```
<potencia> ::= <ID>

Semántica:
  <potencia>.val = TablaSimbolos.buscar(ID.nombre).valor
  <potencia>.lugar = ID.nombre
  <potencia>.codigo = ε (vacío)
```

### Tabla de Símbolos

 - Estructura: nombre, tipo, valor, linea
 - Operaciones: insertar(), buscar(), actualizar()


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
- Codificar las reglas semánticas en los métodos
    
                
  REGLA SEMÁNTICA: NUM.val = NUM.valor
      
            class NodoNumero(NodoAST):
                valor: float
                def evaluar(self, tabla: TablaSimbolos) -> float:
                    return self.valor
                
  REGLA DE TRADUCCIÓN:

  NUM.lugar = NUM.valor
  
  NUM.lugar =NUM.codigo = ε
  
                def generar_codigo(self, generador) -> str:
                    return str(self.valor)
                
  VISUALIZACIÓN:
  
                def imprimir_arbol(self, prefijo="", es_ultimo=True, con_valores=True, tabla=None):
                    conector = "└── " if es_ultimo else "├── "
                    if con_valores:
                        print(f"{prefijo}{conector}NUM: {self.valor} → val={self.valor}")
                    else:
                        print(f"{prefijo}{conector}NUM: {self.valor}")

  
  
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


