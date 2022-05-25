	.data	 
	.align	2 
	.globl	class_nameTab 
	.globl	Main_protObj 
	.globl	Int_protObj 
	.globl	String_protObj 
	.globl	bool_const0 
	.globl	bool_const1 
	.globl	_int_tag 
	.globl	_bool_tag 
	.globl	_string_tag 
_int_tag:
	.word	2 
_bool_tag:
	.word	3 
_string_tag:
	.word	4 
	.globl	_MemMgr_INITIALIZER 
_MemMgr_INITIALIZER:
	.word	_NoGC_Init 
	.globl	_MemMgr_COLLECTOR 
_MemMgr_COLLECTOR:
	.word	_NoGC_Collect 
	.globl	_MemMgr_TEST 
_MemMgr_TEST:
	.word	0 
	.word	-1
str_const14:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const2
	.byte	0	
	.align	2
	.word	-1
str_const13:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const3
	.ascii	"Main"
	.byte	0	
	.align	2
	.word	-1
str_const12:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const3
	.ascii	"Bazz"
	.byte	0	
	.align	2
	.word	-1
str_const11:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const3
	.ascii	"Razz"
	.byte	0	
	.align	2
	.word	-1
str_const10:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const4
	.ascii	"Bar"
	.byte	0	
	.align	2
	.word	-1
str_const9:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const4
	.ascii	"Foo"
	.byte	0	
	.align	2
	.word	-1
str_const8:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const5
	.ascii	"String"
	.byte	0	
	.align	2
	.word	-1
str_const7:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const3
	.ascii	"Bool"
	.byte	0	
	.align	2
	.word	-1
str_const6:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const4
	.ascii	"Int"
	.byte	0	
	.align	2
	.word	-1
str_const5:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const0
	.ascii	"IO"
	.byte	0	
	.align	2
	.word	-1
str_const4:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const5
	.ascii	"Object"
	.byte	0	
	.align	2
	.word	-1
str_const3:
	.word	4
	.word	7
	.word	String_dispTab
	.word	int_const6
	.ascii	"do nothing"
	.byte	0	
	.align	2
	.word	-1
str_const2:
	.word	4
	.word	8
	.word	String_dispTab
	.word	int_const7
	.ascii	"<basic class>"
	.byte	0	
	.align	2
	.word	-1
str_const1:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const1
	.ascii	"\n"
	.byte	0	
	.align	2
	.word	-1
str_const0:
	.word	4
	.word	8
	.word	String_dispTab
	.word	int_const8
	.ascii	"--filename--"
	.byte	0	
	.align	2
	.word	-1
int_const8:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	12
	.word	-1
int_const7:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	13
	.word	-1
int_const6:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	10
	.word	-1
int_const5:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	6
	.word	-1
int_const4:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	3
	.word	-1
int_const3:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	4
	.word	-1
int_const2:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	0
	.word	-1
int_const1:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	1
	.word	-1
int_const0:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	2
	.word	-1
bool_const0:
	.word	3
	.word	4
	.word	Bool_dispTab
	.word	0
	.word	-1
bool_const1:
	.word	3
	.word	4
	.word	Bool_dispTab
	.word	1
class_nameTab:
	.word	str_const4
	.word	str_const5
	.word	str_const6
	.word	str_const7
	.word	str_const8
	.word	str_const9
	.word	str_const10
	.word	str_const11
	.word	str_const12
	.word	str_const13
class_objTab:
	.word	Object_protObj 
	.word	Object_init 
	.word	IO_protObj 
	.word	IO_init 
	.word	Int_protObj 
	.word	Int_init 
	.word	Bool_protObj 
	.word	Bool_init 
	.word	String_protObj 
	.word	String_init 
	.word	Foo_protObj 
	.word	Foo_init 
	.word	Bar_protObj 
	.word	Bar_init 
	.word	Razz_protObj 
	.word	Razz_init 
	.word	Bazz_protObj 
	.word	Bazz_init 
	.word	Main_protObj 
	.word	Main_init 
