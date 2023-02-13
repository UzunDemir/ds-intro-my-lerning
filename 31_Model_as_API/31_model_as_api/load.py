import requests
import random
import time
from concurrent.futures import ProcessPoolExecutor
import datetime
from statistics import median

import psutil  # Нужно установить


def load_cpu(duration):
    t = time.time()
    while (time.time() - t) <= duration:
        _ = pow(random.randint(1, 1000), 32)


def main(path):
    head = '''
CREATE DATABASE /*!32312 IF NOT EXISTS*/`monitoring` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `monitoring`;

CREATE USER 'grafana'@'%' IDENTIFIED BY '123456';
GRANT SELECT ON `monitoring`.* TO 'grafana'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'p76Se7BoVbrn';
FLUSH PRIVILEGES;

FLUSH PRIVILEGES;

DROP TABLE IF EXISTS `metrics`;

CREATE TABLE `metrics` (
    `timestamp` datetime NOT NULL,
    `cpu_usage` decimal(5, 2) NOT NULL,
    `mem_available` bigint NOT NULL,
    `reqs_per_min` int(11) NOT NULL,
    `time_of_proc` decimal(5, 2) NOT NULL,
    PRIMARY KEY (timestamp)
) ENGINE=InnoDB;
    
INSERT  INTO `metrics`(`timestamp`,`cpu_usage`, `mem_available`, `reqs_per_min`, `time_of_proc`) VALUES
'''

    cpu_loader = ProcessPoolExecutor()

    date_now = datetime.datetime.utcnow() - datetime.timedelta(hours=10)

    with open(path, 'w') as out:
        out.write(head)
        for i in range(720):
            t1 = time.time()
            times = []
            count = 0
            while True:
                t2 = time.time()

                r = requests.post('http://127.0.0.1:8000/predict', json={
                    "description": "Lorem ipsum dolor sit amet",
                    "fuel": "gas",
                    "id": random.randint(1, pow(2, 32)),
                    "image_url": "https://images.craigslist.org/00808_i0faaALGPQxz_0CI0t2_600x450.jpg",
                    "lat": 39.1618,
                    "long": -76.6297,
                    "manufacturer": "ford",
                    "model": "mustang",
                    "odometer": random.randint(1000, 500000),
                    "posting_date": "2021-05-03T19:49:21-0400",
                    "price": random.randint(1000, 500000),
                    "region": "baltimore",
                    "region_url": "https://baltimore.craigslist.org",
                    "state": "md",
                    "title_status": "clean",
                    "transmission": "manual",
                    "url": "https://baltimore.craigslist.org/cto/d/glen-burnie-mustang-50-convertible-2013/7316509996.html",
                    "year": 2013
                })

                count += 1
                times.append(time.time() - t2)

                if time.time() - t1 > 1.:
                    if i > 0:
                        out.write(',\n')

                    if random.randint(0, 1):
                        cpu_loader.submit(load_cpu, random.randint(1, 10))

                    out.write(f'("{date_now}", {psutil.cpu_percent()}, {psutil.virtual_memory().available},' +
                              f' {count}, {median(times)*1000:.2f})')
                    out.flush()
                    date_now += datetime.timedelta(minutes=1)
                    break

        out.write(';\n')


if __name__ == '__main__':
    main('grafana.sql')
