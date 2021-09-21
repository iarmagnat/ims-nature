#!/usr/bin/env python
import gzip
import os
import re
from datetime import datetime

INPUT_DIR = "/var/log/nginx"

lineformat = re.compile(
    r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""",
    re.IGNORECASE)

values = {}
is_byte = False

for f in os.listdir(INPUT_DIR):
    if f.endswith(".gz"):
        logfile = gzip.open(os.path.join(INPUT_DIR, f))
        is_byte = True
    else:
        logfile = open(os.path.join(INPUT_DIR, f))
        is_byte = False

    for line in logfile.readlines():
        if is_byte:
            data = re.search(lineformat, line.decode("utf-8"))
        else:
            data = re.search(lineformat, line)
        if data:
            datadict = data.groupdict()
            ip = datadict["ipaddress"]
            datetimeobj = datetime.strptime(datadict["dateandtime"],
                                            "%d/%b/%Y:%H:%M:%S %z")  # Converting string to datetime obj
            url = datadict["url"]
            bytessent = datadict["bytessent"]
            referrer = datadict["refferer"]
            useragent = datadict["useragent"]
            status = datadict["statuscode"]
            method = data.group(6)
            if not url.endswith("/") and status == "200":
                key = str(datetimeobj.day) + "/" + str(datetimeobj.month) + "/" + str(datetimeobj.year)
                if not values.get(key):
                    values[key] = 1
                else:
                    values[key] = values[key] + 1

    logfile.close()

print(values)
