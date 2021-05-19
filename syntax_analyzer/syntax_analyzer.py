import sys

A = sys.argv[1]
file = open(A,"rt")
LAcode = file.read() # lexical_analyzer의 결과를 input으로 받아 LAcode에 저장합니다
file.close
if len(LAcode) > 1: # LAcodel 에 하나라도 들어있다면 양 끝의 '<', '>'를 없애줍니다
    LAcode = LAcode[1:-1]
SAcode = LAcode.split('><') # '><'를 기준으로 토큰별로 나눠서 SAcode에 저장합니다
SAcode.append('$') # 마지막에 '$' 토큰을 추가합니다
SAcode_save = SAcode[:] # 에러가 발생했을 때 위치를 알려주기 위해 따로 저장을 해둡니다

# SAcode에서 주어진 Terminals로 변환하기 위한 dictionary 자료형입니다
SAcodetoTerminals = {'INT':'vtype',
'CHAR':'vtype',
'STR':'vtype',
'BOOL':'vtype',
'INTEGER':'num',
'CHARACTER':'character',
'BOOLEAN':'boolstr',
'STRING':'literal',
'IDENTIFIER':'id',
'COMPARE':'comp',
'PLUS':'addsub',
'MINUS':'addsub',
'MULTIFLY':'multdiv',
'DIVISION':'multdiv',
'ASSIGNMENT':'assign',
'SEMI':'semi',
'LBRACE':'lbrace',
'RBRACE':'rbrace',
'LPAREN':'lparen',
'RPAREN':'rparen',
# 'LBRACKET':'',
# 'RBRACKET':'',
'COMMA':'comma',
'IF':'if',
'ELSE':'else',
'WHILE':'while',
'CLASS':'class',
'RETURN':'return'}

# '$'가 나오기 전까지 SAcode를 Termials로 변환합니다
for i in range(len(SAcode)-1):
    SAcode[i] = SAcode[i].split(',',1)[0]
    if SAcode[i] in SAcodetoTerminals:
        SAcode[i] = SAcodetoTerminals[SAcode[i]]
    else:
        print('err :' + SAcode[i]) # Terminals로 변환하지 못하는 경우에 에러를 출력해줍니다

