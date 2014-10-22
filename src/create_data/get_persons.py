import cPickle
import re

def process_line(line, t2i, i2t, outfile):
    ''' 
    Find all person's ID, They have to link to the category 
    'Living_people'
    '''
    pattern = "\((\d+),'(.*?)',(.*?)\)"
    for match in re.finditer(pattern, line):
        topage, category, _ = match.groups()
        if category == "Living_people":
            outfile.write(topage)
            outfile.write('\n')

def main(out_dir):
    '''
    Reads categorylinks.sql line by line and processes it. Needs the pickled 
    dictionary mapping page names to IDs '''
    print "Getting person's ID..."
    crap = 'INSERT INTO `categorylinks` VALUES'
    pickle = 'title-ID_dict.pickle'
    t2i = cPickle.load(open(out_dir + pickle, 'rb'))
    i2t = cPickle.load(open(out_dir + 'ID-title_dict.pickle', 'rb'))

    with open(out_dir + 'person_id.txt', 'w') as outfile:
        for line in open(out_dir + 'categorylinks.sql'):
            if line[:len(crap)] == crap: 
                process_line(line, t2i, i2t, outfile)
                
    print "Getting person's ID... Done."

if __name__ == "__main__":
    main("../../data/")
