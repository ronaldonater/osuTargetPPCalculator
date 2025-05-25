#!/usr/bin/env python3
"""
osu! PP Target Calculator - Single Play Version

This script calculates the PP value needed for ONE new top play to reach a target overall PP.

Requirements:
- requests library for API calls (optional)
- osu! API v2 client credentials (optional)

Usage:
1. Set API credentials (optional but recommended) or use manual input
2. Enter username and target PP
3. Get the required PP for a new #1 play
"""

import requests
import json

# osu! API v2 Configuration (optional - leave as-is for manual input)
CLIENT_ID = "41041"
CLIENT_SECRET = "RH5sL4kInLUCi5Z3lePrvPvR0w1zYa7b0T87v92F"
API_BASE_URL = "https://osu.ppy.sh/api/v2"

class OsuPPCalculator:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        if client_id != "your_client_id_here" and client_id != "":
            self.authenticate()
    
    def authenticate(self):
        """Authenticate with osu! API v2"""
        auth_url = "https://osu.ppy.sh/oauth/token"
        auth_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "public"
        }
        
        try:
            response = requests.post(auth_url, data=auth_data)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            print("✓ Connected to osu! API")
        except requests.RequestException as e:
            print(f"✗ API connection failed: {e}")
            raise
    
    def get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def get_user_data(self, username: str, mode: str = "osu"):
        """Get user profile and top scores"""
        user_url = f"{API_BASE_URL}/users/{username}/{mode}"
        user_response = requests.get(user_url, headers=self.get_headers())
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Get top 200 scores (more accurate for bonus PP calculation)
        scores_url = f"{API_BASE_URL}/users/{user_data['id']}/scores/best"
        scores_response = requests.get(scores_url, headers=self.get_headers(), 
                                     params={"limit": 200, "mode": mode})
        scores_response.raise_for_status()
        scores_data = scores_response.json()
        
        return user_data, [score["pp"] for score in scores_data if score["pp"] is not None]
    
    def calculate_weighted_pp(self, pp_values):
        """Calculate total weighted PP"""
        total = 0
        for i, pp in enumerate(pp_values):
            total += pp * (0.95 ** i)
        return total
    
    def calculate_bonus_pp(self, ranked_score_count):
        """Calculate bonus PP based on ranked score count"""
        return 416.6667 * (1 - (0.9994 ** ranked_score_count))
    
    def calculate_total_pp(self, pp_values, ranked_score_count):
        """Calculate total PP including bonus PP"""
        weighted_pp = self.calculate_weighted_pp(pp_values)
        bonus_pp = self.calculate_bonus_pp(ranked_score_count)
        return weighted_pp + bonus_pp
    
    def find_required_pp(self, current_scores, target_pp, ranked_score_count=0, actual_current_pp=None):
        """Find minimum PP needed for any new play to reach target"""

        # Sort current scores in descending order
        current_scores = sorted(current_scores, reverse=True)
        
        # Calculate current total PP with bonus PP
        calculated_current = self.calculate_total_pp(current_scores, ranked_score_count)
        
        # If we have the actual current PP, use it to correct our calculations
        if actual_current_pp is not None:
            current_total = actual_current_pp
        else:
            current_total = calculated_current
        
        pp_gain_needed = target_pp - current_total
        
        # Try inserting the new play at different positions to find minimum PP needed
        min_required_pp = float('inf')
        best_position = 0
        
        # Test positions from #1 to #100 (or end of current scores + 1)
        max_positions = min(101, len(current_scores) + 2)
        
        for position in range(max_positions):
            # For small gains, start search range much lower
            low = 0
            high = max(1000, current_scores[0] * 1.2 if current_scores else 1000)
            
            # Binary search for required PP at this position
            for _ in range(100):  # Limit iterations
                if high - low < 0.01:
                    break
                    
                mid = (low + high) / 2
                
                # Create new score list with test PP inserted at this position
                new_scores = current_scores.copy()
                new_scores.insert(position, mid)
                
                # Only top 100 scores count for weighted PP
                new_scores_top100 = new_scores[:100]
                
                # Calculate new weighted PP (only the weighted part changes)
                new_weighted_pp = self.calculate_weighted_pp(new_scores_top100)
                old_weighted_pp = self.calculate_weighted_pp(current_scores[:100])
                
                # The total PP change is just the weighted PP change
                # (bonus PP doesn't change when adding a new play)
                weighted_pp_gain = new_weighted_pp - old_weighted_pp
                new_total_pp = current_total + weighted_pp_gain
                
                if new_total_pp < target_pp:
                    low = mid
                else:
                    high = mid
            
            required_at_position = (low + high) / 2
            
            # Track the minimum PP needed across all positions
            if required_at_position < min_required_pp:
                min_required_pp = required_at_position
                best_position = position
        
        return min_required_pp, best_position

