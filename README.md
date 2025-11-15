# Código intermedio

## Como ejecutar:

    python3 codigo_intermedio.py 


### Diseño de la gramática sencilla GIC de python

    sentencia  → ID = expresion | expresion
    expresion  → termino ((+|-) termino)*
    termino    → factor ((*|/|//|%) factor)*
    factor     → potencia (** potencia)*
    potencia   → ( expresion ) | NUM | ID

 Precedencia:

1. ( )          (mayor precedencia)
2. **           (exponenciación - asociativa a la derecha)
3. *, /, //, %  (multiplicación, división)
4. +, -         (suma, resta - menor precedencia)

### Definir atributos

Todos los atributos son **sintetizados** (se calculan de abajo hacia arriba en el árbol):

| **No Terminal** | **Atributo** | **Tipo** | **Descripción** |
| :--- | :--- | :--- | :--- |
| `<sentencia>` | `.val` | `float` | Valor evaluado de la sentencia |
| `<sentencia>` | `.codigo` | `string` | Código de 3 direcciones generado |
| `<sentencia>` | `.lugar` | `string` | Variable/temporal que contiene el resultado |
| `<expresion>` | `.val` | `float` | Valor de la expresión |
| `<expresion>` | `.codigo` | `string` | Código de 3 direcciones |
| `<expresion>` | `.lugar` | `string` | Temporal con el resultado |
| `<termino>` | `.val` | `float` | Valor del término |
| `<termino>` | `.codigo` | `string` | Código de 3 direcciones |
| `<termino>` | `.lugar` | `string` | Temporal con el resultado |
| `<factor>` | `.val` | `float` | Valor del factor |
| `<factor>` | `.codigo` | `string` | Código de 3 direcciones |
| `<factor>` | `.lugar` | `string` | Temporal con el resultado |
| `<potencia>` | `.val` | `float` | Valor de la potencia |
| `<potencia>` | `.lugar` | `string` | Nombre de variable o valor |

**REGLAS SEMÁNTICAS Y DE TRADUCCIÓN**

### **Regla 1: Asignación**
```
<sentencia> ::= <ID> = <expresion>

Semántica:
  <sentencia>.val = <expresion>.val
  TablaSimbolos.insertar(ID.nombre, <expresion>.val)

Código 3D:
  <sentencia>.codigo = <expresion>.codigo || 
                       gen(ID.nombre + " = " + <expresion>.lugar)
```

### **Regla 2: Expresión Suma/Resta**
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

### **Regla 3: Término Multiplicación/División**
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

### **Regla 4: Potencia**
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

### **Regla 5: Número**
```
<potencia> ::= <NUM>

Semántica:
  <potencia>.val = NUM.valor
  <potencia>.lugar = NUM.valor
  <potencia>.codigo = ε (vacío)
```

### **Regla 6: Variable**
```
<potencia> ::= <ID>

Semántica:
  <potencia>.val = TablaSimbolos.buscar(ID.nombre).valor
  <potencia>.lugar = ID.nombre
  <potencia>.codigo = ε (vacío)
```
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


