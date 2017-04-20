#!/bin/bash
(echo -n $(date --utc +%FT%TZ) && uptime) >> /var/uhcm/log/uptime.log
(echo -n $(date --utc +%FT%TZ) && uptime) >> /var/kmetlog/log/uptime.log
