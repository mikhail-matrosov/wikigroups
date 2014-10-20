wget http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz -P ../data/
#wget -c http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz -P ../data/
gunzip -c ../data/*page.sql.gz > ../data/page.sql
wget http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pagelinks.sql.gz -P ../data/
#wget -c http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pagelinks.sql.gz -P ../data/ 
gunzip -c ../data/*pagelinks.sql.gz > ../data/pagelinks.sql
