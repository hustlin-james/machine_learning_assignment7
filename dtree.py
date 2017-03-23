import sys
import math
import random
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

class Node:
    def __init__(self,type="",node_id=-1,attribute=-1,threshold=-1.0,information_gain=0.0,distribution=[],left_child=None,right_child=None):
        self.type=""
        self.node_id = node_id
        self.attribute = attribute
        self.threshold = threshold
        self.information_gain = information_gain
        self.distribution = distribution
        self.left_child=left_child
        self.right_child=right_child
    def __str__(self):
        output = "type: %s,node_id: %d,attribute: %d,threshold: %f,information_gain: %f"%(self.type,self.node_id,self.attribute,self.threshold,self.information_gain)
        return output

def classify(n,row):
    if n.attribute != -1:
        attribute = n.attribute
        threshold = n.threshold 
        if row[attribute] < threshold:
            return classify(n.left_child,row)
        else:
            return classify(n.right_child,row)
    else:
        return n

def training_ouput(n,tree_id):
    if n.left_child == None and n.right_child == None:
        print("tree=%2d, node=%3d, feature=%2d, thr=%6.2lf, gain=%lf"%(tree_id,n.node_id,n.attribute,n.threshold,n.information_gain))
    else:
        print("tree=%2d, node=%3d, feature=%2d, thr=%6.2lf, gain=%lf"%(tree_id,n.node_id,n.attribute,n.threshold,n.information_gain))
        if(n.left_child != None):
            training_ouput(n.left_child,tree_id)
        
        if(n.right_child != None):
            training_ouput(n.right_child,tree_id)


def choose_attribute(examples,attributes):
    max_gain = -1
    best_attribute = best_threshold = -1
    times = 50

    if option == "optimized":
        for A in attributes:
            min_max = find_min_max(examples,A)
            l = min_max[0]
            m = min_max[1]
            for k in range(times):
                threshold = l + (k+1)*(m-l)/(times+1)
                gain = information_gain(examples,A,threshold)
                if gain > max_gain:
                    max_gain = gain
                    best_attribute = A
                    best_threshold = threshold
    else:
        best_attribute = random.randint(0,len(attributes))
        min_max = find_min_max(examples,best_attribute)
        l = min_max[0]
        m = min_max[1]
        for k in range(times):
            threshold = l + (k+1)*(m-l)/(times+1)
            gain = information_gain(examples,best_attribute,threshold)
            if gain > max_gain:
                max_gain = gain
                best_threshold = threshold
    
    return [best_attribute,best_threshold,max_gain]

def find_min_max(examples,A):
    l = []
    for e in examples:
        l.append(e[A])
    return (min(l),max(l))

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

    parent_node_class_count_ary = get_class_count_ary(examples)
    H_e = calculate_entropy(parent_node_class_count_ary)

    #sum entropy for each class
    left_class_count_ary = get_class_count_ary(examples_left)  
    right_class_count_ary = get_class_count_ary(examples_right)  

    entropy_left_child = calculate_entropy(left_class_count_ary)
    entropy_right_child = calculate_entropy(right_class_count_ary)

    left_prop = len(examples_left)/float(total_examples)
    right_prop = len(examples_right)/float(total_examples)

    information_gain = H_e - ((left_prop*entropy_left_child) + (right_prop*entropy_right_child))
    return information_gain

def calculate_entropy(split_ary):
    entropy_sum = 0.0

    total = 0
    for s in split_ary:
        total += s
    
    for s in split_ary:
        p = 0.0

        if total != 0:
            p = (s/float(total))
        if p != 0.0:
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

def find_distribution(examples):
    distribution = [0.0]*num_classes
    total = float(len(examples))

    for e in examples:
        distribution[e[-1]] += 1.0
    
    for idx in range(len(distribution)):
        distribution[idx] = distribution[idx]/total

    return distribution

