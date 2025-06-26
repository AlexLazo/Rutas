#!/usr/bin/env bash
# Script de construcción para Railway

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del sistema si es necesario
pip install --upgrade setuptools wheel

# Instalar las dependencias Python en el orden correcto
pip install numpy>=1.21.0,<2.0.0
pip install pandas>=1.5.0,<2.1.0

# Instalar el resto de dependencias
pip install -r requirements.txt
