from genie import testbed

#Class to represent a monitoring object
class VPNMonitor():

    #Function that will connect the the device CSR2 as defined in the testbed
    def build_connection(self, testbedfile):
        mytestbed = testbed.load(testbedfile)
        device = mytestbed.devices['CSR2']
        device.connect()

        self.device = device

        return None

    #Function will check the Gig2 IP address on the device/connection contained in the object
    #Will return the value of the IP address
    def check_IP(self):        
        output = self.device.parse('show ip interface brief')
        branch_vpn_addr = output['interface']['GigabitEthernet2']['ip_address']

        return branch_vpn_addr


