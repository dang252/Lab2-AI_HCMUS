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
    return clause_new

def alway_true(clause: list):
    for i in range(len(clause) - 1):
        for j in range(i+1, len(clause)):
            if is_opposite(clause[i], clause[j]):
                return True
    return False

def split_clause(clause: str)->list:
    '''
    Phân tách các clause (chỉ gồm literal và phép OR) thành các literal
    '''
    literals = clause.split(' OR ')
    return literals

def pl_resolve(clause1: list, clause2:list)->list:
    clauses = []
    for i in range(len(clause1)):
        for j in range(len(clause2)):
            if is_opposite(clause1[i], clause2[j]):
                clause1_new = clause1.copy()
                clause1_new.pop(i)
                clause2_new = clause2.copy()
                clause2_new.pop(j)
                clause = clause2_new + clause1_new
                clauses.append(clause)
    return clauses

def pl_resolution(kb: list, alpha: str):
    ''''''
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
            alpha_new.append(list(Not(literal)))
    #đưa các literal mới có được từ việc phân giải alpha vào kb
    for literal in alpha_new:
        if literal not in kb_new:
            kb_new.append(literal)
    
    for i in range(len(kb) - 1):
        for j in range(len(kb)):
            pl_res = pl_resolve(kb[i], kb[j])

def main():
    dirname = os.path.dirname(os.path.abspath(__file__))
    print(dirname)
    path = os.path.join(dirname, 'Testcase', 'Test1','input.txt')
    print(path)
    with open(path, 'r+') as fin:
        alpha = fin.readline().strip()
        n = int(fin.readline())
        kb = []
        for i in range(n):
            kb.append(fin.readline().strip()) 
    pl_resolution(kb,alpha)
    # print(is_opposite('10','9'))
    
 

if __name__ == "__main__":
    main()