#!/bin/sh
set -e

# Fix ownership of the bind-mounted directories (runs as root)
chown -R worker:worker /data/sql /data/files

# Execute the main command as the worker user
exec gosu worker "$@"
