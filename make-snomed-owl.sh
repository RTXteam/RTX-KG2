#!/bin/bash
# java -jar snomed-owl-toolkit-2.0.1-executable.jar rf2-to-owl -rf2-snapshot-archives SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z.zip
unzip SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z.zip
SNOMEDToOWL -f xml SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z/Snapshot SNOMEDToOWL/sct_core_us_gb.json -o snomed.owl
