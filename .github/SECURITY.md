# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in AurantisSync, please report it responsibly:

### How to Report

1. **Do NOT** create a public GitHub issue
2. Send an email to: [your-email@example.com]
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- We will acknowledge receipt within 48 hours
- We will provide regular updates on our progress
- We will credit you in our security advisories (unless you prefer to remain anonymous)

### Scope

This security policy applies to:
- The main AurantisSync application
- All dependencies listed in requirements.txt
- Build and deployment scripts

### Out of Scope

- Third-party services or APIs
- Issues in dependencies that are not directly used by AurantisSync
- Social engineering attacks
- Physical attacks

## Security Best Practices

When using AurantisSync:

1. **Keep dependencies updated**: Regularly update your Python packages
2. **Use trusted audio files**: Only process audio files from trusted sources
3. **Secure your system**: Keep your operating system and Python installation updated
4. **Review code**: If you're using a custom build, review the source code

## Security Considerations

AurantisSync processes audio files locally on your machine. No data is sent to external servers during normal operation. However:

- Audio files are temporarily stored in memory during processing
- Transcription models are downloaded from the internet on first use
- FFmpeg is used for audio processing (ensure it's from a trusted source)

## Contact

For security-related questions or concerns, please contact:
- Email: [your-email@example.com]
- GitHub: [@JoaoSantosCodes](https://github.com/JoaoSantosCodes)

## Acknowledgments

We thank the security researchers and community members who help keep AurantisSync secure.
