import math
import time

# Function to calculate average and statistical uncertainty
def calculate_average_and_uncertainty(total, count):
    """Calculate average and statistical uncertainty."""
    if count > 0:
        average = total / count
        # Using Poisson statistics for uncertainty
        uncertainty = math.sqrt(total) / count if count > 1 else 0  
        return average, uncertainty
    return 0, 0  # Return zero if no counts

# Function to determine particle type based on PDG code
def check_type(pdg_code):
    if pdg_code == 211:
        return 1  # Positive pion
    elif pdg_code == -211:
        return -1  # Negative pion
    else:
        return 0  # Not a pion

# Start timing
start_time = time.time()

# Define the batch size (you can adjust this to control memory usage)
batch_size = 1000  # Number of events in a batch

# Array of file paths
file_paths = [
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set1.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set2.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set3.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set4.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set5.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set6.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set7.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set8.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set9.txt",
    "C:/Users/Ioana/Desktop/ciorna_uni/lab/DataFiles/DataFiles/output-Set10.txt"
]

# Loop through each file path
for file_index, file_path in enumerate(file_paths):
    print(f"\nProcessing file {file_index + 1}: {file_path}")

    total_positive = 0
    total_negative = 0
    event_counter = 0  # Total events processed
    subsample_size = 10000  # Number of events in each subsample

    # Initialize batch-specific counters
    batch_positive = 0
    batch_negative = 0
    batch_counter = 0  # Count for the current batch

    try:
        with open(file_path, "r") as infile:
            # Read until the end of the file
            while True:
                # Read the first line of an event
                line = infile.readline()
                if not line:  # End of file
                    break

                # Attempt to split and read event_id and num_particles
                try:
                    # Split the line and convert to the appropriate types
                    parts = line.strip().split()
                    event_id = float(parts[0])  # Event ID as float (if needed)
                    num_particles = int(parts[1])  # Number of particles as int
                except (ValueError, IndexError):
                    print(f"Skipping invalid line: {line.strip()}")
                    continue

                event_counter += 1
                
                # Reset counters for each event
                positive_count = 0
                negative_count = 0

                # Read particle data for the current event
                for _ in range(num_particles):
                    particle_data = infile.readline().strip()
                    if particle_data:
                        try:
                            px, py, pz, pdg_code = map(float, particle_data.split())
                            particle_type = check_type(int(pdg_code))

                            if particle_type == 1:  # Positive pion
                                positive_count += 1
                            elif particle_type == -1:  # Negative pion
                                negative_count += 1
                        except ValueError:
                            print(f"Skipping invalid particle data: {particle_data}")
                            continue

                # Update batch counters
                batch_positive += positive_count
                batch_negative += negative_count
                batch_counter += 1

                # Check if we have reached the batch size
                if batch_counter == batch_size:
                    total_positive += batch_positive
                    total_negative += batch_negative

                    # Reset batch-specific counters
                    batch_positive = 0
                    batch_negative = 0
                    batch_counter = 0

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found. Please check the file path and try again.")
        continue
    except IOError:
        print(f"An error occurred while trying to read the file '{file_path}'.")
        continue

    # Add any remaining counts from the final batch
    if batch_counter > 0:
        total_positive += batch_positive
        total_negative += batch_negative

    # Calculate averages and uncertainties
    avg_positive, unc_positive = calculate_average_and_uncertainty(total_positive, event_counter)
    avg_negative, unc_negative = calculate_average_and_uncertainty(total_negative, event_counter)

    # Calculate the mean difference
    avg_difference = avg_positive - avg_negative
    unc_difference = math.sqrt(unc_positive ** 2 + unc_negative ** 2)  # Combined uncertainty for the difference

    # Calculate how many sigma the mean difference is from zero
    if unc_difference > 0:  # Ensure there's no division by zero
        num_sigma = avg_difference / unc_difference
    else:
        num_sigma = float('inf')  # If uncertainty is zero, set to infinity

    # Check if the difference is statistically significant
    significance = "not statistically significant"
    if abs(num_sigma) > 3:
        significance = "statistically significant"

    # Print results for the file
    print(f"Average Positive Pions per Event: {avg_positive:.5f} ± {unc_positive:.5f}")
    print(f"Average Negative Pions per Event: {avg_negative:.5f} ± {unc_negative:.5f}")
    print(f"Mean Difference (Average Positive - Average Negative): {avg_difference:.5f} ± {unc_difference:.5f}")
    print(f"Mean Difference is {num_sigma:.2f} sigma from zero, indicating it is {significance}.")

# Print overall execution time
execution_time = time.time() - start_time
print(f"\nTotal Execution Time: {execution_time:.2f} seconds")
