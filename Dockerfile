FROM python:3
ADD src/main.py /
RUN chmod +x main.py
ADD / /usr/local
ENTRYPOINT [ "python",  "./main.py" ]
