from common import *


class sender:
    RTT = 20
    
    def isCorrupted (self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        print("S Corrupt: {} + {} - {} + {} = {}".format(checksumCalc(packet.payload), packet.ackNum, packet.checksum, self.seqNum, abs(checksumCalc(packet.payload) + packet.ackNum - packet.checksum + self.seqNum)))
        return abs(checksumCalc(packet.payload) + packet.ackNum - packet.checksum - self.seqNum) > 0

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''
        print("Send Dup: ", packet.ackNum != self.seqNum)
        return packet.ackNum != self.seqNum
 
    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        print("Next Send Seq: ", (self.seqNum + 1)%2)
        self.seqNum = (self.seqNum + 1)%2
        return self.seqNum 

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        self.seqNum = 0
        self.packet = None

        return

    def timerInterrupt(self):
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        #print("Interrupting")
        #self.networkSimulator.stopTimer(A)
        #print("Sending")
        self.networkSimulator.udtSend(A, self.packet)
        #print("Starting")
        #self.networkSimulator.startTimer(A, self.RTT)
        
        return


    def output(self, message):
        '''prepare a packet and send the packet through the network layer
        by calling calling udtSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        print("Outputting... ")
        if len(self.networkSimulator.eventList.event_list) == 0:
            self.packet = Packet(self.seqNum, 0, checksumCalc(message.data), message.data)
            self.networkSimulator.udtSend(A, self.packet)
            self.networkSimulator.startTimer(A, self.RTT)
            print("Success!")
        else:
            print(" Failed :(")
        return
 
    
    def input(self, packet):

        '''If the acknowlegement packet isn't corrupted or duplicate, 
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does 
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''

        print("S Inputting... ")
        if not self.isCorrupted(packet) and not self.isDuplicate(packet):
            self.networkSimulator.stopTimer(A)
            self.getNextSeqNum()
            print("Success")
        else:
            print("Failed :(")

        return 

