#FROM dperson/openvpn-client
FROM nikolaik/python-nodejs:python3.11-nodejs20
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get install -y openvpn \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app

RUN chmod 777 /app
WORKDIR /app

RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
# Run the VPN script when the container starts
EXPOSE 7860
#CMD ["sh","/start_vpn.sh"]
CMD ["python", "-m", "YukkiMusic"]
