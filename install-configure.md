#Use the next commands to install / configure speech-recognition with CMUSphinx
#Open terminal on this dir

#In MacOS xcode required

sudo -i

apt -y update

apt -y upgrade

apt -y autoremove

apt install autoconf

apt install automake

apt install swig

cd sphinxbase

chmod +x ./autogen.sh

chmod +x ./configure

./autogen.sh --disable-dependency-tracking

#./configure --disable-dependency-tracking

make clean all

make install

nano /etc/ld.so.conf

#Apply the setting bellow:

include /etc/ld.so.conf.d/*.conf
/usr/local/lib


cd ../pocketsphinx

chmod +x ./autogen.sh

chmod +x ./configure

./autogen.sh

./configure

make clean all

make install

pip3 install pocketsphinx

cd ../sphinxtrain

chmod +x ./autogen.sh

chmod +x ./configure

./autogen.sh

./configure

make clean all

make install

export PATH=/usr/local/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig