FROM postgres:10-alpine

COPY pgpass /root/.pgpass
COPY entrypoint.sh /entrypoint.sh
COPY host_data /tmp
RUN     chmod 600 /root/.pgpass; \
        chmod a+x /entrypoint.sh; \
        cat /tmp/host_data >> /etc/hosts;
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "bash" ]