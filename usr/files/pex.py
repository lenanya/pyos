with open("pextest.pex", "r") as f:
    data = f.read()

lines = data.split("\n")

terms = []

for i in lines:
    

variables = {}

ptr = 0


