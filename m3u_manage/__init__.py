# -*- coding: utf-8 -*-
# m3u-manage (c) Ian Dennis Miller

import json

def load_cfg(config):
    try:
        with open(config, 'r') as f:
            cfg = json.load(f)
    except FileNotFoundError:
        print("Error: config {} not found".format(config))
        return(-1)
    except json.decoder.JSONDecodeError as e:
        print("Error: cannot parse {}".format(config))
        print(e)
        return(-1)
    return(cfg)

class M3UManage:
    def __init__(self):
        pass
