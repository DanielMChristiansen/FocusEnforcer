Idea: Application to shut down or block distracting apps, games, and websites.  
What makes it unique: Encouraging users to find and report workarounds and exploits so that they can be fixed or mitigated

Current Name: Focus Enforcer

Who: Students and beginner reverse engineers  
What: Application to shut down or block distracting apps, games, and websites  
Where: Will be available to students worldwide using Windows machines  
When: Hope to get a beta version running by October  
How: The application will operate in user mode, possibly with administrator permissions but never kernel level. It will initially be written in Python, an example of a user-readable language, to accommodate beginner reverse engineers  
Why: Students like me want to eliminate distractions during study hours but allow them during playtime. It will also give beginning reverse engineers a legal and hopefully fun target to hone their skills with

## To-do

| Task                                              | Status      | Notes                                 |
| :------------------------------------------------ | :---------- | :------------------------------------ |
| Gather list of distracting apps for tasklist scan | Not started |                                       |
| Scan system processes for matching file names     | Complete    |                                       |
| Kill processes with taskkill command              | Complete    |                                       |
| Scan window titles for matching names             | Not started | Will likely give false positives      |
| Figure out loop delay                             | Complete    | 10 seconds seems to work well for now |

### How it works

1. Gets foreground window from windows API
2. Checks if the window is "distracting" ie: a video game
3. If the window is "distracting", close it through windows API (same as clicking close button)
