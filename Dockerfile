FROM python:3
ADD src/main.py /

CMD [ "python", "./main.py" ]
