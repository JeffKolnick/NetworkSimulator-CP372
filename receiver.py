from common import *

class receiver:
    
    def isCorrupted(self, packet):
        ''' Checks if a received packet has been corrupted during transmission.
        Return true if computed checksum is different than packet checksum.'''
   
        print("S Corrupt: {} + {} - {} + {} = {}".format(checksumCalc(packet.payload), packet.seqNum, packet.checksum, self.seqNum, abs(checksumCalc(packet.payload) + packet.seqNum - packet.checksum + self.seqNum)))
        return abs(checksumCalc(packet.payload) - packet.checksum + packet.seqNum) > 0
   
    def isDuplicate(self, packet):
        '''checks if packet sequence number is the same as expected sequence number'''
        print("R Dup: ", packet.seqNum != self.seqNum)
        return packet.seqNum != self.seqNum
    
    def getNextExpectedSeqNum(self):
        '''The expected sequence numbers are 0 or 1'''
        print("Next Receiver Seq: ", (self.seqNum + 1)%2)
        self.seqNum = (self.seqNum + 1)%2
        return self.seqNum
    
    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))


    def init(self):
        '''initialize expected sequence number'''
        self.seqNum = 0
        return
         

    def input(self, packet):
        '''This method will be called whenever a packet sent 
        from the sender arrives at the receiver. If the received
        packet is corrupted or duplicate, it sends a packet where
        the ack number is the sequence number of the  last correctly
        received packet. Since there is only 0 and 1 sequence numbers,
        you can use the sequence number that is not expected.
        
        If packet is OK (not a duplicate or corrupted), deliver it to the
        application layer and send an acknowledgement to the sender
        '''
        print("R Inputting")
        if not self.isCorrupted(packet) and not self.isDuplicate(packet):
            self.networkSimulator.deliverData(B, packet)
            #self.networkSimulator.stopTimer(A)
            #self.networkSimulator.startTimer(B, 100)
            self.networkSimulator.udtSend(B, Packet(0, self.seqNum, 0, ''))
            self.getNextExpectedSeqNum()
            print("Success!")
        elif not self.isCorrupted(packet) or not self.isDuplicate(packet):
            self.networkSimulator.udtSend(B, Packet(0, (self.seqNum + 1)%2, 0, ''))
        else:
            
            print("Failed :(")


        return
