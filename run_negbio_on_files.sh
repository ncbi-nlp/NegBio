#!/usr/bin/env bash

python negbio/negbio_csv2bioc.py --output $OUTPUT/report $INPUT_FILES
python negbio/negbio_pipeline.py section_split --pattern patterns/section_titles_cxr8.txt --output $OUTPUT/sections $OUTPUT/report/* --workers=6
python negbio/negbio_pipeline.py ssplit --output $OUTPUT/ssplit $OUTPUT/sections/* --workers=6
python negbio/negbio_pipeline.py parse --output $OUTPUT/parse $OUTPUT/ssplit/* --workers=6
python negbio/negbio_pipeline.py ptb2ud --output $OUTPUT/ud $OUTPUT/parse/* --workers=4
python negbio/negbio_pipeline.py dner_regex --phrases_file patterns/chexpert_phrases.yml --output $OUTPUT/dner $OUTPUT/ud/* --suffix=.chexpert-regex.xml --workers=6
python negbio/negbio_pipeline.py neg2 --output $OUTPUT/neg $OUTPUT/dner/* --workers=6
python negbio/ext/chexpert_collect_labels.py --phrases_file patterns/chexpert_phrases.yml --output $OUTPUT_LABELS $OUTPUT/neg/*
