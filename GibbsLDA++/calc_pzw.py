# -*- coding: utf-8 -*-

import codecs
import re
from collections import defaultdict
import sys
import re


NUM_STR = re.compile(u" ([0-9.]+)$")
WORD_STR = re.compile(u"^(\\S+)")

def main():
    topic_num = extract_topic_num()
    p_zw = calc_pzw(topic_num)

    for word in p_zw.keys():
        sys.stdout.write(word.encode('utf-8') + "\n")
        for prob in p_zw[word]:
            sys.stdout.write("\t" + str(prob) + "\n")


def extract_topic_num():
    other_file = codecs.open("model-final.others", "r", "utf-8")
    
    for raw_line in other_file:
        if re.search(u"ntopics", raw_line):
            res = re.search("\\d+$", raw_line.rstrip())
            num = int(res.group(0))

    return num



def calc_pzw(topic_num):
    file_path = "model-final.twords"
    twords_file = codecs.open(file_path, "r", "utf-8")

    p_zw = defaultdict(list)
    tpc_n = -1
    for raw_line in twords_file:
        if decide_line(raw_line):
            tpc_n += 1
        else:
            res = extract_info(raw_line)
            p_zw[res[1]].append(res[0])
    twords_file.close()

    p_zw = convert_prob(p_zw, topic_num)

    return p_zw


def decide_line(raw_line):
    return len(raw_line) >= 5 and raw_line[0:5] == u"Topic"


def extract_info(raw_line):
    raw_line = raw_line.rstrip().lstrip()

    prob = NUM_STR.search(raw_line)
    word = WORD_STR.search(raw_line)

    return (float(prob.group(1)), word.group(1))


def convert_prob(p_wz, topic_num):
    p_z  = calc_pz(topic_num)
    p_zw = defaultdict(list)

    for word in p_wz.keys():
        normal = sum(p_wz[word])
        normal = 0.0
        for i in range(len(p_wz[word])):
            normal += p_wz[word][i] * p_z[i]
        for i in range(len(p_wz[word])):
            p_zw[word].append(p_wz[word][i] * p_z[i] / normal)

    return p_zw



def calc_pz(topic_num):
    file_path = "model-final.tassign"
    assign_file = codecs.open(file_path, "r", "utf-8")

    topic_count = [0 for _ in xrange(topic_num)]
    for raw_line in assign_file:
        topics = extract_topics(raw_line)
        for t in topics:
            topic_count[t] += 1

    total = sum(topic_count) + 0.0

    return [cnt / total for cnt in topic_count]
    

def extract_topics(raw_line):
    pairs = raw_line.rstrip().split(u" ")
    topics = [int(res.split(u":")[1]) for res in pairs]

    return topics


if __name__ == "__main__":
    main()
