FROM python:3.9

RUN useradd -m jimbo

# set the working directory in the container
WORKDIR /home/jimbo

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./service1 ./service1

RUN chown -R jimbo:jimbo ./

USER jimbo

EXPOSE 3000

CMD python3.9 -m uvicorn service1:app --port 3000 --host 0.0.0.0
