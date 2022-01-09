FROM python:3
ADD src/main.py /
RUN chmod +x main.py
ENTRYPOINT [ "python",  "./main.py" ]
#CMD ["python", "./main.py", "File name"]