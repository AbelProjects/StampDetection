FROM python:3.8-slim

RUN apt-get update && apt-get install wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev -y
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz \
    && tar -xf poppler-data-0.4.9.tar.gz \
    && cd poppler-data-0.4.9 \
    && make install \
    && cd .. \
    && wget https://poppler.freedesktop.org/poppler-20.08.0.tar.xz \
    && tar -xf poppler-20.08.0.tar.xz \
    && cd poppler-20.08.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig

#Set working directory to app
WORKDIR /usr/app

#Copy over files to app directory
COPY ./requirements.txt ./

#Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Copy rest of files over to working directory
COPY ./ ./

CMD ["flask", "run", "--host", "0.0.0.0" ]
