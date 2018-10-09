#!/bin/bash
command=${1:-/bin/bash};shift
args=$*
export PGDATABASE=egfds
export PGUSER=root
export PGHOST=postgres-dev
case $args in
    live)
        export PGHOST=postgres-live
    ;;
esac

case $command in
     connect|c)
        psql egfds
        ;;
     dump|d)
        date=`date '+%Y%m%d%H%M%S'`;
        dir=/data/db-data/backup/$args;
        mkdir -p $dir;
        lpg_dump -s egfds > $dir/backup-${date}.dump
        ;;
    *)
        ${command} ${*}
        ;;
esac