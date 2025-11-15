# Código intermedio

## Como ejecutar:

    python3 codigo_intermedio.py 


### Diseño de la gramática sencilla GIC de python

    sentencia  → ID = expresion | expresion
    expresion  → termino ((+|-) termino)*
    termino    → factor ((*|/|//|%) factor)*
    factor     → potencia (** potencia)*
    potencia   → ( expresion ) | NUM | ID

Precedencia: () > * / > + -

### Definir atributos

| Atributo | Tipo | Descripción |
| :--- | :--- | :--- |
| **.val** | Sintetizado | Valor numérico calculado (float) |
| **.nodo** | Sintetizado | Nodo del AST construido |
| **.nombre** | Sintetizado | Nombre de variable (string) |
| **.izq** | Heredado | Valor acumulado en recursión |
| **.nodo_izq** | Heredado | Nodo acumulado en recursión |

    
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


