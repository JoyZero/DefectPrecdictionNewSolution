import numpy as np
import Solution.Util as myUtil
import Solution.Evaluation as Eval
import random


class MainClass:
    initial_defect_rate = 0.5

    def __init__(self, name, sim_type, dir, lambda1, lambda2, lambda3):
        self.name = name
        self.sim_type = sim_type
        self.dir = dir
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.ver_files = self.get_ver_files()
        self.pre_version_num = self.ver_files.__len__() - 1
        self.total_file_num = self.read_files_num()
        self.f = np.zeros(self.total_file_num, dtype=np.double)
        self.w = np.zeros(self.pre_version_num, dtype=np.double)

    def get_ver_files(self):
        file_dir = self.dir + self.name
        return myUtil.read_tera_all_csv(file_dir)

    def read_files_num(self):
        filepath = myUtil.get_allfile_path(self.dir, self.name)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        empty_count = 0
        for line in lines:
            if line == "" or line.isspace():
                empty_count += 1
        return lines.__len__() - empty_count

    @classmethod
    def __vector_2_matrix(cls, vector):
        len = vector.__len__()
        matrix = np.zeros((len, len), dtype=np.double)
        index = 0
        while index < len:
            matrix[index][index] = vector[index]
            index += 1
        return matrix

    def initial_w(self):
        weight = 1.0 / self.pre_version_num
        index = 0
        while index < self.w.size:
            self.w[index] = weight
            index += 1

    def initial_f(self):
        index = 0
        while index < self.f.size:
            rand = random.random()
            if rand < self.initial_defect_rate:
                self.f[index] = 1
            else:
                self.f[index] = 0
            index += 1

    def update_f(self):
        matrix_l = self.read_l(self.ver_files[self.pre_version_num])
        matrix2 = np.zeros((self.total_file_num, self.total_file_num), dtype=np.double)
        vector_b = np.zeros(self.total_file_num, dtype=np.double)
        index = 0
        while index < self.pre_version_num:
            vector_i = self.read_I(self.ver_files[index], self.ver_files[self.pre_version_num])
            matrix_i = self.__vector_2_matrix(vector_i)
            matrix_i = self.w[index] * matrix_i
            matrix2 += matrix_i
            vector_y = self.read_y(self.ver_files[index])
            vector_y = np.dot(matrix_i, vector_y)
            vector_b += vector_y
            index += 1
        matrix2 = self.lambda2 * matrix2
        vector_b = self.lambda2 * vector_b
        matrix_a = matrix_l + matrix2
        f = np.linalg.lstsq(matrix_a, vector_b, rcond=None)[0]
        self.f = f

    def update_w(self):
        gamma = self.lambda3
        vector_v = self.calc_v()
        indexes = np.argsort(vector_v)
        vector_v.sort()
        p = self.calc_p(vector_v, gamma)
        theta = self.calc_theta(vector_v, gamma, p)
        index = 0
        while index < self.pre_version_num:
            w_index = indexes[index]
            if index < p:
                self.w[w_index] = (theta - vector_v[w_index] ) / (2 * gamma)
            else:
                self.w[w_index] = 0
            index += 1
        print('=== w:', self.w)
        # for w in self.w:
        #     sum += w
        # print(sum)

    def calc_p(self, vector_v, gamma):
        p = vector_v.__len__()
        while p > 0:
            theta = self.calc_theta(vector_v, gamma, p)
            if theta - vector_v[p-1] > 0:
                break
            p -= 1
        return p

    def calc_theta(self, vector_v, gamma, p):
        theta = 2 * gamma + sum(vector_v[:p])
        theta /= p
        return theta

    def calc_v(self):
        vector_v = np.zeros(self.pre_version_num, dtype=np.double)
        index = 0
        while index < vector_v.__len__():
            vector_i = self.read_I(self.ver_files[index], self.ver_files[self.pre_version_num])
            vector_y = self.read_y(self.ver_files[index])
            matrix_l = self.read_l(self.ver_files[index])
            term1 = np.dot(vector_y, matrix_l)
            term1 = np.dot(term1, vector_y)
            f_l = self.f - vector_y
            term2 = vector_i * f_l
            term2 = np.dot(term2, term2)
            vector_v[index] = self.lambda1 * term1 + self.lambda2 * term2
            index += 1
        return vector_v

    def run(self):
        self.initial_f()
        self.initial_w()
        count = 0
        evaluator = Eval.Evaluator(self.dir, self.name)
        pre_value = self.function_value()
        while count < 5:
            print('=== function value: ', pre_value)
            self.update_f()
            self.update_w()
            value = self.function_value()
            eval_res = evaluator.evaluate(self.f)
            print(eval_res)
            pre_value = value
            count += 1
        return eval_res

    def write_result(self):
        f_path = myUtil.get_result_fpath(self.dir, self.name)
        w_path = myUtil.get_result_wpath(self.dir, self.name)
        f_content = self.vector_2_str(self.f, to_int=True)
        w_content = self.vector_2_str(self.w)
        with open(f_path, 'w') as f:
            f.write(f_content)
        with open(w_path, 'w') as f:
            f.write(w_content)

    @staticmethod
    def vector_2_str(vector, to_int=False):
        index = 0
        content = ''
        while index < vector.__len__():
            if index != 0:
                content += ','
            if to_int:
                content += str(int(vector[index]))
            else:
                content += str(vector[index])
        return content

    def function_value(self):
        return self.f_L_f() + self.lambda1 * self.y_L_y() \
               + self.lambda2 * self.f_y() + self.lambda3 * self.w2()

    def f_L_f(self):
        index = self.ver_files.__len__() - 1
        file_path = self.ver_files[index]
        matrix_l = self.read_l(file_path, target=True)
        product = np.dot(self.f, matrix_l)
        product = np.dot(product, self.f)
        return product

    def y_L_y(self):
        index = 0
        res = np.double(0)
        while index < self.pre_version_num:
            y = self.read_y(self.ver_files[index])
            l = self.read_l(self.ver_files[index])
            product = np.dot(y, l)
            product = np.dot(product, y)
            res += product * self.w[index]
            index += 1
        return res

    def f_y(self):
        index = 0
        res = np.double(0)
        while index < self.pre_version_num:
            y = self.read_y(self.ver_files[index])
            i = self.read_I(self.ver_files[index], self.ver_files[self.pre_version_num])
            diff = i * (y - i)
            res += np.dot(diff, diff) * self.w[index]
            index += 1
        return res

    def w2(self):
        return np.dot(self.w, self.w)

    def read_l(self, filename, target=False):
        l_path = myUtil.get_l_path(filename, self.sim_type, target)
        with open(l_path, 'r') as f:
            lines = f.readlines()
        matrix_l = np.zeros((self.total_file_num, self.total_file_num), dtype=np.double)
        row = 0
        while row < lines.__len__():
            line = lines[row]
            if line.isspace() or line == "":
                continue
            parts = line.split(',')
            col = 0
            while col < parts.__len__():
                matrix_l[row][col] = float(parts[col])
                col += 1
            row += 1
        return matrix_l

    def read_y(self, filename):
        y_path = myUtil.get_y_path(filename)
        vector_y = np.zeros(self.total_file_num)
        with open(y_path, 'r') as f:
            line = f.readline()
        parts = line.split(',')
        index = 0
        while index < parts.__len__():
            vector_y[index] = float(parts[index])
            index += 1
        return vector_y

    def read_I(self, file1, file2):
        i_path = myUtil.get_i_path(file1, file2)
        vector_i = np.zeros(self.total_file_num)
        with open(i_path, 'r') as f:
            line = f.readline()
        parts = line.split(',')
        index = 0
        while index < parts.__len__():
            vector_i[index] = float(parts[index])
            index += 1
        return vector_i

    @classmethod
    def params_generator(cls):
        value_set = [0.01, 0.1, 1, 10, 10000]
        params_list = []
        index1 = 0
        while index1 < value_set.__len__():
            index2 = 0
            while index2 < value_set.__len__():
                index3 = 4
                while index3 < value_set.__len__():
                    params_list.append([value_set[index1], value_set[index2], value_set[index3]])
                    index3 += 1
                index2 += 1
            index1 += 1
        return params_list


if __name__ == '__main__':
    tera = ["camel", "ivy", "jedit", "log4j", "lucene", "poi","synapse",
            "velocity", "xalan", "xerces"]
    dir_path = "C:/Users/1/Desktop/tera/"
    lambda1 = 1
    lambda2 = 1
    lambda3 = 1
    # params_list = MainClass.params_generator()
    # print(params_list)
    # eval_res_list = []
    # for name in tera:
    #     print('============' + name + '===========')
    #     for params in params_list:
    #         print('--------' + str(params) + '---------')
    #         main = MainClass(name, myUtil.SIM_COS, dir_path, params[0], params[1], params[2])
    #         eval_res = main.run()
    #         eval_res_list.append(eval_res)
    #     myUtil.write_eval_result(main.dir, main.name, params_list, eval_res_list)
    main = MainClass('camel', myUtil.SIM_COS, dir_path, lambda1, lambda2, lambda3)
    eval_res = main.run()
