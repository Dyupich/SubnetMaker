FROM python
COPY . .
WORKDIR .
RUN python ./SubnetMaker.py
CMD ["python", "./SubnetMaker.py"]