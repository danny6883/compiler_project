import sys

A = sys.argv[1]
file = open(A,"rt")
javacode = file.read()
LAcode = ""
file.close

def _isnonzerodigit(i): # 0을 제외한 한자리 숫자인지 확인
    if i=='1' or i=='2' or i=='3' or i=='4' or i=='5' or i=='6' or i=='7' or i=='8' or i=='9':
        return True
    else:
        return False

def _isdigit(i): # 0을 포함한 한자리 숫자인지 확인
    if i=='0' or i=='1' or i=='2' or i=='3' or i=='4' or i=='5' or i=='6' or i=='7' or i=='8' or i=='9':
        return True
    else:
        return False

def _isletter(i): # 한자리 문자인지 확인
    if i.isalpha():
        return True
    return False

def op_or_int(m): # operator일때 False, integer일때 True
    if m == 0 or len(LAcode) == 0:
        return True
    i = LAcode.rfind("<")
    if LAcode[i:].find("IDENTIFIER") == -1 and LAcode[i:].find("INTEGER") == -1 and LAcode[i:].find("CHARACTER") == -1 : # 앞에 오는 토큰이 identifier, integer, character가 아닐때, '-'는 정수 부호가 된다
        return True
    return False

def _integer(): # 정수
    global javacode
    global LAcode
    t = 0
    i = 0
    m = 0 # 음수 판별
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '-' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            m = 1
            continue
        if javacode[i] == '0' and t == 0 : # T0 -> T2
            i = i + 1
            t = 2
            break
        if _isnonzerodigit(javacode[i]) and t == 0 : # T0 -> T3
            i = i + 1
            t = 3
            continue
        if _isnonzerodigit(javacode[i]) and t == 1 : # T1 -> T3
            i = i + 1
            t = 3
            continue
        if _isdigit(javacode[i]) and t == 3: # T3 -> T3
            i = i + 1
            t = 3
            continue
        if (t == 2 or t == 3) and op_or_int(m) : # 문자열의 길이가 남아 탈출하지 않았을 경우, '-'가 연산자로 쓰이지 않은 경우
            LAcode = LAcode + "<INTEGER, "+ javacode[0:i] +">"
            javacode = javacode[i:]
            return True
        return False
    if (t == 2 or t == 3) and op_or_int(m): # 문자열의 길이가 맞아 탈출했을 경우, '-'가 연산자로 쓰이지 않은 경우
        LAcode = LAcode + "<INTEGER, "+ javacode[0:i] +">"
        javacode = javacode[i:]
        return True
    return False    

def _character():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '\'' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if _isdigit(javacode[i]) and t == 1 : # T1 -> T2
            i = i + 1
            t = 2
            continue
        if _isletter(javacode[i]) and t == 1 : # T1 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == ' ' and t == 1 : # T1 -> T4
            i = i + 1
            t = 4
            continue
        if javacode[i] == '\'' and t == 2: # T2 -> T5
            i = i + 1
            t = 5
            break
        if javacode[i] == '\'' and t == 3: # T3 -> T5
            i = i + 1
            t = 5
            break        
        if javacode[i] == '\'' and t == 4: # T4 -> T5
            i = i + 1
            t = 5
            break
        return False
    if t == 5:
        LAcode = LAcode + "<CHARACTER, "+ javacode[0:i] +">"
        javacode = javacode[i:]
        return True
    return False

def _string():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '\"' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if (_isdigit(javacode[i]) or _isletter(javacode[i]) or javacode[i] == ' ' ) and t == 1 : # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == '\"' and t == 1 : # T1 -> T3
            i = i + 1
            t = 3
            break
        if (_isdigit(javacode[i]) or _isletter(javacode[i]) or javacode[i] == ' ' ) and t == 2 : # T2 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == '\"' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            break
        return False
    if t == 3:
        LAcode = LAcode + "<STRING, "+ javacode[0:i] +">"
        javacode = javacode[i:]
        return True
    return False    

def _identifier():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if (javacode[i] == '_' or _isletter(javacode[i]) ) and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if (_isdigit(javacode[i]) or _isletter(javacode[i]) or javacode[i] == '_' ) and t == 1 : # T1 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            LAcode = LAcode + "<IDENTIFIER, "+ javacode[0:i] +">"
            javacode = javacode[i:]
            return True
        return False
    if t == 1:
        LAcode = LAcode + "<IDENTIFIER, "+ javacode[0:i] +">"
        javacode = javacode[i:]
        return True
    return False    

def _compare():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if (javacode[i] == '<' or javacode[i] == '>' ) and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if (javacode[i] == '!' or javacode[i] == '=' ) and t == 0 : # T0 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == '=' and t == 1 : # T1 -> T3
            i = i + 1
            t = 3
            break
        if javacode[i] == '=' and t == 2 : # T2 -> T3
            i = i + 1
            t = 3
            break
        if t == 1 or t == 3:
            LAcode = LAcode + "<COMPARE, "+ javacode[0:i] +" >"
            javacode = javacode[i:]
            return True
        return False
    if t == 1 or t == 3:
        LAcode = LAcode + "<COMPARE, "+ javacode[0:i] +" >"
        javacode = javacode[i:]
        return True
    return False

