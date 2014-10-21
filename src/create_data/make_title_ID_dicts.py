#!/usr/bin/python
import cPickle
import re


def process_line(line, d):
    ''' gets the ID and name for each page in the line '''
    pattern = "\((\d+),(\d+),'(.*?)','"
    for match in re.finditer(pattern, line):
        ID, namespace, name = match.groups()
        if namespace == '0' or namespace == '14':
            d[name] = int(ID)


def main(out_dir, in_dir='../../data/', infile='page.sql'):
    ''' Reads page.sql line by line and processes it '''
    print 'making title <--> ID dictionaries...'
    crap = 'INSERT INTO `page` VALUES'
    t2id = {}
    for line in open(in_dir + infile):
        if line[:len(crap)] == crap:
            process_line(line, t2id)
    id2t = {v: k for k, v in t2id.iteritems()}
    cPickle.dump(t2id, open(out_dir + 'title-ID_dict.pickle', 'wb'), 2)
    cPickle.dump(id2t, open(out_dir + 'ID-title_dict.pickle', 'wb'), 2)
    print 'making title <--> ID dictionaries... Done.'

if __name__ == "__main__":
    main()
