import sys

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

def dtl(examples,attributes,class_set,default):
    pass           

def train(training_file,test_file,option,pruning_thr):

    file = open(training_file,"r")

    examples = []
    class_set = set()

    classes_map = {}
    for line in file:
        tokens = line.split()
        class_key = tokens[len(tokens)-1]
        class_set.add(class_key)
        examples.append(tokens[:len(tokens)-1])
        if class_key not in classes_map:
            classes_map[class_key]=True

    attributes = [0.0]*len(examples[0])
    dtl(examples,attributes,class_set,default)


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