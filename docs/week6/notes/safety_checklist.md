# Safety and Privacy Checklist
**Project: COGNIFY | Team: SYNTAX_SYNDICATE**

| Check | Status | Notes |
|-------|--------|-------|
| Removed all API keys from code | ✅ | Using .env file |
| No private or personal data used | ✅ | Test data only |
| Function handles bad inputs safely | ✅ | Pydantic validation active |
| Function returns friendly error messages | ✅ | Try/Except blocks planned for API integration |
| User consent not required | ✅ | No user data storage yet |

### Safety Handling
If a user uploads a PDF with malicious text, our Pydantic models treat it as a string string and do not execute it. We strictly limit the number of questions generated to prevent token overuse/DOS.
