import logging
logging.basicConfig(filename='example.log',filemode='w',level=logging.INFO)
logging.info('I have a car')
logging.info('I know things')
with open('example.log','r') as fp:
    print([i.split(':') for i in fp.readlines()])