import pickle

path = "organize\\pickle_state\\"
pickle_file = "test_spider_state.pkl"

# Define some variables to save
x = 42
y = [1, 2, 3, 4, 5]
starter = ["https://petapixel.com/2023/03/03/apples-29-year-old-landmark-quicktake-100-camera-falters-in-2023/",]
# Save the variables to a file
with open(path+pickle_file, 'wb') as f:
    pickle.dump(starter, f)
    
# Load the variables from the file
with open(path+pickle_file, 'rb') as f:
    starter = pickle.load(f)

# Use the variables in the program
# x += 1
print(starter)
