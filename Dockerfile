FROM python:3.6

# create directories
RUN mkdir -p /opt/app/server
RUN mkdir /opt/libfvad

# change the work directory to /tmp for the libfvad build
WORKDIR /tmp

# checkout libfvad
RUN git clone https://github.com/dpirch/libfvad.git
# change the work directory to the libfvad clone
WORKDIR /tmp/libfvad

# run autoreconf, configure and build/install with make
RUN autoreconf -i
RUN ./configure --prefix=/usr/
RUN make && make install

# change work directory to /opt/app
WORKDIR /opt/app

COPY src/web-source/requirements.txt .

RUN pip install -r requirements.txt

COPY src/web-source/main.py .
COPY src/web-source/server ./server/

COPY src/python-libfvad/* ./
RUN python setup.py build_ext --inplace

COPY resources/hello-world.wav /tmp/
COPY test.py .

CMD [ "python", "-u", "main.py" ]
# CMD ["tail" , "-f" , "/dev/null"]


