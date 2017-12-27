from DBWatcher import *

def main():
    dbconnection = databaseconfig()
    dbconnection.disconnect()
    
if __name__ == '__main__':
    main()