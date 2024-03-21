import os
from dotenv import load_dotenv
from fastapi import FastAPI
from instaloader import Instaloader, Profile

current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

username: str = os.getenv("INSTAGRAM_USERNAME")
password: str = os.getenv("INSTAGRAM_PASSWORD")
target_profile: str = os.getenv("INSTAGRAM_TARGET_PROFILE")

def get_instagram_posts(limit=6):
    L = Instaloader()  # Initialize Instaloader instance

    # Login
    L.login(user=username, passwd=password)

    # Load the target profile
    profile = Profile.from_username(L.context, target_profile)

    # Iterate through posts with a counter
    posts = []
    post_count = 0
    for post in profile.get_posts():
        post_info = {
            "caption": post.caption,
            "date": post.date_utc,
            "url": post.url,
            "likes": post.likes,
            "comments": post.comments
        }
        posts.append(post_info)
        post_count += 1
        if post_count >= limit:
            break  # Exit the loop when limit is reached

    return posts

app = FastAPI()

@app.get("/instagram/posts")
async def get_instagram_posts_api():
    try:
        scraped_posts = get_instagram_posts()
    except Exception as e:
        return {"error": f"Error scraping Instagram posts: {str(e)}"}

    return scraped_posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000) 
