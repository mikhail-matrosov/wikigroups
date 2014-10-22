import make_title_ID_dicts
import make_graph
import compactify
import pagerank
import get_persons
from sys import argv


out_dir = '../../data/'


def test():
    '''
    Does everything, prints top 10 results. needs page.sql and
    pagelinks.sql files which can be downloaded using
    download_and_extract.sh
    '''
    make_title_ID_dicts.main(out_dir=out_dir)
    get_persons.main(out_dir=out_dir)
    make_graph.main(out_dir=out_dir)
    compactify.main(out_dir=out_dir)
    pagerank.main()


def actual(outfile='pageranked.txt'):
    ''' does everything and writes all results to file '''
    make_title_ID_dicts.main(out_dir=out_dir)
    make_graph.main(out_dir=out_dir)
    compactify.main(out_dir=out_dir)
    with open(out_dir + outfile, 'w') as f:
        for page in pagerank.top_k(-1):
            f.write(page + '\n')

if __name__ == '__main__':
    test() if len(argv) == 1 else actual(out_dir)
