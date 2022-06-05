from string import Template

# INIT METHODS, RIGHT AFTER .text START
tpl_start_text = """
    .text                                   # INICIA SEGMENTO DE TEXTO (CODIGO)"""

tpl_global_methods = """
	.globl	Main_init 
	.globl	Int_init 
	.globl	String_init 
	.globl	Bool_init 
	.globl	Main.main"""

tpl_object_init = Template("""
${class_name}_init:
	addiu	$$sp $$sp -12 
	sw	$$fp 12($$sp) 
	sw	$$s0 8($$sp) 
	sw	$$ra 4($$sp) 
	addiu	$$fp $$sp 4 
	move	$$s0 $$a0${inherits_init}${init_code}
	move	$$a0 $$s0 
	lw	$$fp 12($$sp) 
	lw	$$s0 8($$sp) 
	lw	$$ra 4($$sp) 
	addiu	$$sp $$sp 12 
	jr	$$ra""")

tpl_parent_init = Template("""
	jal ${parent_name}_init""")


# FEATURES 

tpl_attribute = Template("""
${attribute_subexpr_code}
	sw	$$a0 ${attr_offset}($$s0)""")


# PRIMARY EXPRESSIONS
tpl_expr_self = """
    move	$a0 $s0     # self"""  # by convention, self is in s0

tpl_primary_true = """
    la	$a0 bool_const1 	# true"""

tpl_primary_false = """
    la	$a0 bool_const0 	# false"""

tpl_expr_isvoid = Template("""
    la	$$a0 ${arg_address} 	# argument in a0
	move	$t1 $$a0 		    # isvoid
	la	$$a0 bool_const1 	    # isvoid
	beqz	$$t1 ${label_if_true} 	# isvoid?
	la	$$a0 bool_const0 	# isvoid
${label_if_true}:""")

tpl_primary_int = Template("""
	la	$$a0 ${int_const_name}		# ${int_value}""")


# PROCEDURE PROTOCOL - CALLER
tpl_push_param = Template("""
${param_subexpr_code} 
    sw      $$a0    0($$sp)
    addiu   $$sp $$sp -4""")

tpl_before_call = Template("""
${pushing_params_code}
    move    $$a0 $$s0  # self as first arg
    bne     $$a0 $$zero ${dispatch_label_name}
	la      $$a0 ${filename_str}		# run-time check
	li	    $$t1 ${call_line_number}	# run-time check
	jal     _dispatch_abort  			# run-time check
${dispatch_label_name}:
    lw  $$t1 8($$a0)  # dispatch table
    lw  $$t1 ${method_offset}($t1)  # dict[method] -> offset bytes
    jalr    $$t1""")  # return to caller follows

tpl_return_to_caller = Template("""
	lw	$$fp ${frame_size_bytes}($$sp) 		# m: restore $$fp
	lw	$$s0 ${frame_size_bytes_minus_4}($$sp) 		# m: restore $$s0 (self)
	lw	$$ra ${frame_size_bytes_minus_8}($$sp) 		# m: restore $$ra
	addiu	$$sp $$sp ${frame_and_formals_bytes} 		# m: restore sp, ${formals_bytes} from formals, ${frame_size_bytes} from local frame
	jr	$$ra""")

# PROCEDURE PROTOCOL - CALLEE
tpl_on_enter_callee = Template("""
${class_method_name}:
    addiu	$$sp $$sp -${frame_size_bytes} 			# method: frame size = 12 + size(locals)
	sw	$$fp ${frame_size_bytes}($$sp) 				# method: save $$fp
	sw	$$s0 ${frame_size_bytes_minus_4}($$sp) 		# method: save $$s0 (self)
	sw	$$ra ${frame_size_bytes_minus_8}($$sp) 		# method: save $$ra
	addiu	$$fp $$sp 4 		# method: $$fp points to locals, move back
	move	$$s0 $$a0 		# method: self to $$s0""")  # method body follows


# LET BLOCK
tpl_single_let_decl_default = Template("""
    la  $$a0 ${default_obj}
    sw  $$a0 ${ith_local_offset}($fp) 		# letd: Store default value of ${identifier}
""")  # ith local offset is calculated: (N-i-1) where N total num of vars

tpl_single_let_decl_init = Template("""
    la  $$a0 ${init_val_address}
    sw  $$a0 ${ith_local_offset}($fp) 		# letd: Store initial value of ${identifier}
""")

tpl_let_decl = Template(
"""${let_init_vars}""") 
# prints single let_decl in sequence, init or default

tpl_local_var = Template("""
    lw $$a0  ${ith_local_offset}($fp)    # load [${local_var_name}]""")

# NEW EXPR
tpl_new_expr = Template("""
	la	$$a0 ${class_name}_protObj 	# new: explicit
	jal	Object.copy 
	jal	${class_name}_init""")




# ARITHMETIC

tpl_arith_add_expr = Template("""
${left_subexpr_code}    
	sw	$$a0 0($$sp) 		# arith: push left subexp to the stack
	addiu	$$sp $$sp -4 		# arith
${right_subexpr_code}
	jal	Object.copy         # copy of new Int to a0
	lw	$$s1 4($$sp) 		# arith: pop left subexpr from stack into $$s1
	addiu	$$sp $$sp 4 		# arith
	lw	$$t2 12($$s1) 		# arith: load Int.value of left into t2
	lw	$$t1 12($$a0) 		# arith: load Int.value of right into t1
	add	$$t1 $$t2 $$t1 		# arith
	sw	$$t1 12($$a0) 		# arith: store result into new Int.value""")

