The repository contains:
 \\   - directory people_data contains all the people file (name, surname, age) generated from randat.com 
 \\   - directory people_preferences contains all the people files with all the people preferences for each category, this directory is generated from the file 'generator_preferences.ipynb'
 \\   - directory work_preferences contains all the work files with all the work preferences for each category, this directory is generated from the the file 'generator_preferences.ipynb'
    - directory people_score contains all the people score file generated from the file 'score_computation', sorted in decreasing order, for each category
    - directory people_match contains all the people-work pairs file for each category, this files are generated from the file 'stable_matching_worker.py'
    - directory final_data contains all the free workplace, represented by the value 0, for each job in each category, this directory is generated from the file 'generator_works_data_ipynb'
    
THE COMBINATION OF ALL THE UNDERLYING FILES REPRESENT THE ENTIRE DATASET:
  IN ORDER: 
      generator_people_csv.ipynb -> does the merge of all the random files in the directory people_data and delete the invalid/duplicate values
      add_columns.ipynb -> add all the parameters for each person 
      generator_works_data -> generates the work dataset
      generator_preferences.ipynb -> generates all the people and work preferences 
      score_computation.ipynb  ->  generates all the people score 

STABLE MATCHING ALGORITHM:
    is the file stable_matching_worker that generates the stable mathching contained in the directory people_match 
    
***TO TEST THE PROJECT IS ENOUGH COMPILE THE FILE STABLE_MATHCING_WORKER THAT WILL MANAGE THE DATASET***
TIME TO MATCH ALL THE PEOPLE IS ABOUT 2 hours and 40 minutes 
      
    