Object_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
IO_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
Int_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
Bool_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
String_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	String.length
	.word	String.concat
	.word	String.substr
Foo_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
	.word	Bazz.printh
	.word	Foo.doh
Bar_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
	.word	Bazz.printh
	.word	Foo.doh
Razz_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
	.word	Bazz.printh
	.word	Foo.doh
Bazz_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
	.word	Bazz.printh
	.word	Bazz.doh
Main_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	Main.main
	.word	-1 
Object_protObj:
	.word	0 
	.word	3 
	.word	Object_dispTab 
	.word	-1 
IO_protObj:
	.word	1 
	.word	3 
	.word	IO_dispTab 
	.word	-1 
Int_protObj:
	.word	2 
	.word	4 
	.word	Int_dispTab 
	.word	0 
	.word	-1 
Bool_protObj:
	.word	3 
	.word	4 
	.word	Bool_dispTab 
	.word	0 
	.word	-1 
String_protObj:
	.word	4 
	.word	5 
	.word	String_dispTab 
	.word	int_const2 
	.word	0 
	.word	-1 
Foo_protObj:
	.word	5 
	.word	8 
	.word	Foo_dispTab 
	.word	int_const2 
	.word	0 
	.word	0 
	.word	0 
	.word	int_const2 
	.word	-1 
Bar_protObj:
	.word	6 
	.word	12 
	.word	Bar_dispTab 
	.word	int_const2 
	.word	0 
	.word	0 
	.word	0 
	.word	int_const2 
	.word	0 
	.word	int_const2 
	.word	int_const2 
	.word	0 
	.word	-1 
Razz_protObj:
	.word	7 
	.word	10 
	.word	Razz_dispTab 
	.word	int_const2 
	.word	0 
	.word	0 
	.word	0 
	.word	int_const2 
	.word	0 
	.word	int_const2 
	.word	-1 
Bazz_protObj:
	.word	8 
	.word	6 
	.word	Bazz_dispTab 
	.word	int_const2 
	.word	0 
	.word	0 
	.word	-1 
Main_protObj:
	.word	9 
	.word	7 
	.word	Main_dispTab 
	.word	0 
	.word	0 
	.word	0 
	.word	0 
	.globl	heap_start 
heap_start:
	.word	0 
	.text	 
	.globl	Main_init 
	.globl	Int_init 
	.globl	String_init 
	.globl	Bool_init 
	.globl	Main.main 
Object_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
IO_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Object_init 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Int_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Object_init 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Bool_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Object_init 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
String_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Object_init 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Foo_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Bazz_init 
	move	$a0 $s0 
	bne	$a0 $zero label1 	# case: protect from case on void
	la	$a0 str_const0 
	li	$t1 -1 			# case: line number
	jal	_case_abort2 
label1:
	lw	$t1 0($a0) 		# case: load obj tag
	blt	$t1 6 label2 		# case: Bar min
	bgt	$t1 6 label2 		# case: Bar max
	sw	$a0 -4($fp) 		# case: save value on local [n]
	lw	$a0 -4($fp) 		# load [n], class cool.structure.Local
	b	label0 			# case: go to end
label2:
	blt	$t1 6 label3 		# case: Razz min
	bgt	$t1 7 label3 		# case: Razz max
	sw	$a0 -8($fp) 		# case: save value on local [n]
	la	$a0 Bar_protObj 	# new: explicit
	jal	Object.copy 
	jal	Bar_init 
	b	label0 			# case: go to end
label3:
	blt	$t1 5 label4 		# case: Foo min
	bgt	$t1 7 label4 		# case: Foo max
	sw	$a0 -12($fp) 		# case: save value on local [n]
	la	$a0 Razz_protObj 	# new: explicit
	jal	Object.copy 
	jal	Razz_init 
	b	label0 			# case: go to end
