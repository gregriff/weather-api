#!/bin/sh

# docker run --name keycloak-dev -p 8080:8080 -m 1g \
#         -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
#         -v ./etc/keycloak/data/realm.json:/opt/keycloak/data/import \
#         quay.io/keycloak/keycloak:latest \
#         start-dev --import-realm

# run this first-time, create realm in UI, export realm to json file for subsequent runs
docker run --name keycloak-dev -p 8080:8080 -m 1g \
        -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
        quay.io/keycloak/keycloak:latest \
        start-dev
