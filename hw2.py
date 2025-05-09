import numpy as np
import matplotlib.pyplot as plt


### Chi square table values ###
# The first key is the degree of freedom 
# The second key is the p-value cut-off
# The values are the chi-statistic that you need to use in the pruning

chi_table = {1: {0.5 : 0.45,
             0.25 : 1.32,
             0.1 : 2.71,
             0.05 : 3.84,
             0.0001 : 100000},
         2: {0.5 : 1.39,
             0.25 : 2.77,
             0.1 : 4.60,
             0.05 : 5.99,
             0.0001 : 100000},
         3: {0.5 : 2.37,
             0.25 : 4.11,
             0.1 : 6.25,
             0.05 : 7.82,
             0.0001 : 100000},
         4: {0.5 : 3.36,
             0.25 : 5.38,
             0.1 : 7.78,
             0.05 : 9.49,
             0.0001 : 100000},
         5: {0.5 : 4.35,
             0.25 : 6.63,
             0.1 : 9.24,
             0.05 : 11.07,
             0.0001 : 100000},
         6: {0.5 : 5.35,
             0.25 : 7.84,
             0.1 : 10.64,
             0.05 : 12.59,
             0.0001 : 100000},
         7: {0.5 : 6.35,
             0.25 : 9.04,
             0.1 : 12.01,
             0.05 : 14.07,
             0.0001 : 100000},
         8: {0.5 : 7.34,
             0.25 : 10.22,
             0.1 : 13.36,
             0.05 : 15.51,
             0.0001 : 100000},
         9: {0.5 : 8.34,
             0.25 : 11.39,
             0.1 : 14.68,
             0.05 : 16.92,
             0.0001 : 100000},
         10: {0.5 : 9.34,
              0.25 : 12.55,
              0.1 : 15.99,
              0.05 : 18.31,
              0.0001 : 100000},
         11: {0.5 : 10.34,
              0.25 : 13.7,
              0.1 : 17.27,
              0.05 : 19.68,
              0.0001 : 100000}}

def calc_gini(data):
    """
    Calculate gini impurity measure of a dataset.
 
    Input:
    - data: any dataset where the last column holds the labels.
 
    Returns:
    - gini: The gini impurity value.
    """
    gini = 0.0

    ###########################################################################
    # TODO: Implement the function.
    from collections import Counter
            
    arrayOfColumnLabel = [row[-1] for row in data]
    numberOfTotalSamples = len(arrayOfColumnLabel) 
    labelCountsDict = Counter(arrayOfColumnLabel)
    sumOfSquaredProportions=0
    for label, count in labelCountsDict.items():
        proportion = count / numberOfTotalSamples
        sumOfSquaredProportions += proportion ** 2
    gini = 1.0-sumOfSquaredProportions                                         #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return gini

def calc_entropy(data):
    """
    Calculate the entropy of a dataset.

    Input:
    - data: any dataset where the last column holds the labels.

    Returns:
    - entropy: The entropy value.
    """
    entropy = 0.0
    ###########################################################################
    # TODO: Implement the function.  
    #    from collections import Counter
    labels = [row[-1] for row in data]

    _, counts = np.unique(labels, return_counts=True) # |c|
    total_labels = len(labels) # |S|
    from collections import Counter

    labelCountsDict = Counter(labels)
    
    for label, count in labelCountsDict.items():
        proportion = count / total_labels
        entropy -= proportion*np.log2(proportion) #count is |Si|

    entropy = round(float(entropy), 16)                                  
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return entropy

