# 🤖 Craig - The AI Compliance Manager

Craig is an autonomous AI agent that helps your team stay compliant with security requirements by monitoring Vanta and proactively reaching out when people fall behind on trainings, MFA setup, or other compliance tasks.

## What Craig Does

Craig acts as your dedicated compliance manager, running automated workflows to:

### 📊 Daily Compliance Check (Weekdays, 9am)
- Queries Vanta for failing compliance tests
- Identifies employees with incomplete trainings or missing MFA
- Sends personalized Slack reminders for tasks 0-7 days overdue
- Escalates to email for tasks 8-14 days overdue
- CC's managers on critical items 15+ days overdue
- Tracks who's been reminded to avoid spam

### 📈 Weekly Summary (Fridays, 4pm)
- Posts compliance status to your `#compliance-updates` channel
- Celebrates employees who completed tasks this week
- Highlights outstanding items that need attention
- Shows trend from previous week
- Reminds team of upcoming audit deadlines

### 💬 Smart Communication
- Friendly, professional tone (not robotic)
- Explains WHY compliance matters
- Provides direct links to complete tasks
- Celebrates wins when people complete trainings
- Escalates appropriately without being annoying

## Example Interactions

**Slack Reminder (3 days overdue):**
> Hey Sarah! Quick heads up - your Security Awareness Training is 3 days overdue. It takes about 15 minutes. Can you knock it out today?
>
> https://knowbe4.com/training/abc123
>
> Let me know if you have any questions! 🎯

**Email Escalation (10 days overdue):**
> Hi Mike,
>
> Your Security Awareness Training is now 10 days overdue. This is required for our SOC 2 compliance and needs to be completed ASAP.
>
> [Complete Training Button]
>
> If you're running into any issues, just reply and I'll help troubleshoot.
>
> Thanks,
> Craig

**Celebration Message:**
> Hey Sarah! 🎉
>
> Just saw you completed your Security Awareness Training - thank you! ✅
>
> One less thing to worry about. Really appreciate you staying on top of it!

**Weekly Summary to Channel:**
> 📊 **Weekly Compliance Update - January 17, 2025**
>
> Hey team! Here's our compliance status heading into the weekend:
>
> **🎉 This Week's Wins:**
> - 8 employees completed Security Awareness Training
> - Overall compliance: 87% (up from 78% last week!) 📈
>
> **⚠️ Still Outstanding (4 items):**
> - Tom Rodriguez - Security Training (16 days overdue) 🔴
> - James Chen - Security Training (5 days overdue)
>
> **📅 Upcoming Deadlines:**
> - SOC 2 Audit Prep: February 8
>
> I'll continue monitoring and sending reminders. If anyone is blocked, ping me!
>
> Have a great weekend! 🚀

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Craig (Claude AI Agent)                 │
│              Running System Prompt + Workflows          │
└─────────────────────────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Vanta   │   │  Slack   │   │  Email   │
    │   MCP    │   │   API    │   │(SendGrid)│
    │  Server  │   │          │   │          │
    └──────────┘   └──────────┘   └──────────┘
```

### Components

- **`craig.py`** - Main orchestrator and CLI entry point
- **`config.py`** - Configuration management
- **`integrations/`** - Wrappers for Vanta, Slack, and Email APIs
- **`workflows/`** - Daily check and weekly summary workflows
- **`utils/`** - Message templates and reminder tracking

### Key Features

- **Vanta MCP Integration** - Uses official Vanta MCP server for compliance data
- **Smart Escalation** - Automatically escalates based on days overdue
- **Spam Prevention** - Tracks who's been reminded to avoid duplicate messages
- **Dry Run Mode** - Test without actually sending messages
- **Production Ready** - Can run locally via cron or deploy to cloud functions

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required credentials:
- Anthropic API key
- Vanta API credentials
- Slack bot token
- SendGrid API key

### 3. Test

```bash
python craig.py test
```

### 4. Run

```bash
# Run daily check manually
python craig.py daily-check

