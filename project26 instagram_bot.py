import collections
# Compatibility patch for Python 3.10+ (where collections.Iterable was moved)
if not hasattr(collections, 'Iterable'):
    import collections.abc
    collections.Iterable = collections.abc.Iterable

import random
import time
import webbrowser
import os
import sys
import json
import logging
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from threading import Thread
import schedule

# Suppress noisy version conflict warnings between instabot and modern requests/urllib3
try:
    from requests import RequestsDependencyWarning
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
except ImportError:
    pass

try:
    from instabot import Bot
except ImportError:
    print("ERROR: instabot library not found. Install it using:")
    print("pip install instabot schedule")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_bot.log'),
        logging.StreamHandler()
    ]
)


class InstaBot:
    def __init__(self, username, password, config=None):
        self.username = username
        self.password = password
        self.bot = Bot()
        self.is_logged_in = False
        self.session_file = f"config/{username}.session"
        self.config = config or {}
        self.tasks_completed = 0
        self.errors_encountered = 0

    def login(self):
        try:
            logging.info(f"Attempting login for {self.username}...")
            login_success = self.bot.login(
                username=self.username,
                password=self.password,
                use_cookie=False,
            )
            self.is_logged_in = bool(login_success)
            if self.is_logged_in:
                logging.info("✓ Logged in successfully.")
            else:
                logging.error("✗ Login failed. Check username/password or Instagram security checks.")
                self.errors_encountered += 1
            return self.is_logged_in
        except Exception as e:
            self.is_logged_in = False
            self.errors_encountered += 1
            if "ds_user" in str(e):
                logging.error("Login failed due to session issue (`ds_user`).")
                logging.error("Delete old bot session/config files and try again.")
            else:
                logging.error(f"Login failed: {e}")
            return False

    def cooldown(self, min_seconds=2, max_seconds=5):
        wait_for = random.randint(min_seconds, max_seconds)
        print(f"Waiting {wait_for}s to look more human...")
        time.sleep(wait_for)

    def safe_execute(self, action_name, action_fn):
        try:
            result = action_fn()
            if result is False or result is None:
                logging.warning(f"⚠ {action_name} failed (returned None/False).")
                self.errors_encountered += 1
                return result
            self.tasks_completed += 1
            logging.info(f"✓ {action_name} completed successfully.")
            return result
        except Exception as e:
            error_text = str(e)
            logging.error(f"✗ {action_name} failed: {error_text}")
            self.errors_encountered += 1
            if "checkpoint_required" in error_text:
                logging.error("Instagram blocked this action with 'checkpoint_required'.")
                logging.error("ACTION REQUIRED: Open Instagram on your phone/browser and complete the security challenge.")
            elif "challenge_required" in error_text:
                logging.error("Instagram requires a security challenge (SMS/Email).")
                logging.error("Try logging in via a real browser first to verify your identity.")
            elif "login_required" in error_text:
                logging.error("Your session has expired. Relogging may be needed.")
            return None

    @staticmethod
    def normalize_username(raw_value):
        username = raw_value.strip()
        if "instagram.com/" in username:
            username = username.split("instagram.com/")[-1]
        username = username.strip("/").split("/")[0]
        if username.startswith("@"):
            username = username[1:]
        return username

    def follow_user(self, username):
        def _action():
            clean_username = self.normalize_username(username)
            if not clean_username:
                raise ValueError("Please enter a valid username.")

            user_id = self.bot.get_user_id_from_username(clean_username)
            if not user_id:
                raise ValueError(
                    "Could not resolve this username. It may be invalid OR blocked by checkpoint_required."
                )
            # instabot follow works more reliably with user_id.
            return self.bot.follow(user_id)

        return self.safe_execute("Follow", _action)

    def unfollow_user(self, username):
        def _action():
            clean_username = self.normalize_username(username)
            if not clean_username:
                raise ValueError("Please enter a valid username.")

            user_id = self.bot.get_user_id_from_username(clean_username)
            if not user_id:
                raise ValueError(
                    "Could not resolve this username. It may be invalid OR blocked by checkpoint_required."
                )
            return self.bot.unfollow(user_id)

        return self.safe_execute("Unfollow", _action)

    def like_post(self, post_url):
        def _action():
            if not post_url or "instagram.com" not in post_url:
                raise ValueError("Invalid Instagram post URL.")
            try:
                media_id = self.bot.get_media_id_from_link(post_url)
                if not media_id:
                    raise ValueError("Could not extract media ID from URL.")
                return self.bot.like(media_id)
            except Exception as e:
                raise ValueError(f"Failed to like post: {str(e)}")

        return self.safe_execute("Like post", _action)

    def comment_post(self, post_url, comment):
        def _action():
            if not post_url or "instagram.com" not in post_url:
                raise ValueError("Invalid Instagram post URL.")
            if not comment or len(comment.strip()) == 0:
                raise ValueError("Comment cannot be empty.")
            try:
                media_id = self.bot.get_media_id_from_link(post_url)
                if not media_id:
                    raise ValueError("Could not extract media ID from URL.")
                return self.bot.comment(media_id, comment)
            except Exception as e:
                raise ValueError(f"Failed to comment on post: {str(e)}")

        return self.safe_execute("Comment on post", _action)

    def send_message(self, username, message):
        def _action():
            clean_username = self.normalize_username(username)
            if not clean_username:
                raise ValueError("Invalid username.")
            if not message or len(message.strip()) == 0:
                raise ValueError("Message cannot be empty.")
            return self.bot.send_message(message, [clean_username])

        return self.safe_execute("Send message", _action)

    def post_photo_video_with_caption(self, photo_video_path, caption):
        def _action():
            if not self._validate_file_exists(photo_video_path, ["jpg", "jpeg", "png", "mp4", "mov"]):
                raise ValueError(f"File not found or invalid format: {photo_video_path}")
            return self.bot.upload_photo(photo_video_path, caption=caption)

        return self.safe_execute("Upload post", _action)

    def upload_story_photo(self, photo_path):
        def _action():
            if not self._validate_file_exists(photo_path, ["jpg", "jpeg", "png"]):
                raise ValueError(f"Photo file not found or invalid format: {photo_path}")
            return self.bot.upload_story_photo(photo_path)

        return self.safe_execute("Upload story photo", _action)

    def upload_story_video(self, video_path):
        def _action():
            if not self._validate_file_exists(video_path, ["mp4", "mov"]):
                raise ValueError(f"Video file not found or invalid format: {video_path}")
            return self.bot.upload_story_video(video_path)

        return self.safe_execute("Upload story video", _action)

    @staticmethod
    def _validate_file_exists(file_path, allowed_extensions=None):
        """Validate if a file exists and has an allowed extension."""
        if not file_path:
            return False
        
        path = Path(file_path)
        if not path.exists():
            return False
        
        if allowed_extensions:
            file_ext = path.suffix.lstrip(".").lower()
            if file_ext not in allowed_extensions:
                return False
        
        return True

    def view_profile(self, username):
        def _action():
            clean_username = self.normalize_username(username)
            if not clean_username:
                raise ValueError("Invalid username.")
            user_info = self.bot.get_user_info(clean_username)
            if user_info:
                print(f"Username: {clean_username}")
                print(f"User Info: {user_info}")
            return user_info

        return self.safe_execute("View profile", _action)

    def view_stories(self, username):
        def _action():
            clean_username = self.normalize_username(username)
            if not clean_username:
                raise ValueError("Invalid username.")
            stories = self.bot.get_user_stories(clean_username)
            if stories:
                print(f"Stories for {clean_username}: {stories}")
            return stories

        return self.safe_execute("View stories", _action)

    def like_by_hashtag(self, hashtag, amount=10):
        """Like posts by hashtag (amount limit: 10-100 for safety)."""
        def _action():
            clean_hashtag = hashtag.lstrip("#")
            if not clean_hashtag:
                raise ValueError("Invalid hashtag.")
            amount_safe = max(1, min(amount, 100))
            logging.info(f"Liking {amount_safe} posts with #{clean_hashtag}...")
            self.bot.like_by_tags([clean_hashtag], amount=amount_safe)
            return True

        return self.safe_execute(f"Like by hashtag #{hashtag}", _action)

    def follow_by_hashtag(self, hashtag, amount=5):
        """Follow users from hashtag posts (amount limit: 5-50 for safety)."""
        def _action():
            clean_hashtag = hashtag.lstrip("#")
            if not clean_hashtag:
                raise ValueError("Invalid hashtag.")
            amount_safe = max(1, min(amount, 50))
            logging.info(f"Following {amount_safe} users from #{clean_hashtag}...")
            self.bot.follow_user_followers(
                [self.bot.get_user_id_from_username(clean_hashtag)], 
                amount=amount_safe
            )
            return True

        return self.safe_execute(f"Follow by hashtag #{hashtag}", _action)

    def run_automated(self):
        """Run bot with automated tasks based on configuration."""
        if not self.is_logged_in:
            logging.error("Not logged in. Cannot run automated tasks.")
            return
        
        logging.info("="*60)
        logging.info("AUTOMATED BOT STARTED - No human intervention required!")
        logging.info("="*60)
        
        # Schedule tasks based on configuration
        if self.config.get("enable_auto_like_hashtags"):
            hashtags = self.config.get("hashtags", [])
            interval_hours = self.config.get("like_hashtag_interval_hours", 2)
            for hashtag in hashtags:
                schedule.every(interval_hours).hours.do(
                    self._scheduled_like_hashtag, 
                    hashtag=hashtag
                )
                logging.info(f"Scheduled auto-like for #{hashtag} every {interval_hours}h")
        
        if self.config.get("enable_auto_follow_hashtags"):
            hashtags = self.config.get("follow_hashtags", [])
            interval_days = self.config.get("follow_hashtag_interval_days", 1)
            for hashtag in hashtags:
                schedule.every(interval_days).days.do(
                    self._scheduled_follow_hashtag,
                    hashtag=hashtag
                )
                logging.info(f"Scheduled auto-follow for #{hashtag} every {interval_days}d")
        
        if self.config.get("enable_daily_engagement"):
            schedule.every().day.at(self.config.get("engagement_time", "10:00")).do(
                self._scheduled_daily_engagement
            )
            logging.info(f"Scheduled daily engagement at {self.config.get('engagement_time', '10:00')}")
        
        if self.config.get("enable_auto_comment"):
            schedule.every(self.config.get("comment_interval_hours", 4)).hours.do(
                self._scheduled_auto_comment
            )
            logging.info(f"Scheduled auto-comments every {self.config.get('comment_interval_hours', 4)}h")
        
        # Main loop
        logging.info("Bot is now running continuously. Press Ctrl+C to stop.\n")
        try:
            while True:
                schedule.run_pending()
                
                # Heartbeat: Print every 5 minutes to show the bot is still active
                current_time = datetime.now().strftime("%H:%M:%S")
                if int(time.time()) % 300 < 60: # Rough 5-minute heartbeat
                     logging.info(f"[ALIVE] {current_time} - Bot is active and waiting for scheduled tasks...")
                
                time.sleep(60)  # Check every minute
                
                # Log stats every 5 tasks for better feedback
                if self.tasks_completed % 5 == 0 and self.tasks_completed > 0:
                    logging.info(f"[STATS UPDATE] Tasks Successfully Completed: {self.tasks_completed} | Errors: {self.errors_encountered}")
        
        except KeyboardInterrupt:
            logging.info("\n\nShutdown signal received. Logging out...")
            self.safe_execute("Logout", self.bot.logout)
            self._print_final_stats()
    
    def _scheduled_like_hashtag(self, hashtag):
        """Scheduled task: auto-like by hashtag."""
        amount = self.config.get("like_amount", 10)
        logging.info(f"[TASK] Auto-liking {amount} posts from #{hashtag}...")
        self.like_by_hashtag(hashtag, amount)
        self.cooldown(3, 8)
    
    def _scheduled_follow_hashtag(self, hashtag):
        """Scheduled task: auto-follow by hashtag."""
        amount = self.config.get("follow_amount", 5)
        logging.info(f"[TASK] Auto-following {amount} users from #{hashtag}...")
        self.follow_by_hashtag(hashtag, amount)
        self.cooldown(5, 12)
    
    def _scheduled_daily_engagement(self):
        """Scheduled task: daily engagement routine."""
        logging.info("[TASK] Running daily engagement routine...")
        if self.config.get("daily_follow_users"):
            for user in self.config.get("daily_follow_users", [])[:3]:
                self.follow_user(user)
                self.cooldown(2, 5)
        
        if self.config.get("daily_like_users"):
            for user_posts in self.config.get("daily_like_users", [])[:2]:
                logging.info(f"Liking posts from {user_posts}...")
                self.cooldown(3, 8)
    
    def _scheduled_auto_comment(self):
        """Scheduled task: auto-comment on posts."""
        logging.info("[TASK] Auto-commenting on posts...")
        comments = self.config.get("auto_comments", ["Nice!"])
        if self.config.get("recent_post_urls"):
            post_url = random.choice(self.config.get("recent_post_urls", []))
            comment = random.choice(comments)
            self.comment_post(post_url, comment)
            self.cooldown(2, 5)
    
    def _print_final_stats(self):
        """Print final statistics."""
        logging.info("\n" + "="*60)
        logging.info("AUTOMATION SESSION SUMMARY")
        logging.info("="*60)
        logging.info(f"Total Tasks Completed: {self.tasks_completed}")
        logging.info(f"Total Errors: {self.errors_encountered}")
        success_rate = (self.tasks_completed / (self.tasks_completed + self.errors_encountered) * 100) if (self.tasks_completed + self.errors_encountered) > 0 else 0
        logging.info(f"Success Rate: {success_rate:.1f}%")
        logging.info("="*60)