# SLR parsing table에 대한 dictionary 자료형입니다
LRtable = {(0,'vtype'):'s5',  
(2,'vtype'):'s5',  
(3,'vtype'):'s5',  
(4,'vtype'):'s5',  
(13,'vtype'):'r5', 
(14,'vtype'):'s19',
(16,'vtype'):'r6', 
(17,'vtype'):'s5', 
(31,'vtype'):'s5', 
(32,'vtype'):'s5', 
(38,'vtype'):'r36',
(41,'vtype'):'s53',
(43,'vtype'):'s55',
(48,'vtype'):'s53',
(49,'vtype'):'r26',
(59,'vtype'):'r27',
(64,'vtype'):'r19',
(75,'vtype'):'s53',
(77,'vtype'):'s53',
(80,'vtype'):'r34',
(81,'vtype'):'r29',
(82,'vtype'):'r28',
(84,'vtype'):'s53',
(86,'vtype'):'r33',

(5,'id'):'s10',
(6,'id'):'s12',
(13,'id'):'r5',
(15,'id'):'s28',
(16,'id'):'r6',
(19,'id'):'s34',
(27,'id'):'s28',
(35,'id'):'s28',
(36,'id'):'s28',
(41,'id'):'s54',
(48,'id'):'s54',
(49,'id'):'r26',
(53,'id'):'s62',
(55,'id'):'s63',
(57,'id'):'s28',
(59,'id'):'r27',
(75,'id'):'s54',
(77,'id'):'s54',
(80,'id'):'r34',
(81,'id'):'r29',
(82,'id'):'r28',
(84,'id'):'s54',
(86,'id'):'r33',

(10,'semi'):'s13',
(11,'semi'):'s16',
(20,'semi'):'r7',
(21,'semi'):'r8',
(22,'semi'):'r9',
(23,'semi'):'r10',
(24,'semi'):'r11',
(25,'semi'):'r13',
(26,'semi'):'r15',
(28,'semi'):'r17',
(29,'semi'):'r18',
(44,'semi'):'r12',
(45,'semi'):'r14',
(46,'semi'):'r16',
(50,'semi'):'s59',
(62,'semi'):'s13',
(65,'semi'):'s71',

(10,'assign'):'s15',
(54,'assign'):'s15',
(62,'assign'):'s15',

(15,'literal'):'s22',
(57,'literal'):'s22',

(15,'character'):'s23',
(57,'character'):'s23',

(15,'boolstr'):'s24',
(57,'boolstr'):'s24',

(25,'addsub'):'s35',
(26,'addsub'):'r15',
(28,'addsub'):'r17',
(29,'addsub'):'r18',
(45,'addsub'):'r14',
(46,'addsub'):'r16',

(26,'multdiv'):'s36',
(28,'multdiv'):'r17',
(29,'multdiv'):'r18',
(46,'multdiv'):'r16',

(10,'lparen'):'s14',
(15,'lparen'):'s27',
(27,'lparen'):'s27',
(35,'lparen'):'s27',
(36,'lparen'):'s27',
(51,'lparen'):'s60',
(52,'lparen'):'s61',
(57,'lparen'):'s27',

(14,'rparen'):'r21',
(18,'rparen'):'s33',
(25,'rparen'):'r13',
(26,'rparen'):'r15',
(28,'rparen'):'r17',
(29,'rparen'):'r18',
(34,'rparen'):'r23',
(37,'rparen'):'s46',
(42,'rparen'):'r20',
(44,'rparen'):'r12',
(45,'rparen'):'r14',
(46,'rparen'):'r16',
(63,'rparen'):'r23',
(66,'rparen'):'s72',
(67,'rparen'):'r31',
(68,'rparen'):'r32',
(69,'rparen'):'s74',
(70,'rparen'):'r22',
(76,'rparen'):'r30',

(15,'num'):'s29',
(27,'num'):'s29',
(35,'num'):'s29',
(36,'num'):'s29',
(57,'num'):'s29',

(12,'lbrace'):'s17',
(33,'lbrace'):'s41',
(72,'lbrace'):'s75',
(74,'lbrace'):'s77',
(83,'lbrace'):'s84',

(13,'rbrace'):'r5',
(16,'rbrace'):'r6',
(17,'rbrace'):'r39',
(30,'rbrace'):'s38',
(31,'rbrace'):'r39',
(32,'rbrace'):'r39',
(39,'rbrace'):'r37',
(40,'rbrace'):'r38',
(41,'rbrace'):'r25',
(48,'rbrace'):'r25',
(49,'rbrace'):'r26',
(56,'rbrace'):'s64',
(58,'rbrace'):'r24',
(59,'rbrace'):'r27',
(64,'rbrace'):'r19',
(71,'rbrace'):'r35',
(75,'rbrace'):'r25',
(77,'rbrace'):'r25',
(78,'rbrace'):'s80',
(79,'rbrace'):'s81',
(80,'rbrace'):'r34',
(81,'rbrace'):'r29',
(82,'rbrace'):'r28',
(84,'rbrace'):'r25',
(85,'rbrace'):'s86',
(86,'rbrace'):'r33',

(34,'comma'):'s43',
(63,'comma'):'s43',

(13,'if'):'r5',
(16,'if'):'r6',
(41,'if'):'s51',
(48,'if'):'s51',
(49,'if'):'r26',
(59,'if'):'r27',
(75,'if'):'s51',
(77,'if'):'s51',
(80,'if'):'r34',
(81,'if'):'r29',
(82,'if'):'r28',
(84,'if'):'s51',
(86,'if'):'r33',

(13,'while'):'r5',
(16,'while'):'r6',
(41,'while'):'s52',
(48,'while'):'s52',
(49,'while'):'r26',
(59,'while'):'r27',
(75,'while'):'s52',
(77,'while'):'s52',
(80,'while'):'r34',
(81,'while'):'r29',
(82,'while'):'r28',
(84,'while'):'s52',
(86,'while'):'r33',

(67,'comp'):'s73',
(68,'comp'):'r32',

(60,'boolst'):'s68',
(61,'boolst'):'s68',
(73,'boolst'):'s68',

(80,'else'):'s83',

(13,'return'):'r5',
(16,'return'):'r6',
(41,'return'):'r25',
(47,'return'):'s57',
(48,'return'):'r25',
(49,'return'):'r26',
(58,'return'):'r24',
(59,'return'):'r27',
(75,'return'):'r25',
(77,'return'):'r25',
(80,'return'):'r34',
(81,'return'):'r29',
(82,'return'):'r28',
(84,'return'):'r25',
(86,'return'):'r33',

(0,'class'):'s6',
(2,'class'):'s6',
(3,'class'):'s6',
(4,'class'):'s6',
(13,'class'):'r5',
(16,'class'):'r6',
(38,'class'):'r36',
(64,'class'):'r19',

(0,'$'):'r4',
(1,'$'):'acc',
(2,'$'):'r4',
(3,'$'):'r4',
(4,'$'):'r4',
(7,'$'):'r1',
(8,'$'):'r2',
(9,'$'):'r3',
(13,'$'):'r5',
(16,'$'):'r6',
(38,'$'):'r36',
(64,'$'):'r19',


(0,'CODE'):'1',
(2,'CODE'):'7',
(3,'CODE'):'8',
(4,'CODE'):'9',

(0,'VDECL'):'2',
(2,'VDECL'):'2',
(3,'VDECL'):'2',
(4,'VDECL'):'2',
(17,'VDECL'):'31',
(31,'VDECL'):'31',
(32,'VDECL'):'31',
(41,'VDECL'):'49',
(48,'VDECL'):'49',
(75,'VDECL'):'49',
(77,'VDECL'):'49',
(84,'VDECL'):'49',

(5,'ASSIGN'):'11',
(41,'ASSIGN'):'50',
(48,'ASSIGN'):'50',
(53,'ASSIGN'):'11',
(75,'ASSIGN'):'50',
(77,'ASSIGN'):'50',
(84,'ASSIGN'):'50',

(15,'RHS'):'20',
(57,'RHS'):'65',

(15,'EXPR'):'21',
(27,'EXPR'):'37',
(35,'EXPR'):'44',
(57,'EXPR'):'21',

(15,'T'):'25',
(27,'T'):'25',
(35,'T'):'25',
(36,'T'):'45',
(57,'T'):'25',

(15,'F'):'26',
(27,'F'):'26',
(35,'F'):'26',
(36,'F'):'26',
(57,'F'):'26',

(0,'FDECL'):'3',
(2,'FDECL'):'3',
(3,'FDECL'):'3',
(4,'FDECL'):'3',
(17,'FDECL'):'32',
(31,'FDECL'):'32',
(32,'FDECL'):'32',

(14,'ARG'):'18',

(34,'MOREARGS'):'42',
(63,'MOREARGS'):'70',

(41,'BLOCK'):'47',
(48,'BLOCK'):'58',
(75,'BLOCK'):'78',
(77,'BLOCK'):'79',
(84,'BLOCK'):'85',

(41,'STMT'):'48',
(48,'STMT'):'48',
(75,'STMT'):'48',
(77,'STMT'):'48',
(84,'STMT'):'48',

(60,'COND'):'66',
(61,'COND'):'69',
(73,'COND'):'76',

(60,'A'):'67',
(61,'A'):'67',
(73,'A'):'67',

(80,'ELSE'):'82',

(47,'RETURN'):'56',

(0,'CDECL'):'4',
(2,'CDECL'):'4',
(3,'CDECL'):'4',
(4,'CDECL'):'4',

(17,'ODECL'):'30',
(31,'ODECL'):'39',
(32,'ODECL'):'40'}

