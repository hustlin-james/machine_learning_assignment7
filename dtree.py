import sys
import math
#psuedo code, to work for continous values
#if examples is empty then return default
#else if all examples have the same class then return the class
#else
#   (best_attribute, best_threshold) = CHOOSE-ATTRIBUTE(examples, attributes)
#   tree = a new decision tree with root test (best_attribute, best_threshold)
#   examples_left = {elements of examples with best_attribute < threshold}
#   examples_right = {elements of examples with best_attribute >= threshold}
#   tree.left_child = DTL(examples_left, attributes, DISTRIBUTION(examples))
#   tree.right_child = DTL(examples_right, attributes, DISTRIBUTION(examples))
#return tree


#A is integer representing the column (attribute)

def choose_attribute(examples,attributes):
    
def information_gain(examples,A,threshold):
    information_gain = 0.0
    examples_left = []
    examples_right = []

    total_examples = len(examples)

    for idx in range(len(examples)):
        val = examples[idx][A]
        if val < threshold:
            examples_left.append(examples[idx])
        else:
            examples_right.append(examples[idx])

    H_e = calculate_entropy([len(examples_left),len(examples_right)])

    #sum entropy for each class
    left_class_count_ary = get_class_count_ary(examples_left)  
    right_class_count_ary = get_class_count_ary(examples_right)  

    entropy_left_child = calculate_entropy(left_class_count_ary)
    entropy_right_child = calculate_entropy(right_class_count_ary)

    left_prop = len(examples_left)/float(total_examples)
    right_prop = len(examples_right)/float(total_examples)

    information_gain = H_e - (left_prop*entropy_left_child) - (right_prop*entropy_right_child)
    return information_gain

def calculate_entropy(split_ary):
    entropy_sum = 0.0

    total = 0
    for s in split_ary:
        total += s
    
    for s in split_ary:
        p = (s/float(total))
        if p != 0:
            entropy_sum += -(p*math.log(p,2))
        else:
            entropy_sum += 0.0

    return entropy_sum

def get_class_count_ary(examples):
    class_count_ary=[0.0]*num_classes
    total = len(examples)

    for e in examples:
        class_count_ary[int(e[-1])] = class_count_ary[int(e[-1])] + 1
    
    return class_count_ary      

def dtl(examples,attributes,class_set,default):
    global num_classes
    num_classes = len(class_set)           

def train(training_file,test_file,option,pruning_thr):

    file = open(training_file,"r")

    examples = []
    class_set = set()
    for line in file:
        tokens = line.split()
        class_key = tokens[len(tokens)-1]
        class_set.add(class_key)
        #examples.append(tokens[:len(tokens)-1])
        examples.append(tokens)

    attributes = [0.0]*len(examples[0])
    information_gain_test()

    #dtl(examples,attributes,class_set,default)


#Test case to make sure information gain is working correctly
def information_gain_test():
    global num_classes
    num_classes = 3
    examples = []
    examples.append([0,2,1])
    examples.append([1,5,0])
    examples.append([9,8,2])
    examples.append([0,12,1])
    examples.append([2,14,0])
    A = 1
    threshold = 10
    H_e = -(3/5.0)*math.log(3/5.0,2)-(2/5.0)*math.log(2/5.0,2)

    entropy_left = -(1/3.0)*math.log(1/3.0,2) - (1/3.0)*math.log(1/3.0,2) - (1/3.0)*math.log(1/3.0,2)
    entropy_right = -(1/2.0)*math.log(1/2.0,2) - (1/2.0)*math.log(1/2.0,2) - 0

    test_ig = H_e - (3/5.0)*entropy_left - (2/5.0)*entropy_right

    ig = information_gain(examples,A,threshold)

    assert abs((abs(test_ig) - abs(ig))) <= .000000001,"information gain calculate is wrong" 

def main():

    if len(sys.argv)== 5:
        training_file = sys.argv[1]
        test_file = sys.argv[2]
        option = sys.argv[3] 
        pruning_thr = sys.argv[4]

        train(training_file,test_file,option,pruning_thr)
    else:
        sys.exit()

if __name__ == "__main__":
    main()