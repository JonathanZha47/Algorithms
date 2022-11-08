# Zora Che with adaptations from Gavin Brown
# CS330, Fall 2022
# Stable Matching Algorithm Starter Code
import ast
import sys
import time


def read_prefs(pref_1_filename, pref_2_filename):
    # This function reads preferences from two files
    # and returns two-dimensional preference lists and the length of a list.
    with open(pref_1_filename, 'r') as f:
        hospital_raw = f.read().splitlines()
    with open(pref_2_filename, 'r') as f:
        student_raw = f.read().splitlines()
    N = int(student_raw[0])
    hospital_prefs = [[int(id) for id in  x.split(',')] for x in hospital_raw[1:]]
    student_prefs = [[int(id) for id in  x.split(',')] for x in student_raw[1:]]
    return N,  hospital_prefs, student_prefs

def inverse_prefs(N, prefs):    
    ############################################################
    # Implement inverse preference lists as described in lecture
    ############################################################
    ranks = N*[0] # You'll need to replace this.
    for i in prefs:
        ranks[prefs[i]] = i
    return ranks

def run_GS(N, hospital_prefs, student_prefs, out_name):

    free_hospital = list(range(N))
    count = N*[0]               # stores a pointer to each hospital's next unproposed student, going from the left of hospital's preference list 
    current = N*[None]

    student_prefs_inverse = [[0 for j in range(N)] for x in range(N)] # stores current assignment; index -> student, value -> hospital
    for i in range(N):
        student_prefs_inverse[i] = inverse_prefs(N, student_prefs[i])[:]
    # algorithm - Hospital giving offer to student

    while free_hospital:  # returns True if list is nonempty
        #print('--------')
        #print('current:', current)
        #print('free hospital', free_hospital)
        hospital = free_hospital.pop(0)

        student = hospital_prefs[hospital][count[hospital]]
        #print(hospital, 'proposing to', student)
        count[hospital] += 1
        if current[student] is None:   # student is not paired 
            current[student] = hospital
            #print('student is not paired')
        else:
            # slow way to compute 
            if student_prefs_inverse[student][hospital] > student_prefs_inverse[student][current[student]]:
                ############################################################
                # The code in the if statement runs in linear time!
                # Fix that...
                ############################################################
                free_hospital.append(hospital)
            else:
                # student switches to new hospital, old hospital becomes free
                #print('student prefers', hospital)
                free_hospital.append(current[student])
                current[student] = hospital
    # write out matches
    with open(out_name, 'w') as f:
        for student, hospital in enumerate(current):
            f.write(str(hospital)+','+str(student)+'\n')

############################################################
# PART 2 STARTER CODE
############################################################

def check_stable(N, hospital_prefs, student_prefs, match_file):
    # Implement checking of stable matches from output
    # ...
    with open(match_file, "r") as f:
        match_raw = f.read().splitlines()
    match_result = [[int(id) for id in x.split(',')] for x in match_raw[:]]
    #print(match_result)
    match_dic = {}
    number = 1
    for key in match_result:
        match_dic[key[1]] = key[0]
    #print(match_dic)
    for pair_match in match_result:
        hospital = pair_match[0]
        student = pair_match[1]
        hospital_current_position = hospital_prefs[hospital].index(student)
        while hospital_current_position > 0:
              student_prev_index = hospital_prefs[hospital][hospital_current_position-1]
              hospital_prev_index = match_dic[student_prev_index]
              if student_prefs[student_prev_index].index(hospital) < student_prefs[student_prev_index][hospital_prev_index]:
                  number += 1
              hospital_current_position -= 1
    if number == 1:
            print(1) # if stable
    else:
            print(0)     # if not stable
    # Note: Make the printing of stableness be the only print statement for submission

############################################################
# PART 3 STARTER CODE
############################################################

def check_unique(N, hospital_prefs, student_prefs):
    # Implement checking of a unique stable matching for given preferences
    # ...
    hospital_propose = "hospital proposing"
    student_propose = "student proposing"
    run_GS(N,student_prefs,hospital_prefs,student_propose)
    run_GS(N,hospital_prefs,student_prefs,hospital_propose)

    with open(hospital_propose, "r") as f:
        hos_propose_raw = f.read().splitlines()
    hos_propose_match_result = [[int(id) for id in x.split(',')] for x in hos_propose_raw[:]]
    #print(match_result)
    hos_match_dic = {}
    for key in hos_propose_match_result:
        hos_match_dic[key[0]] = key[1]

    with open(student_propose,"r") as f:
        stu_propose_raw = f.read().splitlines()
    stu_propose_match_result = [[int(id) for id in x.split(',')] for x in stu_propose_raw[:]]
    stu_match_dic = {}
    for key in stu_propose_match_result:
        stu_match_dic[key[1]] = key[0]

    if hos_match_dic == stu_match_dic:
        print(1)     # if unique
    else:
        print(0)     # if not unique
    # Note: Make the printing of uniqueness be the only print statement for submission!
        
############################################################
# Main function. (Do not modify for submission.)
############################################################

def main():
    # Do not modify main() other than using the commented code snippet for printing 
    # running time for Q1, if needed
    if(len(sys.argv) < 5):
        return "Error: the program should be called with four arguments"
    hospital_prefs_raw = sys.argv[1] 
    student_prefs_raw = sys.argv[2]
    match_file = sys.argv[3]
    # NB: For part 1, match_file is the file to which the *output* is wrtten
    #     For part 2, match_file contains a candidate matching to be tested.
    #     For part 3, match_file is ignored.
    question = sys.argv[4]
    N, hospital_prefs, student_prefs = read_prefs(hospital_prefs_raw, student_prefs_raw)
    if question=='Q1':
        # start = time.time()
        run_GS(N, hospital_prefs,student_prefs,match_file)
        # end = time.time()
        # print(end-start)
    elif question=='Q2':
        check_stable(N, hospital_prefs, student_prefs, match_file)
    elif question=='Q3':
        check_unique(N, hospital_prefs, student_prefs)
    else:
        print("Missing or incorrect question identifier (it should be the fourth argument).")
    return

if __name__ == "__main__":
    # example command: python stable_matching.py pref_file_1 pref_file_2 out_name Q1
    
    # stable_matching.py: filename; do not change this
    # pref_file_1: filename of the first preference list (proposing side)
    # pref_file_2: filename of the second preference list (proposed side)
    # out_name: desired filename for output matching file
    # Q1: desired question for testing 
    main()
