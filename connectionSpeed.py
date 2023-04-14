import subprocess, re

def ping(host, attemptCount = 5):
    '''
    output = [min, avg, max, mdev]
    '''

    try:
        ping = subprocess.Popen(
        ['ping', '-c', str(attemptCount), host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
        )

        out, error = ping.communicate()
        out = out.decode('utf-8')
        out = out.split('min/avg/max/mdev = ')[1]
        out = out.split(' ms')[0]

        out = out.split('/')

        return list(map(lambda x: float(x), out))

    except:
        print(host)

def compareHosts(hosts, attemptCount = 5):
    '''
    results are based on average speed.
    criteria can be changed from ping() function

    Result
    ----------------
    [bestURL, pingOfBestURL]
    '''

    speeds = {}

    for host in hosts:
        speeds[host] = ping(host)[1]

    best = min(speeds, key=speeds.get)

    return [best, speeds[best]]