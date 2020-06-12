"""
This script will return various reports from as many AWS accounts as you have configured in the config.conf file.
Written by:  Mike Kress ::  michael.s.kress@gmail.com


Current Reports:

all users
user mfa status

"""

import boto3
import pandas as pd
from datetime import datetime
from configparser import ConfigParser
import os.path


config = ConfigParser()
config.read('config.conf')


try:
    assert os.path.exists('config.conf')
except AssertionError:
    print(f'You do not have a config.conf file.  Make one and try again.')


def conf(environment):
    try:
        region_name = config[environment]['region_name']
        aws_access_key_id = config[environment]['aws_access_key_id']
        aws_secret_access_key = config[environment]['aws_secret_access_key']
    except KeyError:
        print(f'You have a config.conf file, but is not formatted correctly or is missing values')
    return region_name, aws_access_key_id, aws_secret_access_key


class User(object):
    Path: str
    UserName: str
    UserId: str
    Arn: str
    CreateDate: datetime
    PasswordLastUsed: datetime
    PermissionsBoundary: dict
    Tags: list

    def __init__(self, **kwargs):
        for field in self.__annotations__:
            if field in kwargs:
                setattr(self, field, kwargs.get(field))
            else:
                setattr(self, field, None)

    def __str__(self):
        return self.UserName

    def __repr__(self):
        return f"{self.__class__.__name__, getattr(self, 'UserName', 'Not Found')}"

    def dict(self):
        data = {}
        for field in self.__annotations__:
            data.update({field: getattr(self, field)})
        return data

    def _get_mfa(self, user):
        user = self.UserName
        mfa = self.iam.list_mfa_devices(UserName=user)
        try:
            a = mfa['MFADevices'][0]
            self.mfa_enabled = True
        except IndexError:
            self.mfa_enabled = False
        return self.mfa_enabled


def csv_out(data, arg, environment):
    df = pd.DataFrame()
    for i in data:
        df = df.append(i.dict(), ignore_index=True)


def output_router(*output):
    pass


def csv_out(users, report, environment):
    df = df_out(users)
    timestmp = datetime.now()
    df.to_csv(f'~/IAM_{report}_{environment}_{timestmp.strftime("%Y-%m-%d_%H%M%S")}.csv')
    print(df)


def main(*args):
    for environment in config.keys():
        if environment == 'DEFAULT':
            pass
        else:
            region_name, aws_access_key_id, aws_secret_access_key = conf(environment)
            iam = boto3.client(
                service_name="iam",
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
            data = iam.list_users()
            users = (User(**i) for i in data['Users'])
            for arg in args:
                print(arg)
                if arg == 'list_users_csv':
                    csv_out(users, arg, environment)
                if arg == 'mfa_report':
                    pass


if __name__ == '__main__':
    main(config['DEFAULT']['reports'])


