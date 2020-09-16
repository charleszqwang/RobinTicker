"""Contains all functions for the purpose of logging in and out to Robinhood."""
import getpass
import os
import pickle
import random

import robin_stocks.helper as helper
import robin_stocks.urls as urls


def generate_device_token():
    """This function will generate a token used when loggin on.

    :returns: A string representing the token.

    """
    rands = []
    for i in range(0, 16):
        r = random.random()
        rand = 4294967296.0 * r
        rands.append((int(rand) >> ((3 & i) << 3)) & 255)

    hexa = []
    for i in range(0, 256):
        hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

    id = ""
    for i in range(0, 16):
        id += hexa[rands[i]]

        if (i == 3) or (i == 5) or (i == 7) or (i == 9):
            id += "-"

    return(id)


def respond_to_challenge(challenge_id, sms_code):
    """This functino will post to the challenge url.

    :param challenge_id: The challenge id.
    :type challenge_id: str
    :param sms_code: The sms code.
    :type sms_code: str
    :returns:  The response from requests.

    """
    url = urls.challenge_url(challenge_id)
    payload = {
        'response': sms_code
    }
    return(helper.request_post(url, payload))


def login(username=None, password=None, expiresIn=86400, scope='internal', by_sms=True, store_session=True):
    """This function will effectivly log the user into robinhood by getting an
    authentication token and saving it to the session header. By default, it
    will store the authentication token in a pickle file and load that value
    on subsequent logins.

    :param username: The username for your robinhood account, usually your email.
        Not required if credentials are already cached and valid.
    :type username: Optional[str]
    :param password: The password for your robinhood account. Not required if
        credentials are already cached and valid.
    :type password: Optional[str]
    :param expiresIn: The time until your login session expires. This is in seconds.
    :type expiresIn: Optional[int]
    :param scope: Specifies the scope of the authentication.
    :type scope: Optional[str]
    :param by_sms: Specifies whether to send an email(False) or an sms(True)
    :type by_sms: Optional[boolean]
    :param store_session: Specifies whether to save the log in authorization
        for future log ins.
    :type store_session: Optional[boolean]
    :returns:  A dictionary with log in information. The 'access_token' keyword contains the access token, and the 'detail' keyword \
    contains information on whether the access token was generated or loaded from pickle file.

    """
    device_token = generate_device_token()
    home_dir = os.path.expanduser("~")
    data_dir = os.path.join(home_dir, ".tokens")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    creds_file = "robinhood.pickle"
    pickle_path = os.path.join(data_dir, creds_file)
    # Challenge type is used if not logging in with two-factor authentication.
    if by_sms:
        challenge_type = "sms"
    else:
        challenge_type = "email"

    url = urls.login_url()
    payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': expiresIn,
        'grant_type': 'password',
        'password': password,
        'scope': scope,
        'username': username,
        'challenge_type': challenge_type,
        'device_token': device_token
    }
    print('1')
    # If authentication has been stored in pickle file then load it. Stops login server from being pinged so much.
    if os.path.isfile(pickle_path):
        # If store_session has been set to false then delete the pickle file, otherwise try to load it.
        # Loading pickle file will fail if the acess_token has expired.
        print('isfile', store_session)
        if store_session == 'true':
            print('storesession')
            try:
                with open(pickle_path, 'rb') as f:
                    print('here')
                    pickle_data = pickle.load(f)
                    access_token = pickle_data['access_token']
                    token_type = pickle_data['token_type']
                    refresh_token = pickle_data['refresh_token']
                    # Set device_token to be the original device token when first logged in.
                    pickle_device_token = pickle_data['device_token']
                    payload['device_token'] = pickle_device_token
                    # Set login status to True in order to try and get account info.
                    helper.set_login_state(True)
                    helper.update_session(
                        'Authorization', '{0} {1}'.format(token_type, access_token))
                    # Try to load account profile to check that authorization token is still valid.
                    res = helper.request_get(
                        urls.portfolio_profile(), 'regular', payload, jsonify_data=False)
                    # Raises exception is response code is not 200.
                    res.raise_for_status()
                    return({'access_token': access_token, 'token_type': token_type,
                            'expires_in': expiresIn, 'scope': scope, 'detail': 'logged in using authentication in {0}'.format(creds_file),
                            'backup_code': None, 'refresh_token': refresh_token})
            except:
                print(
                    "ERROR: There was an issue loading pickle file. Authentication may be expired - logging in normally.")
                helper.set_login_state(False)
                helper.update_session('Authorization', None)
        else:
            os.remove(pickle_path)
    # Try to log in normally.
    if not username:
        return {'detail': 'no pickle'}
    if not password:
        password = getpass.getpass("Robinhood password: ")
        payload['password'] = password

    data = helper.request_post(url, payload)
    # Handle case where mfa or challenge is required.
    if data:
        if 'access_token' in data:
            token = '{0} {1}'.format(data['token_type'], data['access_token'])
            helper.update_session('Authorization', token)
            helper.set_login_state(True)
            data['detail'] = "logged in with brand new authentication code."
            if store_session:
                with open(pickle_path, 'wb') as f:
                    pickle.dump({'token_type': data['token_type'],
                                 'access_token': data['access_token'],
                                 'refresh_token': data['refresh_token'],
                                 'device_token': device_token}, f)
            return data
        else:
            data['device_token'] = payload['device_token']
            return data
    else:
        return {"error": "Trouble connecting to robinhood API. Check internet connection."}

