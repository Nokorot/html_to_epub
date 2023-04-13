#!/bin/sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
THIS_DIR=$(basename "$SCRIPT_DIR")

echo $THIS_DIR

_sed() {
    sed "s,<+TITLE+>,$TITLE,g;\
         s,<+AUTHOR+>,$AUTHOR,g;\
         s,<+FOLDERNAME+>,$FOLDERNAME,g;\
         s,<+COVER_IMAGE+>,$COVER_IMAGE,g;\
         s,<+ENTRY_POINT+>,$ENTRY_POINT,g" \
        "$1"
}


main() {
    pushd $SCRIPT_DIR/.. >/dev/null
    echo "TITLE       : " "'$TITLE'"
    echo "AUTHOR      : " "'$AUTHOR'"
    echo "FOLDERNAME  : " "'$FOLDERNAME'"
    echo "COVER_IMAGE : " "'$COVER_IMAGE'"
    echo "ENTRY_POINT : " "'$ENTRY_POINT'"
    
    [ -z "$FOLDERNAME" ] && {
        echo "ERROR: The FOLDERNAME most be spesified" > /dev/stderr
    }

    [ -d "$FOLDERNAME" ] && {
        echo "ERROR: The folder '$FOLDERNAME' already exists!" > /dev/stderr
        exit 1
    }
        
    echo $THIS_DIR

    mkdir "$FOLDERNAME"
    _sed "$THIS_DIR/config.yaml" > "$FOLDERNAME/config.yaml"
    _sed "$THIS_DIR/cbs.py"      > "$FOLDERNAME/cbs.py"

    popd >/dev/null
}

unset TITLE
unset AUTHOR
unset FOLDERNAME
unset COVER_IMAGE
unset ENTRY_POINT

# Read arguments
POSITIONAL=()
while [[ $# -gt 0 ]]; do
case $1 in
    --config)         source "$2"; shift;;

    -t|--title)       TITLE="$2";      shift ;;
    -a|--author)      AUTHOR="$2";      shift ;;
    -f|--folder-name) FOLDERNAME="$2";  shift ;;
    -c|--cover-image) COVER_IMAGE="$2"; shift ;;
    -e|--entry-point) ENTRY_POINT="$2"; shift ;;
    -h|-?|--help) _usage; exit 0 ;;
    -*) echo "Invalid option '$1'" > /dev/stderr; exit 1 ;;
    *) POSITIONAL+=("$1") ;;
esac; shift;
done
main "${POSITIONAL[@]}"