# Run weekly summary manually
python craig.py weekly-summary

# Test without sending messages
python craig.py --dry-run daily-check
```

### 5. Schedule

Add to crontab:

```bash
# Daily check at 9am weekdays
0 9 * * 1-5 python /path/to/craig.py daily-check

# Weekly summary at 4pm Fridays
0 16 * * 5 python /path/to/craig.py weekly-summary
```

## Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[.env.example](.env.example)** - Environment variable reference

## Configuration

### Escalation Thresholds

Control when Craig escalates:

```bash
FIRST_EMAIL_DAYS=8    # Send email after 8 days overdue
MANAGER_CC_DAYS=15    # CC manager after 15 days overdue
```

### Message Customization

Edit `utils/messages.py` to customize Craig's tone and message templates.

### Compliance Frameworks

Configure which frameworks you're tracking:

```bash
COMPLIANCE_FRAMEWORKS="SOC 2,ISO 27001,HIPAA"
```

## Deployment Options

### Option 1: Local (Development)
Run on your laptop with cron jobs. Good for testing and small teams.

### Option 2: Cloud Functions (Production)
Deploy to:
- Google Cloud Functions + Cloud Scheduler
- AWS Lambda + EventBridge
- Azure Functions + Timer Trigger

### Option 3: Container (Production)
Run as a Docker container with cron:

```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "craig.py", "daily-check"]
```

## Security

Craig handles sensitive compliance data. Best practices:

- ✅ Never commit `.env` file (it's in `.gitignore`)
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Limit Slack bot permissions to minimum required
- ✅ Enable MFA on all service accounts
- ✅ Use Redis authentication in production
- ✅ Review audit logs periodically

## Troubleshooting

**Slack messages not sending?**
- Verify bot token is correct
- Ensure bot is invited to channels
- Check users exist in Slack workspace

**Emails not sending?**
- Verify SendGrid API key
- Check domain is verified
- Ensure "From" email matches verified domain

**Vanta data not loading?**
- Ensure Vanta MCP server is configured
- Check Claude Desktop config
- Verify Vanta API credentials

Run with debug flag for detailed logs:

```bash
python craig.py --debug daily-check
```

## Customization Ideas

Craig is extensible! Here are some ideas:

- **Custom Workflows** - Add new compliance checks
- **Integration Alerts** - Alert when Vanta integration goes down
- **Manager Dashboards** - Send weekly reports to managers
- **Onboarding Automation** - Remind new hires about compliance tasks
- **Slack Commands** - Let employees query their status: `/craig status`
- **Compliance Bot** - Answer questions in Slack about compliance

## Philosophy

Craig's design philosophy:

1. **Helpful, not annoying** - Reminds people without spam
2. **Context-aware** - Understands edge cases (parental leave, etc.)
3. **Celebrates wins** - Positive reinforcement for completing tasks
4. **Transparent** - Always explains WHY something is required
5. **Autonomous** - Runs without human intervention for routine tasks
6. **Escalates appropriately** - Knows when to loop in humans

## Contributing

Want to improve Craig? Ideas for contributions:

- Additional integrations (KnowBe4, Okta, etc.)
- Better message templates
- More sophisticated escalation logic
- Slack slash commands
- Manager dashboard
- Analytics and reporting

## License

MIT License - See LICENSE file for details

## Support

Questions or issues? Check:

1. [SETUP.md](SETUP.md) for detailed configuration
2. Run `python craig.py test` to verify integrations
3. Use `--debug` flag for detailed error messages

---

Built with ❤️ using:
- [Claude](https://www.anthropic.com/claude) by Anthropic
- [Vanta MCP Server](https://github.com/VantaInc/vanta-mcp-server)
- [Slack SDK](https://slack.dev/python-slack-sdk/)
- [SendGrid](https://sendgrid.com/)

**Craig - Keeping your team compliant, one reminder at a time.** 🤖
