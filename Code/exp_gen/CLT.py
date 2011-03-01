from exp_management.Experiment import Experiment
def parse_flags():
    import getopt
    import sys
    experiment = Experiment("EXP1")

    #Check for Help Flag
    if(sys.argv.count("--help")):
        sys.exit(0)
    #Make sure there is a filename passed in using a flag
    if(not sys.argv.count("-f")):
        sys.stderr.write("Must pass in filename using -f <filename>\n")
        sys.exit(1)

    #Get all pairing of options to args
    try:
        opts,args = getopt.getopt(sys.argv[1:],"f:n:t:dt:r")
    except getopt.GetoptError,err:
        print str(err)
        sys.exit(1)
    
    experiment.loadXMLFile( filter(lambda x:x[0] == '-f',opts)[-1][1] )
    
    return experiment
    

if __name__ == "__main__":
    parse_flags()
