#!/bin/bash
echo "TASK: Entrypoint script started"
export MONGO_DB_DATA=$PYTHAGORA_DATA_DIR/mongodata
mkdir -p $MONGO_DB_DATA

# Start MongoDB in the background
mongod --dbpath "$MONGO_DB_DATA" --bind_ip_all >> $MONGO_DB_DATA/mongo_logs.txt 2>&1 &

# Loop until MongoDB is running (use pgrep for speed)
for ((i=0; i<10*5; i++)); do
  if pgrep -x mongod > /dev/null; then
    echo "TASK: MongoDB started"
    break
  fi
  sleep 0.2
done

export DB_DIR=$PYTHAGORA_DATA_DIR/database

chown -R devuser: $PYTHAGORA_DATA_DIR
su -c "mkdir -p $DB_DIR" devuser

# Ensure code-server directories have correct permissions
chown -R devuser:devusergroup /usr/local/share/code-server
chmod -R 755 /usr/local/share/code-server

set -e

# Start the VS Code extension installer/HTTP server script in the background
su -c "cd /var/init_data/ && ./on-event-extension-install.sh" devuser

# Set up git config
su -c "git config --global user.email 'devuser@pythagora.ai'" devuser
su -c "git config --global user.name 'pythagora'" devuser

# Mark entrypoint as done
su -c "touch /tmp/entrypoint.done" devuser

echo "FINISH: Entrypoint script finished"

# Keep container running
tail -f /dev/null
