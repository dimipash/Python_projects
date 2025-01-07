import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

class ExpenseCategorizer:
    def __init__(self, transactions):
        self.transactions = transactions
        self.categories = {}
        
    def preprocess_data(self):
        """Clean and prepare transaction data"""
        self.transactions['description'] = self.transactions['description'].str.lower()
        self.transactions = self.transactions[self.transactions['amount'] > 0]
        
    def vectorize_text(self):
        """Convert transaction descriptions to numerical features"""
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.text_features = vectorizer.fit_transform(self.transactions['description'])
        
    def cluster_transactions(self, n_clusters=5):
        """Group similar transactions using KMeans clustering"""
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.transactions['category'] = self.kmeans.fit_predict(self.text_features)
        
    def analyze_categories(self):
        """Generate insights and visualizations"""
        category_summary = self.transactions.groupby('category').agg({
            'amount': ['sum', 'count'],
            'description': lambda x: x.value_counts().index[0]
        })
        
        plt.figure(figsize=(10, 6))
        category_summary['amount']['sum'].plot(kind='bar')
        plt.title('Total Spending by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.savefig('category_spending.png')
        
        return category_summary
    
    def run_analysis(self):
        """Run complete analysis pipeline"""
        self.preprocess_data()
        self.vectorize_text()
        self.cluster_transactions()
        return self.analyze_categories()

if __name__ == "__main__":
    # Sample transaction data
    data = {
        'date': pd.date_range('2023-01-01', periods=100, freq='D'),
        'description': [
            'Starbucks Coffee', 'Whole Foods Market', 'Uber Ride', 
            'Amazon Purchase', 'Shell Gas Station', 'Netflix Subscription',
            'Apple App Store', 'CVS Pharmacy', 'Target', 'Walmart',
            'Spotify Subscription', 'AT&T Bill', 'Comcast Bill',
            'Electricity Bill', 'Water Bill', 'Mortgage Payment',
            'Car Insurance', 'Health Insurance', 'Gym Membership',
            'Restaurant Bill'
        ] * 5,
        'amount': [abs(x) for x in pd.np.random.normal(50, 20, 100)]
    }
    
    transactions = pd.DataFrame(data)
    categorizer = ExpenseCategorizer(transactions)
    results = categorizer.run_analysis()
    print("Expense Analysis Results:")
    print(results)
    print("Visualization saved as category_spending.png")
