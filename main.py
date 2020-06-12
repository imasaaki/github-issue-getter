
import requests, os, json, datetime, time
import sys

args = sys.argv

print(args)
print("arg1：" + args[1])
print("arg2：" + args[2])
print("arg3：" + args[3])
print("arg4：" + args[4])
print("arg5：" + args[5])
print("arg6：" + args[6])

github_id = args[1]
github_password = args[2]
github_owner = args[3]
github_repository = args[4]
github_max_issue_number = int(args[5])
github_search_txt = args[6]

# issue_max_number = 39782

with open("output_" + github_owner + github_repository + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv', mode='a') as out_file:
    out_file.write('"url","title","state","milestone","created_at","updated_at","labels"' + '\r\n')
    for i in range(30000, github_max_issue_number):
        api_url = 'https://api.github.com/repos/' + github_owner + '/' + github_repository + '/issues/' + str(i + 1)
        # deprecate(up to 2020/9/30) it should be oauh token
        # res = requests.get(api_url,  auth=('imasaaki2', '1234567890github'))
        res = requests.get(api_url,  auth=(github_id, github_password))
        result = res.json()
        # print(api_url)

        time.sleep(1)

        # print(json.dumps(result))

        try:
            # if '🐛' in result['body']:
            if github_search_txt != '' and github_search_txt in result['body']:
                print('search hit!!!: ' + result['html_url'])

                url = ''
                title = ''
                state = ''
                milestone = ''
                created_at = ''
                updated_at = ''
                labels_str = ''

                url = result['html_url']
                title = result['title']
                state = result['state']

                try:
                    milestone = result['milestone']
                except:
                    print('error: no milestone')
                
                created_at = result['created_at']

                try:
                    updated_at = result['updated_at']
                except:
                    print('error: no updated_at')

                try:
                    labels = result['labels']
                    for label in labels:
                        labels_str = labels_str + ';' + label['name']
                except:
                    print('error: no labels')

                out_file.write('"{}","{}","{}","{}","{}","{}","{}"'.format(
                        url,
                        title,
                        state,
                        milestone,
                        created_at[0:10],
                        updated_at[0:10],
                        labels_str) + '\r\n')
            else:
                print('search no hit: ' + result['html_url'])
        except:
            print('loop error')

