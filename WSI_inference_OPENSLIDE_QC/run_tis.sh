#!/bin/bash
# setting
SLIDE_FOLDER="/exports/path-pulmogroep-hpc/Jurre/SalvDataset/LUMC_cohort/test_tissue"
OUTPUT_DIR=""/exports/path-pulmogroep-hpc/Jurre/SalvDataset/LUMC_cohort/test_tissue""

python wsi_tis_detect.py --slide_folder "$SLIDE_FOLDER" --output_dir "$OUTPUT_DIR"

echo "Tissue Segmentation is completed!"
