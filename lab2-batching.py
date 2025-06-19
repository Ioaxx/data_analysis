import math
import time  # For timing

threshold = 0.05
BATCH_SIZE = 1000

def calculate_p( py, px, pz):
    return math.pow( (math.pow(py, 2)+math.pow(px, 2)+math.pow(pz,2 )), 1/2)

def calculate_pT (px, py):
    return math.pow( (math.pow(px, 2)+math.pow(py, 2)), 1/2)

def calculate_pseudorapidity( p, pz):
    if pz != p:
        return 1/2*(math.log((p+pz)/(p-pz)))
    else:
        print("this is an error. your angle will be infinite")
        return None

def calculate_azimuthal_angle(px, py):
    return math.atan(px/py)

def check_type (pdg_code):
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    return 0

def poisson_distribution(average):
    return math.sqrt(average)

def difference(no_1, no_2):
    return abs(no_1-no_2)

def combined_uncertainty(no_1, no_2):
    return math.sqrt(no_1+no_2)

def significance(no_1, no_2, comb_uncertainty):
    if no_1 > no_2:
        return (no_1 - no_2) / comb_uncertainty
    else:
        return (no_2 - no_1) / comb_uncertainty


start_time = time.time()

try:
    with open("./output-Set1.txt", "r") as infile:
        first_line = infile.readline().strip()
        event_id, num_particles = map(int, first_line.split())
        lines_list = [line.strip().split() for line in infile]
except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
    exit(1)
except IOError:
    print("An error occurred while trying to read the file.")
    exit(1)


total_contor_positive = 0
total_contor_negative = 0

contor_positive = 0
contor_negative = 0
event_counter = 0
current_event_id = event_id

batch_contor_positive = 0
batch_contor_negative = 0
batch_event_count = 0

for i in range(len(lines_list)):

    if len(lines_list[i]) == 2:  # new event
        batch_contor_positive += contor_positive
        batch_contor_negative += contor_negative

        event_counter += 1
        batch_event_count += 1

        contor_positive = 0
        contor_negative = 0

        event_id, num_particles = map(int, lines_list[i])
        current_event_id = event_id

        # No batch prints here, just accumulate

    elif len(lines_list[i]) == 4:  # particle line
        px, py, pz, pdg_code = map(float, lines_list[i])
        particle_type = check_type(pdg_code)
        if particle_type == 1:
            contor_positive += 1
        elif particle_type == -1:
            contor_negative += 1

# Handle last event and batch counts
batch_contor_positive += contor_positive
batch_contor_negative += contor_negative
batch_event_count += 1
event_counter += 1

total_contor_positive += batch_contor_positive
total_contor_negative += batch_contor_negative

# Final summary print
print(f"\nIn {event_counter} total events, we had {total_contor_positive} positive particles and {total_contor_negative} negative particles.")

average_positive = total_contor_positive / event_counter
print("there s an average of ", average_positive, "particles(positive pions)")
average_negative = total_contor_negative / event_counter
print("there s an average of ", average_negative, "anti-particles(negative pions)")

poisson_positive = poisson_distribution(total_contor_positive)
poisson_negative = poisson_distribution(total_contor_negative)

print(f"the poisson distribution for the positive pions is {poisson_positive} and the poisson distribution for the negative(antiparticle) pions is {poisson_negative}")

comparison = difference(total_contor_positive, total_contor_negative)
if total_contor_positive > total_contor_negative:
    print("there are ", comparison, " more particles then antiparticles")
else:
    print("there are ", -comparison, " more antiparticles then particles")

combined_uncertainty_value = combined_uncertainty(total_contor_positive, total_contor_negative)
print("the combined uncertainty of the total amount of particles and antiparticles is ", combined_uncertainty_value)

significance_value = significance(total_contor_positive, total_contor_negative, combined_uncertainty_value)
print("the significance is ", significance_value)
if significance_value > threshold:
    print("the significance is very large compared to the threshold")
else:
    print("the significance is not larger then the threshold")

end_time = time.time()
print(f"\nExecution time: {end_time - start_time:.2f} seconds")
