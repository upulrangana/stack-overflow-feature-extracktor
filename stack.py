import csv


class DataList(object):
    user_dict = {}
    user_csv_path = 'csv/users.csv'
    user_posts_csv = 'csv/posts.csv'
    user_comments_csv = 'csv/comments.csv'

    def __init__(self):
        # users
        with open(self.user_csv_path, encoding="utf8") as f:
            users_array = [{k: v for k, v in row.items()}
                           for row in csv.DictReader(f, skipinitialspace=True)]
        for row in users_array:
            user_id = row['Id']
            self.user_dict[user_id] = {'users': row, 'posts': [], 'comments': []}
        # posts
        with open(self.user_posts_csv, encoding="utf8") as f:
            posts_array = [{k: v for k, v in row.items()}
                           for row in csv.DictReader(f, skipinitialspace=True)]
            for row in posts_array:
                self.user_dict[row["UserId"]]['posts'].append(row)
        # comments
        with open(self.user_comments_csv, encoding="utf8") as f:
            comments_array = [{k: v for k, v in row.items()}
                              for row in csv.DictReader(f, skipinitialspace=True)]
        for row in comments_array:
            self.user_dict[row["OwnerUserId"]]['comments'].append(row)

    key_list = user_dict.keys()
    users_dict = {}

    def get_user_data(self, i):
        user_features = {}
        user_data = self.user_dict[i]
        id = user_data["users"]["Id"]
        user_features['Id'] = id
        post_Reputation = user_data["users"]["Reputation"]
        user_features['Reputation'] = post_Reputation
        post_Views = user_data["users"]["Views"]
        user_features['Views'] = post_Views
        post_UpVotes = user_data["users"]["UpVotes"]
        user_features['UpVotes'] = post_UpVotes
        post_DownVotes = user_data["users"]["DownVotes"]
        user_features['DownVotes'] = post_DownVotes
        return user_features

    def get_user_data_all(self):
        for i in self.key_list:
            post_Score = 0
            post_text_len = 0
            create_date_yr = 0
            all_features_dict = self.get_user_data(i)
            post_data = self.user_dict[i]["posts"]
            comments_data = self.user_dict[i]["comments"]
            for j in range(len(post_data)):
                data = post_data[j]
                post_Score = post_Score + int(data['Score'])
                post_text_len = post_text_len + len(data["Text"])
                create_date_yr = create_date_yr + int(data['CreationDate'][:4])

            post_score_val = post_Score / (j + 1)
            post_text_val = post_text_len / (j + 1)
            create_date_yr_val = create_date_yr / (j + 1)
            all_features_dict['post_score_val'] = post_score_val
            all_features_dict['post_text_val'] = post_text_val
            all_features_dict['create_date_yr_val'] = create_date_yr_val
            print(all_features_dict)
            self.users_dict[i] = all_features_dict
        print('gggggggggggggggggggggggggggggggggggggg')
        print(self.users_dict)
        reputation_list = []
        views_list = []
        upvotes_list = []
        downvotes_list = []
        post_score_val_list = []
        post_text_val_list = []
        create_date_yr_val_val_list = []
        for i in self.users_dict.keys():
            reputation = self.users_dict[i]['Reputation']
            reputation_list.append(reputation)
            view = self.users_dict[i]['Views']
            views_list.append(view)
            upvote = self.users_dict[i]['UpVotes']
            upvotes_list.append(upvote)
            downvote = self.users_dict[i]['DownVotes']
            downvotes_list.append(downvote)
            score = self.users_dict[i]['post_score_val']
            post_score_val_list.append(score)

            text = self.users_dict[i]['post_text_val']
            post_text_val_list.append(text)

            date = self.users_dict[i]['create_date_yr_val']
            create_date_yr_val_val_list.append(date)

        print(upvotes_list)
