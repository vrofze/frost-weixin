#!/bin/bash

tmp_dir=/tmp/frostwx

app_dir=/var/www/frostwx
wwwlog_dir=/var/log/www
frostwslog_dir=/var/log/www/frostwx
socket_dir=/var/www/frostwx/socket
config_dir=/var/www/config
nginx_config_dir=${config_dir}/nginx
uwsgi_config_dir=${config_dir}/uwsgi
env_dir=${app_dir}/venv

echo intall gcc,pip,virtualenv,uwsgi
if test $(gcc --version|wc -l) -eq 0
then
    apt-get install -y --force-yes build-essential
fi
if test $(pip --version|wc -l) -eq 0
then
    apt-get install -y --force-yes python-pip
fi
if test $(virtualenv --version|wc -l) -eq 0
then
    pip install virtualenv
fi
if test $(uwsgi --version|wc -l) -eq 0
then
    pip install uwsgi
fi

echo create app_dir
test -d $app_dir || mkdir $app_dir
test -d $wwwlog_dir || mkdir $wwwlog_dir
test -d $frostwxlog_dir || mkdir $frostwxlog_dir
test -d $config_dir || mkdir $config_dir
test -d $socket_dir || mkdir $socket_dir
test -d $nginx_config_dir || mkdir $nginx_config_dir
test -d $nginx_config_dir/sites-available || mkdir $nginx_config_dir/sites-available
test -d $nginx_config_dir/sites-enabled || mkdir $nginx_config_dir/sites-enabled
test -d $uwsgi_config_dir || mkdir $uwsgi_config_dir
test -d $env_dir || virtualenv -p /usr/bin/python3 $env_dir

cd $app_dir
cp frostwx_nginx.conf $nginx_config_dir/sites-available
ln -s $nginx_config_dir/sites_available/frostwx_nginx.conf $nginx_config_dir/sites-enabled/frostwx_nginx.conf
cp frostwx_uwsgi.ini $uwsgi_config_dir

echo install frostwx
${env_dir}/bin/pip install -r requirements.txt

echo reload uwsgi
if test $(ps -aux|grep "uwsgi --emperor"|wc -l) -eq 1
then
    uwsgi --emperor ${uwsgi_config_dir} --daemonize ${log_fir}/uwsgi_emperor.log
else
    touch ${uwsgi_config_dir}/frostwx_uwsgi.ini
fi

echo reload nginx
if test $(pgrep nginx|wc -l) -eq 0
then
    nginx
else
    nginx -s reload
fi

echo start uwsgi on startup
cp uwsgi.conf /etc/init
initctl reload-configuration

chown -R www-data:www-data $app_dir
chown -R www-data:www-data $socket_dir
chmod o+r ${log_dir}/*

exit 0
