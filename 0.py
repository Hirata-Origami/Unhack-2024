import json

machine = []
step = {}
wafers = []
output = {'schedule':[]}

class Step:
    def __init__(self,id,parameter,dependency):
        self.id = id
        self.parameter = parameter
        self.dependency = dependency

class Wafer:
    def __init__(self,types,process):
        self.type = types
        self.process = process
        self.time = 0
    
    def assignMachine(self):
        for i in self.process.keys():
            self.checkAndRun(i)
            
    def checkAndRun(self,steps):
        for j in machine:
                if j.time != 0:
                    break
                if j.step == steps:
                    if step[steps][0] < j.current and j.current < step[steps][1]:
                        j.assignStep()
                        output['schedule'].append({'wafer_id':self.type,'step':step,'machine':j.id,'start_time':self.time,'end_time':self.time+j.time})
                        self.time += j.time
                        j.time = 0
                        break 

         

class Machine:
    def __init__(self,id,step,cooldown,initial,fluctuation,n):
        self.id = id
        self.step = step
        self.cooldown = cooldown
        self.initial = initial
        self.time = 0
        self.fluctuation = fluctuation
        self.n = n
        self.currentn = n
        self.current = initial
        
    def assignStep(self):
        self.currentn -= 1
        self.current += self.fluctuation
        if(self.currentn == -1):
            self.time += self.cooldown
        while(self.time!=0):
            self.time += 1
        
   

def main():
    with open('Input/Milestone0.json', 'r') as file:
        data = json.load(file)
    for j in data['steps']:
        step[j['id']] = [j['parameters'],j['dependency']] 
    for j in data['machines']:
        machine.append(Machine(j['machine_id'],j['step_id'],j['cooldown_time'],j['initial_parameters'],j['fluctuation'],j['n'])) 
    for j in data['wafers']:
        for k in range(1,j['quantity']+1):
            wafers.append(Wafer(j['type']+"-"+str(k),j['processing_times']))
            wafers[-1].assignMachine()
    print(output)
    
main()
        