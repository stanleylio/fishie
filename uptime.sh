#!/bin/bash
(echo -n $(date --utc +%FT%TZ) && uptime) >> /var/kmetlog/log/uptime.log
