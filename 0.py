import json

machines = []
steps = {}
wafers = []
output = {'schedule': []}

class Step:
    def __init__(self, id, parameters, dependency):
        self.id = id
        self.parameters = parameters
        self.dependency = dependency

class Wafer:
    def __init__(self, wafer_id, process):
        self.wafer_id = wafer_id
        self.process = process
        self.time = 0

    def assignMachine(self):
        for step_id, duration in self.process.items():
            print(self.wafer_id,step_id)
            self.checkAndRun(step_id, duration)

    def checkAndRun(self, step_id, duration):
        while True:
            for machine in machines:
                if machine.step == step_id and machine.isAvailable(self.time):
                    parameters = steps[step_id].parameters
                    valid = all(parameters[key][0] <= machine.current[key] <= parameters[key][1] for key in parameters)
                    if valid:
                        start_time = max(self.time, machine.next_available_time)
                        machine.assignStep(start_time, duration)
                        output['schedule'].append({'wafer_id': self.wafer_id,'step': step_id,'machine': machine.id,'start_time': start_time,'end_time': start_time + duration})
                        self.time = start_time + duration
                        return
            self.time += 1

class Machine:
    def __init__(self, id, step, cooldown, initial, fluctuation, n):
        self.id = id
        self.step = step
        self.cooldown = cooldown
        self.initial = initial
        self.current = initial
        self.fluctuation = fluctuation
        self.n = n
        self.current_n = n
        self.next_available_time = 0

    def isAvailable(self, current_time):
        print(current_time,self.next_available_time)
        return current_time >= self.next_available_time

    def assignStep(self, start_time, duration):
        self.current_n -= 1
        if self.current_n == 0:
            self.current_n = self.n
            self.next_available_time = start_time + duration + self.cooldown
            for key in self.current:
                self.current[key] = self.initial[key]
        else:
            self.next_available_time = start_time + duration

def main():
    with open('Input/Milestone3b.json', 'r') as file:
        data = json.load(file)
    for i in data['steps']:
        steps[i['id']] = Step(i['id'], i['parameters'], i['dependency'])
    for i in data['machines']:
        machines.append(Machine(i['machine_id'],i['step_id'],i['cooldown_time'],i['initial_parameters'], i['fluctuation'],i['n']))
    for j in data['wafers']:
        for i in range(1, j['quantity'] + 1):
            wafers.append(Wafer(f"{j['type']}-{i}", j['processing_times']))
            wafers[-1].assignMachine()
    print(output)
main()
