# meal-mate
An python app that reminds you to eat three times a day and provides diet recommendations for managing low iron.

```

### What’s included in the code:
1. **User Profile Handling**:
   - Users can input their name, age, and health condition.
   - The profile is saved to a `user_profile.json` file and automatically loaded when the app starts.
  
2. **Meal Recommendations**:
   - Users get meal recommendations based on their health condition (e.g., "Low Iron", "Vegetarian", "Vegan").
   - The meal suggestions are displayed below the form when the user clicks the "Get Meal Recommendations" button.

3. **Meal Reminders**:
   - Users can input their custom meal times (Breakfast, Lunch, Dinner).
   - The app will send notifications when it's time for each meal based on the entered times.
   - Notifications are handled by `plyer`, and reminders run in a background thread that checks the time every minute.

4. **Threading for Background Reminders**:
   - Meal reminders run continuously in the background to notify the user when it's time to eat.

### How to Use:
1. **Profile**: When the app starts, input your name, age, and health condition and save the profile.
2. **Meal Recommendations**: Once the profile is saved, click "Get Meal Recommendations" to receive meal suggestions tailored to the health condition.
3. **Custom Meal Reminders**: Enter your preferred meal times (e.g., Breakfast at 08:00, Lunch at 12:30, Dinner at 19:00), then click "Start Meal Reminders". The app will notify you at those times.

### Next Steps:
- You can improve the meal recommendations logic by adding more health conditions and meal options.
- You can implement a better UI by adding styles or using `ttk` widgets.
- Add more features, such as tracking past meals or offering recipes based on recommendations.

