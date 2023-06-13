import pandas as pd
import glob
import os
import time


def generate_people_preferences_dict():
    job_index = 0
    list_people_preferences = data_people.preferences.to_list()
    cont = 0
    for _ in list_people_preferences:
        tmp_list_people_preferences = list_people_preferences[cont].replace("[", "").replace("]", "").replace("'", "")
        people_tmp_list = tmp_list_people_preferences.split(',')
        for index in range(len(people_tmp_list)):
            people_tmp_list[index] = people_tmp_list[index].strip()
        people_pref_list = list()
        for element in people_tmp_list:
            for row in range(len(data_work)):
                if data_work.at[row, 'job name'] == element:
                    job_index = row
            job_number = data_work.at[job_index, 'job number']
            for jobs in range(job_number):
                people_pref_list.append(f'{element}_{jobs}')
        people_preferences[str(data_people.at[cont, 'name and surname'])] = people_pref_list
        cont += 1


def generate_work_preferences_dict():
    list_jobs_preferences = data_work.people.to_list()
    cont = 0
    for _ in list_jobs_preferences:
        job_tmp_list = list()
        for row in range(len(data_people)):
            job_tmp_list.append(data_people.at[row, 'name and surname'])
        for index in range(data_work.at[cont, 'job number']):
            work_preferences[str(data_work.at[cont, 'job name']) + f'_{index}'] = job_tmp_list
        cont += 1


def init_free_jobs():
    for work in work_preferences.keys():
        free_jobs.append(work)
    for person in people_preferences.keys():
        free_people.append(person)


def match(work):
    # print(f'{work} is looking for a worker')
    for possible_people in work_preferences[work]:
        is_free = True if possible_people in free_people else False
        if is_free:
            tentative_match[possible_people] = work
            free_jobs.remove(work)
            free_people.remove(possible_people)
            # print(f' the work {work} is assigned to {possible_people}')
            break
        else:
            # print(f'{possible_people} is already employed')
            current_job = people_preferences[possible_people].index(tentative_match[possible_people])
            potential_job = people_preferences[possible_people].index(work)
            if current_job <= potential_job:
                # print(f'{possible_people} doesn't want to change his/her job')
                pass
            else:
                # print(f'{possible_people} prefers to change his/her current job with {work}')
                free_jobs.remove(work)
                free_jobs.append(tentative_match[possible_people])
                tentative_match.pop(possible_people)
                tentative_match[possible_people] = work
                break


def stable_matching():
    while len(free_jobs) > 0 and len(free_people) > 0:
        work = free_jobs[0]
        match(work)


def is_smp(preferences_people, preferences_job, matching):
    for person, job in matching.items():
        if person not in preferences_people or job not in preferences_job:
            return False
        person_preferences = preferences_people[person]
        job_preferences = preferences_job[job]
        person_index = person_preferences.index(job)
        for preferred_job in person_preferences[:person_index]:
            if matching.get(preferred_job) == person:
                return False
        for other_person in job_preferences:
            if other_person == person:
                break
            if matching.get(other_person) == job:
                return False
    return True


start_time = time.time()
categories = ['economic', 'healthcare', 'informatics', 'instruction', 'worker', 'zgeneric']  # categories of jobs
path_people_files = os.getcwd() + '/people_preferences'
csv_files_people = glob.glob(os.path.join(path_people_files, '*.csv'))
path_works_files = os.getcwd() + '/work_preferences'
csv_files_work = glob.glob(os.path.join(path_works_files, '*.csv'))
people_not_accepted = list()  # list of people who have not found the job in their specific sector

for number_of_file in range(len(csv_files_people)):  # index of file in the people_preferences directory
    people_preferences = dict()  # dictionary containing pairs person and favorite job list
    work_preferences = dict()  # dictionary containing pairs job and favorite people list

    data_people = pd.read_csv(csv_files_people[number_of_file])  # dataset people    name and surname, preferences
    data_work = pd.read_csv(csv_files_work[number_of_file])  # dataset work    job name, preferences

    generate_people_preferences_dict()  # generate the people_preferences dictionary
    generate_work_preferences_dict()  # generate the work_preferences dictionary

    tentative_match = dict()  # final dictionary containing stable matching pairs of people - job
    free_jobs = list()  # list containing free jobs to assign
    free_people = list()  # list containing free people to assign

    init_free_jobs()  # initialize the dictionary with jobs/people preferences
    stable_matching()  # start the matching
    if is_smp(people_preferences, work_preferences, tentative_match):  # check if it is really a stable matching
        print(f'{categories[number_of_file]} is a stable matching')
    else:
        print(f'{categories[number_of_file]} is not a stable matching')
    match_data_frame = pd.DataFrame.from_dict(tentative_match, orient="index")  # create a csv file with all the matches
    match_data_frame.to_csv(f'{categories[number_of_file]}_match.csv')
    if len(free_people) > 0:  # added all the people who could not find work
        for people in free_people:
            people_not_accepted.append(people)
print(f'{time.time() - start_time} IS THE TIME TO FINISH THE TASK')
