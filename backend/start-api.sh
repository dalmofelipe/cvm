#!/bin/bash

echo "iniciando api rest"

uvicorn cvm.api:api --reload