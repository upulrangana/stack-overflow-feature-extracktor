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

        post_Reputation = user_data["users"]["Reputation"]
        user_features['Reputation'] = post_Reputation
        post_Views = user_data["users"]["Views"]
        user_features['Views'] = post_Views
        post_UpVotes = user_data["users"]["UpVotes"]
        user_features['UpVotes'] = post_UpVotes
        post_DownVotes = user_data["users"]["DownVotes"]
        user_features['DownVotes'] = post_DownVotes
        return user_features

    def get_feature_set_with_lable(self):
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
            self.users_dict[i] = all_features_dict
        reputation_list = []
        views_list = []
        upvotes_list = []
        downvotes_list = []
        post_score_val_list = []
        post_text_val_list = []
        create_date_yr_val_val_list = []
        for i in self.users_dict.keys():
            reputation = self.users_dict[i]['Reputation']
            reputation_list.append(int(reputation))
            view = self.users_dict[i]['Views']
            views_list.append(int(view))
            upvote = self.users_dict[i]['UpVotes']
            upvotes_list.append(int(upvote))
            downvote = self.users_dict[i]['DownVotes']
            downvotes_list.append(int(downvote))
            score = self.users_dict[i]['post_score_val']
            post_score_val_list.append(int(score))
            text = self.users_dict[i]['post_text_val']
            post_text_val_list.append(int(text))
            date = self.users_dict[i]['create_date_yr_val']
            create_date_yr_val_val_list.append(int(date))
        # print(upvotes_list)
        reputation_list_max = int(max(reputation_list))
        reputation_list_min = int(min(reputation_list))
        views_list_max = int(max(views_list))
        views_list_min = int(min(views_list))
        upvotes_list_max = int(max(upvotes_list))
        upvotes_list_min = int(min(upvotes_list))
        downvotes_list_max = int(max(downvotes_list))
        downvotes_list_min = int(min(downvotes_list))
        post_score_val_list_max = int(max(post_score_val_list))
        post_score_val_list_min = int(min(post_score_val_list))
        post_text_val_list_max = int(max(post_text_val_list))
        post_text_val_list_min = int(min(post_text_val_list))
        create_date_yr_val_list_max = int(max(create_date_yr_val_val_list))
        create_date_yr_val_list_min = int(min(create_date_yr_val_val_list))

        def normalize(key, i, list_max, list_min):
            feature_val = (int(self.users_dict[i][key]) - list_min) / (list_max - list_min)
            return feature_val

        # print(self.users_dict)
        normalize_features_list = []
        lable_list = []
        for i in self.users_dict.keys():
            reputation_weight = 3
            view_weight = 2
            upvote_weight = 1
            downvote_weight = 0.2
            post_score_val_weight = 0
            post_text_val_weight = 2
            create_date_yr_weight = 2
            normalize_feature_list = []
            normalize_feature_list.append(
                reputation_weight * normalize('Reputation', i, reputation_list_max, reputation_list_min))
            normalize_feature_list.append(view_weight * normalize('Views', i, views_list_max, views_list_min))
            normalize_feature_list.append(upvote_weight * normalize('UpVotes', i, upvotes_list_max, upvotes_list_min))
            normalize_feature_list.append(
                downvote_weight * (1 - normalize('DownVotes', i, downvotes_list_max, downvotes_list_min)))
            normalize_feature_list.append(
                post_score_val_weight * normalize('post_score_val', i, post_score_val_list_max,
                                                  post_score_val_list_min))
            normalize_feature_list.append(
                post_text_val_weight * normalize('post_text_val', i, post_text_val_list_max, post_text_val_list_min))
            normalize_feature_list.append(
                create_date_yr_weight * normalize('create_date_yr_val', i, create_date_yr_val_list_max,
                                                  create_date_yr_val_list_min))

            normalize_features_list.append(normalize_feature_list)

        for i in range(len(normalize_features_list)):
            lable_val=sum(normalize_features_list[i])
            normalize_features_list[i].append(lable_val)



            lable_list.append(lable_val)
        # print(lable_list)

        lable_val_max = max(lable_list)#4.465173766346023
        lable_val_min = min(lable_list)#1.0043620892965808
        for i in range(len(normalize_features_list)):
            lable_val=normalize_features_list[i][7]

            toatal_weight=reputation_weight+view_weight+upvote_weight+downvote_weight+post_score_val_weight+post_text_val_weight+create_date_yr_weight
            if toatal_weight > lable_val and lable_val>(lable_val_max-lable_val_min)*0.75+lable_val_min:
                normalize_features_list[i].append('expert')

            elif (lable_val_max-lable_val_min)*0.75+lable_val_min > lable_val and lable_val>(lable_val_max-lable_val_min)*0.5+lable_val_min:
                normalize_features_list[i].append('advanced')

            elif (lable_val_max-lable_val_min)*0.5+lable_val_min > lable_val and lable_val>(lable_val_max-lable_val_min)*0.25+lable_val_min:
                normalize_features_list[i].append('intermediate')

            elif (lable_val_max-lable_val_min)*0.25+lable_val_min > lable_val and lable_val>0:
                normalize_features_list[i].append('beginner')
        print(normalize_features_list)


