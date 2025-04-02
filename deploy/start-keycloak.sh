#!/bin/sh

docker run --name keycloak -p 8443:8443 -p 9000:9000 \
        -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD} \
        -e KC_DB_URL=${KC_DB_URL} -e KC_DB_USERNAME=${KC_DB_USERNAME} -e KC_DB_PASSWORD=${KC_DB_PASSWORD}
        keycloak \
        start --optimized --hostname=localhost
