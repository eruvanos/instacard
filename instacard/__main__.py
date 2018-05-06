import logging

from instacard import create_app, log_util

if __name__ == '__main__':
    log_util.configure().setLevel('INFO')
    logging.getLogger('urllib3.connectionpool').setLevel('WARN')

    create_app().run('0.0.0.0', port=5000, debug=False)
