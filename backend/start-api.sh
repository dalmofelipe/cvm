#!/bin/bash

echo "iniciando api rest"

uvicorn cvm.api.main:app --reload