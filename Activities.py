class Activities:
    def __init__(self, id, name, incoming, outgoing):
        self.id = id
        self.name = name
        self.incoming = incoming
        self.outgoing = outgoing


# Getters
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getIncoming(self):
        return self.incoming
    
    def getOutgoing(self):
        return self.outgoing
    
# Setters
    def setId(self, id):
        self.id = id

    def setType(self, name):
        self.name = name
    
    def setIncoming(self, incoming):
        self.incoming = incoming

    def setOutgoing(self, outgoing):
        self.outgoing = outgoing

 