def _plus():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '+' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<PLUS>"
        javacode = javacode[i:]
        return True
    return False    

def _minus():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '-' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<MINUS>"
        javacode = javacode[i:]
        return True
    return False

def _multifly():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '*' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<MULTIFLY>"
        javacode = javacode[i:]
        return True
    return False    

def _division():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '/' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<DIVISION>"
        javacode = javacode[i:]
        return True
    return False

def _assignment():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '=' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<ASSIGNMENT>"
        javacode = javacode[i:]
        return True
    return False

def _semi():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == ';' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<SEMI>"
        javacode = javacode[i:]
        return True
    return False

def _lbrace():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '{' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<LBRACE>"
        javacode = javacode[i:]
        return True
    return False

def _rbrace():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '}' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<RBRACE>"
        javacode = javacode[i:]
        return True
    return False

def _lparen():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '(' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<LPAREN>"
        javacode = javacode[i:]
        return True
    return False

def _rparen():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == ')' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<RPAREN>"
        javacode = javacode[i:]
        return True
    return False

def _lbracket():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == '[' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<LBRACKET>"
        javacode = javacode[i:]
        return True
    return False

def _rbracket():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == ']' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<RBRACKET>"
        javacode = javacode[i:]
        return True
    return False        

def _comma():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == ',' and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            break
        return False
    if t == 1:
        LAcode = LAcode + "<COMMA>"
        javacode = javacode[i:]
        return True
    return False        

def _whitespace():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if (javacode[i] == '\n' or javacode[i] == '\t' or javacode[i] == ' ') and t == 0 : # T0 -> T1
            i = i + 1
            t = 1
            continue
        if (javacode[i] == '\n' or javacode[i] == '\t' or javacode[i] == ' ') and t == 1 : # T1 -> T1
            i = i + 1
            t = 1
            continue
        if t == 1:
            javacode = javacode[i:]
            return True
        return False
    if t == 1:
        javacode = javacode[i:]
        return True
    return False    


def _isiden(a): # 문자 혹은 숫자 혹은 '-'인지 확인
    if a.isalpha() or a.isdigit() or a == '_':
        return True
    else:
        return False

def _int():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'i' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'n' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 't' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if (not _isiden(javacode[i])) and t == 3: # int를 포함한 identifier인지 판별
            LAcode = LAcode + "<INT>"
            javacode = javacode[i:]
            return True
        return False
    if t == 3:
        LAcode = LAcode + "<INT>"
        javacode = javacode[i:]
        return True
        
def _char():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'c' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'h' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 'a' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 'r' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if (not _isiden(javacode[i])) and t == 4: # char를 포함한 identifier인지 판별
            LAcode = LAcode + "<CHAR>"
            javacode = javacode[i:]
            return True
        return False
    if t == 4:
        LAcode = LAcode + "<CHAR>"
        javacode = javacode[i:]
        return True

def _bool():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'b' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'o' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 'o' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 'l' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if javacode[i] == 'e' and t == 4: # T4 -> T5
            i = i + 1
            t = 5
            continue
        if javacode[i] == 'a' and t == 5: # T5 -> T6
            i = i + 1
            t = 6
            continue
        if javacode[i] == 'n' and t == 6: # T6 -> T7
            i = i + 1
            t = 7
            continue
        if (not _isiden(javacode[i])) and t == 7: # boolean을 포함한 identifier인지 판별
            LAcode = LAcode + "<BOOL>"
            javacode = javacode[i:]
            return True
        return False
    if t == 7:
        LAcode = LAcode + "<BOOL>"
        javacode = javacode[i:]
        return True

def _str():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'S' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 't' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 'r' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 'i' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if javacode[i] == 'n' and t == 4: # T4 -> T5
            i = i + 1
            t = 5
            continue
        if javacode[i] == 'g' and t == 5: # T5 -> T6
            i = i + 1
            t = 6
            continue
        if (not _isiden(javacode[i])) and t == 6: # string을 포함한 identifier인지 판별
            LAcode = LAcode + "<STR>"
            javacode = javacode[i:]
            return True
        return False
    if t == 6:
        LAcode = LAcode + "<STR>"
        javacode = javacode[i:]
        return True

