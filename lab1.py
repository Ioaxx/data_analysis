import math             #library used for pow(good for squares and logs)
  
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
        print("this is a positive pion")
    elif pdg_code == -211:
        print("this is a negative pion")
    elif pdg_code == 111:
        print("this is a neutral pion")
    else: 
        print("this is not a pion of any kind")

#i used my path for the input file, but if someone else wants to run this, they have to copy their own path
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Hello! if you are peer reviewing this code, please remember to change the path of the input file")
print("you can just go to your file, click right, and copy path, then paste it.")



try: 
    with open(".\output-Set0.txt", "r") as infile:     #reading the file, had to change the path for my computer
        first_line = infile.readline().strip()              #first line will contain the first numbers of the file, but without spaces between(this is what strip does)
        event_id, num_particles = map(int, first_line.split())           #separates the parts of the first line and converst them into integers that we save into num1 and num2
        lines_list = [line.strip().split() for line in infile]  #with this evey line will be a list with separate components. 
                                                                #so there will be a very big list of lists that represent the particle with each of their components
except FileNotFoundError:
    print("The file was not found. Please check the file path and try again.")
except IOError:
    print("An error occurred while trying to read the file.")

print()         #this prints an empty line. it's just for the aesthetic of the terminal
print("event id is", event_id, "and there are", num_particles, "particles")       #print to show the events id and no of particles in the event


for i in range(len(lines_list)):            #going through every list (line) in the main list of particles. 
    print()         #this prints an empty line
    print ("for particle ", i+1 )
    px, py, pz, pdg_code = map(float, lines_list[i])        #giving each one of the 4 compoents in the list a name and making them from string to float
   
    check_type(pdg_code)

    p= calculate_p(py, px, pz)              #using the defined function to calculate p, which will be needed for the pseudopolarity function
    
    pseudo= calculate_pseudorapidity(p, pz)       #calculating pseudopolarity
    print("pseudorapidity = ", pseudo)              #addition print to show what the pseudopolarity is
    
    pT= calculate_pT(px, py)                    #calculate pT
    print("pT = ", pT)                          #additional print to show what the pT of the particle is
    
    azimuth= calculate_azimuthal_angle(px, py)
    print("azimuthal angle is ",azimuth)
    
