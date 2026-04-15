# BSc Thesis Data Repository

This repository contains the data and supporting materials associated with my BSc Computer Science thesis.

## Repository contents

### `transcripts/`
This folder contains the cleaned and anonymized interview transcripts used in the study.

### `scripts/`
This folder contains the scripts used in the transcription workflow:
- `transcribe_videos.py`: used to transcribe interview recordings
- `rename_speakers.py`: used to standardize speaker labels in transcripts

### `full-project/`
This folder contains materials exported from ATLAS.ti:
- `Thesis-excel.xlsx`: Excel export of coding and analysis results
- `Thesis-atlasti.atlasti`: ATLAS.ti project file

### `interview_guide.pdf`
The interview guide used during data collection.

### `requirements.txt`
Python dependencies used for the transcription scripts.

## Anonymization

The transcripts included in this repository are cleaned and anonymized versions. Direct personal identifiers (such as names, organizations, or locations) have been removed or replaced where necessary.

## Reproducibility

This repository includes intermediate data and scripts used during the data processing and analysis workflow, to support transparency and reproducibility of the study.

To install dependencies for the scripts:

```bash
pip install -r requirements.txt
