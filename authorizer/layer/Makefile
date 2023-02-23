CC = gcc
CFLAGS='-static'

DOWNLOAD_DIR=/tmp/download
GPG_BUILD_DIR=/tmp/gpg
PYTHON_DIR="$(ARTIFACTS_DIR)/python"  

build-AuthLayer:
	yum install -y gcc make glibc-static sqlite gnutls libsqlite3-dev adns-tools
	mkdir -p ${DOWNLOAD_DIR} ${PYTHON_DIR} ${GPG_BUILD_DIR}
	curl https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-2.4.0.tar.bz2 --output "$(DOWNLOAD_DIR)/gnupg.tar.bz2"
	tar -xf "$(DOWNLOAD_DIR)/gnupg.tar.bz2" --directory ${GPG_BUILD_DIR} --strip-components=1
	${GPG_BUILD_DIR}/configure
	make CFLAGS='-static'
	cp ${GPG_BUILD_DIR}/g10/gpg ${PYTHON_DIR}
	python -m pip install -r requirements.txt -t ${PYTHON_DIR}
