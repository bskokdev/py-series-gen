FROM python:3.12.8-bookworm

WORKDIR /py-series-gen
COPY . /py-series-gen/

RUN apt-get update && apt-get install -y curl
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "py_series_gen.py"]