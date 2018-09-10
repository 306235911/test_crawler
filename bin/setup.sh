if [[ `pwd` == *'test_crawler' ]]; then
    cd ..
fi

git pull
rm -rf .venv && virtualenv --no-site-packages --python=python3.5 .venv
source .venv/bin/activate && pip install -r requirements.txt
#cd src && python setup.py install
#cd ../bin && sh stop.sh && sh start.sh