#!/bin/bash
# Mini Linux CTF setup script
# Creates files and permissions for the lab

set -e

mkdir -p ~/ctf/{logs,bin,secure,notes}

# Navigation flag
echo "FLAG{navigation_master}" > ~/ctf/notes/flag1.txt

# Log / pipes flag
cat <<LOGS >> ~/ctf/logs/auth.log
User login failed from 10.0.0.23
ERROR: invalid password attempt
FLAG{pipe_detective}
ssh connection closed
LOGS

# Permissions flag
echo "Top Secret" > ~/ctf/secure/flag2.txt
chmod 000 ~/ctf/secure/flag2.txt

# Execute permission flag
cat <<'SCRIPT' > ~/ctf/bin/runme.sh
#!/bin/bash
echo "FLAG{execute_permission}"
SCRIPT

chmod 644 ~/ctf/bin/runme.sh

echo "CTF setup complete."
