#!/usr/bin/env bash

python negbio/negbio_csv2bioc.py --output $OUTPUT_DIR/report $INPUT_FILES
python negbio/negbio_pipeline.py section_split --pattern patterns/section_titles_cxr8.txt --output $OUTPUT_DIR/sections $OUTPUT_DIR/report/* --workers=6
python negbio/negbio_pipeline.py ssplit --output $OUTPUT_DIR/ssplit $OUTPUT_DIR/sections/* --workers=6
python negbio/negbio_pipeline.py parse --output $OUTPUT_DIR/parse $OUTPUT_DIR/ssplit/* --workers=6
python negbio/negbio_pipeline.py ptb2ud --output $OUTPUT_DIR/ud $OUTPUT_DIR/parse/* --workers=4
python negbio/negbio_pipeline.py dner_regex --phrases_file patterns/chexpert_phrases.yml --output $OUTPUT_DIR/dner $OUTPUT_DIR/ud/* --suffix=.chexpert-regex.xml --workers=6
python negbio/negbio_pipeline.py neg2 --output $OUTPUT_DIR/neg $OUTPUT_DIR/dner/* --workers=6
python negbio/ext/chexpert_collect_labels.py --phrases_file patterns/chexpert_phrases.yml --output $OUTPUT_LABELS $OUTPUT_DIR/neg/*
