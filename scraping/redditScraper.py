import praw
import config
CLIENT_ID = config.client_id
CLIENT_SECRET = config.client_secret
USER_AGENT = config.user_agent
TARGET_USERNAME = config.target_username
QUERY = config.comment_query

def count_user_comments_with_term(
    username: str, 
    search_term: str, 
    client_id: str,
    client_secret: str,
    user_agent: str = "script:comment_search:v1.0 (by u/your_reddit_username)"
):
    """
    Connects to Reddit via the PRAW library, fetches the comment history
    of the specified user, and counts how many comments contain `search_term`.
    """
    # 1) Create a Reddit instance with your credentials
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    
    # 2) Access the user's comment stream
    redditor = reddit.redditor(username)
    
    # 3) Iterate through the user's comments, counting matches
    count = 0
    # By default, .new(limit=None) attempts to fetch up to 1000 comments, 
    # limited by the Reddit API's constraints.
    for comment in redditor.comments.new(limit=None):
        if search_term.lower() in comment.body.lower():
            count += 1
    
    return count


if __name__ == "__main__":
        
    matches = count_user_comments_with_term(
        username=TARGET_USERNAME, 
        search_term=QUERY,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    
    print(f"Number of comments by u/{TARGET_USERNAME} that contain '{QUERY}': {matches}")
