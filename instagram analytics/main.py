import os
import sys
import json
import logging
from datetime import datetime, timedelta

import facebook
import requests
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('instagram_analytics.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class InstagramAnalytics:
    def __init__(self):
        """
        Initialize Instagram Analytics by loading credentials and establishing connection
        """
        # Load environment variables
        load_dotenv()
        
        # Instagram/Facebook Graph API credentials
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.instagram_account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
        
        # Validate credentials
        if not all([self.access_token, self.page_id, self.instagram_account_id]):
            logger.error("Missing credentials. Please check your .env file.")
            sys.exit(1)
        
        # Initialize Facebook Graph API
        try:
            self.graph = facebook.GraphAPI(self.access_token)
        except Exception as e:
            logger.error(f"Failed to initialize Graph API: {e}")
            sys.exit(1)
    
    def get_account_insights(self, period='last_30d'):
        """
        Retrieve Instagram account insights
        """
        try:
            insights = self.graph.get_connections(
                path=f"{self.instagram_account_id}/insights",
                fields=[
                    'followers_count',
                    'profile_views',
                    'impressions',
                    'reach',
                    'email_contacts',
                    'get_directions_clicks',
                    'phone_call_clicks',
                    'text_message_clicks'
                ],
                period=period
            )
            return insights
        except Exception as e:
            logger.error(f"Error retrieving account insights: {e}")
            return None
    
    def get_media_insights(self, period='last_30d'):
        """
        Retrieve insights for recent media posts
        """
        try:
            # Get recent media
            media = self.graph.get_connections(
                path=f"{self.instagram_account_id}/media",
                fields=['id', 'caption', 'media_type', 'timestamp']
            )
            
            # Collect insights for each media post
            media_insights = []
            for post in media['data'][:10]:  # Limit to last 10 posts
                try:
                    post_insights = self.graph.get_connections(
                        path=f"{post['id']}/insights",
                        fields=[
                            'impressions', 
                            'engagement', 
                            'reach', 
                            'saved'
                        ]
                    )
                    media_insights.append({
                        'id': post['id'],
                        'caption': post.get('caption', 'No Caption'),
                        'timestamp': post.get('timestamp', 'Unknown'),
                        **post_insights['data'][0]
                    })
                except Exception as e:
                    logger.warning(f"Could not retrieve insights for post {post['id']}: {e}")
            
            return media_insights
        except Exception as e:
            logger.error(f"Error retrieving media insights: {e}")
            return None
    
    def visualize_follower_growth(self, insights):
        """
        Create a visualization of follower growth
        """
        try:
            # Extract follower count
            followers = insights.get('followers_count', {}).get('values', [])
            
            if not followers:
                logger.warning("No follower data available for visualization")
                return
            
            dates = [datetime.fromisoformat(entry['end_time'].replace('Z', '+00:00')) for entry in followers]
            counts = [entry['value'] for entry in followers]
            
            plt.figure(figsize=(10, 5))
            plt.plot(dates, counts, marker='o')
            plt.title('Follower Growth in Last 30 Days')
            plt.xlabel('Date')
            plt.ylabel('Follower Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('follower_growth.png')
            plt.close()
            
            logger.info("Follower growth visualization saved as 'follower_growth.png'")
        except Exception as e:
            logger.error(f"Error creating follower growth visualization: {e}")
    
    def generate_report(self):
        """
        Generate a comprehensive Instagram analytics report
        """
        logger.info("Starting Instagram Analytics Report Generation...")
        
        # Retrieve account insights
        account_insights = self.get_account_insights()
        if not account_insights:
            logger.error("Failed to retrieve account insights")
            return
        
        # Retrieve media insights
        media_insights = self.get_media_insights()
        if not media_insights:
            logger.error("Failed to retrieve media insights")
            return
        
        # Visualize follower growth
        self.visualize_follower_growth(account_insights)
        
        # Print account insights
        print("\n===== INSTAGRAM ACCOUNT INSIGHTS =====")
        for metric in account_insights['data']:
            print(f"{metric['name']}: {metric['values'][0]['value']}")
        
        # Print media insights
        print("\n===== TOP PERFORMING POSTS =====")
        media_df = pd.DataFrame(media_insights)
        print(tabulate(media_df, headers='keys', tablefmt='pretty'))
        
        # Export report to JSON
        with open('instagram_analytics_report.json', 'w') as f:
            json.dump({
                'account_insights': account_insights,
                'media_insights': media_insights
            }, f, indent=2)
        
        logger.info("Instagram Analytics Report Complete")

def main():
    """
    Main function to run Instagram Analytics
    """
    try:
        analytics = InstagramAnalytics()
        analytics.generate_report()
    except Exception as e:
        logger.error(f"An error occurred during analytics generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()