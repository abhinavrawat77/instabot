# including libraries
import requests,urllib
from textblob import TextBlob
from instabot import get_keywords
# Access Token to get the access for instagram exchange
APP_ACCESS_TOKEN = '4125485297.91d5653.0a9d3a55c5bb425493773be71cef0ec3'
#acces token for  paralleldots
APP_ACCESS_TOKEN_PD = 'rnaQPDGNt7ZmD8wFa1e3qlDu9SQnEf52ZGdhAJXB8Q0'
BASE_URL = 'https://api.instagram.com/v1/'
BASE_URL_PD = 'https://apis.paralleldots.com/'


# Function for getting your own details
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function for obtaining user-id from username
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

# Function for getting other user's information

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


# Function to get your own recent post
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# Function to get user recent post
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# Function to get id of recent post by the user using their username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
   #  print user_media

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


# Function to make a like on a user's recent post
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:

        print 'Your like was unsuccessful. Try again!'


# Function to make a comment on a user's recent post
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"
# Function to post our promotional comment on the desired post
def post_promotional_comment(insta_promotional_message, insta_username):
    media_id = get_post_id(insta_username)
    payload = {"access_token": APP_ACCESS_TOKEN, "text": insta_promotional_message}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a promotional comment!"
    else:
        print "Unable to add comment. Try again!"


# function to do marketing
#this function will help us finding and analysing desired caption , tags and comments
#and then comment on that post related to our marketing product
def insta_marketing(insta_keyword,insta_promotional_message,insta_username):
    # Analyze comments
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    print comment_info
    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']):

            for index_var in range(0, len(comment_info['data'])):
                comment_text = comment_info['data'][index_var]['text']
                print comment_text
                comment_words = comment_text.split()
                print comment_words
                for i in range(0,comment_words.__len__()):
                    if(comment_words[i] == insta_keyword):
                        post_promotional_comment(insta_promotional_message,insta_username)
                        break
    else:
        print 'Status code other than 200 received'

    # Analyze captions and tags
    request_url = (BASE_URL+'media/%s?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    media_data=requests.get(request_url).json()

    if(media_data) is not None:

        print media_data

        if (media_data['meta']['code']== 200):

            if len(media_data['data']['tags']):
                insta_tag = media_data['data']['tags']
                for index_var in range(0,insta_tag.__len__()):
                    if insta_tag[index_var]==insta_keyword:
                        print insta_tag[index_var]
                        post_promotional_comment(insta_promotional_message,insta_username)
                        break
                    else:
                        print 'Not matched'
            else:
                print 'No tags'


            if  (media_data['data']['caption']) is  not  None:
                insta_caption = media_data['data']['caption']['text']
                type(insta_caption)
                insta_caption_words = insta_caption.split()

                # using paralleldots to check keywords of caption
                c= insta_caption.encode('ascii','ignore')
                print type(c)
                op_of_func=get_keywords(c ,APP_ACCESS_TOKEN_PD)

                if(len(op_of_func) >0):
                    keywords_in_caption = op_of_func[0]

                    print op_of_func[0]
                    print type(op_of_func)
                    for p in range(0, keywords_in_caption.__len__()):
                        if (keywords_in_caption[p] == insta_keyword):
                            print keywords_in_caption[p]
                            post_promotional_comment(insta_promotional_message, insta_username)
                            break
                        else:
                            print 'Not matched'

                # directly checking all words of caption
                for p in range(0, insta_caption_words.__len__()):
                    if (insta_caption_words[p] == insta_keyword):
                        print insta_caption_words[p]
                        post_promotional_comment(insta_promotional_message, insta_username)
                        break
                    else:
                        print 'Not matched'
            else:
                print 'No caption'
        else:
            'Status code other than 200 received'



# Function to start the bot and presenting a menu

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instabotapi!'
        print 'chooese any of the following:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e. Like the recent post of a user \n"
        print "f.Make a comment on the recent post of a user\n"
        print "g.To do marketing using specific captions\n"
        print "h.Exit"

        choice = raw_input("Enter your choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            if insta_username=="":
                print 'enter a valid username'
            else:
                another_user_detail(insta_username)
        elif choice == "c":
            user_recent_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            if insta_username=="":
                print 'enter a valid username'
            else:
                user_recent_media(insta_username)

        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           if insta_username == "":
               print 'enter a valid username'
           else:
               like_a_post(insta_username)

        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           if insta_username == "":
               print 'enter a valid username'
           else:
               post_a_comment(insta_username)
        elif choice=="g":
            insta_keyword = raw_input("Enter the keyword to be searched :")
            insta_promotional_message = raw_input("Enter the text to be commented :")
            insta_username = raw_input("Enter the username :")
            insta_marketing(insta_keyword, insta_promotional_message, insta_username)



        elif choice == "h":
            exit()
        else:
            print "wrong choice"



start_bot()









