#!/bin/bash

# Import utils.
source $PYESSV_WRITER_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "writing AMF vocabs ..."

	declare source=$1

	python $PYESSV_WRITER_HOME/sh/write_amf_cvs.py --source=$source

	log "AMF vocabs written to "$HOME/.esdoc/pyessv-archive
}

# Invoke entry point.
main $1
