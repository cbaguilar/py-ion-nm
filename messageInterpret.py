import cbor

#Interpret message programatically


INPUT_STR = "82005827020081c11541050502252381c7182d41010501126769706e3a312e310501126769706e3a312e31";

REGISTER_AGNT = "820049006769706e3a322e31"

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

def changeBit(int_type, offset, state):
    output = int_type
    output ^= (-state ^ int_type) & (1 << offset)
    return output

def setBit(int_type, offset):
    mask = 1 << offset
    return (int_type | offset)

class RegisterAgent:
    def __init__(self):
        pass

    def decode(self, in_bytes):
        self.raw_bytes = in_bytes
        decoded = cbor.loads(in_bytes)
        print(in_bytes)
        self.agent_id = decoded
        pass

    def encode(self):
        encoded = cbor.dumps(self.agent_id)
        return encoded.hex()

    @classmethod
    def from_bytes(cls, in_bytes):
        cls = RegisterAgent()
        cls.decode(in_bytes)
        return cls
        


    def __str__(self):
        return f"Message: Register Agent \t Agent ID:{self.agent_id}"

class ARI:
    def __init__(self, in_bytes):
        pass


class ReportSet:
    def __init__(self):
        pass

#Class methods

class PerformControl:
    TV = 0
    def __init__(self, in_bytes):
       pass

    
    def decode(self, in_bytes):
        self.raw_bytes = in_bytes
        decoded = cbor.loads(in_bytes)
        AC_raw = cbor.loads(in_bytes[1:])
        self.TV = decoded
        

    @classmethod
    def from_bytes(cls, in_bytes):
        cls = PerformControl()
        cls.decode(in_bytes)

    def __str__(self):
        return f"Perform Control: TV: {TV}\t  "

class Message:
    flags = {}
    def __init__(self):
        pass

    def decode(self, in_bytes):
        self.raw_bytes = in_bytes
        raw_header = in_bytes[0]
        body_bytes = in_bytes[1:]
        self.flags['Opcode'] = raw_header & (7) #Opcode = Lowest 3 bits

        #Flags based off of packed flag byte/bitfield
        self.flags['Ack'] = testBit(raw_header, (3))
        self.flags['Nack'] = testBit(raw_header, 4)
        self.flags['ACL'] = testBit(raw_header, 5)
        self.body = self.opcode_to_body(self.flags['Opcode'], body_bytes)

    def opcode_to_body(self, opcode, in_bytes):
        if opcode == 0:
            return RegisterAgent.from_bytes(in_bytes)
        if opcode == 1:
            return ReportSet(in_bytes)
        if opcode == 2:
            return PerformControl(in_bytes)
    def flags_to_hex(self):
        flagByte = self.flags['Opcode']
        print("fb1:" + str(flagByte))
        flagByte = changeBit(flagByte, 3, self.flags['Ack'])
        flagByte = changeBit(flagByte, 4, self.flags['Nack'])
        flagByte = changeBit(flagByte, 5, self.flags['ACL'])
        flagHex = "{:02x}".format(flagByte)
        return flagHex


    @classmethod
    def from_bytes(cls, in_bytes):
        cls = Message()
        cls.decode(in_bytes)
        return cls

    def encode(self):
        body_hex = self.body.encode()
        flag_hex = self.flags_to_hex()
        return flag_hex + body_hex


    def __str__(self):
        output = "Flags: " + str(self.flags)
        output += " "
        output += "Body: " + str(self.body)
        return output


class MessageGroup:
    messages = []
    def __init__(self):
        pass

    def decode(self, in_bytes):
        self.raw_bytes = in_bytes
        top_level = cbor.loads(self.raw_bytes)
        self.timestamp = top_level[0]
        for i in range(1, len(top_level)):
            self.messages.append(Message.from_bytes(top_level[i]))
        
    def encode(self):
        message_array = []
        message_array.append(self.timestamp)
        for message in self.messages:
            message_array.append(bytes.fromhex(message.encode()))
        out_bytes = cbor.dumps(message_array)
        return out_bytes.hex()
        

    @classmethod
    def from_bytes(cls, in_bytes):
        cls = MessageGroup()
        cls.decode(in_bytes)
        return cls
        

    def __str__(self):
        output = f"Timestamp: {self.timestamp}\n"
        for msg in self.messages:
            output += str(msg)
        return output





my_msg_group = MessageGroup.from_bytes(bytes.fromhex(REGISTER_AGNT))
print(my_msg_group)

print(my_msg_group.encode())

