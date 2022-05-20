from string import Template

tpl_start_text = """
    .text                                   # INICIA SEGMENTO DE TEXTO (CODIGO)"""

tpl_start_data = """
    .data                                   # INICIA SEGMENTO DE DATOS (VARIABLES)"""

tpl_var_decl = Template("""
$varname:   .word 0                         # variable valor inicial 0""")

tpl_end = """
    li	    $v0     10                      # 10 para terminar la emulación
    syscall"""

tpl_immediate = Template("""
    li      $$a0    $immediate              # Cargar valor inmediato""")

tpl_suma = Template("""
$left
    sw      $$a0    0($$sp)                 # suma: salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)                 # suma: recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4           # suma: pop
    add     $$a0    $$a0        $$t1        # suma: operar""")

tpl_resta = Template("""
$left
    sw      $$a0    0($$sp)                 # resta: salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)                 # resta: recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4           # resta: pop
    sub     $$a0    $$t1        $$a0        # resta: operar""")

tpl_menorque = Template("""
$left
    sw      $$a0    0($$sp)                 # resta: salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)                 # resta: recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4           # resta: pop
    blt     $$t1    $$a0        lt$n        # resta: branch if lt
    li      $$a0    0
    j       label_exit_lt$n
lt$n:
    li      $$a0    1
label_exit_lt$n:
""")

tpl_print_int = Template("""
$prev
	li	    $$v0     1                      # para imprimir enteros
	syscall			                        # imprimir""")

tpl_print_str = Template("""
$prev
	li	    $$v0     4                      # para imprimir cadenas
	syscall			                        # imprimir""")

tpl_var = Template("""
    lw      $$a0        $name               # Usar variable""")

tpl_var_from_stack = Template("""
    lw      $$a0        $offset($$fp)      # Referencia a $name
""")

tpl_asignacion = Template("""
$prev
    sw      $$a0        $name               # Guardar valor""")

tpl_asignacion_from_stack = Template("""
$prev
    sw      $$a0        $offset($$fp)      # Referencia a $name
""")

tpl_string_const_decl = Template("""
$name:      .asciiz $content                # Declaración de string""")

tpl_string_const = Template("""
    la      $$a0        $name               # Cargar dirección de variable""")

tpl_if = Template("""
$prev
    beqz    $$a0        label$n             # if: el predicado es 0?
$stmt_true
label$n:                                    # if: salir""")

tpl_if_else = Template("""
$prev
    beqz    $$a0        label$n             # if-else: el predicado es 0?
$stmt_true
    j       labelexit$n                     # if-else: ir a salir
label$n:                                    # if-else: sentencia else
$stmt_false
labelexit$n:                                # if-else: etiqueta salir""")

tpl_while = Template("""
label_test$n:                               # while: etiqueta inicio
$test
    beqz    $$a0   label_exit$n             # while: el predicado es 0?
$stmt
    j       label_test$n                    # while: regresar al inicio
label_exit$n:                               # while: etiqueta fin while""")

tpl_procedure = Template("""
$name:
    addiu   $$sp    $$sp        -$frame_size  # function $name: recalcular stack
    sw      $$ra    8($$sp)                  # function $name: prolog, salvar ra
    sw      $$fp    4($$sp)                  # function $name: prolog, salvar fp
    addiu   $$fp    $$sp        $frame_size
     
$code
    lw      $$fp    4($$sp)                 # function $name: postlog, restaurar fp
    lw      $$ra    8($$sp)                 # function $name: postlog, restaurar ra
    addiu   $$sp    $$sp        $stack_size # pop de fp, ra, locals, params
    jr      $$ra                            # function $name: regresar a caller""")

tpl_push_arg = """
    sw      $a0    0($sp)                   # call: salvar param en el stack
    addiu   $sp    $sp          -4"""

tpl_call = Template("""
$push_arguments
    jal     $name                           # transfer control!""")

