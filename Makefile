# Makefile for source rpm: mc
# $Id$
NAME := mc
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
