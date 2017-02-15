'''
DOCOOLER Wifi RGB LED controller

:maintainer:    Robert Booth <robert.booth@trebortech.com>

'''
import sys
import socket
import optparse
from collections import namedtuple
from ConfigParser import SafeConfigParser, DEFAULTSECT
from cStringIO import StringIO


BUILTIN_MODE = namedtuple('BUILTIN_MODE', ['name', 'description', 'id'])

MODE_LIST = (
    BUILTIN_MODE('1', '7 colors gradual change', '25'),
    BUILTIN_MODE('2', 'Red gradual change', '26'),
    BUILTIN_MODE('3', 'Green gradual change', '27'),
    BUILTIN_MODE('4', 'Blue gradual change', '28'),
    BUILTIN_MODE('5', 'Yellow gradual change', '29'),
    BUILTIN_MODE('6', 'Cyan gradual change', '2A'),
    BUILTIN_MODE('7', 'Purple gradual change', '2B'),
    BUILTIN_MODE('8', 'White gradual change', '2C'),
    BUILTIN_MODE('9', 'Red and Green gradual change', '2D'),
    BUILTIN_MODE('10', 'Red and Blue gradual change', '2E'),
    BUILTIN_MODE('11', 'Green and Blue gradual change', '2F'),
    BUILTIN_MODE('12', '7 colors flicker', '30'),
    BUILTIN_MODE('13', 'Red flicker', '31'),
    BUILTIN_MODE('14', 'Green flicker', '32'),
    BUILTIN_MODE('15', 'Blue flicker', '33'),
    BUILTIN_MODE('16', 'Yellow flicker', '34'),
    BUILTIN_MODE('17', 'Cyan flicker', '35'),
    BUILTIN_MODE('18', 'Purple flicker', '36'),
    BUILTIN_MODE('19', 'White flicker', '37'),
    BUILTIN_MODE('20', 'Jumpy 7 colors', '38'),
    )

# Higher the number the faster
SPEED = {
    1: '1F',
    2: '1E',
    3: '1D',
    4: '1C',
    5: '1B',
    6: '1A',
    7: '10',
    8: '09',
    9: '08',
    10: '07',
    11: '06',
    12: '05',
    13: '04',
    14: '03',
    15: '02',
    16: '01'
}

COLOR_LIST = {
    'red': 'FF0000',
    'green': '00FF00',
    'blue': '0000FF'
}

STATUS_LIST = {
    'on': '23',
    'off': '24',
    'run': '20',
    'pause': '21'
}

def conn()
    host = options.device
    port = options.port
    s = socket.socket()
    s.connect((host, port))
    return s

def call(type, data):
    conn = conn()

    if type == 'get_status':
        payload = 'EF0177'
    if type == 'send_status':
        payload = 'CC{0}33'.format(STATUS_LIST(data[0]))
    if type == 'send_color':
        payload = '56{0}AA'.format(COLOR_LIST(data[0]))
    if type == 'send_builtin':
        payload = 'BB{0}{1}44'.format(BUILTIN_MODE(data[0]), SPEED(data[1]))

    conn.send(payload.decode('hex'))
    conn.close()

def get_defaults():
    cfg = SafeConfigParser()

    with open('docooler.cfg') as f:
        cfg_contents += f.read()
    cfg.readfp(StringIO(cfg_contents))

    def cfg_get(key, default=None):
        if cfg.has_option(DEFAULTSECT, key):
            return cfg.get(DEFAULTSECT, key)
        return default

    return {
        'device': cfg_get('device'),
        'port': cfg_get('port')
    }


def parse_options():
    parser = optparse.OptionParser()
    defaults = get_defaults()
    parser.add_option("-d", "--device", dest='device',
                      default=defaults['device'],
                      help="Device IP address")
    parser.add_option("-p", "--port", dest='port',
                      default=defaults['port'],
                      help="Port number to use")

    options, _ = parser.parse_args()

    for option in parser.option_list:
        if not option.dest:
            continue
        if not getattr(options, option.dest, None):
            parser.print_help()
            print >> sys.stderr, "\nRequired option {0} not specified".format(option)
            sys.exit(2)
    return options

if __name__ = '__main__':
    options = parse_options()
