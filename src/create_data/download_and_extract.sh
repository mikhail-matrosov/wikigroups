curl http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz > ../../data/simplewiki-latest-page.sql.gz --progress-bar
gunzip -c ../../data/*page.sql.gz > ../../data/page.sql

curl http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pagelinks.sql.gz > ../../data/simplewiki-latest-pagelinks.sql.gz --progress-bar
gunzip -c ../../data/*pagelinks.sql.gz > ../../data/pagelinks.sql

curl http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-categorylinks.sql.gz > ../../data/simplewiki-latest-categorylinks.sql.gz --progress-bar
gunzip -c ../../data/*categorylinks.sql.gz > ../../data/categorylinks.sql
