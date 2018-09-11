if [[ `pwd` == *'test_crawler/bin' ]]; then
    cd ..
fi

git pull
cd src/crawler/tutorial
scrapy crawl tutorial
#rm -rf .venv && virtualenv --no-site-packages --python=python3.7 .venv
#source .venv/bin/activate && pip install -r requirements.txt
#cd src && python setup.py install
#cd ../bin && sh stop.sh && sh start.sh