FROM python:3.6

COPY . /node
WORKDIR /node

RUN pip install -r requirements.txt
RUN curl -o /usr/local/bin/jq http://stedolan.github.io/jq/download/linux64/jq && chmod +x /usr/local/bin/jq

CMD ["python node.py"]
