import Solution.Util as Util
import numpy as np
import random
import math


class Evaluator:
    def __init__(self, dir, name):
        self.dir = dir
        self.name = name
        allfiles = Util.read_tera_all_csv(dir + name)
        self.raw_filepath = allfiles[allfiles.__len__() - 1]
        self.truth_filepath = Util.get_exist_path(self.raw_filepath)
        self.all_file_path = Util.get_allfile_path(self.dir, self.name)
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0
        self.read_ground_truth()

    def read_ground_truth(self):
        all_file_map = self.read_all_file_map()
        with open(self.truth_filepath, 'r') as f:
            lines = f.readlines()
        truth_vector = np.zeros(all_file_map.__len__(), dtype=np.int)
        first_line = True
        for line in lines:
            line = line.strip()
            if first_line:
                first_line = False
                continue
            parts = line.split(',')
            name = parts[0]
            label = int(parts[parts.__len__()-1])
            index = all_file_map[name]
            label_value = int(label)
            if label_value == 0:
                label_value = -1
            truth_vector[index] = label_value
        return truth_vector

    def read_all_file_map(self):
        data_map = {}
        with open(self.all_file_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.isspace() or line == '':
                continue
            parts = line.split(',')
            data_map[parts[1]] = int(parts[0])
        return data_map

    def reset_data(self):
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0

    def evaluate(self, vector_f, new_files=None):
        self.reset_data()
        vector_f = self.normalize_f(vector_f)
        # print(vector_f)
        vector_truth = self.read_ground_truth()
        index = 0
        while index < vector_truth.__len__():
            # print(vector_truth[index], vector_f[index])
            if vector_truth[index] == 0:
                index += 1
                continue
            if vector_truth[index] == 1:
                if vector_f[index] == 1:
                    self.true_positive += 1
                else:
                    self.false_negative += 1
            elif vector_truth[index] == -1:
                if vector_f[index] == -1:
                    self.true_negative += 1
                else:
                    self.false_positive += 1
            else:
                print('error')
            index += 1
        if new_files is not None:
            self.true_positive += new_files[0]
            self.false_positive += new_files[1]
            self.true_negative += new_files[2]
            self.false_negative += new_files[3]
        print(self.true_positive, self.false_positive, self.true_negative, self.false_negative)
        precision = self.calc_precision()
        recall = self.calc_recall()
        fmeasure = self.calc_f1measure()
        gmean = self.calc_gmean()
        balance = self.calc_balance()
        if new_files is not None:
            self.true_positive -= new_files[0]
            self.false_positive -= new_files[1]
            self.true_negative -= new_files[2]
            self.false_negative -= new_files[3]
        return [precision, recall, fmeasure, gmean, balance]

    def calc_precision(self):
        if self.true_positive == 0:
            return 0
        return float(self.true_positive) / float(self.true_positive + self.false_positive)

    def calc_recall(self):
        if self.true_positive == 0:
            return 0
        return float(self.true_positive) / float(self.true_positive + self.false_negative)

    def calc_f1measure(self):
        precision = self.calc_precision()
        recall = self.calc_recall()
        if precision == 0 or recall == 0:
            return 0
        return 2 * precision * recall / (precision + recall)

    def calc_gmean(self):
        a = self.true_positive / (self.true_positive + self.false_negative)
        b = self.true_negative / (self.true_negative + self.false_positive)
        return math.sqrt(a * b)

    def calc_balance(self):
        pf = self.false_positive / (self.false_positive+self.true_negative)
        pd = self.calc_recall()
        a = math.pow(0 - pf, 2)
        b = math.pow(1 - pd, 2)
        return 1 - math.sqrt((a + b) / 2)

    @classmethod
    def normalize_f(cls, vector_f):
        vector_res = np.zeros(vector_f.__len__(), dtype=np.int)
        index = 0
        temp = sorted(vector_f)
        f_index = int(0.8 * vector_f.__len__())
        # print('f_index', f_index, 'len', vector_f.__len__())
        offset = temp[f_index]
        # print('offset', offset)
        while index < vector_f.__len__():
            if vector_f[index] > offset:
                vector_res[index] = 1
            elif vector_f[index] < offset:
                vector_res[index] = -1
            else:
                rand = random.random()
                defect_rate = 0.5
                if rand < defect_rate:
                    vector_res[index] = 1
                else:
                    vector_res[index] = -1
            index += 1
        # print('count', count)
        return vector_res
