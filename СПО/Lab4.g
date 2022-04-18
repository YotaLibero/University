grammar Lab4;
options 
{language = CSharp3;}

@header
{ using translatorCoursework;}

@members
{
	Emitter emitter; 
	
	public Lab4Parser(ITokenStream input, Emitter emitter): this(input) 
	{
		this.emitter = emitter;
	}
}

public
start_rule: statement*; 

statement : declaration SEMI
	| if
	| while
	| switch
	| assign_exp SEMI
	| dec_or_inc SEMI
	| expression (math_op expression {emitter.AddOperation($math_op.text);})* SEMI;
if	options{greedy=true;}: IF expression_logic (logic_op expression_logic {emitter.AddOperation($logic_op.text);})* {emitter.AddIfLabel(true);} statementblock {emitter.AddIfLabel();} (options{greedy=true;}: ELSE statementblock)?;	

while	: WHILE LPAREN (expression_logic (logic_op expression_logic {emitter.AddOperation($logic_op.text);})* {emitter.AddCycleLabel(false, true);})? {emitter.AddCycleLabel(false, false, true);} RPAREN
         statementblock {emitter.AddCycleLabel(false, false, false, false, true);};

switch	: SWITCH {emitter.AddSwitchLabel(true);} expression {emitter.AddAssignStatement();} LBRACKET (BY const {emitter.AddSwitchLabel(false, true, $const.text);}  ':' statementblock {emitter.AddSwitchLabel(false, false, $const.text);})+ RBRACKET;

assign_exp:	assignment (math_op expression {emitter.AddOperation($math_op.text);})* {emitter.AddAssignStatement();};

declaration  :	 type  x=ID {emitter.AddDeclarationStatement($x.text);} (COMMA y=ID {emitter.AddDeclarationStatement($y.text);})*  
	| TINT z=ID EQUAL INT {emitter.AddDeclarationStatement($z.text, $INT.text, true);}
	| TREAL u=ID EQUAL REAL {emitter.AddDeclarationStatement($u.text, $REAL.text, true);}
	| TCHAR i=ID EQUAL CHAR {emitter.AddDeclarationStatement($i.text, $CHAR.text, true);}
	| TBOOL j=ID EQUAL BOOL {emitter.AddDeclarationStatement($j.text, $BOOL.text, true);};

statementblock:	statement | LBRACKET statement* RBRACKET;

expression options{greedy=true;}: l=ID {emitter.AddLoadID($l.text);}  math_op r=ID {emitter.AddLoadID($r.text);} {emitter.AddOperation($math_op.text);}
	| l=ID {emitter.AddLoadID($l.text);} math_op const {emitter.AddLoadConst($const.text);} {emitter.AddOperation($math_op.text);}
	| l=(INT | REAL | CHAR | QUANC) {emitter.AddLoadConst($l.text);} math_op r=(INT | REAL | CHAR | QUANC) {emitter.AddLoadConst($r.text);} {emitter.AddOperation($math_op.text);}
	| const {emitter.AddLoadConst($const.text);} math_op ID {emitter.AddLoadID($ID.text);} {emitter.AddOperation($math_op.text);}
	| LPAREN expression RPAREN
	| const {emitter.AddLoadConst($const.text);}
	| ID {emitter.AddLoadID($ID.text);}
	;

expression_logic: l=ID {emitter.AddLoadID($l.text);} compare_op r=ID {emitter.AddLoadID($r.text);} {emitter.AddOperation($compare_op.text);}
	|	l=ID {emitter.AddLoadID($l.text);} compare_op const {emitter.AddLoadConst($const.text);} {emitter.AddOperation($compare_op.text);}
	|	l=(INT | REAL | CHAR | QUANC) {emitter.AddLoadConst($l.text);} compare_op r=(INT | REAL | CHAR | QUANC) {emitter.AddLoadConst($r.text);} {emitter.AddOperation($compare_op.text);}
	|	const {emitter.AddLoadConst($const.text);} compare_op r=ID {emitter.AddLoadID($r.text);} {emitter.AddOperation($compare_op.text);}
	|	LPAREN expression_logic RPAREN
	|	ID {emitter.AddLoadID($ID.text);}
	| 	const{emitter.AddLoadConst($const.text);}
	;

assignment : ID {emitter.AddLValue($ID.text);} EQUAL expression;

type	:	TINT | TREAL | TCHAR | TBOOL;

const : INT | REAL | CHAR | QUANC;

dec_or_inc :	ID y=(INC|DEC) {emitter.AddDecOrInc($ID.text, $y.text);}
	| x=(INC|DEC) ID {emitter.AddDecOrInc($ID.text, $x.text);};

compare_op: GT | GE | LT | LE | EQ | NE;

math_op: MINUS|PLUS|MUL|DIV;

logic_op: AND|OR;

	   
IF	:	'if';
ELSE 	:	'else';
WHILE 	:	'while';
SWITCH 	:	'switch';
BY	:	'by';

TINT	:	'int';
TREAL	:	'real';
TCHAR	:	'char' | 'chara' | 'charac' | 'charact' | 'characte' | 'character';
TBOOL	:	'bool';

AND	:	'&&';
OR	:	'||';
INC 	:	'++';
DEC	:	'--';

MUL  : '*' ;
DIV   : '/' ;
PLUS  : '+' ;
MINUS : '-' ;

GT : '>' ;
GE : '>=' ;
LT : '<' ;
LE : '<=' ;
EQ : '==' ;
NE : '!=' ;

LBRACKET : '{' ;
RBRACKET : '}' ;
LPAREN : '(' ;
RPAREN : ')' ;
SEMI : ';';
EQUAL	:	'=';
COMMA	:	',';

ID  :	('a'..'z'|'A'..'Z')+ ('0'..'9');
INT :	'0'..'9'+;
REAL:   ('0'..'9')+ '.' ('0'..'9')* EXPONENT? |   '.' ('0'..'9')+ EXPONENT? |   ('0'..'9')+ EXPONENT;
WS  :   ( ' ' | '\t' | '\r' | '\n') {$channel=HIDDEN;};
CHAR:  '\'' ( ESC_SEQ | ~('\''|'\\') ) '\'';
BOOL	:	'yes' | 'no';
QUANC: 'F' '1'..'3'+ '0'*;

fragment
EXPONENT : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;
fragment
HEX_DIGIT : ('0'..'9'|'a'..'f'|'A'..'F') ;
fragment
ESC_SEQ:   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\') |   UNICODE_ESC |   OCTAL_ESC;
fragment
OCTAL_ESC:   '\\' ('0'..'3') ('0'..'7') ('0'..'7') |   '\\' ('0'..'7') ('0'..'7') |   '\\' ('0'..'7');
fragment
UNICODE_ESC:   '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT;