def load_config(config_file="bot_config.json"):
    """Load automation configuration from JSON file."""
    if not os.path.exists(config_file):
        logging.error(f"Config file not found: {config_file}")
        logging.info("Creating default config file...")
        create_default_config(config_file)
        logging.info(f"Default config created at {config_file}")
        sys.exit(0)
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logging.info(f"✓ Configuration loaded from {config_file}")
        return config
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return {}


def create_default_config(config_file="bot_config.json"):
    """Create a default configuration file template."""
    default_config = {
        "username": "your_instagram_username",
        "password": "your_instagram_password",
        "enable_auto_like_hashtags": True,
        "enable_auto_follow_hashtags": False,
        "enable_daily_engagement": True,
        "enable_auto_comment": False,
        "hashtags": ["python", "coding", "automation"],
        "follow_hashtags": ["technology"],
        "like_hashtag_interval_hours": 2,
        "follow_hashtag_interval_days": 1,
        "like_amount": 5,
        "follow_amount": 3,
        "engagement_time": "10:00",
        "comment_interval_hours": 4,
        "daily_follow_users": ["user1", "user2"],
        "daily_like_users": ["user1_profile"],
        "auto_comments": ["Nice!", "Love this!", "Great content!"],
        "recent_post_urls": ["https://www.instagram.com/p/ABC123/"],
        "max_errors_before_stop": 10,
        "daily_action_limit": 100
    }
    
    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=4)


