import math             #library used for pow(good for squares and logs)
import matplotlib.pyplot as plt
import numpy as np
threshold = 0.05

def calculate_p( py, px, pz):
    return math.pow( (math.pow(py, 2)+math.pow(px, 2)+math.pow(pz,2 )), 1/2)        #uses the formula for p

def calculate_pT (px, py):
    return math.pow( (math.pow(px, 2)+math.pow(py, 2)), 1/2)        #use pow to the power of 1/2 instread of a square root

def calculate_pseudorapidity( p, pz):               #pseudorapidity is the n with a long end
    if pz!= p:
        return 1/2*(math.log((p+pz)/(p-pz)))            #the function log automaticly calculates ln(with e as a base)
    else:
        print("this is an error. your angle will  be infinite")
        return None

def calculate_azimuthal_angle(px, py):
    return math.atan(px/py)

def check_type (pdg_code):
    if pdg_code == 211:
        #print("this is a positive pion")
        return 1
    elif pdg_code == -211:
        #print("this is a negative pion")
        return -1
    return 0

def poisson_distribution(average):
    return math.sqrt(average)

def difference( no_1, no_2):
    return abs(no_1-no_2)

def combined_uncertainty(no_1, no_2):
    return math.sqrt(no_1+no_2)

def significance (no_1, no_2, comb_uncertainty):
    if no_1>no_2:
        return (no_1-no_2)/comb_uncertainty
    else:
        return (no_2-no_1)/comb_uncertainty



try: 
    with open("./output-Set1.txt", "r") as infile:     #reading the file, had to change the path for my computer
        first_line = infile.readline().strip()              #first line will contain the first numbers of the file, but without spaces between(this is what strip does)
        event_id, num_particles = map(int, first_line.split())           #separates the parts of the first line and converst them into integers that we save into num1 and num2
        lines_list = [line.strip().split() for line in infile]  #with this evey line will be a list with separate components. 
                                                                #so there will be a very big list of lists that represent the particle with each of their components
except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except IOError:
    print("An error occurred while trying to read the file.")


total_contor_positive = 0
total_contor_negative = 0

contor_positive = 0
contor_negative = 0
event_counter = 0 
current_event_id = event_id


positive_per_event = []
negative_per_event = []

for i in range(len(lines_list)):
    if len(lines_list[i]) == 2:
        # Store the counts for the previous event (skip for the very first event)
        if event_counter > 0:
            positive_per_event.append(contor_positive)
            negative_per_event.append(contor_negative)
        total_contor_positive += contor_positive
        total_contor_negative += contor_negative
        event_id, num_particles = map(int, lines_list[i])
        current_event_id = event_id
        event_counter += 1
        contor_positive = 0
        contor_negative = 0
    if len(lines_list[i]) == 4:
        px, py, pz, pdg_code = map(float, lines_list[i])
        particle_type = check_type(pdg_code)
        if particle_type == 1:
            contor_positive += 1
        elif particle_type == -1:
            contor_negative += 1

# After the loop, append the last event's counts
positive_per_event.append(contor_positive)
negative_per_event.append(contor_negative)
    
# fter the loop, print the results of the last event
#print(f"In event {current_event_id}, we had {contor_positive} positive particles and {contor_negative} negative particles.")
total_contor_positive += contor_positive
total_contor_negative += contor_negative
event_counter+=1 

# Print the final summary
print(f"\nIn {event_counter} total events, we had {total_contor_positive} positive particles and {total_contor_negative} negative particles.")

average_positive= total_contor_positive/event_counter
print("there s an average of ", average_positive, "particles(positive pions)")
average_negative= total_contor_negative/event_counter
print("there s an average of ", average_negative, "anti-particles(negative pions)")
    

poisson_positive = poisson_distribution(total_contor_positive)
poisson_negative = poisson_distribution(total_contor_negative)

print(f"the poisson distribution for the positive pions is {poisson_positive} and the poisson distribution for the negative(antiparticle) pions is {poisson_negative}")

comparison=difference(total_contor_positive, total_contor_negative)
if total_contor_positive>total_contor_negative:
    print("there are ", comparison, " more particles then antiparticles")
else:
    print("there are ", -comparison, " more antiparticles then particles")
    
combined_uncertainty = combined_uncertainty(total_contor_positive, total_contor_negative)
print("the combined uncertainty of the total amount of particles and antiparticles is ", combined_uncertainty)

significance = significance(total_contor_positive, total_contor_negative, combined_uncertainty)
print("the significance is ", significance)
if significance> threshold:
    print("the significance is very large compared to the threshold")
else:
    print("the significance is not larger then the threshold")


# Aggregate sums per 1000 events
batch_size = 1000
batch_positive = []
batch_negative = []

for i in range(0, len(positive_per_event), batch_size):
    batch_positive.append(sum(positive_per_event[i:i+batch_size]))
    batch_negative.append(sum(negative_per_event[i:i+batch_size]))

x = [i * batch_size for i in range(len(batch_positive))]

plt.figure(figsize=(10, 6))
plt.plot(x, batch_positive, label='Positive pions per 1000 events', color='blue', linewidth=1)
plt.plot(x, batch_negative, label='Negative pions per 1000 events', color='red', linewidth=1)
plt.xlabel('Event number')
plt.ylabel('Number of pions in 1000 events')
plt.title('Positive and Negative Pions per 1000 Events')
plt.legend()
plt.tight_layout()
plt.show()
