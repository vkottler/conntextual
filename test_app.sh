#!/bin/bash

./venv/bin/conntextual ui --udp 10000 \
	package://conntextual/json.yaml \
	package://conntextual/sample.yaml "$@"