def _boolean():
    global javacode
    global LAcode
    t1 = 0
    t2 = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 't' and t1 == 0: # T0 -> T1
            i = i + 1
            t1 = 1
            continue
        if javacode[i] == 'r' and t1 == 1: # T1 -> T2
            i = i + 1
            t1 = 2
            continue
        if javacode[i] == 'u' and t1 == 2: # T2 -> T3
            i = i + 1
            t1 = 3
            continue
        if javacode[i] == 'e' and t1 == 3: # T3 -> T4
            i = i + 1
            t1 = 4
            continue
        if (not _isiden(javacode[i])) and t1 == 4: # true를 포함한 identifier인지 판별
            LAcode = LAcode + "<BOOLEAN, true>"
            javacode = javacode[i:]
            return True     
        
        if javacode[i] == 'f' and t2 == 0: # true 와 겹치지 않게 t2를 사용 T0 -> T1
            i = i + 1
            t2 = 1
            continue
        if javacode[i] == 'a' and t2 == 1: # T1 -> T2
            i = i + 1
            t2 = 2
            continue
        if javacode[i] == 'l' and t2 == 2: # T2 -> T3
            i = i + 1
            t2 = 3
            continue
        if javacode[i] == 's' and t2 == 3: # T3 -> T4
            i = i + 1
            t2 = 4
            continue
        if javacode[i] == 'e' and t2 == 4: # T4 -> T5
            i = i + 1
            t2 = 5
            continue        
        if (not _isiden(javacode[i])) and t2 == 5: # false를 포함한 identifier인지 판별
            LAcode = LAcode + "<BOOLEAN, false>"
            javacode = javacode[i:]
            return True     
        return False

    if t1 == 4:
        LAcode = LAcode + "<BOOLEAN, true>"
        javacode = javacode[i:]
        return True
    if t2 == 5:
        LAcode = LAcode + "<BOOLEAN, false>"
        javacode = javacode[i:]
        return True    

def _if():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'i' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'f' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if (not _isiden(javacode[i])) and t == 2: # if를 포함한 identifier인지 판별
            LAcode = LAcode + "<IF>"
            javacode = javacode[i:]
            return True
        return False
    if t == 2:
        LAcode = LAcode + "<IF>"
        javacode = javacode[i:]
        return True

def _else():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'e' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'l' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 's' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 'e' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if (not _isiden(javacode[i])) and t == 4: # else를 포함한 identifier인지 판별
            LAcode = LAcode + "<ELSE>"
            javacode = javacode[i:]
            return True
        return False
    if t == 4:
        LAcode = LAcode + "<ELSE>"
        javacode = javacode[i:]
        return True

def _while():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'w' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'h' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 'i' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 'l' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if javacode[i] == 'e' and t == 4: # T4 -> T5
            i = i + 1
            t = 5
            continue        
        if (not _isiden(javacode[i])) and t == 5: # while을 포함한 identifier인지 판별
            LAcode = LAcode + "<WHILE>"
            javacode = javacode[i:]
            return True
        return False
    if t == 5:
        LAcode = LAcode + "<WHILE>"
        javacode = javacode[i:]
        return True

def _class():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'c' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'l' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 'a' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 's' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if javacode[i] == 's' and t == 4: # T4 -> T5
            i = i + 1
            t = 5
            continue        
        if (not _isiden(javacode[i])) and t == 5: # class를 포함한 identifier인지 판별
            LAcode = LAcode + "<CLASS>"
            javacode = javacode[i:]
            return True
        return False
    if t == 5:
        LAcode = LAcode + "<CLASS>"
        javacode = javacode[i:]
        return True        

def _return():
    global javacode
    global LAcode
    t = 0
    i = 0
    while i != len(javacode): # 문자열의 길이가 더 짧을 경우 탈출
        if javacode[i] == 'r' and t == 0: # T0 -> T1
            i = i + 1
            t = 1
            continue
        if javacode[i] == 'e' and t == 1: # T1 -> T2
            i = i + 1
            t = 2
            continue
        if javacode[i] == 't' and t == 2: # T2 -> T3
            i = i + 1
            t = 3
            continue
        if javacode[i] == 'u' and t == 3: # T3 -> T4
            i = i + 1
            t = 4
            continue
        if javacode[i] == 'r' and t == 4: # T4 -> T5
            i = i + 1
            t = 5
            continue
        if javacode[i] == 'n' and t == 5: # T5 -> T6
            i = i + 1
            t = 6
            continue
        if (not _isiden(javacode[i])) and t == 6: # return을 포함한 identifier인지 판별
            LAcode = LAcode + "<RETURN>"
            javacode = javacode[i:]
            return True
        return False
    if t == 6:
        LAcode = LAcode + "<RETURN>"
        javacode = javacode[i:]
        return True

def lexical_analyzer():
    global javacode
    while len(javacode) != 0 :
        if _int():
            continue
        if _char():
            continue
        if _bool():
            continue
        if _str():
            continue
        if _character():
            continue
        if _boolean():
            continue
        if _string():
            continue
        if _if():
            continue
        if _else():
            continue
        if _while():
            continue
        if _class():
            continue
        if _return():
            continue
        if _plus():
            continue
        if _integer():
            continue
        if _minus():
            continue
        if _multifly():
            continue
        if _division():
            continue
        if _compare():
            continue
        if _assignment():
            continue
        if _semi():
            continue
        if _lbrace():
            continue
        if _rbrace():
            continue
        if _lparen():
            continue
        if _rparen():
            continue
        if _lbracket():
            continue
        if _rbracket():
            continue
        if _comma():
            continue
        if _whitespace():
            continue
        if _identifier():
            continue   
        break


print(javacode)
lexical_analyzer()
print(LAcode)

f = open(A + "_output.txt",'w')
f.write(LAcode)
f.close