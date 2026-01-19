# Craig - Setup Guide

This guide will walk you through setting up Craig, your AI Compliance Manager.

## Prerequisites

- Python 3.9 or higher
- Access to:
  - Vanta account with API credentials
  - Slack workspace with admin permissions
  - SendGrid account for email
  - Anthropic API key

## Installation

### 1. Clone and Install Dependencies

```bash
cd /path/to/craigthecompliancemanager
python -m pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```bash
# Company Configuration
COMPANY_NAME="Your Company Name"
COMPLIANCE_FRAMEWORKS="SOC 2,ISO 27001"
TIMEZONE="America/Los_Angeles"

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Vanta MCP Server
VANTA_CLIENT_ID=your_vanta_client_id
VANTA_CLIENT_SECRET=your_vanta_client_secret

# Slack
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_COMPLIANCE_CHANNEL="#compliance-updates"

# SendGrid
SENDGRID_API_KEY=SG.your-sendgrid-api-key
EMAIL_FROM_ADDRESS=craig@yourcompany.com
EMAIL_FROM_NAME="Craig (Compliance Manager)"
```

### 3. Configure Vanta MCP Server

Create a Vanta credentials file:

```bash
cat > ~/vanta-credentials.json << EOF
{
  "client_id": "your_vanta_client_id",
  "client_secret": "your_vanta_client_secret"
}
EOF
```

Update your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "vanta": {
      "command": "npx",
      "args": ["-y", "@vantasdk/vanta-mcp-server"],
      "env": {
        "VANTA_ENV_FILE": "/absolute/path/to/vanta-credentials.json"
      }
    }
  }
}
```

### 4. Set Up Slack Bot

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name it "Craig - Compliance Manager"
4. Select your workspace
5. Navigate to "OAuth & Permissions"
6. Add the following Bot Token Scopes:
   - `chat:write` - Send messages
   - `users:read.email` - Look up users by email
   - `channels:read` - List channels
7. Click "Install to Workspace"
8. Copy the "Bot User OAuth Token" (starts with `xoxb-`)
9. Paste it into your `.env` file as `SLACK_BOT_TOKEN`
10. Invite the bot to your `#compliance-updates` channel: `/invite @Craig`

### 5. Set Up SendGrid

1. Sign up at https://sendgrid.com
2. Verify your domain (yourcompany.com)
3. Create an API key:
   - Settings → API Keys → Create API Key
   - Give it "Mail Send" permissions
4. Copy the API key into your `.env` file as `SENDGRID_API_KEY`
5. Configure the "From" email address (craig@yourcompany.com)

### 6. Optional: Set Up Redis (Production)

For production deployments, use Redis for persistent state management:

```bash
# Install Redis
brew install redis  # Mac
# or
apt-get install redis-server  # Linux

# Start Redis
redis-server

# Update .env
USE_REDIS=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Testing

Test all integrations:

```bash
python craig.py test
```

You should see:

```
✅ Slack connected successfully
✅ SendGrid initialized successfully
✅ Vanta MCP integration initialized
✅ Memory system working

🎉 All tests passed! Craig is ready to go.
```

## Usage

### Run Daily Check Manually

```bash
python craig.py daily-check
```

### Run Weekly Summary Manually

```bash
python craig.py weekly-summary
```

### Test Without Sending Messages (Dry Run)

```bash
python craig.py --dry-run daily-check
```

## Scheduling with Cron

### Option 1: Local Cron (Development)

Edit your crontab:

```bash
crontab -e
```

Add these lines:

```bash
# Craig's daily compliance check (Mon-Fri at 9am)
0 9 * * 1-5 cd /path/to/craigthecompliancemanager && /usr/bin/python3 craig.py daily-check

# Craig's weekly summary (Friday at 4pm)
0 16 * * 5 cd /path/to/craigthecompliancemanager && /usr/bin/python3 craig.py weekly-summary
```

### Option 2: Cloud Scheduler (Production)

#### Google Cloud Platform

1. Deploy as a Cloud Function:

```bash
gcloud functions deploy craig-daily-check \
  --runtime python39 \
  --trigger-http \
  --entry-point run_daily_check \
  --env-vars-file .env.yaml
```

2. Create Cloud Scheduler jobs:

```bash
# Daily check
gcloud scheduler jobs create http craig-daily \
  --schedule="0 9 * * 1-5" \
  --uri="https://YOUR-REGION-YOUR-PROJECT.cloudfunctions.net/craig-daily-check" \
  --http-method=POST \
  --time-zone="America/Los_Angeles"

# Weekly summary
gcloud scheduler jobs create http craig-weekly \
  --schedule="0 16 * * 5" \
  --uri="https://YOUR-REGION-YOUR-PROJECT.cloudfunctions.net/craig-weekly-summary" \
  --http-method=POST \
  --time-zone="America/Los_Angeles"
```

#### AWS

Use AWS Lambda + EventBridge (CloudWatch Events):

1. Package the application:

```bash
pip install -r requirements.txt -t package/
cd package && zip -r ../craig.zip . && cd ..
zip -g craig.zip craig.py config.py integrations/* workflows/* utils/*
```

2. Create Lambda function and upload `craig.zip`
3. Create EventBridge rules with cron expressions:
   - Daily: `cron(0 9 ? * MON-FRI *)`
   - Weekly: `cron(0 16 ? * FRI *)`

## Customization

### Adjust Escalation Thresholds

Edit `.env`:

```bash
FIRST_EMAIL_DAYS=8    # Send email after 8 days overdue
MANAGER_CC_DAYS=15    # CC manager after 15 days overdue
```

### Customize Message Templates

Edit `utils/messages.py` to change Craig's tone or message content.

### Add New Workflows

Create a new file in `workflows/` following the pattern of `daily_check.py`.

## Troubleshooting

### Slack Messages Not Sending

- Verify bot token is correct: `echo $SLACK_BOT_TOKEN`
- Check bot has been invited to channels
- Ensure users exist in Slack workspace
- Look for specific errors in output

### Emails Not Sending

- Verify SendGrid API key is valid
- Check domain is verified in SendGrid
- Ensure "From" email matches verified domain
- Check SendGrid activity log for bounces

### Vanta Data Not Loading

- Ensure Vanta MCP server is running
- Check Claude Desktop config has correct path to credentials
- Verify Vanta API credentials are valid
- Test MCP connection: `npx @vantasdk/vanta-mcp-server`

### Memory Not Persisting

- If using Redis, ensure server is running: `redis-cli ping`
- Check Redis connection settings in `.env`
- For in-memory mode, state resets on each run (expected)

## Security Best Practices

1. **Never commit `.env` file** - It contains secrets
2. **Use environment variables** in production (not `.env` file)
3. **Rotate API keys** regularly
4. **Limit Slack bot permissions** to minimum required
5. **Use Redis authentication** in production
6. **Enable MFA** for all service accounts (Vanta, Slack, SendGrid)

## Support

If you encounter issues:

1. Run tests: `python craig.py test`
2. Enable debug mode: `python craig.py --debug daily-check`
3. Check logs for specific error messages
4. Review this guide for configuration mistakes

## Next Steps

Once Craig is running:

1. Monitor the first few runs to ensure accuracy
2. Adjust message templates to match your company culture
3. Fine-tune escalation thresholds based on team feedback
4. Add custom workflows for your specific compliance needs
5. Set up monitoring/alerting for Craig's own health
