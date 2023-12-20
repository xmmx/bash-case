#!/usr/bin/env bash

########
# THIS SCRIPT PLACED in /apps/utility/ ON cdn server and run by travis (steps/themes_locales_geodata.sh:17)
# Put correct versions of [themes, locales, geodata] products into distribution package and cdn.
# 
########

# script.sh 8.5.0 2.0.0 2.0.0 2.0.0
PRODUCT_VERSION=$1
THEMES_VERSION=$2
LOCALES_VERSION=$3
GEODATA_VERSION=$4
CDN_PATH="/apps/static/cdn"
THEMES_PATH="${CDN_PATH}/themes/${THEMES_VERSION}"
LOCALES_PATH="${CDN_PATH}/locales/${LOCALES_VERSION}"
GEODATA_PATH="${CDN_PATH}/geodata/${GEODATA_VERSION}"

RELEASE="${CDN_PATH}/releases/${PRODUCT_VERSION}"
RELEASE_THEMES_PATH="${RELEASE}/themes"
RELEASE_LOCALES_PATH="${RELEASE}/locales"
RELEASE_GEODATA_PATH="${RELEASE}/geodata"

INSTALL_PACKAGE_NAME="installation-package-${PRODUCT_VERSION}.zip"

echo " ===="
echo "| VERSION: ${PRODUCT_VERSION}"
echo "| THEMES: ${THEMES_VERSION}"
echo "| LOCALES: ${LOCALES_VERSION}"
echo "| GEODATA: ${GEODATA_VERSION}"
echo " ===="

echo "clean release folders"
rm -rf ${RELEASE_THEMES_PATH}
rm -rf ${RELEASE_LOCALES_PATH}
rm -rf ${RELEASE_GEODATA_PATH}

echo
echo "copy themes, locales, geodata releases to product release"
cp -r ${THEMES_PATH} ${RELEASE_THEMES_PATH}
cp -r ${LOCALES_PATH} ${RELEASE_LOCALES_PATH}
cp -r ${GEODATA_PATH} ${RELEASE_GEODATA_PATH}

echo
echo "build resources.json"
python /apps/utility/generate_resources_json.py ${RELEASE}

echo
echo "rebuild installation package"
rm ${RELEASE}/${INSTALL_PACKAGE_NAME}
cd ${RELEASE}
zip -q -r ${INSTALL_PACKAGE_NAME} *

echo
# create latest release if it was release (eg. 8.5.0)
# if there was release higher (eg 8.5.1) and you re-release 8.5.0
# it will override v8 folder, so be careful
if [[ "${PRODUCT_VERSION}" =~ ^([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
    echo "Update major release (v8)"
    MAJOR_VERSION=$(tr "." "\n" <<< ${PRODUCT_VERSION} | sed -n '1 p')
    MAJOR_RELEASE="${CDN_PATH}/releases/v${MAJOR_VERSION}"
    rm -rf ${MAJOR_RELEASE}
    cp -r ${RELEASE} ${MAJOR_RELEASE}
fi