class DecisionNode:

    
    def __init__(self, data, impurity_func, feature=-1,depth=0, chi=1, max_depth=1000, gain_ratio=False):
        
        self.data = data # the data instances associated with the node
        self.terminal = False # True iff node is a leaf
        self.feature = feature # column index of feature/attribute used for splitting the node
        self.pred = self.calc_node_pred() # the class prediction associated with the node
        self.depth = depth # the depth of the node
        self.children = [] # the children of the node (array of DecisionNode objects)
        self.children_values = [] # the value associated with each child for the feature used for splitting the node
        self.max_depth = max_depth # the maximum allowed depth of the tree
        self.chi = chi # the P-value cutoff used for chi square pruning
        self.impurity_func = impurity_func # the impurity function to use for measuring goodness of a split
        self.gain_ratio = gain_ratio # True iff GainRatio is used to score features
        self.feature_importance = 0
    
    def calc_node_pred(self):
        """
        Calculate the node's prediction.

        Returns:
        - pred: the prediction of the node
        """
        pred = None
        ###########################################################################
        # TODO: Implement the function.     
        from collections import Counter
        labelCountsDict = Counter([row[-1] for row in self.data]) 
        mostCommonfeature=""
        mostCommonfeatureNumber=0
        for label, count in labelCountsDict.items():
            if(mostCommonfeatureNumber<count):
                mostCommonfeatureNumber=count
                mostCommonfeature=label
        pred = mostCommonfeature
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred
        
    def add_child(self, node, val):
        """
        Adds a child node to self.children and updates self.children_values

        This function has no return value
        """
        ###########################################################################
        # TODO: Implement the function.    
        self.children.append(node)
        self.children_values.append(val)
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def goodness_of_split(self, feature):
        """
        Calculate the goodness of split of a dataset given a feature and impurity function.

        Input:
        - feature: the feature index the split is being evaluated according to.

        Returns:
        - goodness: the goodness of split
        - groups: a dictionary holding the data after splitting 
                  according to the feature values.
        """
        goodness = 0
        groups = {} # groups[feature_value] = data_subset
        ###########################################################################
        # TODO: Implement the function.                                           #
        from collections import defaultdict
        groups = defaultdict(list)
        for row in self.data:
            value = row[feature]
            if value not in groups:
                groups[value] = []
            groups[value].append(row)

        totalSize = len (self.data)
        sigma=0

        if not self.gain_ratio:
            totalSize = len (self.data)
            for data_subset in groups.values():
                sigma+=(len(data_subset)/totalSize)*self.impurity_func(data_subset)

            goodness = self.impurity_func(self.data)-sigma

        else:
            splitInfo = 0
            for values in groups.values():
                sigma +=(len(values)/totalSize)* calc_entropy(self.data)
                splitInfo -= (len(values)/totalSize)* np.log2(len(values)/totalSize)
            informationGain = calc_entropy(self.data) - sigma
            if(not splitInfo):
                goodness = 0
            else:
                goodness = informationGain / splitInfo

        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return goodness, groups
    
    def calc_feature_importance(self, n_total_sample):
        """
        Calculate the selected feature importance.
            
        Input:
        - n_total_sample: the number of samples in the dataset.

        This function has no return value - it stores the feature importance in 
        self.feature_importance
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        goodness, _ = self.goodness_of_split(self.feature)
        self.feature_importance = (len(self.data)/n_total_sample)*goodness
        print(f"[DEBUG] feature=X{self.feature} importance={self.feature_importance:.4f} samples={len(self.data)}")

        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def split(self):
        """
        Splits the current node according to the self.impurity_func. This function finds
        the best feature to split according to and create the corresponding children.
        This function should support pruning according to self.chi and self.max_depth.

        This function has no return value
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        def chi_is_good(db):
            """
            Check whether the split should be pruned based on Chi-square test.
            Returns True if the split is NOT statistically significant.
            """
            chi_stat = compute_chi_squared_stat(db)
            df = len(db) - 1
            if df in chi_table:
                threshold = chi_table[df].get(self.chi, 100000)
                return chi_stat < threshold
            return True 
        from collections import Counter

        def compute_chi_squared_stat(groups):
            """
            Compute Chi-squared statistic for a proposed split.
            - groups: dict mapping feature values to subsets (list of rows)

            Returns:
            - sigma: float
            """
            total_size = len(self.data)
            # The overall distribution of class labels before the split
            #total_label_counts = {'+': 5, '-': 3}
            total_label_counts = Counter([row[-1] for row in self.data])

            # General probabilities p_j for each class label
            #p_j = {'+': 5/8 = 0.625, '-': 3/8 = 0.375}
            p_j = {}
            for label, count in total_label_counts.items():
                p_j[label] = count / total_size

            sigma = 0

            for subset in groups.values():
                m = len(subset)
                if m == 0:
                    continue
                # Count the occurrences of each class label in the current subset.
                # Assumes the class label is the last element in each row.
                subset_label_counts = Counter([row[-1] for row in subset])
                for label in total_label_counts:
                    m_j = subset_label_counts.get(label, 0)
                    expected = m * p_j[label]
                    if expected > 0:
                        sigma += ((m_j - expected) ** 2) / expected

            return sigma
        bestGoodness = -1
        bestFeature = None
        bestDataSubset = None
        n_Features = len(self.data[0])-1
        for feature in range(n_Features):
            goodness, groups = self.goodness_of_split(feature)
            if goodness > bestGoodness:
                bestGoodness = goodness
                bestFeature = feature
                bestDataSubset = groups
        # Stopping condition – leaf node
         # Stopping condition – leaf node
        if bestGoodness <= 0:
            self.terminal = True
            return

        if self.depth >= self.max_depth:
            self.terminal = True
            return

        if self.chi < 1 and chi_is_good(bestDataSubset):
            self.terminal = True
            return
        self.feature = bestFeature
        self.calc_feature_importance(n_total_sample=len(self.data))



        
        for featureKind,data_subset in bestDataSubset.items():
            childNode=DecisionNode(data_subset,self.impurity_func,self.feature,self.depth+1,self.chi,self.max_depth,self.gain_ratio)
            self.add_child(childNode,featureKind)

        


        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

                    
