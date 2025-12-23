# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email the maintainer directly or use GitHub's private vulnerability reporting feature
3. Provide details about the vulnerability and steps to reproduce

## Security Best Practices for Users

When using this dashboard:

- **Never commit your `.env` file** – It contains your API tokens
- **Never commit `credentials.json` or `token.json`** – These are Google OAuth secrets
- **Rotate tokens periodically** – Especially if you suspect they may have been exposed
- **Use tokens with minimal scopes** – Only grant the permissions the dashboard needs

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Known Security Considerations

- This dashboard runs **locally only** – no data is sent to external servers (except the APIs you configure)
- CORS is configured permissively for local development – do not expose the backend to the public internet
- Database credentials in `.env.example` are placeholder values – always use strong passwords in production
