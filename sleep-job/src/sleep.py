import time
import argparse

def Sleep(sleepTime):
   print(1)
   time.sleep(60*sleepTime)
   print(2)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--sleepTime',type=int,required=True,help='sleet time to be input')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    Sleep(args.sleepTime)

if __name__ == '__main__':
    main()
