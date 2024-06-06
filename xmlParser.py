from xml.dom.minidom import parse, Node, parseString
import Gateways, Activities


# Set the id attribute for all elements that have an attribute named "id"
def set_id_attribute(parent, attribute_name="id"):
    if parent.nodeType == Node.ELEMENT_NODE:
        if parent.hasAttribute(attribute_name):
            parent.setIdAttribute(attribute_name)
    for child in parent.childNodes:
        set_id_attribute(child, attribute_name)

# Parse XML from a filename
document = parse("/Users/jin/jin-git/HiWi/data/deliveryProcess.bpmn")
set_id_attribute(document)

# Activities
# Save all task IDs in a list
taskIds = []
for element in document.getElementsByTagNameNS("*", "task"):
    taskIds.append(element.getAttribute("id"))
print(f"\nTask IDs: {taskIds} \n")

# Count the number of tasks
taskCount = len(taskIds)
print(f"How many tasks do we have? {taskCount}\n")

taskList = []
dfa = {}

# Retrieve first task and child nodes
for idx in range(0, taskCount):
    elements = document.getElementsByTagNameNS("*", "task")
    if not elements:
        continue
    taskList.append(elements[idx]) # Saves all task elements in a list

for idx in range(0, taskCount):
    task_name = str(taskList[idx].getAttribute("name"))
    if task_name not in dfa:
        dfa[task_name] = {}
    for child in taskList[idx].childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.tagName == "incoming":
                dfa[task_name]['incoming'] = child.firstChild.data
            elif child.tagName == "outgoing":
                dfa[task_name]['outgoing'] = child.firstChild.data

print(f"Task list length: {len(taskList)}")
print(taskList[3].getAttribute("id"))
print(f"Here's the incoming of the first task {dfa.get(str(taskList[0].getAttribute('name'))).get('incoming')}")
print(f"Here's the outgoing of the first task {dfa.get(str(taskList[0].getAttribute('name'))).get('outgoing')}")
print(f"Here's the task DFA {dfa}")


#TODO inclusive gateway must remember which activities have executed

# Gateways
# Get all gateway IDs
gatewayTypes = ["exclusiveGateway", "inclusiveGateway", "parallelGateway", "complexGateway"]
gatewayIds = []
gatewayIdx = 0
gatewayList = []

for gatewayType in gatewayTypes:
    gatewayIdx += 1
    for element in document.getElementsByTagNameNS("*", gatewayType):
        gatewayIds.append(str(gatewayType) + f"{gatewayIdx}: " + element.getAttribute("id"))
        gatewayList.append(element)
        element.setAttribute("name", str(gatewayType) + f"{gatewayIdx}: " + element.getAttribute("id"))

print(f"\nGateway List: {gatewayIds} \n")
print(f"How many gateways do we have? {len(gatewayIds) / 2}\n")

gatewayCount = len(gatewayIds)


for idx in range(0, gatewayCount):
    elements = document.getElementsByTagNameNS("*", "gateway")
    if not elements:
        continue
    gatewayList.append(elements[idx]) # Saves all task elements in a list




for idx in range(0, gatewayCount):
    gatewayName = str(gatewayList[idx].getAttribute("name"))
    dfa[gatewayName] ={'incoming': [], 'outgoing': []}  
    if gatewayName not in dfa:
        dfa[gatewayName] = {}
    for child in gatewayList[idx].childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.tagName == "incoming":
                dfa[gatewayName]['incoming'].append(child.firstChild.data)
            elif child.tagName == "outgoing":
                dfa[gatewayName]['outgoing'].append(child.firstChild.data)

print(f"Here's the gateway DFA {dfa}\n")

mergedList = taskList + gatewayList


#TODO Match the incoming and outgoing of tasks
for idx in range(0, len(mergedList)):
    for index in range(0, len(mergedList)):
        if dfa.get(str(mergedList[idx].getAttribute('name'))).get('outgoing') == dfa.get(str(mergedList[index].getAttribute('name'))).get('incoming'):
            print(f"Matched {mergedList[idx].getAttribute('name')} and {mergedList[index].getAttribute('name')}")

#TODO Match tasks and gateways using the DFA
for task in taskList:
    for gateway in gatewayList:
        for idx in range(0, len(dfa.get(str(gateway.getAttribute('name'))).get('incoming'))):
            if dfa.get(str(task.getAttribute('name'))).get('outgoing') == dfa.get(str(gateway.getAttribute('name'))).get('incoming')[idx]:
                print(f"Matched {task.getAttribute('name')} to {gateway.getAttribute('name')}")
        for idx in range(0, len(dfa.get(str(gateway.getAttribute('name'))).get('outgoing'))):    
            if dfa.get(str(task.getAttribute('name'))).get('incoming') == dfa.get(str(gateway.getAttribute('name'))).get('outgoing')[idx]:
                print(f"Matched {gateway.getAttribute('name')} to {task.getAttribute('name')}")