def login_automated(username, password):
    """Attempt login without user interaction."""
    logging.info("Starting automated login process...")
    bot = InstaBot(username, password)
    
    for attempt in range(3):
        if bot.login():
            return bot
        if attempt < 2:
            logging.warning(f"Login attempt {attempt + 1} failed. Retrying in 30s...")
            time.sleep(30)
    
    logging.error("Failed to login after 3 attempts. Exiting.")
    return None


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" INSTAGRAM BOT - AUTOMATED VERSION")
    print(" (Running without human intervention)")
    print("="*60)
    
    config_file = "bot_config.json"
    
    # Load configuration
    config = load_config(config_file)
    
    if not config or "username" not in config or "password" not in config:
        logging.error("Invalid configuration. Please edit bot_config.json with your credentials.")
        sys.exit(1)
    
    username = config.get("username", "").strip()
    password = config.get("password", "").strip()
    
    if username == "your_instagram_username" or not username:
        logging.error("Please Update bot_config.json with your actual Instagram username!")
        sys.exit(1)
    
    if password == "your_instagram_password" or not password:
        logging.error("Please update bot_config.json with your actual Instagram password!")
        sys.exit(1)
    
    # Attempt automated login
    instagram_bot = login_automated(username, password)
    
    if instagram_bot:
        instagram_bot.run_automated()
    else:
        logging.error("Failed to start bot. Check credentials and try again.")
        sys.exit(1)

    