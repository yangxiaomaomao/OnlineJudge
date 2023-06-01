#!/bin/bash

dd if=/dev/urandom bs=1M count=3 | base64 > client-input.dat