def verify(username=None, password=None, expiresIn=86400, scope='internal', by_sms=True, store_session=True, auth_type="challenge", code=None, device_token=None, challenge_id=None):
    """This function will effectivly log the user into robinhood by getting an
    authentication token and saving it to the session header. By default, it
    will store the authentication token in a pickle file and load that value
    on subsequent logins.

    :param username: The username for your robinhood account, usually your email.
        Not required if credentials are already cached and valid.
    :type username: Optional[str]
    :param password: The password for your robinhood account. Not required if
        credentials are already cached and valid.
    :type password: Optional[str]
    :param expiresIn: The time until your login session expires. This is in seconds.
    :type expiresIn: Optional[int]
    :param scope: Specifies the scope of the authentication.
    :type scope: Optional[str]
    :param by_sms: Specifies whether to send an email(False) or an sms(True)
    :type by_sms: Optional[boolean]
    :param store_session: Specifies whether to save the log in authorization
        for future log ins.
    :type store_session: Optional[boolean]
    :param auth_type: Specifies whetner authorization is through mfa code or sms challenge
    :type auth_type: Optional[str]
    :param code: Mfa code or sms challenge code
    :type code: Required[str]
    :param device_token: Previously used device token
    :type device_token: Required[str]
    :param challenge_id: Challenge id
    :type challenge_id: Required[str]
    :returns:  A dictionary with log in information. The 'access_token' keyword contains the access token, and the 'detail' keyword \
    contains information on whether the access token was generated or loaded from pickle file.

    """
    home_dir = os.path.expanduser("~")
    data_dir = os.path.join(home_dir, ".tokens")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    creds_file = "robinhood.pickle"
    pickle_path = os.path.join(data_dir, creds_file)
    # Challenge type is used if not logging in with two-factor authentication.
    if by_sms:
        challenge_type = "sms"
    else:
        challenge_type = "email"

    url = urls.login_url()
    payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': expiresIn,
        'grant_type': 'password',
        'password': password,
        'scope': scope,
        'username': username,
        'challenge_type': challenge_type,
        'device_token': device_token
    }

    if auth_type == "mfa":
        mfa_token = code
        payload['mfa_code'] = mfa_token
        res = helper.request_post(url, payload, jsonify_data=False)
        if res.status_code != 200:
            return {'Error': "Incorrect code"}
        data = res.json()
    elif auth_type == "challenge":
        sms_code = code
        print("challenge:\n", challenge_id, code)
        res = respond_to_challenge(challenge_id, sms_code)
        if 'challenge' in res and res['challenge']['remaining_attempts'] > 0:
            print("retry\n")
            return {'error': "Incorrect code", 'attempts_left': res['challenge']['remaining_attempts']}
        else:
            print('res', res)
        helper.update_session(
            'X-ROBINHOOD-CHALLENGE-RESPONSE-ID', challenge_id)
        print('payload:\n', payload)
        data = helper.request_post(url, payload)
        print('data:\n', data)
    # Update Session data with authorization or raise exception with the information present in data.
    if 'access_token' in data:
        token = '{0} {1}'.format(data['token_type'], data['access_token'])
        helper.update_session('Authorization', token)
        helper.set_login_state(True)
        data['detail'] = "logged in with brand new authentication code."
        print('store', store_session)
        if store_session:
            print('yeboi')
            with open(pickle_path, 'wb') as f:
                pickle.dump({'token_type': data['token_type'],
                                'access_token': data['access_token'],
                                'refresh_token': data['refresh_token'],
                                'device_token': device_token}, f)
    else:
        return {"error": data["detail"]}

    return(data)



@helper.login_required
def logout():
    """Removes authorization from the session header.

    :returns: None

    """
    helper.set_login_state(False)
    helper.update_session('Authorization', None)

    home_dir = os.path.expanduser("~")
    data_dir = os.path.join(home_dir, ".tokens")
    if not os.path.exists(data_dir):
        return 
    creds_file = "robinhood.pickle"
    pickle_path = os.path.join(data_dir, creds_file)
    if os.path.isfile(pickle_path):
            os.remove(pickle_path)