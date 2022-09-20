import resources as rs
import sys


def get_capture_prob():
    capture_prob, mf_error, db_error, em_error = rs.get_data(sys.argv[1], sys.argv[2])
    if mf_error:
        raise ValueError('There is something wrong with the "millennium-falcon.json" file')
    elif db_error:
        return ValueError('There is something wrong with the database')
    elif em_error:
        return ValueError('There is something wrong with the "empire.json" file')
    else:
        return capture_prob


print(get_capture_prob())