def dtl(examples,attributes,default,node_id):
    if len(examples) < pruning_thr:
        #print(examples)
        return default
    else:
         classes_in_examples = set([row[-1] for row in examples])
         #print(classes_in_examples)
         if len(classes_in_examples) == 1:
             n = Node()
             distribution = [0.0]*num_classes
             distribution[list(classes_in_examples)[0]] = 1.0
             n.distribution = distribution
             n.node_id = node_id
             return n
         else:
            b_attribute_threshold = choose_attribute(examples,attributes)
            n = Node()
            n.attribute = b_attribute_threshold[0]
            n.threshold = b_attribute_threshold[1]
            n.information_gain = b_attribute_threshold[2]
            n.node_id = node_id
            n.distribution = find_distribution(examples)
            
            examples_left = []
            examples_right = []
            best_attribute = b_attribute_threshold[0]
            best_threshold = b_attribute_threshold[1]

            for idx in range(len(examples)):
                val = examples[idx][best_attribute]
                if val < best_threshold:
                    examples_left.append(examples[idx])
                else:
                    examples_right.append(examples[idx]) 

            n_left_child = Node()
            n_left_child.node_id = 2*node_id
            n_left_child.distribution = find_distribution(examples)
            n.left_child = dtl(examples_left,attributes,n_left_child,n_left_child.node_id)
            
            n_right_child = Node()
            n_right_child.node_id = 2*node_id + 1
            n_right_child.distribution = find_distribution(examples)
            n.right_child = dtl(examples_right,attributes,n_right_child,n_right_child.node_id)
            
            return n

def train(training_file,test_file,option_val,pruning_thr_val):
    global num_classes
    global pruning_thr
    global option

    file = open(training_file,"r")

    examples = []
    class_set = set()
    for line in file:
        tokens = line.split()
        class_key = tokens[len(tokens)-1]
        class_set.add(class_key)
        #examples.append(tokens[:len(tokens)-1])
        for idx in range(len(tokens)):
            tokens[idx] = int(tokens[idx])
        examples.append(tokens)

    num_classes = len(class_set)
    pruning_thr = int(pruning_thr_val)
    option = option_val

    attributes = []

    for idx in range(len(examples[0])-1):
        attributes.append(idx)

    file = open(test_file,"r")
    tests_data = []
    for line in file:
        tokens = line.split()
        for idx in range(len(tokens)):
            tokens[idx] = int(tokens[idx])
        tests_data.append(tokens)
  
    #**********Tests**********
    #information_gain_test()
    #**********END Tests******

    if option == "optimized":
        default = Node()
        node_id = 1
        root_node = dtl(examples,attributes,default,node_id)

        training_ouput(root_node,0)

        num_correct = 0
        for t in tests_data:
            n = classify(root_node,t)
            if len(n.distribution) > 0:
                idx  = n.distribution.index(max(n.distribution))
                if t[-1] == idx:
                    num_correct += 1

        print(num_correct)
        print(len(tests_data))
        print("accuracy: %f"%(num_correct/float(len(tests_data))))
    else:
        trees = []
        num_times = 1

        if option == "forest3":
            num_times=3
        if option == "forest15":
            num_times=15
        
        for idx in range(num_times):
            default = Node()
            node_id = 1
            root_node = dtl(examples,attributes,default,node_id)
            trees.append(root_node)
            training_ouput(root_node,idx)

        classify_dist_prob_ary = []

        for t in tests_data:
            v = [0.0]*num_classes
            classify_dist_prob_ary.append(v)

        if option == "randomized":
            assert len(trees) == 1
        if option == "forest3":
            assert len(trees) == 3
        if option == "forest15":
            assert len(trees) == 15
        
        for root in trees:
            for idx in range(len(tests_data)):
                t = tests_data[idx]
                n = classify(root,t)
                distribution = n.distribution
             
                for n_idx in range(len(distribution)):            
                    classify_dist_prob_ary[idx][n_idx] =  classify_dist_prob_ary[idx][n_idx] + distribution[n_idx]
             
        
        for idx in range(len(classify_dist_prob_ary)):
            for c_idx in range(len(classify_dist_prob_ary[idx])):
                classify_dist_prob_ary[idx][c_idx] = classify_dist_prob_ary[idx][c_idx]/float(num_times)

        num_correct = 0
        for t_idx in range(len(tests_data)):
            t = tests_data[t_idx]
            class_idx = classify_dist_prob_ary[t_idx].index(max(classify_dist_prob_ary[t_idx]))

            if t[-1] == class_idx:
                num_correct += 1
        
        print(num_correct)
        print(len(tests_data))
        print("accuracy: %f"%(num_correct/float(len(tests_data))))

    
#Test case to make sure information gain is working correctly
def information_gain_test():
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
        option_val = sys.argv[3] 
        pruning_thr_val = sys.argv[4]

        train(training_file,test_file,option_val,pruning_thr_val)
    else:
        sys.exit()

if __name__ == "__main__":
    main()