label4:
	jal	_case_abort 		# case: default
label0:
	sw	$a0 24($s0) 
	lw	$a0 24($s0) 		# load [a], class cool.structure.Attribute
	bne	$a0 $zero label6 	# at: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 10 			# at: line number
	jal	_dispatch_abort 
label6:
	lw	$t1 8($a0) 		# at: find dispatch table
	lw	$t1 32($t1) 		# at: Foo.doh is at offset 8
	jalr	$t1 
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	lw	$a0 16($s0) 		# load [g], class cool.structure.Attribute
	bne	$a0 $zero label7 	# at: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 10 			# at: line number
	jal	_dispatch_abort 
label7:
	lw	$t1 8($a0) 		# at: find dispatch table
	lw	$t1 32($t1) 		# at: Foo.doh is at offset 8
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	move	$a0 $s0 
	bne	$a0 $zero label8 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 10 			# call: line number
	jal	_dispatch_abort 
label8:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 32($t1) 		# call: method doh is offset 8
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	move	$a0 $s0 
	bne	$a0 $zero label9 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 10 			# call: line number
	jal	_dispatch_abort 
label9:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 28($t1) 		# call: method printh is offset 7
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 28($s0) 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Bar_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Razz_init 
	move	$a0 $s0 
	bne	$a0 $zero label10 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 18 			# call: line number
	jal	_dispatch_abort 
label10:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 32($t1) 		# call: method doh is offset 8
	jalr	$t1 
	sw	$a0 40($s0) 
	move	$a0 $s0 
	bne	$a0 $zero label11 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 20 			# call: line number
	jal	_dispatch_abort 
label11:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 28($t1) 		# call: method printh is offset 7
	jalr	$t1 
	sw	$a0 44($s0) 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Razz_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Foo_init 
	move	$a0 $s0 
	bne	$a0 $zero label13 	# case: protect from case on void
	la	$a0 str_const0 
	li	$t1 -1 			# case: line number
	jal	_case_abort2 
label13:
	lw	$t1 0($a0) 		# case: load obj tag
	blt	$t1 6 label14 		# case: Bar min
	bgt	$t1 6 label14 		# case: Bar max
	sw	$a0 -16($fp) 		# case: save value on local [n]
	lw	$a0 -16($fp) 		# load [n], class cool.structure.Local
	b	label12 		# case: go to end
label14:
	blt	$t1 6 label15 		# case: Razz min
	bgt	$t1 7 label15 		# case: Razz max
	sw	$a0 -20($fp) 		# case: save value on local [n]
	la	$a0 Bar_protObj 	# new: explicit
	jal	Object.copy 
	jal	Bar_init 
	b	label12 		# case: go to end
label15:
	jal	_case_abort 		# case: default
label12:
	sw	$a0 32($s0) 
	lw	$a0 24($s0) 		# load [a], class cool.structure.Attribute
	bne	$a0 $zero label17 	# at: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 31 			# at: line number
	jal	_dispatch_abort 
label17:
	la	$t1 Bazz_dispTab 	# at: static dispatch
	lw	$t1 32($t1) 		# at: Bazz.doh is at offset 8
	jalr	$t1 
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	lw	$a0 16($s0) 		# load [g], class cool.structure.Attribute
	bne	$a0 $zero label18 	# at: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 31 			# at: line number
	jal	_dispatch_abort 
label18:
	lw	$t1 8($a0) 		# at: find dispatch table
	lw	$t1 32($t1) 		# at: Foo.doh is at offset 8
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	lw	$a0 32($s0) 		# load [e], class cool.structure.Attribute
	bne	$a0 $zero label19 	# at: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 31 			# at: line number
	jal	_dispatch_abort 
label19:
	lw	$t1 8($a0) 		# at: find dispatch table
	lw	$t1 32($t1) 		# at: Foo.doh is at offset 8
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	move	$a0 $s0 
	bne	$a0 $zero label20 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 31 			# call: line number
	jal	_dispatch_abort 