# ambiguity를 없앤 CFG입니다 (''는 ε 입니다)
SLR_grammer = """S -> CODE
CODE -> VDECL CODE
CODE -> FDECL CODE
CODE -> CDECL CODE
CODE -> ''
VDECL -> vtype id semi
VDECL -> vtype ASSIGN semi
ASSIGN -> id assign RHS
RHS -> EXPR
RHS -> literal
RHS -> character
RHS -> boolstr
EXPR -> T addsub EXPR
EXPR -> T
T -> F multdiv T
T -> F
F -> lparen EXPR rparen
F -> id
F -> num
FDECL -> vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace
ARG -> vtype id MOREARGS
ARG -> ''
MOREARGS -> comma vtype id MOREARGS
MOREARGS -> ''
BLOCK -> STMT BLOCK
BLOCK -> ''
STMT -> VDECL
STMT -> ASSIGN semi 
STMT -> if lparen COND rparen lbrace BLOCK rbrace ELSE
STMT -> while lparen COND rparen lbrace BLOCK rbrace
COND -> A comp COND
COND -> A
A -> boolst
ELSE -> else lbrace BLOCK rbrace
ELSE -> ''
RETURN -> return RHS semi
CDECL -> class id lbrace ODECL rbrace 
ODECL -> VDECL ODECL
ODECL -> FDECL ODECL
ODECL -> ''"""

