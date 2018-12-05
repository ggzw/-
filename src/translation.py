
#读取数据
import pickle
def load_obj(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

all_hz = load_obj("../data/all_hz.pkl")
dict_hznum = load_obj("../data/dict_hznum.pkl")
two_hznum = load_obj("../data/two_hznum.pkl")
total_num = pickle.load(open('../data/total_num.txt', 'rb')) 
py_2_hz = load_obj("../data/py_2_hz.pkl")


class Node():
    def __init__(self,hz):
        self.hz = hz
        self.p = 0
        self.pre_node = None
class Sen_nodes():
    def __init__(self,pys):
        self.levels = []
        for py in pys:
            level = []
            hz_list = py_2_hz[py.lower()]
            for hz in hz_list:
                code = all_hz.index(hz)
                node = Node(hz)
                level.append(node)
            self.levels.append(level)
            
def dynamic(sen_nodes, lamda):
    #print("begin dynamic")
    for py_i in range(len(sen_nodes.levels)):  
        if py_i == 0:
            for node in sen_nodes.levels[py_i]:           
                code = all_hz.index(node.hz)
                node.p = dict_hznum[code]/total_num

        else:
            for node in sen_nodes.levels[py_i]:  
                #print(node.hz)
                code = all_hz.index(node.hz)
                probs = []
                for pre_node in sen_nodes.levels[py_i-1]:
                    #print(pre_node.hz)
                    pre_code = all_hz.index(pre_node.hz)
                    if dict_hznum[pre_code]==0:
                        p = 0
                    else:
                        p = two_hznum[pre_code][code]/dict_hznum[pre_code]
                        p = p*lamda+(1-lamda)*dict_hznum[pre_code]/total_num
                    probs.append(p*pre_node.p)
                node.p = max(probs)
                node.pre_node = sen_nodes.levels[py_i-1][probs.index(node.p)]

    return sen_nodes

def path(sen_nodes): 
    i = len(sen_nodes.levels)
    prob = []
    result = []
    for node in sen_nodes.levels[i-1]:
        prob.append(node.p)
    max_index = prob.index(max(prob))
    node = sen_nodes.levels[i-1][max_index]          
    while True:
        result.append(node.hz)
        node = node.pre_node
        if node is None:
            break
    real_result = ''
    while len(result)>0:
        real_result += result.pop()
    return real_result

#拼音转化成汉字
lamda = 0.9999
def test(test_file_path,output_file_path):
    print("begin translation")
    test = open(test_file_path,encoding='gbk')
    output = open(output_file_path,'w')
    i = 0
    test_input = []    
    test_output = []
    pre_output = []
    for test_line in test.readlines():
       # print(test_line)
        if i%2 == 0:
            test_input.append(test_line)
        if i%2 == 1:
            test_output.append(test_line)
        i += 1
    for test_sentence in test_input:
        pys = test_sentence.split()
        #print(pys)
        sen_nodes = Sen_nodes(pys)
        sen_nodes = dynamic(sen_nodes,lamda)
        result = path(sen_nodes)
        output.write('%s\n' % result)
        pre_output.append(result)
    for i in range(len(pre_output)):
        test_output[i] = test_output[i][:-1]
    output.close()
    test.close()
    print("end translation")
    return test_input,test_output,pre_output



import sys
test_file_path = sys.argv[1]
output_file_path = sys.argv[2]
test_input,test_output,pre_output = test(test_file_path,output_file_path)

#为了后续准确率测试保存结果
def save_obj(obj, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
save_obj(test_output,"../data/test_output.pkl")
save_obj(pre_output,"../data/pre_output.pkl")
