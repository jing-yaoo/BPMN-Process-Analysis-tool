class Gateways:
    def __init__(self, id, type, incoming, outgoing):
        self.id = id
        self.type = type
        self.incoming = incoming
        self.outgoing = outgoing
        


# Getter and setter methods
    def getIncoming(self):
        return self.incoming
    
    def getOutgoing(self):
        return self.outgoing
    
    def getType(self):
        return self.type

    def getId(self):
        return self.id
    
    def setIncoming(self, incoming):
        self.incoming = incoming

    def setOutgoing(self, outgoing):
        self.outgoing = outgoing

    def setType(self, type):
        self.type = type

    def setId(self, id):
        self.id = id