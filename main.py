import requests
import json
import argparse

def request(method, params, token):
    url = f'https://api.vk.com/method/{method}'
    params.update({
        'access_token': token,
        'v': '5.131'
    })
    response = requests.get(url, params=params)
    response_data = response.json()
    if 'error' in response_data:
        raise Exception(f"Ошибка VK API: {response_data['error']['error_msg']}")
    return response_data['response']

def get_user_info(token, user_id):
    user = request('users.get', {'user_ids': user_id, 'fields': 'followers_count'}, token)[0]
    followers = request('users.getFollowers', {'user_id': user_id}, token).get('items', [])
    subscriptions = request('users.getSubscriptions', {'user_id': user_id, 'extended': 0}, token).get('groups', {}).get('items', [])
    return {
        'user': user,
        'followers': followers,
        'subscriptions': subscriptions
    }

def save(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main(token, user_id, result_path):
    data = get_user_info(token, user_id)
    save(data, result_path)
    print(f"Данные сохранены в {result_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VK user data collector")
    parser.add_argument('--token', type=str, help="VK API Access Token", required=True)
    parser.add_argument('--user_id', type=str, help="VK user ID", default=None)
    parser.add_argument('--result_path', type=str, help="Path to save the result JSON file", default="result.json")
    args = parser.parse_args()

    user_id = args.user_id if args.user_id else '185283514'
    result_path = args.result_path

    main(args.token, user_id, result_path)