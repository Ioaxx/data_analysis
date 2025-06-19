import math
import time
from concurrent.futures import ProcessPoolExecutor

# Function to calculate average and statistical uncertainty
def calculate_average_and_uncertainty(total, count):
    if count > 0:
        average = total / count
        uncertainty = math.sqrt(total) / count if count > 1 else 0  
        return average, uncertainty
    return 0, 0

def check_type(pdg_code):
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    else:
        return 0

# Main per-file function
def process_file(file_path):
    total_positive = 0
    total_negative = 0
    event_counter = 0
    batch_size = 1000

    batch_positive = 0
    batch_negative = 0
    batch_counter = 0

    try:
        with open(file_path, "r") as infile:
            while True:
                line = infile.readline()
                if not line:
                    break

                try:
                    parts = line.strip().split()
                    event_id = float(parts[0])
                    num_particles = int(parts[1])
                except (ValueError, IndexError):
                    continue

                event_counter += 1
                positive_count = 0
                negative_count = 0

                for _ in range(num_particles):
                    particle_data = infile.readline().strip()
                    if particle_data:
                        try:
                            px, py, pz, pdg_code = map(float, particle_data.split())
                            particle_type = check_type(int(pdg_code))
                            if particle_type == 1:
                                positive_count += 1
                            elif particle_type == -1:
                                negative_count += 1
                        except ValueError:
                            continue

                batch_positive += positive_count
                batch_negative += negative_count
                batch_counter += 1

                if batch_counter == batch_size:
                    total_positive += batch_positive
                    total_negative += batch_negative
                    batch_positive = 0
                    batch_negative = 0
                    batch_counter = 0

    except FileNotFoundError:
        return (file_path, None, "File not found")
    except IOError:
        return (file_path, None, "IO error")

    # Add remaining
    if batch_counter > 0:
        total_positive += batch_positive
        total_negative += batch_negative

    avg_positive, unc_positive = calculate_average_and_uncertainty(total_positive, event_counter)
    avg_negative, unc_negative = calculate_average_and_uncertainty(total_negative, event_counter)

    avg_diff = avg_positive - avg_negative
    unc_diff = math.sqrt(unc_positive**2 + unc_negative**2)
    num_sigma = avg_diff / unc_diff if unc_diff > 0 else float('inf')
    significance = "statistically significant" if abs(num_sigma) > 3 else "not statistically significant"

    result = {
        "avg_pos": avg_positive,
        "unc_pos": unc_positive,
        "avg_neg": avg_negative,
        "unc_neg": unc_negative,
        "avg_diff": avg_diff,
        "unc_diff": unc_diff,
        "num_sigma": num_sigma,
        "significance": significance
    }
    return (file_path, result, None)

# Paths
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

# Run in parallel
if __name__ == "__main__":
    start_time = time.time()

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_file, file_paths))

    for file_path, result, error in results:
        print(f"\nResults for file: {file_path}")
        if error:
            print(f"  Error: {error}")
        else:
            print(f"  Average Positive Pions/Event: {result['avg_pos']:.5f} ± {result['unc_pos']:.5f}")
            print(f"  Average Negative Pions/Event: {result['avg_neg']:.5f} ± {result['unc_neg']:.5f}")
            print(f"  Difference (Pos - Neg): {result['avg_diff']:.5f} ± {result['unc_diff']:.5f}")
            print(f"  {result['num_sigma']:.2f}σ from zero, {result['significance']}.")

    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
