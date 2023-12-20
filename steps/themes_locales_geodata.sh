#!/usr/bin/env bash

function themes_locales_geodata() {
    # script to execute
    SCRIPT="/apps/utility/themes_locales_geodata_dist.sh"

    # get themes version from version.ini
    THEMES_VERSION=$(cat version.ini | sed -n '/themes/ p' | sed 's/themes=//')

    # get locales version from version.ini
    LOCALES_VERSION=$(cat version.ini | sed -n '/locales/ p' | sed 's/locales=//')

    # get geodata version from version.ini
    GEODATA_VERSION=$(cat version.ini | sed -n '/geodata/ p' | sed 's/geodata=//')

    # run script
    echo "Run script to update distribution with locales, themes, geodata"
    ssh -i ~/.ssh/id_rsa $STATIC_HOST_SSH_STRING "bash ${SCRIPT} ${VERSION} ${THEMES_VERSION} ${LOCALES_VERSION} ${GEODATA_VERSION}"
}
