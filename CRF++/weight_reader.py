# -*- coding: utf-8 -*-

import codecs
import re
from collections import defaultdict, deque
import cPickle as pickle




class wReader(object):

    SEP     = u"##"

    PATTERN = re.compile(u'^\d+ (.+)$')
    MACRO   = re.compile(u'%x\[-?\d+,\d+\]')
    NUMS    = re.compile(u'-?\d+')

    def read(self, model_path):
        model_fp = codecs.open(model_path, "r", "utf-8")
        labels     = self._read_labels(model_fp)
        templats   = self._read_templats(model_fp)
        expd_temps = self._read_expanded_tmps(model_fp)
        weights    = self._read_weights(model_fp)
        model_fp.close()

        weight_dic = defaultdict(int)
        for expd_temp in expd_temps:
            if expd_temp[0] == u"B":
                for pre_label in labels:
                    for cur_label in labels:
                        weight_dic[expd_temp + self.SEP + pre_label + self.SEP + cur_label] = weights.popleft()
            else:
                for label in labels:
                    weight_dic[expd_temp + self.SEP + label] = weights.popleft()

        return weight_dic, templats


    def _read_labels(self, model_fp):
        for raw_line in model_fp:
            line = raw_line.rstrip(u"\n\r")
            if line == u"":
                break

        labels = []
        for raw_line in model_fp:
            if raw_line == u"\n":
                break
            labels.append(raw_line.rstrip(u"\n\r"))

        return labels

    def _read_templats(self, model_fp):
        templats = []
        for raw_line in model_fp:
            if raw_line == u"\n":
                break
            line = raw_line.rstrip(u"\n\r")
            templats.append(self._decode_template(line))

        return templats

    def _read_expanded_tmps(self, model_fp):
        expd_temps = []
        for raw_line in model_fp:
            if raw_line == u"\n":
                break
            line = raw_line.rstrip(u"\n\r")
            expd_temp = re.search(self.PATTERN, line).group(1)
            expd_temps.append(expd_temp)

        return expd_temps


    def _read_weights(self, model_fp):
        weights = deque()
        for raw_line in model_fp:
            line = raw_line.rstrip(u"\n\r")
            weights.append(float(line))

        return weights


    def _decode_template(self, temp_str):
        fractions = self.MACRO.split(temp_str)
        macros = self.MACRO.findall(temp_str)

        num_pairs = []
        for macro in macros:
            num_pair = self.NUMS.findall(macro)
            num_pairs.append((int(num_pair[0]), int(num_pair[1])))


        is_unigram = True if fractions[0][0] == u"U" else False

        return (fractions, num_pairs, is_unigram)

        


if __name__ == "__main__":
    rdr = wReader()
    info = rdr.read("modeld.txt")

    dump_f = open("dump.txt", "w")
    pickle.dump(info, dump_f)
    dump_f.close()
