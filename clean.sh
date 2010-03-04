#!/bin/bash
find . -name "*.pyc" -exec rm '{}' ';'
find . -name "*.py~" -exec rm '{}' ';'
find . -name "*.po~" -exec rm '{}' ';'
find . -name "*.mo~" -exec rm '{}' ';'
find . -name "*.html~" -exec rm '{}' ';'
find . -name "*.css~" -exec rm '{}' ';'