label20:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 32($t1) 		# call: method doh is offset 8
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	move	$a0 $s0 
	bne	$a0 $zero label21 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 31 			# call: line number
	jal	_dispatch_abort 
label21:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 28($t1) 		# call: method printh is offset 7
	jalr	$t1 
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 36($s0) 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Bazz_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	IO_init 
	la	$a0 int_const1 		# 1
	sw	$a0 12($s0) 
	move	$a0 $s0 
	bne	$a0 $zero label23 	# case: protect from case on void
	la	$a0 str_const0 
	li	$t1 -1 			# case: line number
	jal	_case_abort2 
label23:
	lw	$t1 0($a0) 		# case: load obj tag
	blt	$t1 6 label24 		# case: Bar min
	bgt	$t1 6 label24 		# case: Bar max
	sw	$a0 -24($fp) 		# case: save value on local [n]
	lw	$a0 -24($fp) 		# load [n], class cool.structure.Local
	b	label22 		# case: go to end
label24:
	blt	$t1 6 label25 		# case: Razz min
	bgt	$t1 7 label25 		# case: Razz max
	sw	$a0 -28($fp) 		# case: save value on local [n]
	la	$a0 Bar_protObj 	# new: explicit
	jal	Object.copy 
	jal	Bar_init 
	b	label22 		# case: go to end
label25:
	blt	$t1 5 label26 		# case: Foo min
	bgt	$t1 7 label26 		# case: Foo max
	sw	$a0 -32($fp) 		# case: save value on local [n]
	la	$a0 Razz_protObj 	# new: explicit
	jal	Object.copy 
	jal	Razz_init 
	b	label22 		# case: go to end
label26:
	blt	$t1 5 label27 		# case: Bazz min
	bgt	$t1 8 label27 		# case: Bazz max
	sw	$a0 -36($fp) 		# case: save value on local [n]
	la	$a0 Foo_protObj 	# new: explicit
	jal	Object.copy 
	jal	Foo_init 
	b	label22 		# case: go to end
label27:
	jal	_case_abort 		# case: default
label22:
	sw	$a0 16($s0) 
	move	$a0 $s0 
	bne	$a0 $zero label29 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 46 			# call: line number
	jal	_dispatch_abort 
label29:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 28($t1) 		# call: method printh is offset 7
	jalr	$t1 
	sw	$a0 20($s0) 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Main_init:
	addiu	$sp $sp -12 
	sw	$fp 12($sp) 
	sw	$s0 8($sp) 
	sw	$ra 4($sp) 
	addiu	$fp $sp 4 
	move	$s0 $a0 
	jal	Object_init 
	la	$a0 Bazz_protObj 	# new: explicit
	jal	Object.copy 
	jal	Bazz_init 
	sw	$a0 12($s0) 
	la	$a0 Foo_protObj 	# new: explicit
	jal	Object.copy 
	jal	Foo_init 
	sw	$a0 16($s0) 
	la	$a0 Razz_protObj 	# new: explicit
	jal	Object.copy 
	jal	Razz_init 
	sw	$a0 20($s0) 
	la	$a0 Bar_protObj 	# new: explicit
	jal	Object.copy 
	jal	Bar_init 
	sw	$a0 24($s0) 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Foo.doh:
	addiu	$sp $sp -16 		# m: frame has 1 locals
	sw	$fp 16($sp) 		# m: save $fp
	sw	$s0 12($sp) 		# m: save $s0 (self)
	sw	$ra 8($sp) 		# m: save $ra
	addiu	$fp $sp 4 		# m: $fp points to locals
	move	$s0 $a0 		# m: self to $s0
	lw	$a0 12($s0) 		# load [h], class cool.structure.Attribute
	sw	$a0 -36($fp) 		# letd: Store initial value of i
	lw	$a0 12($s0) 		# load [h], class cool.structure.Attribute
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	la	$a0 int_const0 		# 2
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 12($s0) 		# assignment of h
	lw	$a0 -36($fp) 		# load [i], class cool.structure.Local
	lw	$fp 16($sp) 		# m: restore $fp
	lw	$s0 12($sp) 		# m: restore $s0 (self)
	lw	$ra 8($sp) 		# m: restore $ra
	addiu	$sp $sp 16 		# m: restore sp, 0 from formals, 16 from local frame
	jr	$ra 
