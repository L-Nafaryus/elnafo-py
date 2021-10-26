FROM bougyman/voidlinux:glibc 

LABEL maintainer="L-Nafaryus <l.nafaryus@gmail.com>" \
    description="Elnafo web server" \
    name="elnafo"

RUN set -ex \
	&& xbps-install -Suy \
        python3 \
        python3-pip \
		git \
        libmagic \
    && rm -rf /var/cache/xbps
    
RUN git clone --depth 1 https://github.com/L-Nafaryus/elnafo.git \
	&& cd elnafo \
    && python -m pip install -U pip \
    && python -m pip install -r requirements.txt \
	&& mkdir logs

WORKDIR /elnafo
EXPOSE 5000

ENTRYPOINT ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]
