import os

def Not(literal: str):
    if '-' in literal:
        return literal[1:]
    else:
        return '-' + literal

def is_opposite(liteal1: str, literal2: str):
    '''
    Kiểm tra xem liệu 2 leterial truyền vào có đối nghịch nhau không
    '''
    return Not(liteal1) == literal2

def delete_AND(clause: str)->list:
    '''
    xóa And trong các vế, vd từ (A OR B) AND (C OR D) sẽ phân tích thành [A OR B, C OR D]
    '''
    clause_new = clause.split(' AND ')
    for i in range(len(clause_new)):
        if '(' in clause or ')' in clause_new[i]:
            clause_new[i] = clause_new[i].replace("(", "")
            clause_new[i] = clause_new[i].replace(")", "")
    return clause_new

def alway_true(clause: list):
    '''
    Kiểm tra các clause xem chúng có luôn đúng không, vd: A OR B OR -A sẽ luôn đúng
    '''
    for i in range(len(clause) - 1):
        for j in range(i + 1, len(clause)):
            if is_opposite(clause[i], clause[j]):
                return True
    return False

def split_clause(clause: str)->list:
    '''
    Phân tách các clause (chỉ gồm literal và phép OR) thành các một list gồm các literal
    '''
    literals = clause.split(' OR ')
    return literals

def sort_clause(clause: list)->list:
    '''
    Sort các literal (sau khi đã qua hàm split clause) theo thứ tự bảng chữ cái, bỏ qua dấu '-'
    '''
    return sorted(list(set(clause)), key=lambda x:x[-1])

def pl_resolve(clause1: list, clause2: list)->list:
    '''
    Hợp giải 2 clause để trả về danh sách những mệnh đề có thể được phát sinh ra.
    '''
    clauses = []
    for i in range(len(clause1)):
        for j in range(len(clause2)):
            if is_opposite(clause1[i], clause2[j]):
                clause1_new = clause1.copy()
                clause1_new.pop(i)
                clause2_new = clause2.copy()
                clause2_new.pop(j)
                clause = clause2_new + clause1_new
                clauses.append(sort_clause(clause))
    return clauses


def pl_resolution(kb: list, alpha: str, steps: list):
    '''
    Sử dụng hợp giải để trả lời KB có entail alpha hay không
    '''
    entail=False
    #phân tách các vế của KB đã cho thành các mảng gồm toàn literal
    kb_new=[]
    for clause in kb:
        for clause_new in delete_AND(clause):
            kb_new.append(split_clause(clause_new))
    #phân tách các vế của alpha thành các literal và phủ định lại chúng
    alpha_new = []
    for clause in delete_AND(alpha):
        # alpha_new.append(Not(literal) for literal in phan_tach(clause))
        for literal in split_clause(clause):
            alpha_new.append([])
            alpha_new[-1].append((Not(literal)))
    #đưa các literal mới có được từ việc phân giải alpha vào kb
    for literal in alpha_new:
        if literal not in kb_new:
            kb_new.append(literal)
    while True:
        #Tìm trong kb hiện tại có 2 clause nào có thể thực hiện hợp giải được.
        steps.append([])
        is_new_clause = False
        for i in range(len(kb_new) - 1):
            for j in range(i + 1, len(kb_new)):
                pl_res = pl_resolve(kb_new[i], kb_new[j])
                for clause in pl_res:
                    #Nếu mệnh đề mới hợp giải được là luôn đúng thì ta bỏ qua nó
                    if alway_true(clause): continue
                    #Nếu mệnh đề này chưa có trong kb và chưa được tìm thấy trong vòng lặp này thì thêm nó vào danh sách.
                    if clause not in kb_new and clause not in steps[-1]:
                        #is_new_clause sẽ dùng để thể hiện xem trong vòng lặp này có mệnh đề nào mới được tạo ra không.
                        is_new_clause = True
                        steps[-1].append(clause)
                    #Nếu mệnh đề mới này là mệnh đề rỗng, thì ta có thể kết luận được luôn kết quả của bài toán.    
                    if clause==[]: entail = True
        if is_new_clause:
            #Sau khi đã xong vòng lặp ta mới thêm những mệnh đề mới vào kb.
            for clause in steps[-1]:
                kb_new.append(clause)
        else: return False
        if entail: 
            return True

def to_CNF(clause: list) -> str:
    '''
    In clause theo chuẩn CNF
    '''
    res = ""
    if len(clause) == 0:
        res = "{}"
    else:
        res = clause[0]
        for i in range (1, len(clause)):
            res = res + ' OR ' + clause[i]
    return res 

def print_steps(f, steps: list):
    '''
    In kết quả của các bước được lưu trong mảng steps
    '''
    for step in steps:
        f.write(str(len(step)) + '\n')
        for clause in step:
            f.write(to_CNF(clause) + '\n')
            

def main():
    dirname = os.path.dirname(os.path.abspath(__file__))
    for i in range(1,8):
        case = "Test" + str(i)
        in_path = os.path.join(dirname, 'Testcase', case,'input.txt')
        out_path = os.path.join(dirname, 'Testcase', case,'output.txt')
        with open(in_path, 'r+') as fin:
            alpha = fin.readline().strip()
            n = int(fin.readline())
            kb = []
            for i in range(n):
                kb.append(fin.readline().strip())
        steps=[]
        entail = pl_resolution(kb, alpha, steps)
        with open(out_path, 'w') as fout:
            print_steps(fout, steps)
            if entail: fout.write("YES")
            else: fout.write("NO")
 

if __name__ == "__main__":
    main()