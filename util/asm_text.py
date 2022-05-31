from string import Template

tpl_expr_self = """
    move	$a0 $s0     # self"""  # by convention, self is always in s0

tpl_primary_true = """
    la	$a0 bool_const1 	# true"""

tpl_primary_false = """
    la	$a0 bool_const0 	# false"""

tpl_expr_isvoid = Template("""
    la	$$a0 $arg 	# argument in a0
	move	$t1 $$a0 		    # isvoid
	la	$$a0 bool_const1 	    # isvoid
	beqz	$t1 $labelX 	# isvoid
	la	$$a0 bool_const0 	# isvoid""")

tpl_push_param = Template("""
$param_evaluation_code  # places result in param_address
    la      $$param_address
    sw      $$a0    $param_address
    addiu   $sp $sp -4
""")

tpl_before_call = Template(
"""$push_params_code
    move    $$a0 $$s0  # self as first arg
    bne $$a0 $$zero ${dispatch_label_name}
	la	$$a0 ${filename_str}  
	li	$$t1 ${call_line_number}
	jal	_dispatch_abort  # built-in routine""")

tpl_dispatch_label = Template("""
${dispatch_label_name}:
    lw  $$t1 8($$a0)  # dispatch table
    lw  $$t1 ${method_offset}($t1)  # method key -> offset
    jalr    $$t1""")

tpl_return_to_caller = Template("""
	lw	$$fp 12($$sp) 		# m: restore $$fp
	lw	$$s0 8($$sp) 		# m: restore $$s0 (self)
	lw	$$ra 4($$sp) 		# m: restore $$ra
	addiu	$$sp $$sp ${locals_and_formals_bytes} 		# m: restore sp, ${formals_bytes} from formals, ${frame_bytes} from local frame
	jr	$$ra 
""")


# consult notes and Cool Lab