class DecisionTree:
    def __init__(self, data, impurity_func, feature=-1, chi=1, max_depth=1000, gain_ratio=False):
        self.data = data # the training data used to construct the tree
        self.root = None # the root node of the tree
        self.max_depth = max_depth # the maximum allowed depth of the tree
        self.chi = chi # the P-value cutoff used for chi square pruning
        self.impurity_func = impurity_func # the impurity function to be used in the tree
        self.gain_ratio = gain_ratio #
        
    def depth(self):
        return self.root.depth
    

    def build_tree(self):
        """
        Build a tree using the given impurity measure and training dataset. 
        You are required to fully grow the tree until all leaves are pure 
        or the goodness of split is 0.

        This function has no return value
        """
        self.root = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        #build the root
        self.root = DecisionNode(self.data, self.impurity_func, depth=0, chi=self.chi, max_depth=self.max_depth, gain_ratio=self.gain_ratio)
        def build_tree_recursive(node,current_depth):
            if node.terminal or current_depth>=self.max_depth:
                return
            else:
                node.split()
                for child in node.children:
                    build_tree_recursive(child,current_depth+1) 
       
        build_tree_recursive(self.root,0)
               
       

        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def predict(self, instance):
        """
        Predict a given instance
     
        Input:
        - instance: an row vector from the dataset. Note that the last element 
                    of this vector is the label of the instance.
     
        Output: the prediction of the instance.
        """
        pred = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        node = self.root
        while not node.terminal:
            featureValue = instance[node.feature] 
            if featureValue in node.children_values:
                indexOfNodeToMove = node.children_values.index(featureValue) 
                node = node.children[indexOfNodeToMove]
            else:
                break
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return node.pred

    def calc_accuracy(self, dataset):
        """
        Predict a given dataset 
     
        Input:
        - dataset: the dataset on which the accuracy is evaluated
     
        Output: the accuracy of the decision tree on the given dataset (%).
        """
        accuracy = 0
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        numOfCorrectPrediction = 0
        totalNumOfTests = len(dataset)

        for instance in dataset:
            prediction = self.predict(instance)
            if prediction == instance[-1]:
                numOfCorrectPrediction += 1
        
        accuracy = numOfCorrectPrediction / totalNumOfTests
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return accuracy
def depth_pruning(X_train, X_validation):
    """
    Calculate the training and validation accuracies for different depths
    using the best impurity function and the gain_ratio flag you got
    previously. 

    Input:
    - X_train: the training data where the last column holds the labels
    - X_validation: the validation data where the last column holds the labels
 
    Output: the training and validation accuracies per max depth
    """
    training = []
    validation  = []
    root = None
    for i,max_depth in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        tree = DecisionTree(
            data=X_train,
            impurity_func=calc_entropy,
            max_depth=max_depth,
            gain_ratio=False,
        )
        tree.build_tree()
        trainingAccuracy = tree.calc_accuracy(X_train)
        validationAccuracy = tree.calc_accuracy(X_validation)
        
        training.append(trainingAccuracy)
        validation.append(validationAccuracy)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
    return training, validation

def chi_pruning(X_train, X_test):

    """
    Calculate the training and validation accuracies for different chi values
    using the best impurity function and the gain_ratio flag you got
    previously. 

    Input:
    - X_train: the training data where the last column holds the labels
    - X_validation: the validation data where the last column holds the labels
 
    Output:
    - chi_training_acc: the training accuracy per chi value
    - chi_validation_acc: the validation accuracy per chi value
    - depth: the tree depth for each chi value
    """
    chi_training_acc = []
    chi_validation_acc  = []
    depth = []

    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    chi_values = [1, 0.5, 0.25, 0.1, 0.05, 0.0001]
    for chi_val in chi_values:
        tree = DecisionTree(
            data=X_train,
            impurity_func=calc_entropy, 
            chi=chi_val,
            gain_ratio=False,
            max_depth=1000
        )
        tree.build_tree() 
        trainAccuracy = tree.calc_accuracy(X_train)
        val_acc = tree.calc_accuracy(X_test)

        chi_training_acc.append(trainAccuracy)
        chi_validation_acc.append(val_acc)
        def get_max_depth(node):
            if node.terminal:
                return node.depth
            return max(get_max_depth(child) for child in node.children)

        depth.append(get_max_depth(tree.root))
     

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
        
    return chi_training_acc, chi_validation_acc, depth


def count_nodes(node):
    """
    Count the number of node in a given tree
 
    Input:
    - node: a node in the decision tree.
 
    Output: the number of node in the tree.
    """
    ###########################################################################
    # TODO: Implement the function.                                           #
    n_nodes=0
    def count_nodes_rec(node):
        if node.terminal:
                return 1
        return 1 + sum(count_nodes_rec(child) for child in node.children)
    n_nodes=count_nodes_rec(node)

    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return n_nodes






