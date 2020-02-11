FROM frater

ADD diva/ diva/
ADD setup.py setup.py

RUN python setup.py install

RUN rm -rf diva/ setup.py