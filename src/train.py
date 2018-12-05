import os
import time
import sys
#dir_name = '/Users/guiziwei/Documents/MacBook/清华/课程/人工智能/拼音输入法作业/sina_news_gbk/'
#hz_file = '/Users/guiziwei/Documents/MacBook/清华/课程/人工智能/拼音输入法作业/拼音汉字表_12710172/一二级汉字表.txt'
#py_file = '/Users/guiziwei/Documents/MacBook/清华/课程/人工智能/拼音输入法作业/拼音汉字表_12710172/拼音汉字表.txt'
dir_name = sys.argv[1]
hz_file = sys.argv[2]
py_file = sys.argv[3]

#识别字符是否为汉字，汉字返回true,字符或数字返回false
def isChinese(s):
    for c in s:
        if u'\u4e00' <= c <= u'\u9fff':
            return True
        if '\u0030' <= c <= '\u0039':
            return False

#将句子中的非汉字变成‘’并将训练集所有的句子存到sentences数组中
def make_sentences(line_new,sentences):
    sentence=""
    start=True
    for i in range(len(line_new)):
        if start and line_new[i]!='':
            sentence+=line_new[i]
            start=False
        elif start and line_new[i]=='':
            continue
        elif not start and line_new[i]!='':
            sentence+=line_new[i]
        elif not start and line_new[i]=='':
            if len(sentence) > 1:
                sentences.append(sentence)
            sentence=""
            start=True
    return sentences

#生成单个汉字出现次数字典dict_hznum（空）、两个字同时出现次数字典two_hznum（空）、和为了生成汉字编码的数组all_hz
def make_dict(hz_file):
    f = open(hz_file,encoding='gbk')
    all_hz = f.readlines()[0]
    dict_hznum={}
    two_hznum={}
    for i in range(6763):
        dict_hznum[i]=0
        two_hznum[i]={}
        for k in range(6763):
            two_hznum[i][k]=0
    return  all_hz, dict_hznum, two_hznum 

#生成一个拼音对应所有字的字典py_2_hz
def make_py_2_hz_dict(py_file):
    py_2_hz = {}
    f = open(py_file,encoding='gbk')
    for line in f.readlines():
        list_ = line.split()
        py = list_[0]
        hz = list_[1:]
        py_2_hz[py] = hz
    return py_2_hz

#训练填入单个汉字出现次数字典dict_hznum、两个字同时出现次数字典two_hznum、训练机中汉字总字数
def train_num_dict(sentences,dict_hznum, two_hznum):
    total_num = 0
    for sentence in sentences:
        for i in range(len(sentence)):
            hz = sentence[i]            
            if hz in all_hz:
                code = all_hz.index(hz)            
                value = dict_hznum[code]
                value += 1
                dict_hznum[code] = value
                total_num += 1        
                if i != 0:
                    d_value = two_hznum[pre_code][code]
                    d_value += 1
                    two_hznum[pre_code][code] = d_value
                    pre_hz = hz
                    pre_code = all_hz.index(pre_hz)
                else:
                    pre_hz = hz
                    pre_code = all_hz.index(pre_hz)
            else:
                rare_hz = sentence[i]
                #print(rare_hz)
    return total_num,dict_hznum, two_hznum

#输入训练文件，执行训练
def train_all(dir_name,dict_hznum, two_hznum):  
    sentences=[]
    file_list = os.listdir(dir_name) 
    for file in file_list[1:]:
        with open(dir_name+file, encoding='gbk')as news:
            print(dir_name+file)
            for line in news.readlines():
                line_new = [ch if isChinese(ch) else '' for ch in line]
                sentences = make_sentences(line_new, sentences)
    total_num,dict_hznum, two_hznum = train_num_dict(sentences, dict_hznum, two_hznum)
    return total_num,dict_hznum, two_hznum

start = time.time()
all_hz, dict_hznum, two_hznum = make_dict(hz_file)
total_num,dict_hznum, two_hznum = train_all(dir_name,dict_hznum, two_hznum)
end = time.time()
print("time cost： {}".format(end-start))#1235.9874539375305


print(total_num)#400702350

#保存字典的函数
import pickle
def save_obj(obj, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

#保存训练好的文件
py_2_hz = make_py_2_hz_dict(py_file)
save_obj(py_2_hz,"../data/py_2_hz.pkl")
save_obj(all_hz,"../data/all_hz.pkl")
save_obj(dict_hznum,"../data/dict_hznum.pkl")
save_obj(two_hznum,"../data/two_hznum.pkl")
pickle.dump(total_num,open('../data/total_num.txt', 'wb')) 

