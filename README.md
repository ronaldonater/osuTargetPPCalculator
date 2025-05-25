# osu! PP Target Calculator

A Python script that calculates the exact PP value needed for a new top play to reach your target overall PP in osu!.

## Features

- 🎯 **Precise calculations** - Uses the exact osu! PP weighting formula (0.95^n)
- 🏆 **Bonus PP support** - Accounts for bonus PP from ranked score count
- 🔄 **Position optimization** - Finds the minimum PP needed by testing all possible ranking positions
- 🌐 **API integration** - Automatically fetches your profile data (optional but recommended)
- 📝 **Manual mode** - Works without API credentials for privacy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/osu-pp-calculator.git
cd osu-pp-calculator
```

2. Install required dependencies:
```bash
pip install requests
```

## Setup

### Option 1: API Mode (Recommended)

1. **Get osu! API credentials:**
   - Go to [osu! account settings](https://osu.ppy.sh/home/account/edit)
   - Navigate to "OAuth" section
   - Click "New OAuth Application"
   - Fill in the form:
     - **Application Name**: `PP Calculator` (or any name you prefer)
     - **Application Callback URL**: Used to be required, but nowadays, you could leave this blank.
   - Click "Register Application"
   - Copy your **Client ID** and **Client Secret**

2. **Add credentials to the script:**
   - Open `osu_pp_calculator.py`
   - Replace the placeholder values:
   ```python
   CLIENT_ID = "your_actual_client_id_here"
   CLIENT_SECRET = "your_actual_client_secret_here"
   ```

### Option 2: Manual Mode

Leave the credentials as placeholders - the script will automatically switch to manual input mode.

## Usage

Run the script:
```bash
python osu_pp_calculator.py
```

### API Mode
1. Enter your osu! username
2. Enter your target PP
3. Select game mode (osu/taiko/fruits/mania)
4. Get your result!

### Manual Mode
1. Enter your username (for display only)
2. Enter your current total PP
3. Enter your target PP
4. Enter your total ranked score count
5. Input your top play PP values one by one
6. Get your result!

## Example Output

```
osu! PP Target Calculator
==============================
✓ Connected to osu! API

Enter username: cookiezi
Enter target PP: 17000
Mode (osu/taiko/fruits/mania) [osu]: osu

Fetching cookiezi's data...
Current PP: 16543.21
Ranked scores: 1,247
Loaded 200 top plays

========================================
RESULT FOR COOKIEZI
========================================
Current PP:  16543.21
Target PP:   17000.00
Difference:  +456.79

🎯 MINIMUM REQUIRED PP: 687.45pp
   (This play would rank #3 in your top plays)
========================================
```

## How It Works

The calculator uses osu!'s exact PP calculation formula:

1. **Weighted PP**: Each play contributes `PP × 0.95^(position-1)` to your total
2. **Bonus PP**: Additional PP based on ranked score count: `416.6667 × (1 - 0.9994^ranked_scores)`
3. **Optimization**: Tests inserting a new play at every possible position to find the minimum PP needed

## Accuracy Notes

- **API Mode**: Fetches up to 200 of your top plays for maximum accuracy
- **Manual Mode**: Accuracy depends on how many plays you input
- The script accounts for plays being pushed down in rankings when a new top play is added
- Bonus PP calculations are included for precise results

## Game Mode Support

- ✅ osu! (standard)
- ✅ osu!taiko
- ✅ osu!catch (fruits)
- ✅ osu!mania

## Requirements

- Python 3.6+
- `requests` library
- osu! API v2 credentials (optional)

## Privacy

- **API Mode**: Only uses public profile data available on your osu! profile
- **Manual Mode**: No data is sent anywhere - all calculations are done locally
- API credentials are only used for authentication and are not stored or shared

## Contributing

Feel free to open issues or submit pull requests! Some ideas for improvements:

- GUI interface
- Multiple play scenarios
- Export results to file
- More detailed analysis

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is not affiliated with osu! or ppy Pty Ltd. PP values are calculated based on the current osu! PP system and may not account for future changes to the PP algorithm.
