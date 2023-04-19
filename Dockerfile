ARG BASE_IMAGE=python:3.8-alpine3.12
FROM ${BASE_IMAGE}

ARG GIT_BRANCH
ARG GIT_COMMIT_ID
ARG GIT_BUILD_TIME
ARG GITHUB_RUN_NUMBER
ARG GITHUB_RUN_ID
ARG PROJECT_URL
ARG PACKAGE_NAME

LABEL git.branch=${GIT_BRANCH}
LABEL git.commit.id=${GIT_COMMIT_ID}
LABEL git.build.time=${GIT_BUILD_TIME}
LABEL git.run.number=${GITHUB_RUN_NUMBER}
LABEL git.run.id=${GITHUB_RUN_ID}
LABEL org.opencontainers.image.authors="support@sixsq.com"
LABEL org.opencontainers.image.created=${GIT_BUILD_TIME}
LABEL org.opencontainers.image.url=${PROJECT_URL}
LABEL org.opencontainers.image.vendor="SixSq SA"
LABEL org.opencontainers.image.title="NuvlaEdge Base"
LABEL org.opencontainers.image.description="Contains common software to serve as base image for NuvlaEdge components"

COPY LICENSE /opt/nuvlaedge/

WORKDIR /opt/nuvlaedge/
COPY ${PACKAGE_NAME} /tmp/${PACKAGE_NAME}

RUN pip install /tmp/${PACKAGE_NAME}
