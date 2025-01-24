# judge-sort

`judge-sort` is a python script designed to make the sorting & grouping of judges easy based off a wide range of variables.

## Key features

- Automatically identifies conflicts of interest based on company associations, brand involvement, and other criteria.
- Dynamically assigns judges to teams, ensuring diversity in terms of company type, job role, seniority, and more.
- Data Validation and Cleaning: Processes and validates input data to ensure accuracy and completeness before allocation.
- Supports flexible team size configurations.
- Exports team assignments and conflict summaries to Excel files for easy review.

## How to use
This tool is to be used with the output CSV of our google form. Once this form has been downloaded, it can be placed into a `data-in` folder next to the script. Once the script has completed, it will have output as many excel sheets as there are sessions. 

To run this script you need to have python (tested with 3.12) installed and the modules in requirements installed. To do this, and run the program you can run the following commands:

```bash
pip install -r requirements.txt
python3 judge-sort.py
```

## Development
Whilst developing this tool, I used github projects to create simple to understand tickets. I chose to use github projects as it very closely links with the rest of github, letting me track progress within pull requests / issues

Whilst writing these tickets, I aimed to write them as cronologically as possible, this means that I am able to go ticket - by - ticket

As I progress throughout the project I update each ticket, making it far easier to track progress & understand what part of the program is next. 

### Test driven development
Whilst writing some of the features for seperating out groups, I utilised test functions that allowed me to evaluate how equally groups were being distributed. This was quite helpful as it allowed me to quickly notice edge cases that weren't being handled. Most of this testing exists in `development.ipynb`.

## Evaluation
In its current state, the program does what I set out for it to do. However, there are improvements that can be made:

- Matching groups with what to judge
- giving more control over the balance of groups
- Checking companies

As this project is part of an assignment, all these future developments will be made in a seperate branch