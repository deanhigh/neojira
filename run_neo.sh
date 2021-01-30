#!/bin/bash 

docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=neodata:/data \
    --volume=neologs:/logs \
    neo4j

