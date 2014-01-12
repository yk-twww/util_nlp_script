# -*- coding: utf-8 -*-

import codecs
import re
from collections import defaultdict
import sys
import os
import re


NUM_STR = re.compile(u" ([0-9.]+)$")
WORD_STR = re.compile(u"^(\\S+)")

CWD_DIR = os.getcwd()
REL_PATH = sys.argv[1] if len(sys.argv) == 2 else "."
BASE_PATH = CWD_DIR + "/" + REL_PATH + "/"


def main():
    topic_num = extract_topic_num()
    p_zw      = calc_pzw(topic_num)
    words     = extract_word()

    for i, w_line in enumerate(p_zw):
        out_line = words[i] + u"\t"
        for prob in w_line:
            out_line += str(prob).decode("utf-8") + u"\t"
        out_line = out_line.rstrip(u"\t")
        sys.stdout.write(out_line.encode('utf-8') + "\n")


def extract_topic_num():
    other_file = codecs.open(BASE_PATH + "model-final.others", "r", "utf-8")
    
    for raw_line in other_file:
        if re.search(u"ntopics", raw_line):
            res = re.search("\\d+$", raw_line.rstrip())
            num = int(res.group(0))
            break

    return num

def extract_word_num():
    other_file = codecs.open(BASE_PATH + "model-final.others", "r", "utf-8")

    for raw_line in other_file:
        if re.search(u"nwords", raw_line):
            res = re.search('\d+$', raw_line.rstrip())
            wd_num = int(res.group(0))
            break

    return wd_num


def calc_pzw(topic_num):
    phi_file = codecs.open(BASE_PATH + "model-final.phi", "r", "utf-8")
    p_wz = []
    for raw_line in phi_file:
        p_wz.append([float(_) for _ in raw_line.rstrip().split(u" ")])
    phi_file.close()

    p_zw = zip(*p_wz)

    return convert_prob(p_zw, topic_num)

def convert_prob(_p_zw, topic_num):
    wd_num = extract_word_num()
    p_z = calc_pz(topic_num)

    p_zw = []
    for w in xrange(wd_num):
        upper = []
        for z in xrange(topic_num):
            upper.append(p_z[z] * _p_zw[w][z])
        nmlz_rev = 1.0 / sum(upper)
        p_zw.append([_ * nmlz_rev for _ in upper])

    return p_zw




def calc_pz(topic_num):
    file_path = "model-final.tassign"
    assign_file = codecs.open(BASE_PATH + file_path, "r", "utf-8")

    topic_count = [0 for _ in xrange(topic_num)]
    for raw_line in assign_file:
        topics = extract_topics(raw_line)
        for t in topics:
            topic_count[t] += 1

    total_rev = 1.0 / sum(topic_count)

    return [cnt * total_rev for cnt in topic_count]

def extract_topics(raw_line):
    pairs = raw_line.rstrip().split(u" ")
    topics = [int(res.split(u":")[1]) for res in pairs]

    return topics


def extract_word():
    map_file = codecs.open(BASE_PATH + "wordmap.txt", "r", "utf-8")

    words = []
    map_file.readline() # abandon first line
    for raw_line in map_file:
        line = raw_line.rstrip()
        fields = line.split(u" ")
        words.append(fields[0])

    return words


if __name__ == "__main__":
    main()

