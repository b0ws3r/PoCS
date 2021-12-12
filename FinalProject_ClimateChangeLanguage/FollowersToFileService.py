from TwitterHttpService import *

GET_FOLLOWER_IDS_PATH = "https://api.twitter.com/2/users/"


class RequestInfo:
    def __init__(self, path: str, output_dir: str):
        self.path = path
        self.output_dir = output_dir
        self.path_params = {}
        self.next_token=None
        self.query_params = {'max_results': 1000, 'user.fields': 'id'}

    def set_next_token(self, next_token):
        self.set_query_param('pagination_token', next_token)

    def set_path_param(self, key, value):
        self.path_params[key] = value

    def set_query_param(self, key, value):
        self.query_params[key] = value


def create_get_followers_request_info(user_id, output_dir):
    search_url = GET_FOLLOWER_IDS_PATH
    request_info = RequestInfo(search_url, output_dir)
    request_info.set_path_param('id', user_id)
    return request_info


def send_request_paginated(request_info: RequestInfo):
    total_tweets = 0
    bearer_token = auth()
    headers = create_headers(bearer_token)
    # Inputs
    count = 0  # Counting tweets per time period
    file_number = 0
    flag = True
    next_token = None

    # Check if flag is true
    while flag:
        print("-------------------")
        print("Token: ", next_token)
        json_response = connect_to_endpoint(request_info.path, headers, request_info)
        result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            next_token = json_response['meta']['next_token']
            request_info.set_next_token(next_token)
            print("Next Token: ", next_token)
            if result_count is not None and result_count > 0 and next_token is not None:
                # print("Start Date: ", start_list[i])
                append_to_csv(json_response, request_info.path_params['id'], request_info.output_dir, file_number)
                count += result_count
                total_tweets += result_count
                print("Total # of records added: ", total_tweets)
                print("-------------------")
                time.sleep(5)
                # If no next token exists

        else:
            if result_count is not None and result_count > 0:
                print("-------------------")
                # print("Start Date: ", start_list[i])
                append_to_csv(json_response, request_info.path_params['id'], request_info.output_dir, file_number)
                count += result_count
                total_tweets += result_count
                print("Total # of records added: ", total_tweets)
                print("-------------------")
                time.sleep(5)

            # Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            next_token = None


def append_to_csv(resp, user_id, output_dir, file_number):
    df = pd.DataFrame(resp['data'])
    df['SourceNode'] = len(resp['data']) * [user_id] # add a column so we know which user was tracked
    df.to_csv(f'{output_dir}/followers_user{user_id}_{str(file_number)}.csv')


def connect_to_endpoint(url, headers, request_info: RequestInfo):
    url = f"{url}{request_info.path_params.get('id')}/followers"
    response = requests.request("GET", url, headers=headers, params=request_info.query_params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

