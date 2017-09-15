#!/bin/bash

if [ "$#" -lt 1 ];then
	echo "Usage: $0 <install folder (absolute path)>"
	echo "For sudoer recommend: $0 /opt"
	echo "For normal user recommend: $0 $HOME/app"
	exit 0
fi

echo -n "installing dcm4che..." #-n without newline

DEST=$1
mkdir -p $DEST

VERSION=dcm4che-3.3.8
DCM4CHE_DIR=$DEST/$VERSION
if [ -d $DCM4CHE_DIR ]; then
	rm -rf $DCM4CHE_DIR
fi
echo wget https://sourceforge.net/projects/dcm4che/files/dcm4che3/3.3.8/$VERSION-bin.zip/download/

wget -O temp.zip https://sourceforge.net/projects/dcm4che/files/dcm4che3/3.3.8/$VERSION-bin.zip/download/ 
unzip temp.zip -d $DEST
rm temp.zip

# bash
PROFILE=~/.bashrc
#check if PATH already exist in $PROFILE
if grep -q "PATH=$DCM4CHE_DIR/bin:\$PATH" $PROFILE #return 0 if exist
then 
	echo "PATH=$DCM4CHE_DIR/bin" in the PATH already.
else
	echo "export PATH=$DCM4CHE_DIR/bin:\$PATH" >> $PROFILE
fi

source $PROFILE

LETSENCRYPT_CA_URL=https://letsencrypt.org/certs/letsencryptauthorityx3.pem.txt
for f in $(find ${DCM4CHE_DIR}/etc -name cacerts.jks)
do
  keytool -noprompt -importcert -trustcacerts -alias letsencrypt -file <(wget -O - -o /dev/null ${LETSENCRYPT_CA_URL}) -keystore $f -storepass secret
done

#test installation
source $PROFILE
dcmdump -h
if [ $? -eq 0 ]; then
	echo ' '
	echo "OK. To update PATH of current terminal: source $PROFILE"
	echo 'use this command to test retrieve(by StudyInstanceUID):'
	echo 'getscu --bind DEFAULT --connect CFMM-Public@dicom.cfmm.robarts.ca:11112 --tls-aes --user YOUR_UWO_USERNAME --user-pass YOUR_PASSWORD, -m StudyInstanceUID=1.3.12.2.1107.5.2.34.18932.30000017052914152689000000013'
else
    echo 'FAIL.'
fi

#by PatientID
#getscu  -L PATIENT -M PatientRoot --bind DEFAULT --connect CFMM-Public@dicom.cfmm.robartsa:11112 --tls-aes --user YOUR_UWO_USERNAME --user-pass YOUR_PASSWORD, -m 00100020=17.05.29-15:47:03-DST-1.3.12.2.1107.5.2.34.18932

