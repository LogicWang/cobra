#!/usr/bin/python3
# -*- coding:utf8 -*-


"""
#Python3.5 Mac OS X
#2015.12.12
#mangobada@163.com
implement of decision tree algorithm  ID3
"""

from math import log
import operator
import numpy as np


# a small data set to verify the correction of program
def create_dataset():
    dataset = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataset, labels


#
def pre_process(dataset):
    pass


# transform the text file to matrix
def file_to_matrix(filename):
    fr = open(filename)
    num_of_lines = len(fr.readlines())
    matrix = np.zeros((num_of_lines, 3))
    class_labels = []
    feature_names = []
    fr = open(filename)
    feature_names = fr.readline().split('\t')[:-1]
    index = 0
    for line in fr.readlines():
        line = line.strip()
        words_list = line.split('\t')
        matrix[index, :] = words_list[0:-2]
        class_labels.append(words_list[-1])
        index += 1
    return matrix, class_labels, feature_names


# partition  dataset to train set and test set
def partition_dataset(dataset, ratio):
    l = len(dataset)
    len_test = l * ratio
    test_set = dataset[:len_test]
    train_set = dataset[len_test:]
    return train_set, test_set


# calculate entropy
def entropy(dataset):
    length = len(dataset)
    labels = {}
    for feature_vec in dataset:
        label = feature_vec[-1]
        if label not in labels.keys():
            labels[label] = 0
        labels[label] += 1
    entropy = 0.0
    for item in labels:
        prob = labels[item] / length
        entropy -= prob * log(prob, 2)
    return entropy


# return the splitted dataset where feature equal to value
# and remove the feature_axis
def split_dataset(dataset, index, value):
    result = []
    for feature_vec in dataset:
        if feature_vec[index] == value:
            reduced_vec = feature_vec[:index]
            reduced_vec.extend(feature_vec[index + 1:])
            result.append(reduced_vec)
    return result


# the best feature is the one that has largest infoGain
def choose_best_feature_split(dataset):
    base_entropy = entropy(dataset)
    num_of_features = len(dataset[0]) - 1
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_of_features):
        feature_values = [x[i] for x in dataset]
        uni_feature_values = set(feature_values)
        new_entropy = 0.0
        for value in uni_feature_values:
            sub_dataset = split_dataset(dataset, i, value)
            prob = len(sub_dataset) / len(dataset)
            new_entropy += prob * entropy(sub_dataset)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature_index


# get the majority count label of a set to represent the set
def majority(label_list):
    label_count = {}
    for vote in label_list:
        if vote not in label_count.keys():
            label_count[vote] = 0
        label_count[vote] += 1
        sorted_label_count = sorted(label_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_label_count[0][0]


# equal to create_tree
def train(dataset, features):
    tree = create_tree(dataset, features)
    return tree


# recursively create a tree based on entropy
def create_tree(dataset, features):
    features_list = features[:]
    label_list = [x[-1] for x in dataset]
    # process special case
    # all of data have same label
    if label_list.count(label_list[0]) == len(label_list):
        return label_list[0]
    # all of feature was splitted
    if len(dataset[0]) == 1:
        return majority(label_list)
    index = choose_best_feature_split(dataset)
    best_feature = features[index]
    my_tree = {best_feature: {}}
    del (features_list[index])
    feature_values = [row[index] for row in dataset]
    unique_values = set(feature_values)
    for value in unique_values:
        sub_features = features_list[:]
        sub_tree = create_tree(split_dataset(dataset, index, value), sub_features)
        my_tree[best_feature][value] = sub_tree
    return my_tree


# classify the test sample by the input tree
def classify(tree, test, test_features):
    first_key = list(tree.keys())[0]
    value_dict = tree[first_key]
    # print(firstKey)
    # print(featureNames)
    feature_index = test_features.index(first_key)
    for key in value_dict.keys():
        if test[feature_index] == key:
            if type(value_dict[key]).__name__ == 'dict':
                class_label = classify(value_dict[key], test, test_features)
            else:
                class_label = value_dict[key]
    return class_label


# based on inputTree and features, classify tests and compare the result with class labels
def test(tree, testset, test_features):
    error_count = 0.0
    num_of_tests = len(testset)
    for i in range(num_of_tests):
        result = classify(tree, test[i], test_features)
        if result != labels[i]:
            error_count += 1
    error_rate = error_count / num_of_tests
    return error_rate
