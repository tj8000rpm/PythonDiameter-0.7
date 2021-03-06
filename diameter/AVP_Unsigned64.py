from diameter.AVP import AVP
from diameter.Error import InvalidAVPLengthError
import struct

class AVP_Unsigned64(AVP):
    "A Diameter Unsigned64 AVP"
    
    def __init__(self,code,value,vendor_id=0):
        AVP.__init__(self,code,struct.pack("!Q",value),vendor_id)
    
    def queryValue(self):
        """Returns the payload as a 64-bit unsigned value."""
        return struct.unpack("!Q",self.payload)[0]
    
    def setValue(self,value):
        """Sets the payload to the specified 64-bit unsigned value."""
        self.payload = struct.pack("!Q",value)
    
    def __str__(self):
        return str(self.code) + ":" + str(self.queryValue())

    def narrow(avp):
        """Convert generic AVP to AVP_Unsigned64
        Raises: InvalidAVPLengthError
        """
        if len(avp.payload)!=8:
            raise InvalidAVPLengthError(avp)
        value = struct.unpack("!Q",avp.payload)[0]
        a = AVP_Unsigned64(avp.code, value, avp.vendor_id)
        a.flags = avp.flags
        return a
    narrow = staticmethod(narrow)

def _unittest():
    a = AVP_Unsigned64(1,17)
    
    assert a.queryValue()==17
    
    a.setValue(42);
    assert a.queryValue()==42
    
    a = AVP_Unsigned64.narrow(AVP(1,"        "))
    assert a.queryValue()==0x2020202020202020
    try:
        a = AVP_Unsigned64.narrow(AVP(1,"     "))
        assert False
    except InvalidAVPLengthError, detail:
        pass
