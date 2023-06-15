FROM postgres:latest
# copy init.sh to container
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
RUN sed -i -e 's/\r$//' docker-entrypoint-initdb.d/init.sh
# copying postgres config to container
COPY ./postgresql.conf etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]