Bazz.printh:
	addiu	$sp $sp -12 		# m: frame has 0 locals
	sw	$fp 12($sp) 		# m: save $fp
	sw	$s0 8($sp) 		# m: save $s0 (self)
	sw	$ra 4($sp) 		# m: save $ra
	addiu	$fp $sp 4 		# m: $fp points to locals
	move	$s0 $a0 		# m: self to $s0
	lw	$a0 12($s0) 		# load [h], class cool.structure.Attribute
	sw	$a0 0($sp) 		# call: Push parameter
	addiu	$sp $sp -4 
	move	$a0 $s0 
	bne	$a0 $zero label30 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 48 			# call: line number
	jal	_dispatch_abort 
label30:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 16($t1) 		# call: method out_int is offset 4
	jalr	$t1 
	la	$a0 int_const2 		# 0
	lw	$fp 12($sp) 		# m: restore $fp
	lw	$s0 8($sp) 		# m: restore $s0 (self)
	lw	$ra 4($sp) 		# m: restore $ra
	addiu	$sp $sp 12 		# m: restore sp, 0 from formals, 12 from local frame
	jr	$ra 
Bazz.doh:
	addiu	$sp $sp -16 		# m: frame has 1 locals
	sw	$fp 16($sp) 		# m: save $fp
	sw	$s0 12($sp) 		# m: save $s0 (self)
	sw	$ra 8($sp) 		# m: save $ra
	addiu	$fp $sp 4 		# m: $fp points to locals
	move	$s0 $a0 		# m: self to $s0
	lw	$a0 12($s0) 		# load [h], class cool.structure.Attribute
	sw	$a0 0($fp) 		# letd: Store initial value of i
	lw	$a0 12($s0) 		# load [h], class cool.structure.Attribute
	sw	$a0 0($sp) 		# ar: keep left subexp in the stack
	addiu	$sp $sp -4 		# ar
	la	$a0 int_const1 		# 1
	jal	Object.copy 
	lw	$s1 4($sp) 		# ar: get saved value from the stack
	addiu	$sp $sp 4 		# ar
	lw	$t2 12($s1) 		# ar
	lw	$t1 12($a0) 		# ar
	add	$t1 $t2 $t1 		# ar
	sw	$t1 12($a0) 		# ar
	sw	$a0 12($s0) 		# assignment of h
	lw	$a0 0($fp) 		# load [i], class cool.structure.Local
	lw	$fp 16($sp) 		# m: restore $fp
	lw	$s0 12($sp) 		# m: restore $s0 (self)
	lw	$ra 8($sp) 		# m: restore $ra
	addiu	$sp $sp 16 		# m: restore sp, 0 from formals, 16 from local frame
	jr	$ra 
Main.main:
	addiu	$sp $sp -12 		# m: frame has 0 locals
	sw	$fp 12($sp) 		# m: save $fp
	sw	$s0 8($sp) 		# m: save $s0 (self)
	sw	$ra 4($sp) 		# m: save $ra
	addiu	$fp $sp 4 		# m: $fp points to locals
	move	$s0 $a0 		# m: self to $s0
	la	$a0 str_const3 
	lw	$fp 12($sp) 		# m: restore $fp
	lw	$s0 8($sp) 		# m: restore $s0 (self)
	lw	$ra 4($sp) 		# m: restore $ra
	addiu	$sp $sp 12 		# m: restore sp, 0 from formals, 12 from local frame
	jr	$ra 
