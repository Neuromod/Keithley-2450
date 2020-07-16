import visa


def file(filename):
    with open(filename) as file:
        return file.read()


class Keithley:
    # Connect to instrument and disable prompt
    def __init__(self, resource, timeout = 60_000):
        self.instrument = visa.ResourceManager().open_resource(resource)
        self.instrument.timeout = timeout
        self.instrument.clear()
        self.instrument.write('localnode.prompts = localnode.DISABLE')


    # Load script
    def loadScript(self, script, scriptName):
        self.instrument.write('script.delete("{:s}")'.format(scriptName))
        self.instrument.write('loadscript {:s}'.format(scriptName))
        self.instrument.write(script)
        self.instrument.write('endscript')


    # Load and run script
    def runScript(self, script):
        self.loadScript(script, 'Code')
        self.instrument.write('Code()')


    # Load and save script to non-volatile memory
    def saveScript(self, script, scriptName):
        self.loadScript(script, scriptName)
        self.instrument.write('{:s}.save()'.format(scriptName))


    # Write to instrument 
    def write(self, code):
        self.instrument.write(code)


    # Read from instrument
    def read(self):
        return self.instrument.read()


    # Close instrument link    
    def close(self):
        self.instrument.close()
