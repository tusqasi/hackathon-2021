# TEAM Hackerz Prototype for TECHNOVATION hackathon

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![opencv](https://img.shields.io/badge/opencv-377600?style=for-the-badge&logo=opencv&logoColor=white)

This the prototype of a basic road and traffic safety.  

This prototype uses multiple haar cascade classifier to detect different entities in the frame.

When a human is found a warning is emitted.

## Cascade classifier
These are entity recognizers. These recognize features starting from large feature going through small features. 

It stops when any large feature doesn't match it skips the entity, when all larger features are matched it start this process with smaller features.

## Installation

These are the steps to install all the requirements for the project.

Clone and cd into the repo
```md
git clone https://github.com/tusqasi/hackathon-2021
cd hackathon-2021
```

Now install the dependencies
```md
python -m venv .env
pip install -r requirements.txt
```

## Usage

Just run
```md
python speed_det.py
```

To exit press q, Escape or Enter while focused on the window.

## Flowchart

![Flowchart](https://raw.githubusercontent.com/tusqasi/hackathon-2021/master/Flowchart.png)