def main():
    print("osu! PP Target Calculator")
    print("=" * 30)
    
    # Check API setup
    use_api = (CLIENT_ID != "your_client_id_here" and CLIENT_SECRET != "your_client_secret_here")
    
    if use_api:
        # API Mode
        calculator = OsuPPCalculator(CLIENT_ID, CLIENT_SECRET)
        username = input("Enter username: ")
        target_pp = float(input("Enter target PP: "))
        mode = input("Mode (osu/taiko/fruits/mania) [osu]: ").strip() or "osu"
        
        print(f"\nFetching {username}'s data...")
        try:
            user_data, scores = calculator.get_user_data(username, mode)
            current_pp = user_data["statistics"]["pp"]
            ranked_score_count = user_data["statistics"]["ranked_score"]
            
            print(f"Current PP: {current_pp:.2f}")
            print(f"Ranked scores: {ranked_score_count:,}")
            print(f"Loaded {len(scores)} top plays")
            
        except Exception as e:
            print(f"Error: {e}")
            return
    else:
        # Manual Mode
        print("Manual input mode (no API)")
        username = input("Enter username: ")
        current_pp = float(input("Enter current total PP: "))
        target_pp = float(input("Enter target PP: "))
        
        print("\nEnter ALL your top play PP values (important for accuracy):")
        print("Also enter your total ranked score count for bonus PP calculation:")
        ranked_score_count = int(input("Total ranked scores: "))
        
        scores = []
        for i in range(1, 201):  # Up to 200 plays
            pp_input = input(f"Play #{i} PP (Enter to finish): ")
            if not pp_input.strip():
                break
            try:
                scores.append(float(pp_input))
            except ValueError:
                print("Invalid input, skipping")
        
        print(f"Entered {len(scores)} plays")
        
        # Verify current PP calculation with bonus PP
        temp_calc = OsuPPCalculator("", "")
        calculated_current = temp_calc.calculate_total_pp(sorted(scores, reverse=True), ranked_score_count)
        print(f"Calculated current PP (with bonus): {calculated_current:.2f}")
        print(f"You entered current PP as: {current_pp:.2f}")
        
        if abs(calculated_current - current_pp) > 10:
            print("⚠️  Warning: Difference between calculated and entered PP")
            print("   This may affect accuracy - try entering more plays")
    
    # Check if target is achievable
    if target_pp <= current_pp:
        print(f"\nTarget PP ({target_pp:.2f}) must be higher than current PP ({current_pp:.2f})")
        return
    
    # Calculate required PP
    if use_api:
        required_pp, position = calculator.find_required_pp(scores, target_pp, ranked_score_count, current_pp)
    else:
        # Create calculator instance without authentication for manual mode
        temp_calculator = OsuPPCalculator("", "")
        required_pp, position = temp_calculator.find_required_pp(scores, target_pp, ranked_score_count, current_pp)
    
    # Results
    print(f"\n{'='*40}")
    print(f"RESULT FOR {username.upper()}")
    print(f"{'='*40}")
    print(f"Current PP:  {current_pp:.2f}")
    print(f"Target PP:   {target_pp:.2f}")
    print(f"Difference:  +{target_pp - current_pp:.2f}")
    print(f"\n🎯 MINIMUM REQUIRED PP: {required_pp:.2f}pp")
    print(f"   (This play would rank #{position + 1} in your top plays)")
    print(f"{'='*40}")

if __name__ == "__main__":
    main()