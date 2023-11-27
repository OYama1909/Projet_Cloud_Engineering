FROM python:3.9


# Any working directory can be chosen as per choice like '/' or '/home' etc
# I have chosen /usr/app/src
WORKDIR /api/src

#To COPY the remote file at working directory in container
COPY store.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

#CMD instruction should be used to run the software
#contained by the image, along with any arguments.
CMD ["uvicorn", "store:app", "--host", "0.0.0.0", "--port", "80"]
