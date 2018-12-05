
import pickle
def load_obj(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

pre_output = load_obj("../data/pre_output.pkl")
test_output = load_obj("../data/test_output.pkl")


#a=set(test_output)
#b=set(pre_output)
#c = a&b
#acc = len(c)/len(a) 
#c
import Levenshtein
total_num = 0
same_num = 0
for i in range(len(pre_output)):
    mini_total_num = len(test_output[i])
    mini_same_num = mini_total_num - Levenshtein.hamming(pre_output[i],test_output[i])
    mini_av = mini_same_num/mini_total_num
    total_num = total_num + mini_total_num
    same_num = same_num + mini_same_num
    #if mini_av == 1:    
     #   print(pre_output[i],test_output[i])

    
print(same_num/total_num)
