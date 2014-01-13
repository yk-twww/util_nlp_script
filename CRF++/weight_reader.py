# -*- coding: utf-8 -*-

import codecs
import re
from collections import defaultdict, deque



class wReader(object):

    SEP = u"##"
    PATTERN = u'^\d+ (.+)$'

    def read(self, model_path):
        model_fp = codecs.open(model_path, "r", "utf-8")
        labels = self._read_labels(model_fp)
        expd_temps = self._read_expanded_tmps(model_fp)
        weights = self._read_weights(model_fp)
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

        return weight_dic


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

    def _read_expanded_tmps(self, model_fp):
        for raw_line in model_fp:
            line = raw_line.rstrip(u"\n\r")
            if line == u"":
                break

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

if __name__ == "__main__":
    rdr = wReader()
    weights_dic = rdr.read("model.txt")

    w_keys = weights_dic.keys()
    w_keys.sort()
    for k in w_keys:
        print k.encode('utf-8') + " => " + str(weights_dic[k])