# CFG를 나눠서 저장합니다
SLR_grammer = SLR_grammer.split('\n')
for i in range(len(SLR_grammer)):
    SLR_grammer[i] = SLR_grammer[i].split('->')
    SLR_grammer[i][1] = SLR_grammer[i][1].split()

# syntax analyze
step, state, i = 1, 0, 0 # step: parsing(action) 단계, state: 현재 상태
stack = []
action = '0'
while True:
    # action을 수행합니다
    # action 이 reduce 일 때
    if action[0] == 'r':
        reduce = SLR_grammer[int(action[1:])][1][:] # 여기서 reduce는 action의 CFG에서 -> 뒤에 있는 부분입니다
        if reduce != ["''"]: # reduce가 ε 이 아닐 때 해당하는 stack을 지워줍니다
            if stack[-1] == reduce[-1]:
                stack = stack[:-len(reduce)*2+1]
            else:
                stack = stack[:-len(reduce)*2]
        stack.append(SLR_grammer[int(action[1:])][0]) # CFG에서 -> 앞에 있는 부분을 stack에 추가해줍니다
    # action 이 shift and goto 일 때
    elif action[0] == 's':
        stack.append(SAcode[i]) # SAcode의 첫번째 데이터를 stack으로 옮겨줍니다
        i = i + 1
        state = int(action[1:]) # state를 갱신시키고 stack에 넣어줍니다
        stack.append(state)
    # action 이 accept 일 때
    elif action == 'acc':
        print('accept') # accept를 출력해주고 프로그램이 끝납니다
        break
    # action 이 goto 일 때
    else:
        state = int(action) # state를 갱신시키고 stack에 넣어줍니다
        stack.append(state)

    # 다음 action을 결정합니다
    if stack[-1] == state: # stack의 마지막이 state일 때
        # LRtable에 있으면 action을 갱신합니다
        if (state, SAcode[i]) in LRtable:
            action = LRtable[(state, SAcode[i])]
        # LRtable에 없으면 reject를 출력해주고 에러의 위치와 이유를 알려줍니다
        else:
            print('reject')
            print('에러가 {} 번째 토큰인 <{}> 에서 발생하였습니다'.format(i+1,SAcode_save[i]))
            expect = [] # 에러가 나온 토큰 자리에 기대되는 토큰 배열입니다
            for key_ in LRtable.keys():
                if key_[0]==state:
                    expect.append(key_[1])
            print('<{}> 이 아닌 {} 가 올 것으로 기대됩니다'.format(SAcode_save[i], expect))
            break
    else: # stack의 마지막이 state가 아닐 때
        # LRtable에 있으면 action을 갱신합니다
        if (stack[-2], stack[-1].strip()) in LRtable:
            action = LRtable[(stack[-2], stack[-1].strip())]
        # LRtable에 없으면 reject를 출력해주고 에러의 위치와 이유를 알려줍니다
        else:
            print('reject')
            print('에러가 {} 번째 토큰인 <{}> 에서 발생하였습니다'.format(i+1,SAcode_save[i]))
            expect = [] # 에러가 나온 토큰 자리에 기대되는 토큰 배열입니다
            for key_ in LRtable.keys():
                if key_[0]==stack[-2]:
                    expect.append(key_[1])
            print('<{}> 이 아닌 {} 가 올 것으로 기대됩니다'.format(SAcode_save[i], expect))
            break

    step = step + 1
    # print('{}   {}  {}  {}'.format(step, stack, SAcode[i:], action)) # parsing 과정을 보여줍니다
    