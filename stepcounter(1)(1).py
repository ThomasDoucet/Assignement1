import numpy as np
import matplotlib.pyplot as plt

# Thomas Doucet
#Student number : 2301955
# ASSIGNEMENT 1:

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.xlabel("time")
  plt.ylabel("Acceleration(m.s-2)")
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()
timestamps = []
x_arr = []
y_arr = []
z_arr = []

#Function to read the data from the log file
#TODO Read the measurements into array variables and return them

filename = "C:\\Users\\thoma\\OneDrive\\Bureau\\Bah_sors\\out.csv"

def read_data(filename):
  g= open(filename,"r")
  les_lignes = g.readlines()
  for ligne in les_lignes[1:]: # we look in each line
    liste  = ligne.strip().split(",") # We can see that data are separeted by a comma when we open the file
    timestamps.append(float(liste[0]))
    x_arr.append(float(liste[1]))
    y_arr.append(float(liste[2]))
    z_arr.append(float(liste[3]))
  g.close()
  return timestamps, x_arr, y_arr, z_arr
Liste = read_data(filename)
timestamps = Liste[0]
x_arr =  Liste[1]
y_arr =  Liste[2]
z_arr =  Liste[3]

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.4



def count_steps1(timestamps, x_arr, y_arr, z_arr) : # simple solution without dinamyc treshold
  rv = []
  s = 0
  L = []
  k = 0
  mean = 0
  max = -1000
  for i, time in enumerate(timestamps): # determination of the mean & max aceleration value
    mean = mean + y_arr[i]
    if (y_arr[i]>max ) :
      max = y_arr[i]
  for i, time in enumerate(timestamps):
    if(y_arr[i]<mean/len(timestamps) + max/10): # if the given data is under the treshold values, we add it to the list
      rv.append(time)
  long = len(rv)
  for i in range(long-1): # loop to get rid of parasitic steps id est steps counted twice in a row
    s = s + rv[i+1]-rv[i]
    if (i%5 ==0 and i>0) :
      for j in range(i-5,i) : # if the step are too closed compared to the mean gap between every 5 values, then we get rid of this value
        if  (rv[j+1]-rv[j] < (s/2.4)):
          L.append(j)
      s = 0
  for i in L :
    del rv[i-k]
    k = k+1
  return rv



def count_steps2(timestamps, x_arr, y_arr, z_arr) :
  rv = []
  s = 0
  L = []
  k = 0
  max = -10000
  min = 100000
  P = []
  for i, time in enumerate(timestamps):
    s = s + y_arr[i] # we still calculate the mean & find the max but for a size of 50 times units, therefor the mean & max are local here, not global
    if (y_arr[i]>max ) :
      max = y_arr[i]
    if (y_arr[i]< min  ) :
      min  = y_arr[i]
    if (i%50 ==0 and i>0) :
      L.append(s/50)
      L.append(max)
      L.append(min)
      P.append(L)
      L = []
      s = 0
      max = -10000
      min = 100000
  for i, time in enumerate(timestamps): # same principle than in the first function, except that the treshold changes according to the mean & max calculated previously
    if (i>0):
      if ( y_arr[i-1]< P[k][0] and y_arr[i]> P[k][0] ) :
        rv.append(time)
    if (i%50 ==0 and k<len(P)-1) :
      k = k+1 # increase of the index which means we moved to the next set of 50 time units
  long = len(rv)
  p = 0
  M =[]
  for i in range(long-1):
    p = p + rv[i+1]-rv[i]
    if (i%5 ==0 and i>0) :
      for j in range(i-5,i) :
        if  (rv[j+1]-rv[j] < (p/4)):
          M.append(j)
      p = 0
  c = 0
  for i in M :
    del rv[i-c]
    c = c+1

  return rv

# A2 = count_steps2(timestamps, x_arr, y_arr, z_arr)
# print(len(A2))
# A1 = count_steps1(timestamps, x_arr, y_arr, z_arr)
# print(len(A1))
# plt.figure(1)
# plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
# plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
# plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
# plt.xlabel("time(s)")
# plt.ylabel("Acceleration(m.s-2)")
# plt.show()


# Calculate
# the magnitude of the given vector

def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps hapîîi==ipened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 50000 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main():
  #read data from a measurement file, change the inoput file name if needed

  timestamps, x_array, y_array, z_array = read_data(filename)
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  st = count_steps1(timestamps, x_array, y_array, z_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array)

main()

