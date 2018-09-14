if [[ `pwd` == *'test_crawler/bin' ]]; then
    cd ..
fi

git pull
source .venv/bin/activate
cd src && python setup.py install
cd common_crawler/instance && python test_schduler.py
#scrapy crawl tutorial
#rm -rf .venv && virtualenv --no-site-packages --python=python3.7 .venv
#source .venv/bin/activate && pip install -r requirements.txt
#cd src && python setup.py install
#cd ../bin && sh stop.sh && sh start.sh