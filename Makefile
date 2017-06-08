install:
	-groupadd toughee
	-useradd toughee -g toughee -M -d /var/toughee -s /bin/false
	-mkdir -p /var/toughee/lib
	-mkdir -p /var/toughee/data
	install /opt/toughee/lib/python2.7/site-packages/OpenSSL/libssl.so.1.0.0 /var/toughee/lib/libssl.so.1.0.0
	install /opt/toughee/lib/python2.7/site-packages/OpenSSL/libcrypto.so.1.0.0 /var/toughee/lib/libcrypto.so.1.0.0
	install /opt/toughee/lib/python2.7/site-packages/OpenSSL/libssl.so.1.0.0 /var/toughee/lib/libssl.so.10
	install /opt/toughee/lib/python2.7/site-packages/OpenSSL/libcrypto.so.1.0.0 /var/toughee/lib/libcrypto.so.10
	install /opt/toughee/lib/libmysqlclient.so.18 /var/toughee/lib/libmysqlclient.so.18
	install /opt/toughee/lib/libpgm-5.2.so.0 /var/toughee/lib/libpgm-5.2.so.0
	install /opt/toughee/lib/libzmq.so.3 /var/toughee/lib/libzmq.so.3
	echo "/var/toughee/lib" >> /etc/ld.so.conf && ldconfig
	install etc/toughee.service /usr/lib/systemd/system/toughee.service
	install -m 0755 /opt/toughee/bin/toughkey  /usr/local/bin/toughkey
	install -m 0755 /opt/toughee/radiusctl  /usr/local/bin/radiusctl
	chown -R toughee /opt/toughee
	chown -R toughee /var/toughee
	chmod +x /opt/toughee/radiusctl
	systemctl enable toughee && systemctl daemon-reload

upgrade-libs:
	bin/pip install -r requirements.txt

initdb:
	bin/python radiusctl initdb -f -c etc/toughee.json
	chown -R toughee /var/toughee

updb:
	bin/python radiusctl updb -c etc/toughee.json
	chown -R toughee /var/toughee

backup:
	bin/python radiusctl backup -c etc/toughee.json
	chown -R toughee /var/toughee

clean-build:
	sh release.sh clean

buildver:
	sh release.sh buildver

package:
	sh release.sh package

patch:
	sh release.sh patch

run:
	python radiusctl standalone -c testdata/master.json

freerun:
	python freectl standalone -c testdata/master.json

freesspd:
	python freectl ssportal -c testdata/master.json

sspd:
	python radiusctl ssportal -c testdata/master.json

wland:
	python radiusctl wlanportal -lp 50100 -c testdata/master.json

acsim:
	python radiusctl acsim -c testdata/master.json

mpd:
	export DEV_OPEN_ID=oFXX6s_ftj6LOYDodkcxoHNjlXj0;\
	python radiusctl mpd -c testdata/master.json

runs:
	python radiusctl standalone -c testdata/slave.json

suprun:
	python radiusctl daemon -s startup -n -c testdata/toughee.conf

shell:
	python radiusctl shell -c testdata/master.json

test:
	python radiusctl initdb -f -c toughradius/tests/test.json;\
	trial toughradius.tests

inittest:
	python radiusctl initdb -c testdata/master.json
	python radiusctl initdb -c testdata/slave.json

uptest:
	python radiusctl updb -c testdata/master.json
	python radiusctl updb -c testdata/slave.json

baktest:
	python radiusctl backup -c testdata/master.json

dbdoc:
	python radiusctl dbdoc > docs/manual/database.rst


clean:
	rm -fr _trial_temp

all:install

.PHONY: all clean initdb install