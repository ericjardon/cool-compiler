grammar cool;           

program
    : ( klass ';' ) *
    ;

klass
    : KLASS TYPE ( 'inherits' TYPE )? '{' ( feature ';' )* '}'
    ;

feature
    : ID '(' ( params+=formal (',' params+=formal)* )? ')' ':' TYPE '{' expr '}' #feature_function
    | ID ':' TYPE ( '<-' expr )? #feature_attribute
    ;

formal
    : ID ':' TYPE
    ;

expr
    :
    primary  # primary_expr
    | ID '(' ( params+=expr ( ',' params+=expr)* )? ')'  # method_call
    | IF expr THEN expr ELSE expr FI  # if_else
    | WHILE expr LOOP expr POOL  # while
    | expr '.' ID '(' ( params+=expr  ( ',' params+=expr)* )? ')'  # dispatch
    | LET let_decl ( ',' let_decl )* IN expr  # let_expr
    | CASE expr OF (case_stat)+ ESAC  # case_expr
    | NEW TYPE  # new
    | '{' ( expr ';' )+ '}'  # block
    | expr ( '@' TYPE )? '.' ID '(' ( params+=expr  ( ',' params+=expr)* )? ')'  #static_dispatch
    | '˜' expr  # number_egation
    | ISVOID expr  # isvoid
    | expr '*' expr  # multiplication
    | expr '/' expr  # division
    | expr '+' expr  # addition
    | expr '-' expr  # subtraction
    | expr '<' expr  # less_than
    | expr '<=' expr # less_or_equal 
    | expr '=' expr  # equals
    | 'not' expr  # not
    | <assoc=right> ID '<-' expr  #assignment
    ;

case_stat:
    ID ':' TYPE '=>' expr ';'
    ;

let_decl:
    ID ':' TYPE ('<-' expr )?
    ;

primary:
    '(' expr ')'
    | ID
    | INTEGER
    | STRING
    | TRUE
    | FALSE
    ;

fragment A : [aA] ;
fragment B : [bB] ;
fragment C : [cC] ;
fragment D : [dD] ;
fragment E : [eE] ;
fragment F : [fF] ;
fragment G : [gG] ;
fragment H : [hH] ;
fragment I : [iI] ;
fragment J : [jJ] ;
fragment K : [kK] ;
fragment L : [lL] ;
fragment M : [mM] ;
fragment N : [nN] ;
fragment O : [oO] ;
fragment P : [pP] ;
fragment Q : [qQ] ;
fragment R : [rR] ;
fragment S : [sS] ;
fragment T : [tT] ;
fragment U : [uU] ;
fragment V : [vV] ;
fragment W : [wW] ;
fragment X : [xX] ;
fragment Y : [yY] ;
fragment Z : [zZ] ;

KLASS : C L A S S ;
FI : F I ;
IF : I F ;
IN : I N ;
INHERITS : I N H E R I T S;
ISVOID : I S V O I D;
LET : L E T;
LOOP : L O O P;
POOL : P O O L;
THEN : T H E N;
ELSE : E L S E;
WHILE : W H I L E;
CASE : C A S E;
ESAC : E S A C;
NEW : N E W; 
OF : O F;
NOT : N O T;
TRUE : 't' R U E;
FALSE : 'f' A L S E;

TYPE: [A-Z][_a-zA-Z0-9]* ;
ID: [a-z][_a-zA-Z0-9]* ;
INTEGER : [0-9]+ ;
STRING  : '"' .*? '"' ;

COMMENT : '(*' .*? '*)' -> skip ;
LINE_COMENT : '--' ~[\r\n]* -> skip ;
WS : [ \r\t\u000C\n]+ -> skip ;

